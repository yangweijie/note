---
title: "phpcustom_mysql.ini"
date: 2020-05-28
tags: []
summary: "client"
---

```
[client]
port = 3304

[mysql]
no-auto-rehash
default-character-set = utf8

[mysqld]
port = 3304
server_id = 1
character-set-server = utf8

explicit_defaults_for_timestamp = on
skip-ssl

table_open_cache = 256


#标记为Error，Warning和Note将写入到事件日志
log-error="D:/PHPCUSTOM_Pack/PHPCUSTOM_lib/mariadb-10.4.11/logs/mysql.log"


max_connections=500
query_cache_size=91M
tmp_table_size=54M
thread_cache_size=23
key_buffer_size=15M
innodb_flush_log_at_trx_commit=1
innodb_log_buffer_size=6M
innodb_buffer_pool_size=522M
innodb_log_file_size=105M
innodb_thread_concurrency=26


[mysqldump]
quick
max_allowed_packet = 512M

```
