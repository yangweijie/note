最近用windows 开发了，smartgit 破解不了。
后来发现官方22版去除非商业使用了。之前的smartgit-agent 总是启动不了。
发现家里mac 的21.17 一直使用。去下了对应的便携版无果。于是回到21.1.14（刚又试了下可以。）
最后细心的发现， `-javaagent:D:\GreenSoft\smartgit-agent\smartgit-agent.jar` 是放在最后一行，心想，是不是执行顺序不对。
于是调整了下。也去除了双引号。

~~~
-javaagent:D:\GreenSoft\smartgit-agent\smartgit-agent.jar
;-javaagent:${smartgit.installation}/crack/smartgit-agent.jar
-Dsmartboot.sourceDirectory=.updates
-Dsmartgit.settings=${smartgit.installation}\.settings
-XX:ErrorFile=%EXE4J_EXEDIR%..\.settings\hs_err_pid%p.log
~~~

想着把破解文件直接放在 程序根目录 做成真绿色软件 参考 ${smartgit.installation} 路径的。结果不行。

总结：

-    下载 21.1.17版
-    修改 smartgit.vmoptions 文件， 首行加上`-javaagent:D:\GreenSoft\smartgit-agent\smartgit-agent.jar`  全路径
-   首次启动smart-git 选择注册， 浏览license.zip 点击注册，大工告成！

