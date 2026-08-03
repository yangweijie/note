## inotify扩展介绍

inotify是Linux内核提供的一组系统调用，它可以监控文件系统操作，比如文件或者目录的创建、读取、写入、权限修改和删除等。

inotify使用也很简单，使用inotify_init创建一个句柄，然后通过inotify_add_watch/inotify_rm_watch增加/删除对文件和目录的监听。

PHP中提供了inotify扩展，支持了inotify系统调用。inotify本身也是一个文件描述符，可以加入到事件循环中，配合使用swoole扩展，就可以异步非阻塞地实时监听文件/目录变化。

## 安装inotify/swoole扩展

如果已经安装了inotify/swoole可以跳过此步骤。

~~~
pecl install swoole
pecl install inotify
~~~

操作成功后，修改php.ini，加入

~~~
extension=swoole.so
extension=inotify.so
~~~

查看扩展是否加载成功：

~~~
php -m | grep swoole
php -m | grep inotify
~~~

## inotify的使用

首先在当前目录创建一个inotify.data文件，示例就用来监听此文件。

~~~
//创建一个inotify句柄
$fd = inotify_init();

//监听文件，仅监听修改操作，如果想要监听所有事件可以使用IN_ALL_EVENTS
$watch_descriptor = inotify_add_watch($fd, __DIR__.'/inotify.data', IN_MODIFY); 

while (true) {
    //阻塞地读取数据
    $events = inotify_read($fd);
    if ($events) {
        foreach ($events as $event) {
            echo "inotify Event :".var_export($event, 1)."\n";
        }
    }
}

//释放inotify句柄
inotify_rm_watch($fd, $watch_descriptor);
fclose($fd);
~~~

修改inotify.data，就可以看到程序输出了信息。

~~~
echo "hello world" > inotify.data

inotify Event :array (
  'wd' => 1,
  'mask' => 2,
  'cookie' => 0,
  'name' => '',
)
~~~

## swoole+inotify异步非阻塞监听文件

~~~
//创建一个inotify句柄
$fd = inotify_init();

//监听文件，仅监听修改操作，如果想要监听所有事件可以使用IN_ALL_EVENTS
$watch_descriptor = inotify_add_watch($fd, __DIR__.'/inotify.data', IN_MODIFY);

//加入到swoole的事件循环中
swoole_event_add($fd, function ($fd) {
    $events = inotify_read($fd);
    if ($events) {
        foreach ($events as $event) {
            echo "inotify Event :" . var_export($event, 1) . "\n";
        }
    }
});
~~~

这里使用了swoole扩展提供swoole_event_add函数，将inotify句柄设置为非阻塞，并加入到epoll事件循环中。程序变成异步非阻塞模式。当有事件发生时才会执行inotify_read获取事件。没有事件发生时，程序可以执行其他的逻辑。

此程序与上一个同步阻塞例子的逻辑是相同的，向inotify写入内容时也会打印事件信息。区别在于swoole+inotify的程序是异步的。可以支持并发监听大量文件和目录，并且除了inotify操作之外还可以执行其他的IO操作。

*   关于inotify更多的信息可以到PHP官方网站中查看 [http://php.net/inotify](http://php.net/inotify)

*   关于swoole更多信息，请到swoole官方网站取了解 [http://www.swoole.com/](http://www.swoole.com/)  