每个服务器上都安装yar扩展

然后要被访问的服务器上写一段代码，开启rpc 服务器
index控制器index方法里：
~~~
  if($_SERVER['PHP_SELF'] == '/nmp_remote.php'){
            $this->yar();
            return '';
        }
        
public function yar(){
        $server = new \Yar_Server(new YarApi);
        return $server->handle();
}
~~~

~~~
namespace app\index\controller;
Class YarApi{

	/**
	 * 调用内部函数
	 * @param  string $name   函数名
	 * @param  array  $params 参数 没有传[]
	 * @return mixed         返回结果
	 */
	public function function_call($name, $params=[]){
		if(function_exists($name)){
			return call_user_func_array($name, $params);
		}else{
			return 'function not exists';
		}
	}

	/**
	 * 调用类方法
	 * @param  string $className 类命名空间
	 * @param  string $method    方法名
	 * @param  array  $params    参数 没有传[]
	 * @return mixed            返回结果
	 */
	public function class_call($className, $method, $params=[]){
		if(method_exists($className, $method)){
			return call_user_func_array([$className, $method], $params);
		}else{
			return 'method not exists';
		}
	}

	/**
	 * 实列话类
	 * @param  string $className 类命名空间
	 * @param  array  $params    参数
	 * @return mixed            返回结果
	 */
	public function instance_class($className, $params=[]){
        if(class_exists($className, false)){
            $class = new \ReflectionClass($className);
            $ret = $class->newInstanceArgs($params);
            return $ret;
        }else{
            return 'class not exists';
        }
    }

    public function constant($name){
    	if(defined($name)){
    		return constant($name);
    	}else{
    		return 'constant no defined';
    	}
    }

}

~~~
暴露的是 server里传入的类 的方法

这两个方法其实用于调用函数和类方法 、 类方法支持静态。
然后 其他模块里访问：

~~~
$client = new \yar_client("http://nmp.cn/nmp_remote.php");

$ret = $client->function_call('build_part_commission_table', [['user_id'=>1, 'finish_time'=>'2017-10-28 10:00:00']]);
$data = [];
$ret2 = $client->class_call('\aa', 'sel', ['a']);
}
~~~

![image](https://user-images.githubusercontent.com/1614114/39366390-61adb604-4a66-11e8-97a3-3f34fe3a5eb0.png)
暴露的是 server里传入的类 的方法

这两个方法其实用于调用函数和类方法 、 类方法支持静态。
然后 其他模块里访问：

~~~
$client = new \yar_client("http://nmp.cn/nmp_remote.php");

$ret = $client->function_call('build_part_commission_table', [['user_id'=>1, 'finish_time'=>'2017-10-28 10:00:00']]);
$data = [];
$ret2 = $client->class_call('\aa', 'sel', ['a']);

~~~

