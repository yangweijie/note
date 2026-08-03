# 自建git

由于码云项目出了企业版 每个项目成员最多5个人。
虽然coding允许免费5个私有项目，为了不受限制，我们决定阿里云服务器上自建git仓库。

1.安装
yum install git git-daemon
2. 配置 Git
在 CentOS 中，Git 是以 xinetd 方式提供服务的，默认的 xinetd 配置文件在：/etc/xinetd.d/git。
编辑配置文件，以下是改好的一份 git xinetd 配置文件：
~~~
# default: off
# description: The git dæmon allows git repositories to be exported using \
#       the git:// protocol.
service git
{
    disable = no
        socket_type     = stream
        wait            = no
        user            = nobody
        server          = /usr/libexec/git-core/git-daemon
        server_args     = --base-path=/var/lib/git --export-all --user-path=public_git --syslog --inetd --verbose
        log_on_failure  += USERID
}
~~~
接下来启动 xinetd 服务：
[root@c1.inanu.net]#
`service xinetd start`
3. 建立 Puppet 服务器端 Git 仓库
~~~
[root@c1.inanu.net]# useradd -d /var/lib/git -s /usr/bin/git-shell git #创建 git 用户
[root@c1.inanu.net]# passwd git #设置 git 用户密码
[root@c1.inanu.net]# chown -R git:git /var/lib/git
[git@c1.inanu.net]$ cd /var/lib/git
[git@c1.inanu.net]$ mkdir .ssh
[git@c1.inanu.net]$ chmod 700 .ssh
[git@c1.inanu.net]$ touch .ssh/authorized_keys
[git@c1.inanu.net]$ chmod 600 .ssh/authorized_keys
[git@c1.inanu.net]$ mkdir /var/lib/git/xx.git #创建 Puppet 服务器端 Git 仓库
[git@c1.inanu.net]$ sudo chown -R git:git xx.git
[git@c1.inanu.net]$ cd /var/lib/git/xx.git 注意是否是git的权限
[git@c1.inanu.net]$ git --bare init #初始化 Puppet 服务器端 Git 仓库
~~~
4.客户端clone
`git clone git@ip:xx/path 全路径`

已有项目如何迁移
1. 本地clone  刚建的项目
2. 拷贝本地已有项目所有文件 到这个目录后提交
3. 设置远程项目 remote 为新的地址
4. 尝试更新

更新 账户密码  git git2018

查看远程地址
~~~
Git remote -v
git remote set-url origin ssh://git@116.62.11.197:58585/home/git/ws.git
~~~
无法加入know_hosts 
1.	chown username: /home/username/.ssh  
2.	chown username: /home/username/.ssh/*  
3.	chmod 700 /home/username/.ssh  
4.	chmod 600 /home/username.ssh/*  

![](blob:https://www.kancloud.cn/91d078a3-4863-4441-be5a-943609dbd5a5)