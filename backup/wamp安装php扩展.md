pecl的mongodb扩展链接我们很多开发工作都要在windows下进行，但是在windows下给这些脚本程序安装一些插件扩展都比较麻烦，没有办法像linux环境一样一行命令完成，这里我在为PHP安装mongodb扩展的时候遇到了一些问题，特此写一遍wamp安装php扩展的教程。

1.下载`mongodb`扩展

下载windows环境下php的mongodb扩展。

windows下的php的扩展一般都是dll文件，mongodb的php扩展在这里下载：

[http://pecl.php.net/package/mongo](http://pecl.php.net/package/mongo)

我们这里选择最新的dll下载就好了。

扩展一般会区分non thread safe (非线程安全)和thread safe（线程安全）区别就在于，非线程安全一般搭配IIS环境使用，线程安全搭配apache使用。当然除此之外php还有 VC6 VC9版本区分VC6和VC9一个支持apache一个支持IIS，VC9 用在apache上也没问题。当然这里还有更多内容这里就不再详细讨论了。

我的环境是win10 64位 wamp（apache+php5.5）那么就下载php5.5 Thread Safe(TS)x64的那个文件。

2.安装mongodb扩展

下载好以后打开压缩包我们会发现`php_mongo.dll`文件。

将这个文件复制到“wamp\bin\php\php5.5.12\ext”这个路径的文件夹下面。

如果你自己安装的php就复制到php的ext文件夹当中。然后我们要修改`php.ini`配置文件来让PHP加载这个扩展。

找到你的php.ini编辑这个文件，添加

`extension=php_mongo.dll` 添加到这个文件目的是为了告诉PHP我们安装了这么一个扩展下次启动的时候要启动这个扩展。

3.让mongodb的扩展找到libsasl.dll依赖库

libsasl.dll是在php根目录下的一个文件夹，本文的mongodb需要依赖这个dll。由于wamp安装的过程当中不会添加php的环境变量，所以我们在使用php的mongodb扩展的时候，扩展无法找到libsasl.dll的位置导致mongodb的扩展是无法使用的。

我们需要把php的目录路径添加到我们的系统环境变量里面。

4.测试mongodb扩展安装是否成功

最后我们重启所有的wamp服务，最好把wamp关闭再重新打开。启动wamp的localhost网页，找到phpinfo()

出现mongo的字样就对了，说明mongodb安装成功了。