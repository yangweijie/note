# 速查表 新版升级

## 历史回顾

我感叹于laravel的生态完好，tp5的类api的缺失（以前thinkphp3时代，帮助公司用apigen NetBeans里生成过一个[3.1版本的api](http://www.thinkphp.cn/api/)）。

![](https://box.kancloud.cn/362d9e9b3a4adf2d87d00ef3b88e344a_1634x753.png)

在我走之后，估计没人用NetBeans了 所以就没人做升级。


然后我觉得laravel的速查表不错，见下图：

![](https://box.kancloud.cn/08ce1b130d60e7dd91cb2a2a84a106bf_1880x942.png)

于是就想到了把他移植到tp5上，作为自己回到thinkphp5开发上的第一个贡献。

记得那个时候是清明前开始动手的。使用最土的，静态页面，一个个类手动去编辑。

后来发现类太多了，我每次在sublime 里 先打开一个类，复制出来临时文件，处理好，粘贴到静态index.html里，太麻烦了，要处理左侧的导航，又要定位插入的位置。 于是乎在五一放假时 我换了个思路，我不搞静态了，我搞动态的。

于是在海豚里建了一个插件，
![](https://box.kancloud.cn/9e59b717a605206c9d8524d2df22dd68_408x579.png)

![](https://box.kancloud.cn/151ea4077b21e19b8c5273df961a8bec_1572x283.png)

![](https://box.kancloud.cn/a2706b813b86185a7754188e9a4da023_1568x555.png)

![](https://box.kancloud.cn/a2c1a142688505b1561ce354df0d468e_1572x603.png)

以章节的形式添加。终于效率上去了，五一时候抽空把内容全补全了。

发布到了 掘金上，获得了17个赞。

![](https://box.kancloud.cn/00443be8b9c5c5e7ceed4ed55525fd82_350x209.png)


## 进击的速查表

本来以为完成了。结果老大们太积极7月4日又发布了5.0.10，然后在开发5.1dev版。

既然老大把我的速查表都挂到了tp官网上。我也不能让用的人等，看旧的5.0.7版、

可是我不想在人工去对比改了哪个类，增加还是删除了哪些方法。20多章呢。

我想 “代码的问题应该由代码解决”。于是想到了php的注解、反射类。
 
正好项目用到了一个 **crada/php-apidoc** 的api文档生成工具。

于是我就开始动手实现这通过类反射信息获取方法的工程。

### 反射的资料

> PHP 5 具有完整的反射 API，添加了对类、接口、函数、方法和扩展进行反向工程的能力。 此外，反射 API 提供了方法来取出函数、类和方法中的文档注释。

官网手册提到了反射有这多类：

Reflection
ReflectionClass
ReflectionZendExtension
ReflectionExtension
ReflectionFunction
ReflectionFunctionAbstract
ReflectionMethod
ReflectionObject
ReflectionParameter
ReflectionProperty
ReflectionType
ReflectionGenerator
Reflector
ReflectionException

### 实现思路

~~~
// TODO 获取待处理的类命名空间数据
// TODO 遍历类 反射
// TODO 获取类的信息 (名称、方法列表)
// TODO 遍历方法列表， 获取方法的类型 和注释
~~~

我看了一遍反射是先反射类 再找到方法 再找到方法的参数

#### 类的获取
tp5的核心类 都在一个目录

于是我想到了用glob遍历

~~~
	public function get_core_class(){
		$class_path = CORE_PATH;
		$before_cwd = getcwd();
		chdir($class_path);
		$names = glob('*.php');
		$ret = [];
		foreach ($names as $key => $name) {
			$ret[] = 'think\\'. str_ireplace('.php', '', $name);
		}
		chdir($before_cwd);
		return $ret;
	}
~~~

反射类的初始化要传的是类的实际命名空间路径。

`$class= new\ReflectionClass($className);` 这样。然后有以下方法：

ReflectionClass::__construct — 初始化 ReflectionClass 类
ReflectionClass::export — 导出一个类
ReflectionClass::getConstant — 获取定义过的一个常量
ReflectionClass::getConstants — 获取一组常量
ReflectionClass::getConstructor — 获取类的构造函数
ReflectionClass::getDefaultProperties — 获取默认属性
ReflectionClass::getDocComment — 获取文档注释
ReflectionClass::getEndLine — 获取最后一行的行数
ReflectionClass::getExtension — 根据已定义的类获取所在扩展的 ReflectionExtension 对象
ReflectionClass::getExtensionName — 获取定义的类所在的扩展的名称
ReflectionClass::getFileName — 获取定义类的文件名
ReflectionClass::getInterfaceNames — 获取接口（interface）名称
ReflectionClass::getInterfaces — 获取接口
ReflectionClass::getMethod — 获取一个类方法的 ReflectionMethod。
ReflectionClass::getMethods — 获取方法的数组
ReflectionClass::getModifiers — 获取类的修饰符
ReflectionClass::getName — 获取类名
ReflectionClass::getNamespaceName — 获取命名空间的名称
ReflectionClass::getParentClass — 获取父类
ReflectionClass::getProperties — 获取一组属性
ReflectionClass::getProperty — 获取类的一个属性的 ReflectionProperty
ReflectionClass::getShortName — 获取短名
ReflectionClass::getStartLine — 获取起始行号
ReflectionClass::getStaticProperties — 获取静态（static）属性
ReflectionClass::getStaticPropertyValue — 获取静态（static）属性的值
ReflectionClass::getTraitAliases — 返回 trait 别名的一个数组
ReflectionClass::getTraitNames — 返回这个类所使用 traits 的名称的数组
ReflectionClass::getTraits — 返回这个类所使用的 traits 数组
ReflectionClass::hasConstant — 检查常量是否已经定义
ReflectionClass::hasMethod — 检查方法是否已定义
ReflectionClass::hasProperty — 检查属性是否已定义
ReflectionClass::implementsInterface — 接口的实现
ReflectionClass::inNamespace — 检查是否位于命名空间中
ReflectionClass::isAbstract — 检查类是否是抽象类（abstract）
ReflectionClass::isAnonymous — 检查类是否是匿名类
ReflectionClass::isCloneable — 返回了一个类是否可复制
ReflectionClass::isFinal — 检查类是否声明为 final
ReflectionClass::isInstance — 检查类的实例
ReflectionClass::isInstantiable — 检查类是否可实例化
ReflectionClass::isInterface — 检查类是否是一个接口（interface）
ReflectionClass::isInternal — 检查类是否由扩展或核心在内部定义
ReflectionClass::isIterateable — 检查是否可迭代（iterateable）
ReflectionClass::isSubclassOf — 检查是否为一个子类
ReflectionClass::isTrait — 返回了是否为一个 trait
ReflectionClass::isUserDefined — 检查是否由用户定义的
ReflectionClass::newInstance — 从指定的参数创建一个新的类实例
ReflectionClass::newInstanceArgs — 从给出的参数创建一个新的类实例。
ReflectionClass::newInstanceWithoutConstructor — 创建一个新的类实例而不调用它的构造函数
ReflectionClass::setStaticPropertyValue — 设置静态属性的值
ReflectionClass::__toString — 返回 ReflectionClass 对象字符串的表示形式。

这些方法看着是静态，其实可以 **$class->getShortName()** 直接使用。

我主要需要拿到类简写名和方法。

~~~
public function generate($classNames){
		config('default_return_type', 'json');
		// TODO 获取待处理的类命名空间数据
		// TODO 遍历类 反射
		// TODO 获取类的信息 (名称、方法列表)
		// TODO 遍历方法列表， 获取方法的类型 和注释

		$outputs = [];
		foreach ($classNames as $k => $className) {
			$class= new\ReflectionClass($className);
			$key = $class->getShortName();
			// dump($key);
			$outputs[$key] = $this->getClassAnnotation($class);
		}
		return $outputs;
	}
~~~

getClassAnonation 方法就是我用来获取类的全部方法的信息的方法。

#### 方法相关
拿到反射类之后 想获取反射方法，得实例化 ReflectionMethod 类。

~~~
	// 获取类的注释信息
	public function getClassAnnotation($class){

		$ret = [
			'hasPublicMethods'=>0,
		];
		$ret['name'] = $class->getName();
		$methods = $class->getMethods();
		foreach ($methods as $key => $method) {
			$class = $method->class;
			$method_name = $method->name;
			$rm = new \ReflectionMethod($class, $method_name);
			// 忽略构造和析构
			if($rm->isConstructor() || $rm->isDestructor()){
				continue;
			}
			$foo = [];
			$foo['docComment'] = $rm->getDocComment();
			$foo['docComment_formated'] = $this->parseMethodDoc($foo['docComment']);
			$foo['args'] = $rm->getParameters();
			$foo['args_formated'] = $this->parseParameters($class, $method_name, $foo['args']);
			if($rm->isPublic()){
				$type = $rm->isStatic()? 'public_static' : 'public_public';
			}else{
				$type = $rm->isStatic()? 'private_static' : 'private_public';
			}
			// 只在hasPublicMethods 为0时更新值，保证设置1后不会被复写为0
			if(empty($ret['hasPublicMethods'])){
				$ret['hasPublicMethods'] = stripos($type, '_public') !== false;
			}
			$foo['type'] = $type;
			$ret['methods'][$method_name] = $foo;
		}

		return $ret;
		// $className = 'think\\App';
		// $class = new \ReflectionClass($className);
		// config('default_return_type', 'json');

		// 类名
		// return $class->name;

		// ReflectionClass 实例的一个字符串表示形式
		// return $class->__toString();

		// 同上
		// return \ReflectionClass::export($className, 1);

		// 获取类常量
		// return json_encode($class->getConstants());

		// 获取构造方法
		// return $class->getConstructor();

		// 类名相关
		// var_dump($class->inNamespace());
		// var_dump($class->getName());
		// var_dump($class->getNamespaceName());
		// var_dump($class->getShortName());

		# 文件相关
		// getFileName
		// getExtensionName

		// 属性相关
		// return $class->getDefaultProperties();
		// return $class->getProperties(\ReflectionProperty::IS_PUBLIC | \ReflectionProperty::IS_PROTECTED);

		// const integer IS_STATIC = 1 ;
		// const integer IS_PUBLIC = 256 ;
		// const integer IS_PROTECTED = 512 ;
		// const integer IS_PRIVATE = 1024 ;

		// return $class->getStaticProperties();

		// 类注释
		// return $class->getDocComment();
	}
~~~

先获取全部的类方法：

$class->getMethods();

官网的例子：
~~~
array(3) {
  [0]=>
  &object(ReflectionMethod)#2 (2) {
    ["name"]=>
    string(11) "firstMethod"
    ["class"]=>
    string(5) "Apple"
  }
  [1]=>
  &object(ReflectionMethod)#3 (2) {
    ["name"]=>
    string(12) "secondMethod"
    ["class"]=>
    string(5) "Apple"
  }
  [2]=>
  &object(ReflectionMethod)#4 (2) {
    ["name"]=>
    string(11) "thirdMethod"
    ["class"]=>
    string(5) "Apple"
  }
}
~~~
在获取时还可以传属性类型进行过滤：

~~~
<?php
class Apple {
    public function firstMethod() { }
    final protected function secondMethod() { }
    private static function thirdMethod() { }
}

$class = new ReflectionClass('Apple');
$methods = $class->getMethods(ReflectionMethod::IS_STATIC | ReflectionMethod::IS_FINAL);
var_dump($methods);
?>
~~~

拿到方法后，我们需要获得类的方法的公有私有、静态等属性。

![](https://box.kancloud.cn/8e5426f80c5fd4ff970a167964fb3102_287x529.png)

因为我在显示时做了方法不同类型的区分演示。

~~~
$rm = new \ReflectionMethod($class, $method_name);
// 忽略构造和析构
if($rm->isConstructor() || $rm->isDestructor()){
	continue;
}
~~~

先过滤掉构造和析构方法。


~~~
$foo = [];
$foo['docComment'] = $rm->getDocComment();
$foo['docComment_formated'] = $this->parseMethodDoc($foo['docComment']);
$foo['args'] = $rm->getParameters();
$foo['args_formated'] = $this->parseParameters($class, $method_name, $foo['args']);
~~~
我先获取了原有方法的文档信息和参数信息，并且按照我需要的进行格式化。

获取参数的要注意，返回的是参数数组

官方示例：
~~~
<?php
public static function fire_theme_method($class, $method)
{
        $fire_args=array();
        
        $reflection = new ReflectionMethod($class, $method);

    foreach($reflection->getParameters() AS $arg)
    {
        if($_REQUEST[$arg->name])
        $fire_args[$arg->name]=$_REQUEST[$arg->name];
        else
        $fire_args[$arg->name]=null;
    }
        
    return call_user_func_array(array($class, $method), $fire_args);
}
?>
~~~
主要咱获取到参数名称 然后结合methodName 去实例化 ReflectionParameter 来获取参数信息

#### 类的参数信息

~~~
public function parseParameters($class, $method, $args){
		if($args){
			$args_str = [];
			foreach ($args as $key => $arg) {
				$p = new \ReflectionParameter(array($class, $method), $key);
				// 判断是否引用参数
				if($p->isPassedByReference()){
					$arg_str_new = "&\$".$p->getName();
				}else{
					$arg_str_new = "\$".$p->getName();
				}
				if ($p->isOptional() && $p->isDefaultValueAvailable()) {
					$a_clsss = $class;
					// 获取某些内部类的参数会抛异常，且异常时$class会变化不是我们想知道的哪个类方法一场了
					try{
						$defaul = $p->getDefaultValue();
						$arg_str_new .= is_array($defaul) ? ' = '. '[]': ' = '. var_export($defaul, 1);
					}catch(\Exception $e){
						trace($p->isVariadic());
						trace($a_clsss.'/'.$method.'_'.$key);
					}
				}
				$args_str[] = $arg_str_new;
			}
			return implode(', ', $args_str);
		}
		return '';
	}
~~~

有的方法没参数直接返回空，有的有参数，咱们想拼接处 参数字符串 比如

~~~
<?php
class A{
	function foo($a){
    	
    }
}
~~~

php不会返回` foo($a)`这串的。得自己处理

主要留意参数的 是否有默认值、是否引用

* getName
* isOptional
* isDefaultValueAvailable
* getDefaultValue

在获取默认值参数的时候 我发现有的时候会抛异常，而且都报的是内部类的。

所以一定要try catch 去获取默认值。

至此 整个获取某些类的 方法及方法注释和参数信息 的功能全部实现。

大家如果想获取某一组class的 速查表 只需 修改get_core_class返回值，只要是tp5里自动加载的类。都可以解析。

整体思路，根据类数组获取方法->方法文档、获取参数->获取参数信息

这样，我就可以安心的偷懒了。下次tp升级，我直接composer update一下，刷新一下首页，拿到静态html  更新到我的 gh-pages 分支。就完成了新框架速写表的更新。

一劳永逸啊。

## 尾声

具体源码参考 ：https://github.com/yangweijie/thinkphp-lts

查看速查表 直接：https://yangweijie.github.io/thinkphp-lts/

![](https://box.kancloud.cn/5cc127b3019ca3971a3107237d9569f8_1872x967.png)

欢迎给我提供建议。

