~~~ php
        $model = M();
        $rules = [
            ['a', '1,2', '不支持的商户经营类型',0, 'in'],
        ];
        $ret = $model->validate($rules)->create(['a'=>2]);
        dump($ret);
        die;
~~~

字段、范围值，提示，验证时间，in