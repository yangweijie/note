首先查看系统对中文的支持

```
locale -a | grep zh_CN

    zh_CN
    zh_CN.gb18030
    zh_CN.gb2312
    zh_CN.gbk
    zh_CN.utf8

vi ~/.bash_profile
文件末尾添加:
    export LANG="zh_CN.UTF-8"
    export LC_ALL="zh_CN.UTF-8"
    export LANG="en_US.UTF-8"
    export LC_ALL="en_US.UTF-8"
```


在php文件调用exec前设定环境变量
```
    $locale='en_US.UTF-8';  // 或  $locale='zh_CN.UTF-8';
    setlocale(LC_ALL,$locale);
    putenv('LC_ALL='.$locale);
```
————————————————
版权声明：本文为CSDN博主「小米啄鸡」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_35020783/article/details/81299287