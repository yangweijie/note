 日志记录中HTTP状态码出现499错误有多种情况，我遇到的一种情况是nginx反代到一个永远打不开的后端，就这样了，日志状态记录是499、发送字节数是0。

    老是有用户反映网站系统时好时坏，因为线上的产品很长时间没有修改，所以前端程序的问题基本上可以排除，于是就想着是Get方式调用的接口不稳定，问了相关人员，说没有问题，为了拿到确切证据，于是我问相关人员要了nginx服务器的日志文件（awstats日志），分析后发现日志中很多错误码为499的错误，约占整个日志文件的1%，而它只占全部报错的70%左右（全部报错见下图），那么所有报错加起来就要超过1%了，这个量还是特别大的。

    499错误是什么？让我们看看NGINX的源码中的定义：

ngx_string(ngx_http_error_495_page), /* 495, https certificate error */
ngx_string(ngx_http_error_496_page), /* 496, https no certificate */
ngx_string(ngx_http_error_497_page), /* 497, http to https */
ngx_string(ngx_http_error_404_page), /* 498, canceled */
ngx_null_string,                    /* 499, client has closed connection */

    可以看到，499对应的是 “client has closed connection”。这很有可能是因为服务器端处理的时间过长，客户端“不耐烦”了。

    Nginx 499错误的原因及解决方法
    打开Nginx的access.log发现在最后一次的提交是出现了HTTP1.1 499 0 -这样的错误，在百度搜索nginx 499错误，结果都是说客户端主动断开了连接。
    但经过我的测试这显然不是客户端的问题，因为使用端口+IP直接访问后端服务器不存在此问题，后来测试nginx发现如果两次提交post过快就会出现499的情况，看来是nginx认为是不安全的连接，主动拒绝了客户端的连接.

    但搜索相关问题一直找不到解决方法，最后终于在google上搜索到一英文论坛上有关于此错误的解决方法：
proxy_ignore_client_abort on;
Don’t know if this is safe.
    就是说要配置参数 proxy_ignore_client_abort on;
    表示代理服务端不要主要主动关闭客户端连接。

    以此配置重启nginx,问题果然得到解决。只是安全方面稍有欠缺，但比总是出现找不到服务器好多了。

    还有一种原因是 我后来测试发现 确实是客户端关闭了连接,或者说连接超时 ,无论你设置多少超时时间多没用 原来是php进程不够用了 改善一下php进程数 问题解决 默认测试环境才开5个子进程。