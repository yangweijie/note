---
title: "使用LSP插件将 sublime 变成 PHP IDE-后续篇"
date: 2018-11-27
tags: []
summary: "58 上次说将sublime编程 PHP IDE 其实效果并没有达到。只是状态栏上显示server 启动了。对于他所提供的特性，一点都没能正常使用。我还加了gi…"
---

#58 上次说将sublime编程 PHP IDE 其实效果并没有达到。只是状态栏上显示server 启动了。对于他所提供的特性，一点都没能正常使用。我还加了gitter 想和作者沟通来着。结果没有解决这问题。他们都说没问题。
![image](https://user-images.githubusercontent.com/1614114/49049644-dae03b80-f21a-11e8-8407-d5544e759649.png)

然后最近之前的网友米米饭 突然也进了我们的sublime群，说问有什么好的php工具能及时提示报错的。
我就推荐了lsp，想让他帮着一起研究。但是自己一想，老是这么不明不白的使用，不是办法。vscode的sonarlint 完爆st的lsp。然后公司新电脑的环境又搭了一遍。我就不行这个邪，不能把lsp搞出来。

于是乎上周末在家一天先是将家里电脑系统换成了 win10 ltsc。然后开始折腾st的lsp。他们都说能用了，我想是不是哪配置有问题。就去找issue。别说真让我找到了php无法使用的issue。已经修复好了。

https://github.com/tomv564/LSP/issues/321  和 https://github.com/tomv564/LSP/issues/151

经过我的研究，将配置改为下面的配置，重启st 打开php文件 打开lsp的调试 控制台里看到 parse 你项目目录下的php文件，就大工告成了。并且右键菜单上的也亮了。

```
{
	"clients":
    {
        "phpls": {
            "enabled": true,
            "tcp_port": 5555,
            "command": [
                "php",
                "C:/Users/jay/AppData/Roaming/Composer/vendor/felixfbecker/language-server/bin/php-language-server.php",
                "--memory-limit=512M",
                "--tcp-server=0.0.0.0:5555"
            ],
            "scopes": ["source.php"],
            "syntaxes": ["Packages/PHP/PHP.sublime-syntax"],
            "languageId": "php"
        }
    },
    "show_status_messages": true,
    "show_view_status": true,
    "auto_show_diagnostics_panel": false,
    "show_diagnostics_phantoms": false,
    "show_diagnostics_in_view_status": true,
    // highlight style of code diagnostics: "underline" or "box"
    "diagnostics_highlight_style": "underline",
    // gutter marker for code diagnostics: "dot", "circle", "bookmark", "cross" or ""
    "diagnostics_gutter_marker": "dot",
    "complete_all_chars": true,
    "only_show_lsp_completions": false,
    "resolve_completion_for_snippets": false,
    "log_debug": true,
    "log_server": true,
    "log_stderr": true
}
```

![image](https://user-images.githubusercontent.com/1614114/49049896-f26bf400-f21b-11e8-8efc-45eda8397377.png)
![image](https://user-images.githubusercontent.com/1614114/49049921-0c0d3b80-f21c-11e8-9f6d-42526834c7a9.png)
![image](https://user-images.githubusercontent.com/1614114/49052373-8347cd00-f226-11e8-8d8d-45181e2a0fdb.png)


主要还有一个问题，不知道如何提示方法参数。
![image](https://user-images.githubusercontent.com/1614114/49049946-2810dd00-f21c-11e8-92f0-41127a8b04b1.png)

总结，之前配置的php client 没带端口，而win下 只能带端口才能监听到lsp的server。还是应该多看看issue。差点就跑去看lsp的源码了。
