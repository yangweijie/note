在thinkphp5中提供了数据迁移工具(think-migration),它是机遇phinx开发(文档地址：[http://docs.phinx.org/en/latest/](http://docs.phinx.org/en/latest/))

一：配置think-migration

在commond.php 中添加



~~~
<?php 
return [ "think\\migration\\command\\migrate\\Create",
    "think\\migration\\command\\migrate\\Run",
    "think\\migration\\command\\migrate\\Rollback",
    "think\\migration\\command\\migrate\\Status",
    "think\\migration\\command\\seed\\Create",
    "think\\migration\\command\\seed\\Run", ]; 
~~~



注意由于think-migration存放在thinkphp/vendor中 所以在think中需要将vendor加入auoload

`require __DIR__.'/../thinkphp/vendor/autoload.php';`

二：命令行运行

 在命令行输入php think 可以看见

![](https://images2015.cnblogs.com/blog/447797/201703/447797-20170323101103877-508042847.png)

migrate:数据库迁移工具 seed:数据库填充工具

主要讨论migrate:

  migrate:create : 创建一个新的数据迁移类,php think migrate:create ,文件名须采用驼峰命名法

  forexample:php think migrate:create ScProductImage 文件会在制定目录下生成一个php文件

![](https://images2015.cnblogs.com/blog/447797/201703/447797-20170323102133361-523470162.png)

＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊

migrate:run : 完成数据迁移工作 `php think migrate:run`

＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊

migrate:status:查看migrate工作状态 `php think migrate:status`

![](https://images2015.cnblogs.com/blog/447797/201703/447797-20170323102649471-1084055119.png)

***********************************************************************************************

  migrate:rollback : 回滚数据到指定的一个数据迁移版本 `php think migrate:rollback -t `

   就是我们上图上面红框表示的值

三：migrate文件编写

     在migrate中有三个方法

     up:在migrate:run时执行(前提是文件中不存在change方法)

    down:在migrate:rollback时执行(前提是文件中不存在change方法)

    change:migrate:run 和migrate:rollback时执行 (如果存在该方法 则不会去执行up 与down)