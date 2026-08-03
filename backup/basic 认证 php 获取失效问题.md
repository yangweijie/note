用的php apidoc  有一个basic 认证 之前一直好好的，突然同事说 判断沙盒方式的错了。

百度了一下
> Run phpinfo(). if "Server API" is CGI/FCGI, you can pretty much forget it as there is no sensible way to use HTTP auth from PHP.

通过.htaccess 文件 添加路由 可以解决

```
<IfModule mod_rewrite.c>
RewriteEngine on
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization},L]
</IfModule>
```