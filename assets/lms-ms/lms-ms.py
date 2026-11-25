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

# modelscope 只装在 anaconda 解释器里；当前解释器没有时自动切换过去
try:
    from modelscope.hub.api import HubApi
    from modelscope.hub.snapshot_download import snapshot_download
except ImportError:
    _ALT = "/Volumes/data/Application/anaconda3/bin/python"
    if os.path.exists(_ALT) and os.path.realpath(sys.executable) != os.path.realpath(_ALT):
        os.execv(_ALT, [_ALT, __file__, *sys.argv[1:]])
    sys.exit("需要 modelscope：pip install modelscope，或使用含 modelscope 的 Python")

MODELS_ROOT = Path.home() / ".lmstudio" / "models"
CONFIG_SUFFIXES = (".json", ".txt", ".model")


def split_spec(spec: str):
    """owner/repo@quant -> (repo, quant|None)"""
    if "@" in spec:
        return spec.rsplit("@", 1)
    return spec, None


def quant_token(path: str) -> str:
    """从文件名推断量化标记：X-Y-Q4_K_M.gguf -> Q4_K_M"""
    return Path(path).stem.rsplit("-", 1)[-1]


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
            tag = f"  [{quant_token(path)}]" if path.endswith(".gguf") else ""
            print(f"  {human(size):>10}  {path}{tag}")
        return 0

    patterns = None
    if quant:
        matched = [
            p for p, _ in entries
            if p.endswith(".gguf") and quant_token(p).lower() == quant.lower()
        ]
        if not matched:
            avail = sorted({quant_token(p) for p, _ in entries if p.endswith(".gguf")})
            print(f"错误：{repo} 中没有量化 {quant}。可用: {', '.join(avail)}", file=sys.stderr)
            return 4
        # GGUF 只下匹配文件 + 小配置文件，避免误拉其他量化或全精度文件
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

    # LM Studio 用规范化短名作为 modelKey（小写、连字符、去 -GGUF 后缀）
    repo_name = repo.rsplit("/", 1)[-1]
    model_key = repo_name[:-5] if repo_name.upper().endswith("-GGUF") else repo_name
    key = model_key.lower()
    if os.name == "nt":
        verify = f'lms ls | findstr /i "{key}"'
    else:
        verify = f"lms ls | grep -i '{key}'"
    print(f"\n完成。启动 LM Studio 后验证：")
    print(f"  {verify}")
    print(f"  加载：lms load {key}")
    print(f"  （准确标识符见 lms ls --json 的 modelKey / indexedModelIdentifier）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
