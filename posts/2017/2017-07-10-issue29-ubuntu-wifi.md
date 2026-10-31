---
title: "小米笔记本安装 ubuntu 后，wifi 无法使用的解决方案："
date: 2017-07-10
tags: ["blog", "software", "linux", "shell"]
summary: "~~~ shell"
---

~~~ shell
vi /etc/modprobe.d/blacklist.conf
~~~

最后一行加入

~~~ conf
blacklist acer-wmi
~~~

保存退出重启就好了。
