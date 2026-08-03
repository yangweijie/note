1.float类型
float列类型默认长度查不到结果，必须指定精度，比如 
num float, insert into table (num) values (0.12); select * from table where num=0.12的话，empty set。
num float(9,7), insert into table (num) values (0.12); select * from table where num=0.12的话会查到这条记录。

mysql> create table tt
    -> (
    -> num float(9,3)
    -> );
Query OK, 0 rows affected (0.03 sec)

mysql> insert into tt(num)values(1234567.8);
Query OK, 1 row affected, 1 warning (0.04 sec)
注：超出字段范围，插入数据有误

mysql> select * from tt;
+-------------+
| num         |
+-------------+
| 1000000.000 |
+-------------+
2 rows in set (0.00 sec)

***************************************************************************

注：通常在 linux 下安装完 mysql 后，默认的 sql-mode 值是空，在这种情形下 mysql 执行的是一种不严格的检查，例如日期字段可以插入 ’ 0000-00-00 00:00:00 ’这样的值，还有如果要插入的字段长度超过列定义的长度，那么 mysql 不会终止操作，而是会自动截断后面的字符继续插入操作。

我们发现插入的字符被自动截断了，但是如果我们本意希望如果长度超过限制就报错，那么我们可以设置 sql_mode 为 STRICT_TRANS_TABLES ，如下：
mysql> set session sql_mode='STRICT_TRANS_TABLES';
这样我们再执行同样的操作，mysql 就会告诉我们插入的值太长，操作被终止，如下：

mysql> insert into tt(num) values(1234567.8);
ERROR 1264 (22003): Out of range value for column 'num' at row 1

***************************************************************************

mysql> insert into tt(num)values(123456.8);
Query OK, 1 row affected (0.00 sec)

mysql> select * from tt;
+-------------+
| num         |
+-------------+
| 1000000.000 |
|  123456.797 |
+-------------+
2 rows in set (0.00 sec)
注：小数位数不够，自动补齐，但是存在一个问题就是如上的近似值。

mysql> insert into tt(num)values(123456.867);
Query OK, 1 row affected (0.04 sec)

mysql> select * from tt;
+-------------+
| num         |
+-------------+
| 1000000.000 |
|  123456.797 |
|  123456.867 |
+-------------+
3 rows in set (0.00 sec)

mysql> select * from tt where num=123456.867;
+------------+
| num        |
+------------+
| 123456.867 |
+------------+
1 row in set (0.00 sec)

mysql> insert into tt(num)values(2.8);
Query OK, 1 row affected (0.04 sec)

mysql> select * from tt;
+-------------+
| num         |
+-------------+
| 1000000.000 |
|  123456.797 |
|  123456.867 |
|       2.800 |
+-------------+
4 rows in set (0.00 sec)

mysql> select * from tt where num=2.8;
+-------+
| num   |
+-------+
| 2.800 |
+-------+
1 row in set (0.00 sec)

mysql> insert into tt(num)values(2.888888);
Query OK, 1 row affected (0.00 sec)

mysql> select * from tt;
+-------------+
| num         |
+-------------+
| 1000000.000 |
|  123456.797 |
|  123456.867 |
|       2.800 |
|       2.889 |
+-------------+
5 rows in set (0.00 sec)
注：小数位数超了，自动取近似值。

--------------------------------------------------------------------------------------

2.double类型

mysql> create table tt(
    -> num double(9,3)
    -> );
Query OK, 0 rows affected (0.04 sec)

mysql> insert into tt(num) values(234563.9);
Query OK, 1 row affected (0.00 sec)

mysql> select * from tt;
+------------+
| num        |
+------------+
| 234563.900 |
+------------+
1 row in set (0.00 sec)

mysql> insert into tt(num) values(2345623.2);
Query OK, 1 row affected, 1 warning (0.04 sec)
mysql> insert into tt(num) values(234563.2);
Query OK, 1 row affected (0.00 sec)

mysql> select * from tt;
+------------+
| num        |
+------------+
| 234563.900 |
| 999999.999 |
| 234563.200 |
+------------+
2 rows in set (0.00 sec)

mysql> insert into tt(num) values(2.8);
Query OK, 1 row affected (0.00 sec)

mysql> select * from tt;
+------------+
| num        |
+------------+
| 234563.900 |
| 999999.999 |
| 234563.200 |
|      2.800 |
+------------+
3 rows in set (0.00 sec)

FLOAT(M,D)或REAL(M,D)或DOUBLE PRECISION(M,D)。这里，“(M,D)”表示该值一共显示M位整数，其中D位位于小数点后面。
例如，定义为FLOAT(7,4)的一个列可以显示为-999.9999。MySQL保存值时进行四舍五入，因此如果在FLOAT(7,4)列内插入999.00009，近似结果是999.0001。

单精度浮点数(float)的尾数是用24bit表示的，双精度(double)浮点数的尾数是用53bit表示的，转换成十进制：
2^24 - 1 = 16777215           
2^53 - 1 = 9007199254740991     
由上可见，IEEE754单精度浮点数的有效数字二进制是24位，按十进制来说，是8位；双精度浮点数的有效数字二进制是53位，按十进制来说，是16 位。

## tp5 精度问题
在tp5里 0.9+ -0.9 = 0.00 数据库double 的 数据库查询出来 0.00 结果php dump出来是溢出的。

~~~
'params'          => [
        PDO::ATTR_EMULATE_PREPARES=>true,
    ],
~~~