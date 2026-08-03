tp5 最新版 数据集查询后 调用内置分页后 想修改分页过的数据 补充额外字段 可以用collection 的 offsetSet 方法

~~~php
$productCategory = Db::name('ProductCategory')->alias('a')->field("a.id,a.category_name,a.discount,a.order_index,count(b.id) as product_num")
          ->join('kwy_product b', 'b.product_category_id =a.id', 'left')->where($where)->group("a.id")->order("a.order_index asc")->paginate(10);

        foreach($productCategory->all() as $key =>$val ){
            $productCategory->offsetSet($key, array_merge($val, ['sex'=>1]));
        }
~~~

完成获取器的操作 以后可能支持分页类对象的each 方法修改数据