先手动最小化d盘装一遍 cygwin64 然后将其重命名cygwin642


下载 [网盘](https://www.yunzhongzhuan.com/#sharefile=PUNA75rL_4607214)中的压缩包 解压至d 或其他非C 盘的根目录

压缩包里的用户名是Administrator 如果 当前机器用户不是，就手动将home/Administrator 改为自己用户，然后 双击开始菜单里的Cygwin64 Terminal 进入，将 /usr/bin 下的composer74s.bat 里d 改为实际判断（已经是d 无需更改）。

环境变量path 里 导入d:/cygwin64/bin （terminal里是/usr/bin win里只有/bin）后，

这样就可以 在cmd里 php74s -m  查看确认有swoole 扩展，composer74s 可以更新linux 下依赖了。

composer74s 加速

`composer74s config -g repo.packagist composer https://mirrors.aliyun.com/composer/`

`composer74s repo:use 1`


![5526ed786ac7a500b33d3daaf61fb3d](https://github.com/yangweijie/note/assets/1614114/7cf351b3-309e-45a1-befa-f5a9f586dd02)
