```php
/**date 2015-04-11
     * author http://www.lai18.com
     **/
    echo date("Ymd",strtotime("now")), "\n";
    echo date("Ymd",strtotime("-1 week Monday")), "\n";
    echo date("Ymd",strtotime("-1 week Sunday")), "\n";
    echo date("Ymd",strtotime("+0 week Monday")), "\n";
    echo date("Ymd",strtotime("+0 week Sunday")), "\n";

    echo "*********第几个月:";
    echo date('n');
    echo "*********本周周几:";
    echo date("w");
    echo "*********本月天数:";
    echo date("t");
    echo "*********";

    echo '<br>上周起始时间:<br>';
    echo date("Y-m-d H:i:s",mktime(0, 0 , 0,date("m"),date("d")-date("w")+1-7,date("Y"))),"\n";
    echo date("Y-m-d H:i:s",mktime(23,59,59,date("m"),date("d")-date("w")+7-7,date("Y"))),"\n";
    echo '<br>本周起始时间:<br>';
    echo date("Y-m-d H:i:s",mktime(0, 0 , 0,date("m"),date("d")-date("w")+1,date("Y"))),"\n";
    echo date("Y-m-d H:i:s",mktime(23,59,59,date("m"),date("d")-date("w")+7,date("Y"))),"\n";

    echo '<br>上月起始时间:<br>';
    echo date("Y-m-d H:i:s",mktime(0, 0 , 0,date("m")-1,1,date("Y"))),"\n";
    echo date("Y-m-d H:i:s",mktime(23,59,59,date("m") ,0,date("Y"))),"\n";
    echo '<br>本月起始时间:<br>';
    echo date("Y-m-d H:i:s",mktime(0, 0 , 0,date("m"),1,date("Y"))),"\n";
    echo date("Y-m-d H:i:s",mktime(23,59,59,date("m"),date("t"),date("Y"))),"\n";

    $season = ceil((date('n'))/3);//当月是第几季度
    echo '<br>本季度起始时间:<br>';
    echo date('Y-m-d H:i:s', mktime(0, 0, 0,$season*3-3+1,1,date('Y'))),"\n";
    echo date('Y-m-d H:i:s', mktime(23,59,59,$season*3,date('t',mktime(0, 0 , 0,$season*3,1,date("Y"))),date('Y'))),"\n";

    $season = ceil((date('n'))/3)-1;//上季度是第几季度
    echo '<br>上季度起始时间:<br>';
    echo date('Y-m-d H:i:s', mktime(0, 0, 0,$season*3-3+1,1,date('Y'))),"\n";
    echo date('Y-m-d H:i:s', mktime(23,59,59,$season*3,date('t',mktime(0, 0 , 0,$season*3,1,date("Y"))),date('Y'))),"\n";
```