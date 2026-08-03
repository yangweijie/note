介绍
本章主要介绍怎样对比数据库的表结构的差异，这里主要介绍使用mysqldiff工具来对比表结构的差异，其实在5.6版本之后通过查询information库中的系统表也能对比出来，但是mysqldiff还有一个好处就是可以直接生产差异的SQL语句这个功能就是我们需要利用的，而通过分析系统表要实现这个就比较难；接下来就来看看怎样使用这个工具。


语法

`mysqldiff --server1=user:pass@host:port:socket --server2=user:pass@host:port:socket db1.object1:db2.object1 db3:db4`
这个语法有两个用法：

db1：db2:如果只是指定数据库，那么就将两个数据库中互相缺少的对象显示出来，而对象里面的差异不进行对比；这里的对象包括表、存储过程、函数、触发器等。

db1.object1:db2.object1：如果指定了具体表对象，那么就会详细对比两个表的差异，包括表名、字段名、备注、索引、大小写等都有的表相关的对象。

接下来看一些主要的参数：

~~~
--server1：配置server1的连接

--server2：配置server2的连接

--character-set：配置连接时用的字符集，如果不显示配置默认使用“character_set_client”

--width：配置显示的宽度

--skip-table-options：这个选项的意思是保持表的选项不变，即对比的差异里面不包括表名、AUTO_INCREMENT,ENGINE, CHARSET等差异。

-d DIFFTYPE, --difftype：差异的信息显示的方式，有[unified|context|differ|sql](default: unified),如果使用sql那么就直接生成差异的SQL这样非常方便。

--changes-for=：例如--changes-for=server2,那么对比以sever1为主，生成的差异的修改也是针对server2的对象的修改。

--show-reverse：这个字面意思是显示相反的意思，其实是生成的差异修改里面同时会包含server2和server1的修改。
~~~

测试

~~~
use study;

create table test1
(id int not null primary key,
a varchar(10) not null,
b varchar(10),
c varchar(10) comment 'c',
d int

)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='test1';


create table test2
(id int not null ,
a varchar(10),
b varchar(5),
c varchar(10),
D int
)
ENGINE=myisam DEFAULT CHARSET=utf8 COMMENT='test2';
~~~

1.不使用--skip-table-options

`mysqldiff  --server1=root:root@localhost --server2=root:root@localhost --changes-for=server2   --show-reverse   --difftype=sql study.test1:study.test2`
![](https://box.kancloud.cn/5d8a2e8331cd74dee22384895dc81cca_1610x643.png)

2.使用--skip-table-options
![](https://box.kancloud.cn/580b5c676dee70e986f187ec298d6598_1786x595.png)

其实用SQL语句也可以达到查询的效果，这里就贴上平时用的对比语句。

~~~

###############################################################################################################################
##判断两个数据库相同表的字段不为空是否相同
select a.TABLE_SCHEMA,a.TABLE_NAME,a.COLUMN_NAME,a.COLUMN_TYPE,a.IS_NULLABLE,a.COLUMN_DEFAULT,b.TABLE_SCHEMA,b.TABLE_NAME,b.COLUMN_NAME,b.COLUMN_TYPE,b.IS_NULLABLE ,b.COLUMN_DEFAULT,b.COLUMN_COMMENT 
from information_schema.`COLUMNS` a inner join information_schema.`COLUMNS` b 
on a.TABLE_SCHEMA='db1' and b.TABLE_SCHEMA='db2'and a.TABLE_NAME=b.TABLE_NAME and a.COLUMN_NAME=b.COLUMN_NAME and a.IS_NULLABLE<>b.IS_NULLABLE
where a.IS_NULLABLE='NO';
################################################################################################################################
##判断两个数据库相同表的字段默认值是否相同
select a.TABLE_SCHEMA,a.TABLE_NAME,a.COLUMN_NAME,a.COLUMN_DEFAULT,b.TABLE_SCHEMA,b.TABLE_NAME,b.COLUMN_NAME,b.COLUMN_DEFAULT from information_schema.`COLUMNS` a 
inner join information_schema.`COLUMNS` b on a.TABLE_SCHEMA='db1' and b.TABLE_SCHEMA='db2'
and a.TABLE_NAME=b.TABLE_NAME and a.COLUMN_NAME=b.COLUMN_NAME and a.COLUMN_DEFAULT<>b.COLUMN_DEFAULT;

#################################################################################################################################
##判断两个数据库相同表的字段数据类型是否相同,这里是判断数据类型不同如果要判断数据类型的长度不同需要用COLUMN_TYPE字段
select a.TABLE_SCHEMA,a.TABLE_NAME,a.COLUMN_NAME,a.DATA_TYPE,a.COLUMN_DEFAULT,b.TABLE_SCHEMA,b.TABLE_NAME,b.COLUMN_NAME,b.DATA_TYPE ,b.COLUMN_DEFAULT
from information_schema.`COLUMNS` a inner join information_schema.`COLUMNS` b on a.TABLE_SCHEMA='db1' and b.TABLE_SCHEMA='db2'
and a.TABLE_NAME=b.TABLE_NAME and a.COLUMN_NAME=b.COLUMN_NAME and a.DATA_TYPE<>b.DATA_TYPE;

##################################################################################################################################
##判断两个数据库相同表的中互相不存在的字段
select a.TABLE_SCHEMA,a.TABLE_NAME,a.COLUMN_NAME,a.DATA_TYPE,a.COLUMN_DEFAULT
from information_schema.`COLUMNS` a 
where a.TABLE_SCHEMA='db1' and a.COLUMN_NAME NOT IN(SELECT b.COLUMN_NAME from information_schema.`COLUMNS` b where b.TABLE_SCHEMA='db2' and a.TABLE_SCHEMA='db1'
and a.TABLE_NAME=b.TABLE_NAME );

select a.TABLE_SCHEMA,a.TABLE_NAME,a.COLUMN_NAME,a.DATA_TYPE,a.COLUMN_DEFAULT
from information_schema.`COLUMNS` a 
where a.TABLE_SCHEMA='db2' and a.COLUMN_NAME NOT IN(SELECT b.COLUMN_NAME from information_schema.`COLUMNS` b where b.TABLE_SCHEMA='db1' and a.TABLE_SCHEMA='db2'
and a.TABLE_NAME=b.TABLE_NAME );

####mysql没有full jion所以变相的多做了一次select查询，这种方法性能比较差,对于表比较多的数据库建议使用上面的分开查询
select b.TABLE_SCHEMA,b.TABLE_NAME,b.COLUMN_NAME,b.DATA_TYPE,c.TABLE_SCHEMA,c.TABLE_NAME,c.COLUMN_NAME,c.DATA_TYPE from 
(select TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE from information_schema.`COLUMNS` a where a.TABLE_SCHEMA in('db2','db1') )a left join
(select TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE from information_schema.`COLUMNS` a where a.TABLE_SCHEMA in('db2')) b  on a.TABLE_NAME=b.TABLE_NAME AND a.COLUMN_NAME=b.COLUMN_NAME left join 
(select TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE from information_schema.`COLUMNS` a where a.TABLE_SCHEMA in('db1')) c on a.TABLE_NAME=c.TABLE_NAME AND a.COLUMN_NAME=c.COLUMN_NAME
where b.COLUMN_NAME is null or c.COLUMN_NAME is null ;

#######################################################################################################################
##判断两个数据库互相不存在的表
select a.TABLE_SCHEMA,a.TABLE_NAME
from information_schema.TABLES a 
where a.TABLE_SCHEMA='db1' and a.TABLE_NAME NOT IN(SELECT b.TABLE_NAME from information_schema.TABLES b where b.TABLE_SCHEMA='db2');

select a.TABLE_SCHEMA,a.TABLE_NAME
from information_schema.TABLES a 
where a.TABLE_SCHEMA='db2' and a.TABLE_NAME NOT IN(SELECT b.TABLE_NAME from information_schema.TABLES b where b.TABLE_SCHEMA='db1');


select b.TABLE_SCHEMA,b.TABLE_NAME,c.TABLE_SCHEMA,c.TABLE_NAME from 
(select TABLE_SCHEMA,TABLE_NAME from information_schema.TABLES a where a.TABLE_SCHEMA in('db2','db1') )a left join
(select TABLE_SCHEMA,TABLE_NAME from information_schema.TABLES a where a.TABLE_SCHEMA in('db2')) b  on a.TABLE_NAME=b.TABLE_NAME left join 
(select TABLE_SCHEMA,TABLE_NAME from information_schema.TABLES a where a.TABLE_SCHEMA in('db1')) c on a.TABLE_NAME=c.TABLE_NAME 
where b.TABLE_NAME is null or c.TABLE_NAME is null ;
~~~

 

总结
 这里没有演示对数据库的对比，数据库的对比显示的只是缺少的数据库对象，理解起来更加容易。

 

备注：

    作者：pursuer.chen

    博客：http://www.cnblogs.com/chenmh

本站点所有随笔都是原创，欢迎大家转载；但转载时必须注明文章来源，且在文章开头明显处给明链接。

《欢迎交流讨论》