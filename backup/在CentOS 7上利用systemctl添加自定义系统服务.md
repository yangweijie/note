CentOS 7继承了RHEL 7的新的特性，例如强大的systemctl，而systemctl的使用也使得以往系统服务的/etc/init.d的启动脚本的方式就此改变，也大幅提高了系统服务的运行效率。但服务的配置和以往也发生了极大的不同，说实在的，变的简单而易用了许多。

下面我们以利用forever来实现Node.js项目自启动为例，初探CentOS 7的systemctl。

前提：Node.js环境已配置成功，forever包安装成功，有一个能跑的Node.js程序。

CentOS 7的服务systemctl脚本存放在：/usr/lib/systemd/，有系统（system）和用户（user）之分，像需要开机不登陆就能运行的程序，还是存在系统服务里吧，即：/usr/lib/systemd/system目录下

每一个服务以.service结尾，一般会分为3部分：[Unit]、[Service]和[Install]，我写的这个服务用于开机运行Node.js项目，具体内容如下：

[Unit]
Description=xiyoulibapi
After=network.target remote-fs.target nss-lookup.target
 
[Service]
Type=forking
PIDFile=/node.js/pid
ExecStart=/usr/local/bin/forever start /node.js/xiyoulib/bin/www
ExecReload=/usr/local/bin/forever restart /node.js/xiyoulib/bin/www
ExecStop=/usr/local/bin/forever stop /node.js/xiyoulib/bin/www
PrivateTmp=true
 
[Install]
WantedBy=multi-user.target

[Unit]部分主要是对这个服务的说明，内容包括Description和After，Description用于描述服务，After用于描述服务类别

[Service]部分是服务的关键，是服务的一些具体运行参数的设置，这里Type=forking是后台运行的形式，PIDFile为存放PID的文件路径，ExecStart为服务的具体运行命令，ExecReload为重启命令，ExecStop为停止命令，PrivateTmp=True表示给服务分配独立的临时空间，注意：[Service]部分的启动、重启、停止命令全部要求使用绝对路径，使用相对路径则会报错！

[Install]部分是服务安装的相关设置，可设置为多用户的

服务脚本按照上面编写完成后，以754的权限保存在/usr/lib/systemd/system目录下，这时就可以利用systemctl进行配置了

首先，使用systemctl start [服务名（也是文件名）]可测试服务是否可以成功运行，如果不能运行则可以使用systemctl status [服务名（也是文件名）]查看错误信息和其他服务信息，然后根据报错进行修改，直到可以start，如果不放心还可以测试restart和stop命令。

接着，只要使用systemctl enable xxxxx就可以将所编写的服务添加至开机启动即可。

我的脚本编写方法参照了nginx的编写方法，也可以根据其他功能类似的程序。

这样看来，虽然systemctl比较陌生，但是其实比init.d那种方式简单不少，而且使用简单，systemctl能简化的操作还有很多，现在也有不少的资料，看来RHEL/CentOS比其他的Linux发行版还是比较先进的，此次更新也终于舍弃了Linux 2.6内核，无论是速度还是稳定性都提升不少。
