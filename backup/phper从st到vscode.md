# 是什么

微软出的重新定义编码的一款免费开源跨平台的文本编辑器，媲美IDE。

# 优势

我用过很多文本编辑器 比如notepad、editplus、atom、bracket、sublime等。

比前两个界面好，扩展多。

比atom性能好，人家作者是算法大师。

比bracket扩展性强，比只限于前端。

比sublime来说我觉得最主要是易用性、扩展性上（开源）。

# 下载

https://code.visualstudio.com/

![](https://box.kancloud.cn/7edb1f4e4bee8340a797041177766e44_497x607.png)



注意选择版本。

# 安装

和正常文本编辑器一样安装，值得注意的是最好安装在C盘，因为我发现我安装在其他盘，重装系统后，每次打开编辑器更新 他都给我C盘安装一遍，然后再打开 又提示更新。

# 如何做php开发使用

## 确保本地环境变量里有php

vscode最初是开发前端node 那一套的，其他语言的支持比较后，所以我一直没使用。直到最近更新频繁，我重装了系统，就想体验体验到底能不能用于php项目开发 替代我的sublime，才发现基本上可以了，除了一些小问题。


对于php语言的支持，它是language server方式支持的。建议环境变量里有php 以后跑server、终端也方便。

## 国际化

装好了就是本地语言

## package  control center？

自带ext 扩展管理

## 欢迎界面

![](https://box.kancloud.cn/4b09a6774191d8a60065411838592c25_1920x1046.png)

我觉得vscode 比st 良心的第一个就是欢迎界面。一目了然，信息量足啊。不像st那个空空的主界面。

## 使用php

### 安装php extension pack

咱们点击欢迎界面->自定义->PHP

然后vscode 就默默给我们装一个php集合扩展:php extension pack

![](https://box.kancloud.cn/442133a3c606c1e2b6bd1569b422e63d_963x637.png)

包含了 php debug 和 PHP IntelliSense

### 配置php执行文件
装好之后，你打开一个php文件。如果你没配环境变量他会提示你php language server 无法启动之类的。

你需要配置一个  “php.executablePath" 指向你的php执行文件。就像下面：

`"php.executablePath": "D:/wamp64/bin/php/php7.0.10/php.exe",`

vscode的配置项做的比sublime好的地方是。双栏打开，点击左侧配置值会自动复制到右侧：

![](https://box.kancloud.cn/04edba054f32dae3ffb5a7da422f743e_829x533.png)

![](https://box.kancloud.cn/45c44d667b1a256eb8fdbc99a4ad8255_1342x153.png)

![](https://box.kancloud.cn/0d273489fe2850c68fefe3b9e5073f87_1481x137.png)

太tm 人性化了。这才是我们想要的配置。

而我们sublime怎么做 打开默认配置，打开用户配置，在默认配置里搜索到匹配配置，复制到用户配置。效率太低了。
![](https://box.kancloud.cn/8ddbe9de6002443303a8a91cb12fdadf_1549x924.png)

![](https://box.kancloud.cn/7fff626cb6f7988f29227a5d15e139ea_1519x666.png)

而且除了软件配置外 还有插件配置。给你一个插件列表。

![](https://box.kancloud.cn/3a9e002f2417a7d60906152b31ea44a4_1317x1035.png)

插件配置是开发者开放的。往往用户配置里没有一项，默认配置里很多项。甚至很多隐藏配置在readme 和github上。

> 总结配置的体验就可以发现  vscode做的是工程软件，sublime是极客软件，新手不友好。

我觉得好的软件就是**Don't make me think, Don't make me wrong** 。

### 安装 php 相关扩展

我们先看扩展管理界面

![](https://box.kancloud.cn/c532e8f1349524d49b4bbe63660baa07_438x982.png)

点击“扩展”图标 出现的，在这里你就可以直接输入关键字 搜索扩展。
默认点击进来显示的已安装扩展。

![](https://box.kancloud.cn/cad98e0ac9aa02abd349d15bd84f12c2_635x548.png)

自带的 不需要手动安装 👍。

参照我以前写的那个[sublime培训  密码: 6jyy](https://pan.baidu.com/s/1nvwV7qL)：逐一查找 安装吧

![](https://box.kancloud.cn/750be4f8414113a32a1cec8edaaa5438_1183x826.png)

最终发现只需要以下几个插件就可以足够php开发了：

* CodeRunner, 非常方便的代码执行软件，支持多种语言。

![](https://box.kancloud.cn/19c0f13d14fd209403df33c6332d86de_1539x696.png)

![](https://box.kancloud.cn/40975e2b93b3fadbcc103f2f7894ab58_937x143.png)

* Composer 现在php包管理工具
要配置执行路径

 `"composer.executablePath": "C:/ProgramData/ComposerSetup/bin/composer.bat",`


*  php debug
![](https://box.kancloud.cn/2b38f366683d309dfeef3621ecbdc3a3_1279x627.png)

比sublime界面好看多了

* PHP DocBlocker
写注释的人都知道

* SonarLint
代码质量管理工具，需要Java 支持JavaScript、php 就是报错有点严格。

这个强烈建议装一下：
![](https://box.kancloud.cn/2bbd18baefaae34ef5e4333acf7382f3_1088x446.png)

有了它你可以获得错误提示和优化建议，甚至可以提示未定义的变量，其他文本编辑器可做不到。

### 安装增强插件
* advance new file 
高级新建文件

* Alignment
代码 “=” 对齐插件和st的像但是 必须选中区域对齐，不能自动识别一大段=号的，有时候还对不齐

* All Autocomplete
自动完成插件

* Apache conf
apache 语法高亮插件

* AutoFileName
路径补全插件

* Change Case
用于转换命名方式，如驼峰转下划线

* Chinese Translation
中文繁体转换 支持香港 、台湾等。

*  Clipboard History
剪切板管理软件，方便找多次复制里的内容

* Close tag
闭合最后的标签

* Docker
以后可能会用上吧

* expand-selection-to-scope
扩大所选范围

* File Utils
文件操作插件（重命名、移动、删除等）

* Generic Remote Debugger
远程调试插件，看起来很牛逼的样子，可以调试线上项目

* Markdown All in one
markdown一篮子

* Markdown Preview Enhanced
markdown 预览增强 支持公式 导出啥的

* Markdown Theme Kit
markdown编辑时文件主题

* markdownlint
markdown语法错误检测

* NGINX syntax
Nginx服务器配置语法支持

* paste image to qiniu
粘贴截屏图片直接上传七牛

* Path Autocomplete
路径补全工具

* Python
蟒蛇支持

* Settings Sync
配置同步插件，说实话我是被这个插件吸引过来的，我st重装系统后，忘了备份好多东西没了。
这个可以同步到github上的

* Sublime Commands
支持一些sublime的命令 如分割成多行，合并单行等

* Sublime Text Keymap
支持sublime的键盘设置习惯（不是完全支持）

* Sublime Text Extension Pack
包括了Sublime Text Keymap 、Expand Selection To Scope、Close HTML / XML Tag、Sublime Commands 几个插件

* Tranpose
交换光标插件 一般是两个

### 安装编码插件

vscode中文支持良好不需要插件

### 前端

* Color Highlight
css 颜色高亮

* Color Picker
拾色器

* ESLint
前端报错检测

* Image Preview
图片预览，直接显示在css 当前行前面

* jQuery Code Snippets
写jquery的都想要


### 编码
* Codelf
命名变量搜索插件

* Live Server
直接在浏览器里同步预览项目

* Live Server Preview
在侧栏列同步预览项目

* Local History
本地文件历史

* Log File Highlighter
日志文件高亮 

* Partial Diff
选择文本进行可视化比较

* Typewriter Noises
打字机效果，倍爽

* VS Code database
vscode 中管理数据库



### 项目管理

* EditorConfig
项目风格统一神器

* Gist Extension
代码片段管理

* Git Project Manager
git项目管理器，可以搜索本地git项目

* Project Manager
项目管理工具

![](https://box.kancloud.cn/1fc276b9b42d45f0801040b9ebff9722_999x570.png)

![](https://box.kancloud.cn/d7fd07d18c9705c259a3b477159fa6b8_959x237.png)

保存项目后就可以来回切换了。

* sftp
sftp管理

*  TortoiseSVN
没有svn 插件，不高兴

* WakaTime
程序员编程时间管理插件 能精确统计一周内每个项目花了多少时间，跨编辑器跨IDE，大神必备哦。

## 一些问题

### 自动完成不支持try catch补全
已报issue

### 符号链接 ctrl+r不起作用
去键盘快捷方式里 干掉其他占用ctrl+r的命令
![](https://box.kancloud.cn/821cbe571c45998607ee2b233f7e4204_363x307.png)

保留至：
![](https://box.kancloud.cn/4eb3e42b375d88b3ba89d2068c3ed019_1499x282.png)

默认会是打开最近浏览文件，我才不稀罕

### 打开文件夹是切换当前工作空间
我也不知道怎么配 但是我知道先新开一个窗口就好啦

![](https://box.kancloud.cn/4bc305945475c9bd1918ed9ad85ed826_592x65.png)

## 终端
vscode另外一个优于sublime的功能就是终端，*ctrl+~* 打开

![](https://box.kancloud.cn/06ecb51530a1f7d9df144863f2f446e3_1505x244.png)

我用他多开 多执行cli 就相当于多进程了。

## 我的配置
我的是基于win的，关键处打码，嘿嘿：

~~~
// 将设置放入此文件中以覆盖默认设置
{
    "php.executablePath": "D:/wamp64/bin/php/php7.0.10/php.exe",
    "php.validate.executablePath": "D:/wamp64/bin/php/php7.0.10/php.exe",
    "php.validate.run": "onType",
    "window.zoomLevel": 1,
    "window.restoreWindows": "one",
    "window.openFoldersInNewWindow": "off",
    "files.autoSave": "off",
    "window.openFilesInNewWindow": "on",
    "composer.executablePath": "C:/ProgramData/ComposerSetup/bin/composer.bat",
    "extensions.ignoreRecommendations": false,
    "sonarlint.ls.javaHome": "C:/Program Files/Java/jre1.8.0_141",
    "sync.gist": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "sync.lastUpload": "2017-07-23T13:32:53.762Z",
    "sync.autoDownload": false,
    "sync.autoUpload": false,
    "sync.lastDownload": "",
    "sync.forceDownload": false,
    "sync.anonymousGist": false,
    "sync.host": "",
    "sync.pathPrefix": "",
    "sync.quietSync": false,
    "sync.askGistName": false,
    "gist.oauth_token": "XXXXXXXXXXXXXXXXXXXXXX",
    "local-history.path": "",
    "search.useIgnoreFilesByDefault": true,
    "projectManager.svn.ignoredFolders": [
        "node_modules",
        "out",
        "typings",
        "test",
        ".history"
    ],
    "projectManager.git.ignoredFolders": [
        "node_modules",
        "out",
        "typings",
        "test",
        ".history"
    ],
    "search.exclude": {
        "**/node_modules": true,
        "**/bower_components": true,
        ".history": true
    },
    "php.suggest.basic":false
}

~~~

# 后记：
基本使用和sublime差不多，php主要用到语法报错、自动完成、快速切换文件，查看当前类的所有方法符号链接，切换定义等，还能行内看定义和使用了多少个地方。

查看定义：
![查看定义](https://box.kancloud.cn/0bfacca308dc418e9ab344db67d3fa1a_1144x427.png)

跳转定义：
![](https://box.kancloud.cn/20b6b781804c92b6db98044cc0d0215c_554x112.png)

查看所有引用：
![](https://box.kancloud.cn/77254f56396b89a2acf6ea9a3787f5c7_542x61.png)

格式化代码

欢迎给我提供建议。













