---
title: winc如何正确配置PHP格式化和修复命令
date: 2026-11-25
tags: [PHP, Winc, 工具配置]
summary: Winc 没有内置 PHP 格式化与修复工具，本文用 php-cs-fixer + phpcbf 加一层 stdin→stdout 桥接脚本，实现保存即格式化、保存即修复，附 macOS 与 Windows 双平台完整配置。
---

折腾编辑器配置最容易踩的坑，是默认「它应该支持」——但 Winc 的 PHP 支持恰恰需要自己搭。这篇把配置原理、双平台脚本和验证方法一次讲清楚。

## 先搞懂 Winc 的命令机制

翻了 Winc 的开源源码可以确认：**它没有内置任何 PHP 格式化/修复引擎**。配置里的 `format.commands.<扩展名>` 和 `format.fixCommands.<扩展名>` 接受的是一条外部命令，工作方式固定为：

1. 把当前编辑器缓冲区的内容通过 **stdin** 传给命令；
2. 读取命令的 **stdout**，用它替换编辑器里的内容。

这决定了配置的两个关键点：

- 工具要自己装（本文选 `php-cs-fixer` 做格式化、`phpcbf` 做修复）；
- 这两个工具都只接受「文件路径」参数，不支持 stdin——所以中间必须加一层**桥接脚本**：把 stdin 落盘到临时文件 → 调工具处理 → 把结果 `cat` 回 stdout。

理解了这条链路，下面的配置就都是顺理成章的。

## 一、安装 PHP 工具链

用 Composer 全局安装：

```bash
composer global require friendsofphp/php-cs-fixer squizlabs/php_codesniffer
composer global config bin-dir --absolute
```

实际装到的版本：`php-cs-fixer 3.75` + `phpcbf 4.0.4`。

⚠️ **版本坑**：php-cs-fixer 3.75 最高只支持到 PHP 8.3。如果系统默认是 PHP 8.5，命令里必须写死用 PHP 8.3 来跑它；`phpcbf`（CodeSniffer 4.x）则可以直接用系统 PHP。

## 二、macOS 配置

### 1. 规则文件

新建 `~/Library/Application Support/winc/php-cs-fixer.php`，规则走保守的 PSR-12 + 短数组，只排版、不改代码行为：

```php
<?php

$finder = PhpCsFixer\Finder::create()->in(__DIR__);

return (new PhpCsFixer\Config())
    ->setRules([
        '@PSR12' => true,
        'array_syntax' => ['syntax' => 'short'],
    ])
    ->setFinder($finder);
```

（用 context-kit 检索过项目，没有既定的 PHP 风格配置，所以选 PSR-12 这个最安全的基线。）

### 2. 桥接脚本

新建 `~/Library/Application Support/winc/php-winc.sh`，加可执行权限（`chmod +x`）：

```bash
#!/bin/bash
# 用法: php-winc.sh format|fix
set -euo pipefail
task="${1:-format}"

# 用编辑器传来的文件名做临时文件名；没有则用默认名
name="file.php"
if [ -n "${WINC_FILE:-}" ]; then
  name="$(basename "$WINC_FILE")"
fi

dir="$(mktemp -d)"
tmp="$dir/$name"
trap 'rm -rf "$dir"' EXIT

# stdin → 临时文件
cat > "$tmp"

# 切到原文件所在目录，保证相对路径引用和配置能被正确找到
if [ -n "${WINC_FILE:-}" ] && [ -d "$(dirname "$WINC_FILE")" ]; then
  cd "$(dirname "$WINC_FILE")"
fi

bin="$(composer global config bin-dir --absolute 2>/dev/null)"

if [ "$task" = "fix" ]; then
  # phpcbf 用系统 PHP
  "$bin/phpcbf" --standard=PSR12 "$tmp" >/dev/null 2>&1 || true
else
  # php-cs-fixer 必须用 PHP 8.3；按本机实际路径调整
  php8.3 "$bin/php-cs-fixer" fix --quiet \
    --config "$HOME/Library/Application Support/winc/php-cs-fixer.php" \
    "$tmp" >/dev/null 2>&1 || true
fi

# 处理结果 → stdout
cat "$tmp"
```

脚本用 `mktemp` 把 stdin 写到临时文件，处理完就删——**不会直接改动磁盘上的原文件**，所以未保存的缓冲区也能正常格式化。

### 3. 修改 Winc 配置

编辑 `~/Library/Application Support/winc/config.json`，在 `format` 节加入：

```json
"format": {
  "onSave": true,
  "commands": {
    "php": "\"/Users/jay/Library/Application Support/winc/php-winc.sh\" format"
  },
  "fixOnSave": true,
  "fixCommands": {
    "php": "\"/Users/jay/Library/Application Support/winc/php-winc.sh\" fix"
  }
}
```

`onSave` / `fixOnSave` 都设为 `true`，保存时先修复再格式化。改之前记得备份：

```bash
cp "$HOME/Library/Application Support/winc/config.json" \
   "$HOME/Library/Application Support/winc/config.json.bak-$(date +%Y%m%d-%H%M%S)"
```

## 三、Windows 配置

### 1. 安装与路径

先装 PHP 8.3（php-cs-fixer 3.75 不支持更高版本），然后：

```powershell
composer global require friendsofphp/php-cs-fixer squizlabs/php_codesniffer
composer global config bin-dir --absolute
```

Composer 的 bin 目录通常是 `%APPDATA%\Composer\vendor\bin`。

Winc 的配置目录是 `%APPDATA%\winc\config.json`；源码里做了兜底：APPDATA 缺失时回退到 `HOME\winc`。把上面的 `php-cs-fixer.php` 规则文件放到同一目录。

### 2. 桥接脚本

新建 `%APPDATA%\winc\php-winc.ps1`：

```powershell
param([string]$Task = 'format')
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false

$name = if ($env:WINC_FILE) { [IO.Path]::GetFileName($env:WINC_FILE) } else { 'file.php' }
$dir = Join-Path $env:TEMP ([guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $dir -Force | Out-Null
$tmp = Join-Path $dir $name
try {
    $src = [Console]::In.ReadToEnd()
    [IO.File]::WriteAllText($tmp, $src, (New-Object Text.UTF8Encoding($false)))
    $bin = Join-Path $env:APPDATA 'Composer\vendor\bin'
    if ($Task -eq 'fix') {
        & (Join-Path $bin 'phpcbf.bat') --standard=PSR12 $tmp 2>$null | Out-Null
    } else {
        & php (Join-Path $bin 'php-cs-fixer') fix --quiet --config (Join-Path $env:APPDATA 'winc\php-cs-fixer.php') $tmp 2>$null | Out-Null
    }
    [Console]::Out.Write([IO.File]::ReadAllText($tmp))
}
finally {
    Remove-Item -LiteralPath $dir -Recurse -Force -ErrorAction SilentlyContinue
}
```

### 3. config.json

⚠️ **Winc 不会展开命令里的 `%APPDATA%`**，路径必须写死绝对路径：

```json
"format": {
  "onSave": true,
  "commands": {
    "php": "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\\Users\\你的用户名\\AppData\\Roaming\\winc\\php-winc.ps1\" format"
  },
  "fixOnSave": true,
  "fixCommands": {
    "php": "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\\Users\\你的用户名\\AppData\\Roaming\\winc\\php-winc.ps1\" fix"
  }
}
```

## 四、实测验证

配置写完不要直接信，按 Winc 的真实调用方式验一遍：命令拆分、stdin 输入、设置 `WINC_FILE` 环境变量、以文件所在目录为 cwd。

**格式化测试**——输入：

```php
<?php
function demo(){echo "hi";}
```

输出应自动补空行、函数体换行、4 空格缩进，退出码 0。

**修复测试**——输入：

```php
<?php
if(true){echo "x";}
```

输出应为 `if (true) { echo "x"; }`，退出码 0。

两个命令都通过才算配置成功。如果 Windows 上没生效，先在终端手动跑一次：

```powershell
php php-cs-fixer fix --dry-run --diff 文件.php
```

看具体报错再针对性处理。

## 五、重启并使用

配置是**启动时加载**的，必须完全退出 Winc（macOS 用 ⌘Q）再重新打开。之后：

- `⇧⌥F` 手动格式化；
- Fix 在命令面板搜 “Fix”；
- 因为开了 `onSave` / `fixOnSave`，保存时会自动先修复再格式化。

## 小结

Winc 配置 PHP 工具的关键就一句话：**工具本身不支持 stdin，所以用桥接脚本把 stdin 转成临时文件**。摸清这条链路后，想换风格规则（比如改成 Laravel / Symfony）也只要动规则文件，脚本和配置都不用变。
