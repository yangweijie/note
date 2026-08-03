两种

1. 文件名转gbk
``` php
        $text = '2024年4月15日商品导出';
        $filename = mb_convert_encoding($text, "GBK",  "UTF-8").'.txt';   // a filename in Chinese characters
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: filename='.$filename);
        readfile(realpath('../think'));
        exit();
```
2. urlencode 

  ``` php
        $filename = '2024年4月5日中文文件名.txt';   // a filename in Chinese characters
        $contentDispositionField = 'Content-Disposition: attachment; '
            . sprintf('filename="%s"; ', rawurlencode($filename))
            . sprintf("filename*=utf-8''%s", rawurlencode($filename));
        header('Content-Type: application/octet-stream');
        header($contentDispositionField);
        readfile(realpath('../think'));
        exit();
```