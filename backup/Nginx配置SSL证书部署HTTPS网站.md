**一、什么是 SSL 证书，什么是 HTTPS**
SSL 证书是一种数字证书，它使用 Secure Socket Layer 协议在浏览器和 Web 服务器之间建立一条安全通道，从而实现：
1、数据信息在客户端和服务器之间的加密传输，保证双方传递信息的安全性，不可被第三方窃听；
2、用户可以通过服务器证书验证他所访问的网站是否真实可靠。

HTTPS 是以安全为目标的 HTTP 通道，即 HTTP 下加入 SSL 加密层。HTTPS 不同于 HTTP 的端口，HTTP默认端口为80，HTTPS默认端口为443。

**推荐阅读：**

基于OpenSSL实现C/S架构中的HTTPS会话 [http://www.linuxidc.com/Linux/2013-05/84477.htm](http://www.linuxidc.com/Linux/2013-05/84477.htm)

RHEL6.3下配置简单Apache HTTPS  [http://www.linuxidc.com/Linux/2013-02/78874.htm](http://www.linuxidc.com/Linux/2013-02/78874.htm)

Nginx搭建HTTPS服务器 [http://www.linuxidc.com/Linux/2013-01/78263.htm](http://www.linuxidc.com/Linux/2013-01/78263.htm)

Linux实现HTTPS方式访问站点 [http://www.linuxidc.com/Linux/2012-08/69429.htm](http://www.linuxidc.com/Linux/2012-08/69429.htm)

**二、什么网站需要使用SSL证书**
1、购物交易类网站
不用多说，网上银行、支付宝、Paypal等肯定会全程加密以保护你的信息安全。

2、注册与登陆
一些大的网站，比如电子邮箱，注册会员或者登陆的时候，会专门通过SSL通道，保证密码安全不被窃取。

3、某些在线代理
这个。。。嗯哼，就不说了。

4、装B
比如我……

**三、自行颁发不受浏览器信任的SSL证书**
为晒晒IQ网颁发证书。ssh登陆到服务器上，终端输入以下命令，使用openssl生成RSA密钥及证书。

# 生成一个RSA密钥 
$ openssl genrsa -des3 -out 33iq.key 1024

# 拷贝一个不需要输入密码的密钥文件
$ openssl rsa -in 33iq.key -out 33iq_nopass.key

# 生成一个证书请求
$ openssl req -new -key 33iq.key -out 33iq.csr

# 自己签发证书
$ openssl x509 -req -days 365 -in 33iq.csr -signkey 33iq.key -out 33iq.crt

第3个命令是生成证书请求，会提示输入省份、城市、域名信息等，重要的是，email一定要是你的域名后缀的。这样就有一个 csr 文件了，提交给 ssl 提供商的时候就是这个 csr 文件。当然我这里并没有向证书提供商申请，而是在第4步自己签发了证书。

![](http://www.linuxidc.com/upload/2013_08/130803080155052.png)

编辑配置文件nginx.conf，给站点加上HTTPS协议
~~~
server {
    server_name YOUR_DOMAINNAME_HERE;
    listen 443;
    ssl on;
    ssl_certificate /usr/local/nginx/conf/33iq.crt;
    ssl_certificate_key /usr/local/nginx/conf/33iq_nopass.key;
    # 若ssl_certificate_key使用33iq.key，则每次启动Nginx服务器都要求输入key的密码。
}
~~~
重启Nginx后即可通过https访问网站了。

自行颁发的SSL证书能够实现加密传输功能，但浏览器并不信任，会出现以下提示：

![](http://www.linuxidc.com/upload/2013_08/130803080155051.png)

**四、受浏览器信任的证书**
要获取受浏览器信任的证书，则需要到证书提供商处申请。证书授证中心，又叫做CA机构，为每个使用公开密钥的用户发放一个数字证书。浏览器在默认情况下内置了一些CA机构的证书，使得这些机构颁发的证书受到信任。[VeriSign](http://www.verisign.com/cn/)即是一个著名的国外CA机构，工行、建行、招行、支付宝、财付通等网站均使用VeriSign的证书，而网易邮箱等非金融网站采用的是中国互联网信息中心 CNNIC颁发的SSL证书。一般来说，一个证书的价格不菲，以VeriSign的证书为例，价格在每年8000元人民币左右。

据说也有免费的证书可以申请。和VeriSign一样，[StartSSL](http://www.startssl.com/)也 是一家CA机构，它的根证书很久之前就被一些具有开源背景的浏览器支持（Firefox浏览器、谷歌Chrome浏览器、苹果Safari浏览器等）。后 来StartSSL竟然搞定了微软：在升级补丁中，微软更新了通过Windows根证书认证（Windows Root Certificate Program）的厂商清单，并首次将StartCom公司列入了该认证清单。现在，在Windows 7或安装了升级补丁的Windows Vista或Windows XP操作系统中，系统会完全信任由StartCom这类免费数字认证机构认证的数字证书，从而使StartSSL也得到了IE浏览器的支持。（来源及[申请步骤](http://www.linuxidc.com/Linux/2011-11/47478.htm)）

**五、只针对注册、登陆进行https加密处理**
既然HTTPS能保证安全，为什么全世界大部分网站都仍旧在使用HTTP呢？使用HTTPS协议，对服务器来说是很大的负载开销。从性能上考虑，我 们无法做到对于每个用户的每个访问请求都进行安全加密（当然，Google这种大神除外）。作为一个普通网站，我们所追求的只是在进行交易、密码登陆等操 作时的安全。通过配置Nginx服务器，可以使用rewrite来做到这一点。

在https server下加入如下配置：

~~~
if ($uri !~* "/logging.php$")
{
    rewrite ^/(.*)$ http://$host/$1 redirect;
}
~~~

在http server下加入如下配置：

~~~
if ($uri ~* "/logging.php$")
{
    rewrite ^/(.*)$ https://$host/$1 redirect;
}
~~~

这样一来，用户会且只会在访问logging.php的情况下，才会通过https访问。

更新：有一些开发框架会根据 $_SERVER['HTTPS'] 这个 PHP 变量是否为 on 来判断当前的访问请求是否是使用 https。为此我们需要在 Nginx 配置文件中添加一句来设置这个变量。遇到 https 链接重定向后会自动跳到 http 问题的同学可以参考一下。

~~~
server {
    ...
    listen 443;
    location \.php$ {
        ...
        include fastcgi_params;
        fastcgi_param HTTPS on; # 多加这一句
    }
}

server {
    ...
    listen 80;
    location \.php$ {
        ...
        include fastcgi_params;
    }
}
~~~

**参考链接：**

Nginx下只针对logging.php进行https处理的重写规则 [http://www.linuxidc.com/Linux/2013-08/88272.htm](http://www.linuxidc.com/Linux/2013-08/88272.htm)

全球可信并且唯一免费的HTTPS(SSL)证书颁发机构：StartSSL  [http://www.linuxidc.com/Linux/2011-11/47478.htm](http://www.linuxidc.com/Linux/2011-11/47478.htm)

**Nginx 的详细介绍**：[请点这里](http://www.linuxidc.com/Linux/2012-03/56786.htm "Nginx")
**Nginx 的下载地址**：[请点这里](http://www.linuxidc.com/down.aspx?id=342)