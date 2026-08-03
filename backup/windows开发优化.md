# 命令行

## Scoop
`iex (new-object net.webclient).downloadstring('https://get.scoop.sh')`

`scoop bucket add extras`
`scoop bucket add php-bucket https://github.com/nueko/php-ext-bucket`
`scoop bucket add php`

## pickle
[pickle ](https://github.com/FriendsOfPHP/pickle) 用来安装 php扩展

win php扩展下载目录
http://windows.php.net/downloads/pecl/releases/

https://github.com/Microsoft/php-sdk-binary-tools

```
cd php-sdk 

phpsdk_buildtree phpdev
```
cd C:\php-sdk\phpdev\vc15\x64
`git clone -b PHP-7.2.6 https://github.com/php/php-src.git`

cd php-src

## pacman -Syu