一、安装JDK

1、下载JDK

Oracle 1.7以后才有Mac版，1.6以前的版本都是苹果公司编译的。 

Apple下载地址：https://developer.apple.com/downloads/index.action# 

Oracle下载地址：http://www.oracle.com/technetwork/java/javase/downloads/index.html 

2、安装JDK

双击dmg文件，按提示安装即可。

3、查看JDK安装路径

打开终端，执行     /usr/libexec/java_home -V

MacBook-Air:~ eng$ /usr/libexec/java_home -V
Matching Java Virtual Machines (4):
    1.8.0_101, x86_64:  "Java SE 8"     /Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home
    1.7.0_79, x86_64:   "Java SE 7"     /Library/Java/JavaVirtualMachines/jdk1.7.0_79.jdk/Contents/Home
    1.6.0_65-b14-466.1, x86_64: "Java SE 6"     /System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home
    1.6.0_65-b14-466.1, i386:   "Java SE 6"     /System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home
/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home

  

Apple JDK路径(默认JDK1.6)：/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home

Oracle JDK路径(JDK1.8为例) :  /Library/Java/JavaVirtualMachines/jdk1.8.0_112.jdk/Contents/Home

系统默认的 JDK 版本，是通过 link 来实现的，也就是说 Java 程序如 Maven、Eclispe 选择哪个 JDK 是通过各自的启动脚本，按照约定的 link 文件去查找 Java 程序的。比如 Maven 就会先找 Apple 派的 JDK 后找 Oracle 派的 JDK。

Apple 派的 JDK 通过把文件 /System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDKlink 到某个版本的 JDK 实现了多版本支持。

Oracle 派的 JDK 学习 Aplle 派的方法也支持多版本，link 文件是 /System/Library/Frameworks/JavaVM.framework/Versions/Current。

4、设置JAVA_HOME

最佳方式：export JAVA_HOME='usr/libexec/java_home'

另外，你还可以这样用，来选择不同的Java版本：
export JAVA_HOME='/usr/libexec/java_home -v 1.6'
或者 

export JAVA_HOME='/usr/libexec/java_home -v 1.7'

二、卸载JDK

参考文章：[如何在 Mac 上卸载 Java？](https://java.com/zh_CN/download/help/mac_uninstall_java.xml)

#### 使用终端卸载 Oracle Java

注：要卸载 Java，必须具有管理员权限，并且必须以 root 用户身份或者使用 `sudo` 工具来执行删除命令。

按照下面所示，删除一个目录和一个文件（符号链接）：

1.  单击位于停靠栏中的 Finder 图标
2.  单击实用程序文件夹
3.  双击终端图标
4.  在“终端”窗口中，复制和粘贴命令：
    `sudo rm -fr /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin`
    `sudo rm -fr /Library/PreferencesPanes/JavaControlPanel.prefPane`
    `sudo rm -fr ~/Library/Application\ Support/Java`

请勿尝试通过从 `/usr/bin` 删除 Java 工具来卸载 Java。此目录是系统软件的一部分，下次对操作系统执行更新时，Apple 会重置所有更改。

参考文章：

[有关在 Mac OS X 上安装和使用 Oracle Java 的信息和系统要求](https://java.com/zh_CN/download/faq/java_mac.xml)