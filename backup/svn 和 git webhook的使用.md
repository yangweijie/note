最近由于想提高代码提交的效率不再git commit && git push 和 svn commit 后每次要去服务器更新代码。
就参考了 [分享下使用svn或者git时，测试服务器代码自动更新、线上服务器代码手动更新的配置经验](http://get.ftqq.com/9079.get) 孟康的文章。没有配置服务器上的文件

svn 用的svn bucket 免费的自带钩子

![tim 20181008162318](https://user-images.githubusercontent.com/1614114/46598408-92f44080-cb16-11e8-9fad-663b4b79a63b.png)

这个工具比较好的是有钩子请求历史记录。

然后写了项目里的控制器代码：

```
<?php
namespace app\dev\home;

use think\Controller;

/**
 * Svn钩子
 * @package app\install\controller
 */
class Svn extends Controller
{

    protected function _initialize()
    {
        define('SVN_TOKEN', 'guihzip');
        header("Cache-Control:no-cache,must-revalidate");
    }

    public function commit()
    {
        header("Cache-Control:no-cache,must-revalidate");
        extract($_POST);
        if ($token == SVN_TOKEN) {
            switch ($event) {
                case 'test':
                    return 'ok';
                    break;
                case 'start-commit':
                    return 'ok';
                    break;
                default:
                    // ptrace($log);

                    if(stripos($log, '@commit') !== false){
                        $username   = 'XXXXX';
                        $password   = 'XXXXX';
                        $target_dir = realpath('..');
                        // ptrace($target_dir);
                        ini_set('disable_functions', '');
                        exec("sudo svn up --username {$username} --password {$password} --no-auth-cache {$target_dir} 2>&1", $output, $outresult);
                        ptrace(implode(PHP_EOL, $output).PHP_EOL.$outresult);
                        if ($outresult === 0) {
                            // echo '更新成功！';
                            //echo print_r($output);
                            return 'ok';
                        } else {
                            // echo '更新失败！';
                            // echo print_r($output);
                            return 'failed';
                        }
                    }else{
                        return 'no up';
                    }
                    break;
            }
        } else {
            return 'error token';
        }
    }
}

```
钩子运行时会报各种没权限，因为我的项目是root clone 出来的。于是查找各种办法，

[php利用root权限执行shell脚本(二) ](http://get.ftqq.com/9081.get)

加入了www 用户组后 执行的svn 命令前面一定要带sudo  就可以了。

接下来是git 用的oschina 后来换名为了 gitee 。

在项目里 新增钩子，咱们只管push的钩子

![image](https://user-images.githubusercontent.com/1614114/46598631-5aa13200-cb17-11e8-8136-946736833181.png)

对应的代码：

```
<?php
namespace app\dev\home;

use think\Controller;

/**
 * Git钩子
 * @package app\install\controller
 */
class Git extends Controller
{

    protected function _initialize()
    {
        define('GIT_TOKEN', 'guihzip');
        header("Cache-Control:no-cache,must-revalidate");
    }

    public function push()
    {
        header("Cache-Control:no-cache,must-revalidate");
        // ptrace($_POST);
        $rws_post = file_get_contents('php://input');
        $_POST = json_decode($rws_post, 1);

        // ptrace($_POST);
        extract($_POST);
        $header = $this->request->header();
        // ptrace($header);
        $token = $header['x-gitee-token'];
        $event = $header['x-gitee-event'];
        if ($token == GIT_TOKEN) {
            switch ($event) {
                case 'test':
                    return 'ok';
                    break;
                case 'start-commit':
                    return 'ok';
                    break;
                default:
                    // ptrace($log);
                	$log = $head_commit['message'];
                    if(stripos($log, '@push') !== false){
                        error_reporting ( E_ALL );
			$dir = realpath('..');//该目录为git检出目录
			exec("sudo cd {$dir} && git pull origin master 2>&1", $output, $outresult);
                        ptrace(implode(PHP_EOL, $output).PHP_EOL.$outresult);
                        if ($outresult === 0) {
                            // echo '更新成功！';
                            //echo print_r($output);
                            return 'ok';
                        } else {
                            // echo '更新失败！';
                            // echo print_r($output);
                            return 'failed';
                        }
                    }else{
                        return 'no up';
                    }
                    break;
            }
        } else {
            return 'error token';
        }
    }
}
```

## git 遇到的问题：
1） 没有账号密码
2）git pull 说没有指定分支

第一个问题 通过 设置remote url 为带名称 密码的 地址就行 [https://www.jianshu.com/p/8020de245f6a](https://www.jianshu.com/p/8020de245f6a)
 
第二个问题 通过 [git branch --set-upstream 本地关联远程分支](http://get.ftqq.com/9083.get)


> 孟康文章里的 output 不是一个字符串要自行转换。 
> gitee 里的post不是传统post 7.2 里 全局变量  
$rws_post = $GLOBALS['HTTP_RAW_POST_DATA'];
$mypost = json_decode($rws_post,1);
方式 已经获取不到了  必须 file_get_contents('php://input'); 获取  
> x-gitee-token 在 gitee 的文章里 其实是大写的， 可能我的nginx环境不同，所以大家要自己调试一下获取header 看看。
> ptrace 是自己封装的 钉钉告警函数，大家可以换成发邮件。



