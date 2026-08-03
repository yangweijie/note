<?php    

        exec("java -version",$out,$status);

        var_dump($out);

        echo $status;

?>

执行结果是$out是空数组，$status为0，不知道为什么，java命令（已加入环境变量）在cmd命令行下是可以执行的，而且exec('dir')也是可以成功执行的，不知道java命令为什么会有问题


解决了，后来直接在命令行执行脚本发现java -version竟然是标准错误输出，所以如果要得到输出的话，只要java -version 2>&1就可以了，亲测可用