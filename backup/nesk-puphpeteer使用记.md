一次模拟登录并采集登录后cookie的记录

# 安装

```
composer require nesk/puphpeteer
npm install @nesk/puphpeteer
```
有的人会漏了第二个，然后报奇怪的错误

# 熟悉文档

## 值得注意的PuPHPeteer 和 Puppeteer 之间的不同

### Puppeteer's 的类必须实例化， 所有require 改为new
### 不需要使用 await 关键词
### 一些方法被别名了
* $ => querySelector
* $$ => querySelectorAll
* $x => querySelectorXPath
* $eval => querySelectorEval
* $$eval => querySelectorAllEval
### 执行的 函数必须通过JsFunction 创建

```
use Nesk\Rialto\Data\JsFunction;

$pageFunction = JsFunction::create(['element'], "
    return element.textContent;
");
```
### 已成必须通过->tryCatch 捕获

# 我的实践

```
    public function index()
    {
    	$url = 'http://cpservice.sipo.gov.cn/SecurityCode?timestamp='.time();
    	$ret = $this->ocr_code($url, 4, 1);
    }

    public function get_cookie(){
        // @unlink('verify.png');
        // @unlink('result.png');
        $puppeteer = new Puppeteer;
        $browser = $puppeteer->launch([
            'headless'=>false
        ]);
        try {
            $page = $browser->newPage();
            $page->goto('http://cpservice.sipo.gov.cn/index.jsp');
            $img = $page->querySelector("#Verify");
            $usernameInput = $page->querySelector("#username");
            $usernameInput->focus(); //定位到用户名
            $page->keyboard->type("XXXXXXXXXX");
            $passwordInput = $page->querySelector("#password");
            $passwordInput->focus();
            $page->keyboard->type("XXXXXXXXXX");
            $page->screenshot(['path' => 'verify.png',
                'clip'=>[
                    'x'=>445,'y'=>513, 'width'=>70,'height'=>30
                ]
            ]);
            $url = 'http://dp.cn/verify.png';
            $ocr_url = 'http://dp.cn/index/index/ocr_code';
            $debug_url = 'http://o2.cn/oxygen/user/front_log';
$js =  <<<JS
var xmlhttp;
var ret = '1111';
if (window.XMLHttpRequest){
    xmlhttp = new XMLHttpRequest();
}else{
  xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}
xmlhttp.open("POST","{$ocr_url}",false);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("url={$url}");
xmlhttp.onreadystatechange=function(){
    if (xmlhttp.readyState==4 && xmlhttp.status==200){
        ret = xmlhttp.responseText;
        return;
    }
}
if (xmlhttp.readyState==4 && xmlhttp.status==200){
    ret = xmlhttp.responseText;
}else{
    xmlhttp.open("GET","{$debug_url}?msg="+ JSON.stringify([xmlhttp.readyState, xmlhttp.status,xmlhttp.responseText, xmlhttp.responseXML]),true);
    xmlhttp.send();
}
return ret;
JS;
            $verifyFunction = JsFunction::create([], $js);
            $dimensions = $page->evaluate($verifyFunction);
            dump($dimensions);
            if($dimensions != '1111' && $dimensions != ''){
                $securityCodeInput = $page->querySelector("#securityCode");
                $securityCodeInput->focus();
                $page->keyboard->type($dimensions);
                $page->screenshot(['path' => 'result.png']);
                $loginFunction = JsFunction::create([], "
                    return login();
                ");
                $dimensions2 = $page->evaluate($loginFunction);
                $page->waitForNavigation(['timeout'=>5000]);
                $jumpFunction = JsFunction::create([], "
                    return document.cookie;
                ");
                $dimensions3 = $page->evaluate($jumpFunction);
                $page->screenshot(['path' => 'result2.png']);
                dump($dimensions3);
            }else{

            }
        } catch (Node\Exception $exception) {
            ptrace($e->getMessage().PHP_EOL.$e->getTraceAsString());
            print($e->getMessage().PHP_EOL.$e->getTraceAsString());
        }
        $browser->close();
    }

    public function ocr_code($url, $length = 4, $debug =0){
        if(false !== stripos($url, 'http')){
            $img = file_get_contents($url);
        }else{
            $img = base64_decode($url);
        }
        // TODO md5 缓存识别结果
        // halt($img);
        $tmp = tempnam(sys_get_temp_dir(), 'code');
        file_put_contents($tmp, $img);
        // ptrace($tmp);
        // return $tmp;
		$ret = plugin_action('BaiduAi', 'Ocr', 'basicAccurate', [$img]);
        ptrace($ret);
        $words = $ret['words_result']['0']['words'];
        $words = trim($words, ' ');
        $words = str_ireplace(['.',' ', '\''], '', $words);
		if($debug){
	        echo '<img src="'.base64EncodeImage($tmp).'">';
			// dump($ret);
			// dump($words);
		}
		return strlen($words) == $length? $words: '';
    }
```

百度ai 用的海豚里我封装的插件 不是100%成功率，如果要高成功率 可以尝试自己tensflow训练，因为网站固定字体生成的验证码

# 注意点：
- js里ajax用原生的，我之前node的puphpeteer 就是es7里异步 await 什么的找了一个http node模块写了个请求，结果请求成功参数永远返回不出来。

- 二维码是用的时候先截图固定区域，这个默认窗体大小800X600。没找到device类。
- 调试一种将js函数dump出来，print 不默认换行，开始我打印verify 码和cookie 连一块，仔细看才找出来真正的cookie。
- 不同位置截图。
- headless:false 失效了！！
- 请求跨域问题
- 最好框架对异常进行封装。之前ajax 报500 显示的内容 调试了一下，看不懂啊
- 前端也可以写一个js接口来报前端错误和手动报错。

哎，js不熟只能用php来凑了。希望能给大家一个模拟登录的思路。


