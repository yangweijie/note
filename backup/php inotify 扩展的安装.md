一、安装

1）  从内核和目录里面查看是否支持inotify

[root@nfs01 ~]# **uname -r**

**2.6.32-573.el6.x86_64**

[root@nfs01 ~]#** ls -l /proc/sys/fs/inotify/**    -→主要查看下面有没有三个目录

总用量 0

-rw-r--r-- 1 root root 0 1月  21 13:03 max_queued_events

-rw-r--r-- 1 root root 0 1月  21 13:03 max_user_instances

-rw-r--r-- 1 root root 0 1月  21 13:03 max_user_watches

**2****）检查是否有安装inotify ****如果没有就安装**

**rpm -qa inotify-tools**

没有就先安装epol源

yum.repos.d]# **wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo**

之后安装

[root@nfs01 ~]#** yum install inotify-tools -y**

**二、参数讲解、**

[root@nfs01 ~]# **which inotifywait**

**/usr/bin/inotifywait**

[root@nfsserver inotify-tools]# **bin/inotifywait —help**

r ：递归查询目录

q：打印很少的信息，仅仅打印监控事件的信息  安静状态

m：始终保持事件监听状态

excluder#排除文件或者目录的时候不区分大小写

timefmt：指定时间输出的格式

d ：后台运行

-e： 事件 里面有很多方法

![复制代码](https://common.cnblogs.com/images/copycode.gif)

下面是事件参数

Events:

        access          file or directory contents were read   访问

        modify          file or directory contents were written  修改

        attrib          file or directory attributes changed  属性发生变化

        close_write     file or directory closed, after being opened in 写入之后关闭

                        writeable mode

        close_nowrite   file or directory closed, after being opened in read-only mode

        close           file or directory closed, regardless of read/write mode 

        open            file or directory opened

        moved_to        file or directory moved to watched directory  移动到哪里

        moved_from      file or directory moved from watched directory

        move            file or directory moved to or from watched directory

        create          file or directory created within watched directory

        delete          file or directory deleted within watched directory

        delete_self     file or directory was deleted

        unmount         file system containing file or directory unmounted卸载

![复制代码](https://common.cnblogs.com/images/copycode.gif)

之后就可以和nfs共享服务器之间的实时备份

我曾七次鄙视自己的灵魂: 第一次,当它本可进取时，却故作谦卑； 第二次,当它空虚时，用爱欲来填充； 第三次,在困难和容易之间，它选择了容易； 第四次,它犯了错，却借由别人也会犯错来宽慰自己； 第五次,它自由软弱，却把它认为是生命的坚韧； 第六次,当它鄙夷一张丑恶的嘴脸时，却不知那正是自己面具中的一副； 第七次,它侧身于生活的污泥中虽不甘心，却又畏首畏尾。