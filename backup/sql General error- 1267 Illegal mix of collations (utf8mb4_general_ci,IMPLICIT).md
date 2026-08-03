今天客户的微信注册遇到昵称问题

![image](https://user-images.githubusercontent.com/1614114/41708734-fe46bda2-7573-11e8-8de6-65acadb6fb9c.png)

开始找了个修改表结构的sql 改了几个特殊字段， 结果还是报错

索性tp写了个循环后 将所有表的字符全改utf8mb4了

 ```
   public function modify_table_charset(){
    	$tables = Db::query('show tables');
    	$sql = '';
    	foreach ($tables as $t) {
    		$sql .= PHP_EOL.<<<SQL
ALTER TABLE {$t['Tables_in_novel']} CONVERT TO CHARACTER SET utf8mb4 collate utf8mb4_general_ci;

SQL;

    	}
		echo $sql;
    }
```

还有改数据库默认编码