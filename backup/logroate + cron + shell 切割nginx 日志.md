# logrotate 配置 在 `/etc/logrotate.d` 中 定义 nginx
~~~ conf
/home/wwwlogs/*log {
    daily
    rotate 7
    missingok
    notifempty
    compress
    dateext
    sharedscripts
    create 640 www www
    postrotate
    /usr/sbin/service nginx reload
    endscript
}
~~~

在 /opt/中新建 logrotate-nginx.sh
~~~ shell
#!/bin/bash
#创建转储日志压缩存放目录
mkdir -p /home/wwwlogs/days
#手工对nginx日志进行切割转换
/usr/sbin/logrotate -vf /etc/logrotate.d/nginx
#当前时间
time=$(date -d "yesterday" +"%Y-%m-%d")
#进入转储日志存放目录
cd /home/wwwlogs/days
#对目录中的转储日志文件的文件名进行统一转换
for i in $(ls ./ | grep "^\(.*\)\.[[:digit:]]$")
do
mv ${i} ./$(echo ${i}|sed -n 's/^\(.*\)\.\([[:digit:]]\)$/\1/p')-$(echo $time)
done
#对转储的日志文件进行压缩存放，并删除原有转储的日志文件，只保存压缩后的日志文件。以节约存储空间
for i in $(ls ./ | grep "^\(.*\)\-\([[:digit:]-]\+\)$")
do
tar jcvf ${i}.bz2 ./${i}
rm -rf ./${i}
done
#只保留最近7天的压缩转储日志文件
find /home/wwwlogs/days* -name "*.bz2" -mtime 7 -type f -exec rm -rf {} \;
~~~

`crontab -e`
添加 一行定时任务
~~~
0 0 * * * /bin/bash -x /opt/logrotate-nginx.sh > /dev/null 2>
~~~
chmod 0777 /opt/logrotate-nginx.sh

测试 /opt/logrotate-nginx.sh