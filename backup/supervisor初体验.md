

**1.安装**

宿主机环境：（Centos7）

![](http://upload-images.jianshu.io/upload_images/35360-3d52bb0de044d78d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

宿主机环境

#yum install python-setuptools

![](http://upload-images.jianshu.io/upload_images/35360-e10c50020df81643.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

yum install python-setuptools

#easy_install supervisor

![](http://upload-images.jianshu.io/upload_images/35360-3efd1976de43fa03.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

easy_install supervisor

**测试安装是否成功：**

#echo_supervisord_conf

![](http://upload-images.jianshu.io/upload_images/35360-0fa69d64c0541fd4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

echo_supervisord_conf

**2.创建配置文件**

创建supervisor配置文件目录/etc/supervisor/

#mkdir -m 755 -p /etc/supervisor/

![](http://upload-images.jianshu.io/upload_images/35360-a35442b3b3322d2f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

mkdir -m 755 -p /etc/supervisor/

创建主配文件supervisord.conf

#echo_supervisord_conf > /etc/supervisor/supervisord.conf

![](http://upload-images.jianshu.io/upload_images/35360-57b2b291869440b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

echo_supervisord_conf > /etc/supervisor/supervisord.conf

创建项目配置文件目录

# mkdir -m 755 conf.d

![](http://upload-images.jianshu.io/upload_images/35360-bdf1528dab7d0811.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# mkdir -m 755 conf.d

3.调试

在/home/k1ic/supervisor_simple 目录下创建test.c

![](http://upload-images.jianshu.io/upload_images/35360-02ba4cf694e9a6f0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

test.c

编译为test #gcc -o test test.c

![](http://upload-images.jianshu.io/upload_images/35360-cf151a9c4551a838.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

gcc -o test test.c

在/etc/supervisor/conf.d 目录下创建 test.ini

![](http://upload-images.jianshu.io/upload_images/35360-941fcf9c291e0caf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

test.ini

在主配文档中引入test.ini

![](http://upload-images.jianshu.io/upload_images/35360-7a827afc1b0a1460.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

files = ./conf.d/*.ini

启动supervisor

# supervisord -c /etc/supervisor/supervisord.conf

![](http://upload-images.jianshu.io/upload_images/35360-69e6e917e6739846.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

supervisord -c /etc/supervisor/supervisord.conf

![](http://upload-images.jianshu.io/upload_images/35360-b03469800dce2f08.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

pstree -p | grep supervisord

查看supervisord.log发现program test已启动

# cat /tmp/supervisord.log

![](http://upload-images.jianshu.io/upload_images/35360-5078fcc82a70ca05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# cat /tmp/supervisord.log

用 supervisorctl 查看已经被监控的program（**注：直接用 #supervisorctl 会提示：http://localhost:9001 refused connection**）

#supervisorctl -c /etc/supervisor/supervisord.conf

![](http://upload-images.jianshu.io/upload_images/35360-56c63f5d75495aa4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

supervisorctl -c /etc/supervisor/supervisord.conf

增加一例监控php脚本

创建skud.ini

![](http://upload-images.jianshu.io/upload_images/35360-a3dbfb53f038b47e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

skud.ini

![](http://upload-images.jianshu.io/upload_images/35360-727cca0530107c8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[program:skuld]

在/home/k1ic/supervisor_simple目录下创建skuld.php

![](http://upload-images.jianshu.io/upload_images/35360-6b747b9cd5bf02e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

skuld.php

重启监控服务

![](http://upload-images.jianshu.io/upload_images/35360-e97398ee02681218.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

reload

![](http://upload-images.jianshu.io/upload_images/35360-c8322a7f66809846.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

pstree

================分割线================

**这才是重点^^**

0\. supervisor 比较适合监控业务应用，且只能监控前台程序，**php fork方式实现的daemon不能用它监控，**否则supervisor> status 会提示：**BACKOFF  Exited too quickly (process log may have details)**

![](http://upload-images.jianshu.io/upload_images/35360-e05f53999df42586.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**BACKOFF  Exited too quickly (process log may have details)**

![](http://upload-images.jianshu.io/upload_images/35360-dd9a1b44b39d19e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

cat supervisord.log

1.每次修改配置文件后**需进入supervisorctl，执行reload**， 改动部分才能生效

![](http://upload-images.jianshu.io/upload_images/35360-8aaf0b1f7e40807b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

reload

2.两个命令

supervisord : supervisor的服务器端部分，用于supervisor启动

supervisorctl：启动supervisor的命令行窗口，在该命令行中可执行start、stop、status、reload等操作。

3.web管理界面

将supervisord.conf中[inet_http_server]部分做相应配置，在supervisorctl中reload即可启动web管理界面

![](http://upload-images.jianshu.io/upload_images/35360-55d5439d676f0474.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[inet_http_server]

![](http://upload-images.jianshu.io/upload_images/35360-a95a906d7d1fa4d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

http://107.170.249.52:9001/?message=Page%20refreshed%20at%20Tue%20Sep%2029%2016%3A20%3A40%202015

参考文献：

Supervisor的安装与使用入门

http://fukun.org/archives/07102224.html

按需讲解之Supervisor

http://www.cnblogs.com/yjf512/archive/2012/03/05/2380496.html

supervisord entered FATAL state, too many start retries too quickly错误处理

http://beginman.cn/linux/2015/09/25/error-about-supervisord/

Supervisor监控PHP进程

http://www.phpddt.com/php/supervisor.html

关于进程监控及自动启动

http://www.vimer.cn/2013/07/%E5%85%B3%E4%BA%8E%E8%BF%9B%E7%A8%8B%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%87%AA%E5%8A%A8%E5%90%AF%E5%8A%A8.html

centos服务安装 #37

Supervisor学习

http://beginman.cn/linux/2015/04/06/Supervisor/

通过进程模型进行扩展

http://12factor.net/zh_cn/concurrency

作者：k1ic
链接：http://www.jianshu.com/p/9abffc905645
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。