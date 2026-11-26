#!/usr/bin/env python3
"""lms-ms — 用 ModelScope 高速下载模型到 LM Studio 模型目录。

用法:
  lms-ms owner/repo              下载整个仓库
  lms-ms owner/repo@Q4_K_M       只下载指定量化（GGUF）
  lms-ms --list owner/repo       列出仓库文件与可用量化
  lms-ms --dry-run ...           只预览，不下载
  lms-ms --workers N             并发数（默认 8）
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

try:
    from modelscope.hub.api import HubApi
    from modelscope.hub.snapshot_download import snapshot_download
except ImportError:
    sys.exit("需要 modelscope：pip install modelscope，或设置 LMS_MS_PYTHON 指向含 modelscope 的 Python")

CONFIG_SUFFIXES = (".json", ".txt", ".model")


def models_root() -> Path:
    """优先用 LM Studio 实际配置的模型目录（settings.json 的 downloadsFolder），回退默认 ~/.lmstudio/models。"""
    home = Path.home()
    try:
        import json
        data = json.loads((home / ".lmstudio" / "settings.json").read_text(encoding="utf-8"))
        folder = data.get("downloadsFolder")
        if folder:
            p = Path(os.path.expandvars(folder)).expanduser()
            if p.is_dir():
                return p
    except (OSError, ValueError):
        pass
    return home / ".lmstudio" / "models"


MODELS_ROOT = models_root()


def split_spec(spec: str):
    """owner/repo@quant -> (repo, quant|None)"""
    if "@" in spec:
        return spec.rsplit("@", 1)
    return spec, None


def quant_token(path: str) -> str:
    """从文件名推断量化标记：X-Y-Q4_K_M.gguf -> Q4_K_M"""
    return Path(path).stem.rsplit("-", 1)[-1]


def display_token(path: str) -> str:
    """面向用户的标记：末段不含数字（如 mtp）时取末两段，得到 PTQ1_0-mtp 这类写法。"""
    parts = Path(path).stem.split("-")
    if len(parts) >= 2 and not any(ch.isdigit() for ch in parts[-1]):
        return "-".join(parts[-2:])
    return parts[-1]


def match_ggufs(entries, quant: str):
    """按尾部匹配 GGUF：@PTQ1_0-mtp / @mtp / @Q4_K_M 都支持。"""
    q = quant.lower().lstrip("-")
    ggufs = [p for p, _ in entries if p.endswith(".gguf")]
    tail = [p for p in ggufs if Path(p).stem.lower().endswith("-" + q)]
    if tail:
        return tail
    return [p for p in ggufs if quant_token(p).lower() == q]


def human(n: int) -> str:
    n = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def main() -> int:
    ap = argparse.ArgumentParser(description="用 ModelScope 高速下载模型到 LM Studio")
    ap.add_argument("model", help="owner/repo，或 owner/repo@量化（如 @Q4_K_M）")
    ap.add_argument("--list", action="store_true", help="列出仓库文件与可用量化")
    ap.add_argument("--dry-run", action="store_true", help="只显示将要下载的文件")
    ap.add_argument("--workers", type=int, default=8, help="并发下载数（默认 8）")
    args = ap.parse_args()

    repo, quant = split_spec(args.model)
    if "/" not in repo:
        print(f"错误：模型标识需为 owner/repo 格式，收到: {repo}", file=sys.stderr)
        return 2

    api = HubApi()
    try:
        files = api.get_model_files(repo, recursive=True)
    except Exception as exc:
        print(f"错误：ModelScope 上找不到 {repo}: {exc}", file=sys.stderr)
        return 3

    entries = [(f.get("Path", ""), int(f.get("Size") or 0)) for f in files]
    entries = [(p, s) for p, s in entries if p]

    if args.list:
        print(f"{repo} 的文件（共 {len(entries)} 个）：")
        for path, size in entries:
            tag = f"  [{display_token(path)}]" if path.endswith(".gguf") else ""
            print(f"  {human(size):>10}  {path}{tag}")
        return 0

    patterns = None
    if quant:
        matched = match_ggufs(entries, quant)
        if not matched:
            avail = sorted({display_token(p) for p, _ in entries if p.endswith(".gguf")})
            print(f"错误：{repo} 中没有量化 {quant}。可用: {', '.join(avail)}", file=sys.stderr)
            return 4
        if len(matched) > 1:
            sizes = dict(entries)
            print(f"错误：@{quant} 命中 {len(matched)} 个 GGUF，为避免误下大文件已中止。", file=sys.stderr)
            print("请改用下列更精确的标记之一：", file=sys.stderr)
            for p in matched:
                print(f"  @{display_token(p)}   {human(sizes.get(p, 0))}   {p}", file=sys.stderr)
            return 4
        patterns = matched + [p for p, _ in entries if p.endswith(CONFIG_SUFFIXES)]
        print(f"量化 {quant} -> {', '.join(matched)}")

    selected = [(p, s) for p, s in entries if patterns is None or p in patterns]
    total = sum(s for _, s in selected)
    target = MODELS_ROOT / repo
    print(f"目标目录: {target}")
    print(f"预计下载: {human(total)}（{len(selected)} 个文件）")

    try:
        free = shutil.disk_usage(MODELS_ROOT).free
    except OSError:
        free = None
    if free is not None and total > free:
        print(f"错误：磁盘剩余 {human(free)}，不足以下载 {human(total)}", file=sys.stderr)
        return 5

    if args.dry_run:
        print("dry-run：未下载。")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    kwargs = {"local_dir": str(target), "max_workers": args.workers}
    if patterns:
        kwargs["allow_patterns"] = patterns

    print(f"开始下载（{args.workers} 并发）...")
    snapshot_download(repo, **kwargs)

    repo_name = repo.rsplit("/", 1)[-1]
    model_key = repo_name[:-5] if repo_name.upper().endswith("-GGUF") else repo_name
    key = model_key.lower()
    if os.name == "nt":
        verify = f'lms ls | findstr /i "{key}"'
    else:
        verify = f"lms ls | grep -i '{key}'"
    print("\n完成。启动 LM Studio 后验证：")
    print(f"  {verify}")
    print(f"  加载：lms load {key}")
    print("  （准确标识符见 lms ls --json 的 modelKey / indexedModelIdentifier）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
