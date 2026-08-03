情是这样的,项目里发现一个奇怪的现象,json_encode一个带浮点价格的数据, 出现溢出, 比如:
~~~
<?php
echo json_encode(277.2);
// 输出结果为: 277.199999999999989
~~~
这明显是不能接受的, 数据虽然很接近, 但毕竟已经变更了
下意识地认为这是php的一个bug, 不能准确地json序列化一个浮点小数
这个问题google了半天竟然也无果, 然后我跟同事说, 你们json_encode数据里有小数的时候, 记得先number_format()转化成字符串.

自己又写了个fix方法, 遍历数据, 把is_float()的数据都用number_format()转化了
~~~
function json_encode_pre($d, $depth=128, $level=0){
    if($level>$depth) return $d;
    if(is_array($d)){
        foreach ($d as $i => $v) { $d[$i] = json_encode_pre($v, $depth, $level+1); }
        return $d;
    }
    if(is_float($d)){
        # 测试发现number_format有效数字低于18(保守取16)时,不会溢出
        $p = 16 - strlen(intval($d));
        $f = number_format($d, $p);
        if($p>1){ $f = preg_replace('/0+$/','', $d); }
        return $d;
    }
    return $d;
}
~~~
echo number_format(277.2, 14); // 当18位有效数字处理(277.2已有4位有效数字)
// 277.199999999999989
echo number_format(277.2, 12); // 当16位
// 277.2000000000000
echo json_encode(json_encode_pre(277.2));
// "277.2"
看到这结果时, 便猜测是有效数字位数的问题导致了溢出, PHP怎么会有这么蠢的设计呢?这是我当时的想法.

然后想着是不是能从源码下手, 于是查了下php源码, 发现这段代码:
~~~
static inline void php_json_encode_double(smart_str *buf, double d, int options) /* {{{ */
{
    size_t len;
    char num[PHP_DOUBLE_MAX_LENGTH];

    php_gcvt(d, (int)PG(serialize_precision), '.', 'e', num);
    len = strlen(num);
    if (options & PHP_JSON_PRESERVE_ZERO_FRACTION && strchr(num, '.') == NULL && len < PHP_DOUBLE_MAX_LENGTH - 2) {
        num[len++] = '.';
        num[len++] = '0';
        num[len] = '\0';
    }
    smart_str_appendl(buf, num, len);
}
~~~
是的, 竟然发现了配置项serialize_precision, 这个配置我当初的理解是serialize()方法用的, 而我当初尝试修改过配置项precision, 然并卵, 原来json_encode会用到serialize_precision, 于是修改php.ini, 把它设为16, 原来是17还是18忘了.

<?php
echo json_encode(277.2);
// 输出结果为: 277.2
如果你想重现我的问题, 很简单, 把serialize_precision设为20或更大, 至于这个有效数字最大值是多少才不会溢出, 我还不知道跟什么有关系, 希望能有大神指点了.
我是通过改配置数值, 出现溢出的值再减去2来用的.

附上配置项说明, 从官方说明上看, 很难想像是跟json_encode是有关系的.

; php.ini

; When floats & doubles are serialized store serialize_precision significant
; digits after the floating point. The default value ensures that when floats
; are decoded with unserialize, the data will remain the same.
serialize_precision = 16

; The number of significant digits displayed in floating point numbers.
; http://php.net/precision
precision = 16
另外源码里有个json_encode的选项JSON_PRESERVE_ZERO_FRACTION, 这个的意思是如果是个是个整数, 是否保留小数点和0, 来看测试结果:
~~~
<?php
echo json_encode(277.0);
// 277
echo json_encode(277.0, JSON_PRESERVE_ZERO_FRACTION);
// 277.0
~~~