| kernel 4.9版本后的内核新增了一款TCP拥塞控制技术：BBR，这个是好东西。建议百度细看，你会有惊喜！

首先要看看你但前的内核版本：
在终端输入：`uname -a`
~~~ shell
Linux yh-Study-pc 4.9.0-deepin5-amd64 #1 SMP PREEMPT Deepin 4.9.8-5 (2017-05-02) x86_64 GNU/Linux
~~~
看红色字体哪里，如果是4.9以后的版本就可以使用了。

~~~ shell
sudo gedit /etc/sysctl.conf 
~~~
在 /etc/sysctl.conf  最后面加入下面两行，开启内核BBR的配置

``` shell
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
```
保存退出。

让刚才配置的 sysctl.conf 现在生效
`sudo  sysctl -p`

检查bbr是否生效：
`sudo sysctl net.ipv4.tcp_available_congestion_control`
如果输出
`net.ipv4.tcp_available_congestion_control = bbr cubic reno`
而且
`sudo lsmod | grep bbr`
有 tcp_bbr 进程 号 ，说明开启成功了。

特别是移动 ， 联通 宽带的用户，快来体验一下吧。 |