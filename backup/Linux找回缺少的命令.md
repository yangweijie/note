在操作Linux 系统时，往往会误删除一部分文件或者移除软件时将依赖的系统包个删除掉，而当时未发现。而后续在需要某些命令或者执行某些操作时才发现提示无此命令，例如Centos 下删除iptables，导致initscripts 这个包被删除掉，而这个包提供ifup，ifdown，两个命令，缺少该文件会导致网卡无法启动。如果仅因为缺少某个命令重装系统，成本太高。

下面就是如何来解决这个问题，需要说明的时，下面的方法仅在服务器尚能正常运行且看可以访问网络的情况下才可使用。如果没有网络，那么需要先配置好网络。

在Centos中，删除iptables 后，又重启了network服务后者服务器，就会发现，网卡无法启动，提示缺少ifup这个命令。需要把这个命令找回来，但是这个时候没有网络，就无法进行修复。
此时虽然网络服务虽然无法启动，但是还是可以通过手工启动网卡来恢复网络。
使用ifconfig eth0 up 来启动网卡。
ifconfig eth0 172.16.0.1 netmask 255.255.255.0 #配置IP和掩码
route add default gw 172.16.15.253 # 配置网关

此时再试会发现网络已经恢复了，但是如何知道，ifup来属于哪个软件包提供呢，
这个时候找一个相同系统的机器，
使用which ifup 确定该命令的文件路径，通过此操作知晓ifup的路径 /usr/sbin/ifup
然后借助 rpm -qf /usr/sbin/ifup 或者 yum provides /usr/sbin/ifup 即可查到是哪个软件包提供的。
例如ifup 在Centos 7.4上 是由initscripts-9.49.39-1.el7.x86_64 提供。
执行 yum install initscripts 来安装回来。
此时再尝试重启network 网络服务就可以正常重启。
在某些时候，我们只是删除了某个命令，但是软件包还在，如何处理？
这个时候，可以让yum 重新安装该软件包， yum reinstall initscripts

如果Ubuntu上，遇到类似命令如何处理？

以last命令丢失为例，
先安装 apt-file
apt-get install apt-file
安装完成后，执行 apt-file search /usr/bin/last
此时会提示apt-file 需要更新，
执行apt-file update
然后重新执行 apt-file search /usr/bin/last
得到util-linux: /usr/bin/last
执行 apt-file install util-linux 会提示已经安装过了，
此时就要让其重新安装

apt-get --reinstall install util-linux
完成后，看last 命令是不是回来了。