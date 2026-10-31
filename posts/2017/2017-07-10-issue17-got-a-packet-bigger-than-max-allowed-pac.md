---
title: "数据导入报错：Got a packet bigger than‘max_allowed_packet’bytes的问题"
date: 2017-07-10
tags: ["blog", "software", "mysql"]
summary: "2个解决方法："
---

2个解决方法：

1.临时修改：`mysql>set global max_allowed_packet=524288000;修改 #512M`

2.修改my.cnf，需重启mysql。

在 [MySQLd] 部分添加一句（如果存在，调整其值就可以）： `max_allowed_packet=10M`
