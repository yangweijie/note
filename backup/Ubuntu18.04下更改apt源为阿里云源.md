前言：看见Ubuntu新出了18.04版本感觉不错，装一个玩玩，虽然有很多教程可以参考，但我也给出一个不是很一样的方案吧，尽量解释的详细一点。

为了下载更方便，速度更快，我们往往在使用Linux系列系统时修改apt源为国内的源，一般选择有阿里云，豆瓣之类的，下面简单说下如何更改为阿里云源。

1.复制源文件备份，以防万一

我们要修改的文件是sources.list，它在目录/etc/apt/下，sources.list是包管理工具apt所用的记录软件包仓库位置的配置文件，同样类型的还有位于 同目录下sources.list.d文件下的各种.list后缀的各文件。

命令如下：

sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

2.编辑源列表文件

命令如下：

sudo vim /etc/apt/sources.list

如果报错：sudo:vim:command not found    说明没装vim编辑器

使用命令：

sudo apt-get install vim 安装即可

3.查看新版本信息

其实Ubuntu18.04版之前的任一版更改apt源为国内源方法早就有了，内容大同小异，我们应当掌握其规律了，其实每一版内容不同的地方就是版本号（或者官方一点的说：系统代号），所以我们先了解下新版本的系统代号：

使用如下命令：

lsb_release -c

得到本系统的系统代号，如下图所示：



我们可以看到新版本的Ubuntu系统代号为bionic

同样的我们也可以得到之前任意版本的系统代号：

Ubuntu 12.04 (LTS)代号为precise。

Ubuntu 14.04 (LTS)代号为trusty。

Ubuntu 15.04 代号为vivid。

Ubuntu 15.10 代号为wily。

Ubuntu 16.04 (LTS)代号为xenial。

所以这也就解释了为什么我们百度出来的那么多方案里面内容不尽相同的原因，因为他们更改apt安装源时用的系统不一样。

4.将原有的内容注释掉，添加以下内容（或者你把里面内容修改成下面的就可以，但是不能有除了以下内容的有效内容）

deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

值得注意的是sources.list文件的条目都是有格式的（通过上面的内容大家也看的出来），一般有如下形式

所以后面几个参数是对软件包的分类（Ubuntu下是main， restricted，universe ，multiverse这四个）

所以你把内容写成

deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted 

deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed universe multiverse

之类的也是可以的，之前我有这个疑惑，所以在这里一并告知和我有一样疑惑的朋友。

5.更新软件列表

运行如下命令：

sudo apt-get update

6.更新软件包

运行如下命令：

sudo apt-get upgrade

7.最后说两句

关于sudo apt-get update与sudo apt-get upgrade有什么区别，推荐一篇博文，一看就懂

https://blog.csdn.net/beckeyloveyou/article/details/51352426

同时我借鉴了博友gong_xucheng的少部分博文，地址如下

https://blog.csdn.net/gong_xucheng/article/details/53886271

在此表示感谢。