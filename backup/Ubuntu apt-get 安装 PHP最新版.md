直接用官方PPA源

sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update
1
2
显示软件安装包列表，是否已经有了PHP 7.1，可选

apt-cache pkgnames | grep php7.1
1
安装，2018年05月08日 星期二，现在的最新版是7.2

sudo apt-get install php7.2-fpm
