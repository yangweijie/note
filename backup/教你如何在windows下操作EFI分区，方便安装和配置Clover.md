# 教你如何在windows下操作EFI分区，方便安装和配置Clover

摘 要

使用Clover引导的朋友可能对EFI分区不陌生吧，EFI是中可扩展借口，Clover四叶草启动引导工具就是通过EFI的方式引导的，所以用clover安装黑苹果就需要对CEFI分区进行操作，下面介绍一下在windows下如何操作EFI分区。

*   [文章前言](https://www.kancloud.cn/book/yangweijie/problem/edit#title-0)
*   [必要条件](https://www.kancloud.cn/book/yangweijie/problem/edit#title-1)
*   [操作方法](https://www.kancloud.cn/book/yangweijie/problem/edit#title-2)

文章目录

文章前言

使用Clover引导的朋友可能对[EFI分区](https://imac.hk/tag/efi%e5%88%86%e5%8c%ba/)不陌生吧，EFI是中可扩展借口，英文名Extensible Firmware Interface 或EFI，是由英特尔，一个主导个人电脑技术研发的公司推出的一种在未来的类PC的电脑系统中替代BIOS的升级方案。

跟我们传统的BIOS的引导模式分UEFI的流程对比图：

![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/06eddf11ac10f07d7d679abd8528c8b2.jpg)

Clover四叶草[启动引导](https://imac.hk/tag/%e5%90%af%e5%8a%a8%e5%bc%95%e5%af%bc/)工具就是通过EFI的方式引导的，所以用clover安装黑苹果就需要对CEFI分区进行操作，下面介绍一下在windows下如何操作EFI分区。

必要条件

1.  首先BIOS支持UEFI模式，估计现在的主板都支持吧。
2.  你是有系统Administrator的运行权限。

操作方法

1.  快捷键WIN+R打开运行窗口运行CMD，输入diskpart进行磁盘管理。
    ![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/3ae00088bb97397d55c82377f025baba.png)
2.  输入list disk 查看电脑上挂载的硬盘。
    ![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/5ade6180c092fa7637ff034ca6bfed91.png)下面的“磁盘0”就是你的第一块硬盘，如果你有多个硬盘可以选择其他的。
3.  输入select disk 0 选择编号为0的硬盘进行操作。
    ![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/adf1b8c49022f8f08f445de7a13cc56f.png)
4.  输入list vol 查看我们的分区表。
    ![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/85b1ca6bb380cc74c2fc1e70fd551c60.png)其中看到编号为6的分区200MB左右FAT格式的分区，这个就是我们要操作的EFI分区了，下面对他进行分配磁盘号.
5.  输入select vol 6选择要操作的磁盘号，我的EFI分区号是6所以我这里选择6。
    ![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/a08cf0753ca0b7a11cde4285834e4df7.png)
6.  输入ass让系统给他分配一个驱动号或装载点。
    ![教你如何在windows下操作EFI分区，方便安装和配置Clover](http://newsget-cache.stor.sinaapp.com/17514769c62f93d97f270a28cb2c4df3.png)
7.  输入set id=ebd0a0a2-b9e5-4433-87c0-68b6b72699c7，这一步很重要设置分区属性。

至此，你就可以像普通分区一样操作efi分区了。不过建议efi分区的文件修改完成后把efi分区的id改回去。