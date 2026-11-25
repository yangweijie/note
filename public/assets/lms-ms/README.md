# lms-ms — ModelScope 加速下载器

LM Studio 内置下载走 `search.lmstudio.ai` 中转，在国内网络下常不可达；hf-mirror 单连接仅约 1 MB/s。本工具走 ModelScope 国内 CDN，实测 **30 MB/s**（约快 30 倍），下载后直接落入 LM Studio 模型目录，启动 LM Studio 即自动识别。

## 安装

已安装到 `~/.local/bin/lms-ms`（源码副本 `lms-ms.py` 在工作区）。依赖 `modelscope`，已由本机 anaconda 环境提供；脚本会自动定位该解释器。

## Windows 全局使用

脚本本身跨平台（模型目录自动展开为 `%USERPROFILE%\.lmstudio\models`），Windows 只需解决"全局命令"和"解释器定位"两件事。用附带的 `lms-ms.cmd` 启动器：

1. 把 `lms-ms.py` 和 `lms-ms.cmd` 放到同一目录，例如 `%USERPROFILE%\.lms-ms\`
2. 把该目录加入 PATH（系统属性 → 环境变量，或 PowerShell 执行）：
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\.lms-ms", "User")
   ```
3. 重开终端，即可直接用 `lms-ms`（CMD / PowerShell 均可）

**解释器选择**：启动器优先读环境变量 `LMS_MS_PYTHON`，未设置时回退到 `py -3`。若 `modelscope` 装在 Anaconda，需设置：

```powershell
[Environment]::SetEnvironmentVariable("LMS_MS_PYTHON", "C:\ProgramData\anaconda3\python.exe", "User")
```

（路径按实际 Anaconda 安装位置调整，可用 `where python` 查看。）脚本里原有一处 macOS 专用的 Anaconda fallback 路径在 Windows 上会被忽略，不影响使用。

Windows 下完成提示自动改用 `findstr`，与 CMD 兼容；`lms ls --json` 用法与 macOS 相同。

## 用法

```bash
lms-ms owner/repo                    # 下载整个仓库
lms-ms owner/repo@Q4_K_M             # 只下指定量化 + 配置文件（推荐）
lms-ms bartowski/Qwen2.5-0.5B-Instruct-GGUF@Q4_K_M
lms-ms --list owner/repo             # 列出所有文件及可用量化标记
lms-ms --dry-run owner/repo@Q8_0     # 预览要下载的文件与体积
lms-ms owner/repo --workers 16       # 调整并发数（默认 8）
```

`@量化` 语法与 `lms get` 一致，匹配规则为文件名末尾的量化标记精确匹配（如 `Q4_K_M`、`Q8_0`、`IQ2_M`、`f16`）。无效量化会报错并列出全部可用项。

## 下载位置

`~/.lmstudio/models/<owner>/<repo>/`，与 LM Studio 原生目录结构一致。下载后：

```bash
lms ls                               # 确认模型出现在列表
lms ls --json                        # 看准确的 modelKey / indexedModelIdentifier
lms load <modelKey>                  # 加载（短名，如 qwen2.5-0.5b-instruct）
```

**注意**：`lms ls` 显示的是规范化短名（`modelKey`），不是下载目录的 repo 名。例如 `bartowski/Qwen2.5-0.5B-Instruct-GGUF` 显示为 `qwen2.5-0.5b-instruct`（小写、去 `-GGUF` 后缀）。直接用 repo 名 grep 会匹配不到，这是正常的——用 `lms ls --json` 的 `path` 字段可确认文件确实来自该 repo。

## 设计说明

- **为何不是 LM Studio 插件**：官方插件系统只提供 `withToolsProvider` / `withConfigSchematics` / prompt 预处理，无法拦截 GUI 或 `lms get` 的下载流程。命令行包装是唯一能真正替换下载通道的形态。
- **仓库映射**：HF 常用组织（`mlx-community`、`lmstudio-community`、`bartowski`、`Qwen` 等）在 ModelScope 上多为同名仓库，脚本直接用 `owner/repo` 查询；不存在时明确报错。
- **安全约束**：`@量化` 模式只下载匹配的 GGUF 与小型配置文件（`.json/.txt/.model`），不会误拉 f16 全精度文件。下载前有磁盘空间预检。
- **断点续传**：由 `modelscope.snapshot_download` 提供，重复执行同一命令会跳过已完成文件。

## 实测记录

`bartowski/Qwen2.5-0.5B-Instruct-GGUF@Q4_K_M`：397 MB，13 秒完成，平均 30 MB/s；文件落地 `~/.lmstudio/models/bartowski/Qwen2.5-0.5B-Instruct-GGUF/`，GGUF 魔数校验通过。

## 局限

- 仅覆盖 ModelScope 上有镜像的仓库；冷门模型可能缺失，需 `--list` 先确认。
- 不会自动调用 `lms load`；下载与加载分离，避免误加载大模型占满内存。
