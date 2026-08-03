  swoole的资料：
https://wiki.swoole.com

主要看了 环境依赖、编译安装、快速起步

2. 起步 聊天室 websocket 参见ws.zip。

开始遇到的问题：
如何重载
Swoole提供了柔性终止/重启的机制，管理员只需要向SwooleServer发送特定的信号，Server的worker进程可以安全的结束。
•	SIGTERM: 向主进程/管理进程发送此信号服务器将安全终止
•	在PHP代码中可以调用$serv->shutdown()完成此操作
•	SIGUSR1: 向主进程/管理进程发送SIGUSR1信号，将平稳地restart所有worker进程
•	在PHP代码中可以调用$serv->reload()完成此操作
•	swoole的reload有保护机制，当一次reload正在进行时，收到新的重启信号会丢弃
•	如果设置了user/group，Worker进程可能没有权限向master进程发送信息，这种情况下必须使用root账户，在shell中执行kill指令进行重启
由于swoole 是常驻内存的，如果修改了代码 直接继续发送包代码是不生效的。需要reload
1. 设置进程标题，通过ps grep 查找来kill
~~~
cli_set_process_title('chat_process'); 这个mac  不支持
kill -15 pid
~~~
2. 将进程pid 写入脚本，root用户手动重启

~~~
ps -efH|grep swoole mac上 是 ps -efh|grep php
$server->on('start',function($serv ) {
    // cli_set_process_title('chat_process');
    $managerPid = $serv->manager_pid;

    $shString = <<<SH
echo "Reloading..."

kill -USR1 {$managerPid}

echo "Reloaded"
SH;
	$sh_file = '.reload_manager.sh';
    file_put_contents($sh_file, $shString);
});
~~~
3. 安装inotify 扩展 监听文件，将文件 在onWorkStart 回调中require_once. 监听到文件变化了，自动重启
参考sd框架
4. 链接的fd 不好感知是哪个设备，如何将针对不同设备形成定向广播
$server->connection_list()  获取全部在线链接

5. 数据库超时
暂时设置了数据库的重连参数
'break_reconnect' => true,
6. 引入tp框架后，调试输出的不显示了
介入其他项目里的 alert dlert 函数
7. 报错在终端不方便追踪bug，
接管异常
设计同步方案
针对重载，在根目录建立server_function.php workStart里 require_once

~~~
<?php
function onMessage($server, $frame){
	\Think\App::invokeClass('\app\index\controller\Message', [])->receive($server, $frame);
}

function onTask($server, $task_id, $src_worker_id, $data){
	\Think\App::invokeClass('\app\index\controller\Task', [])->run($server, $task_id, $src_worker_id, $data);
}

function onClose($server, $fd){
    $data = json_encode([
        'op'      => 'after_close',
        'data'    => '',
        'from_fd' => $fd,
    ], JSON_UNESCAPED_UNICODE);
    $server->task($data);
}

function onRequest ($server, $request, $response) {
    //请求过滤
    if ($request->server['path_info'] == '/favicon.ico' || $request->server['request_uri'] == '/favicon.ico') {
        return $response->end();
    }
	// 环境常量
    $response->header('Access-Control-Allow-Origin', "*");
	$_SERVER = [
        'argv' => [],
    ];
    $_GET    = $request->get?:[];
    $_POST   = $request->post;
    foreach ($request->server as $key=>$value) {
    	$_SERVER[strtoupper($key)] = $value;
    }
    $_COOKIE = $request->cookie;
    $_FILES  = $request->files;
    $ret = \Think\App::invokeClass('\app\index\controller\Index', [$server, $request, $response])->request();
    $response->end($ret);
    exit();
}
~~~

主文件index.php

~~~
<?php
namespace think;
global $server;
$server = new \swoole_websocket_server("0.0.0.0", 9501);
$server->set(
	['task_worker_num'=>10]
);

$server->on('start',function($serv ) {
    // cli_set_process_title('chat_process');
    $managerPid = $serv->manager_pid;

    $shString = <<<SH
echo "Reloading..."

kill -USR1 {$managerPid}

echo "Reloaded"
SH;
	$sh_file = '.reload_manager.sh';
    file_put_contents($sh_file, $shString);
});

$server->on('WorkerStart',function($serv , $worker_id) {
	define('ERROR_LOG_TYPE', 'ws_error_log');
	define('APP_PATH', __DIR__ . '/application/');
	define('THINK_PATH', __DIR__ . '/thinkphp/');
	// 加载框架引导文件
	require_once __DIR__ . '/base.php';
	$_SERVER = [
		'REQUEST_METHOD' => 'GET',
		'argv'           => [],
	];
});


$server->on('open', function (\swoole_websocket_server $server, $request) {
    echo "server: handshake success with fd{$request->fd}\n";
});

$server->on('message', function (\swoole_websocket_server $server, $frame) {
	echo "receive from {$frame->fd}:{$frame->data},opcode:{$frame->opcode},fin:{$frame->finish}\n";
	$_SERVER['REQUEST_TIME'] = time();
	App::initCommon();
	require_once __DIR__. '/server_function.php';
    onMessage($server, $frame);
});

$server->on('close', function ($ser, $fd) {
    echo "client {$fd} closed\n";
	require_once __DIR__. '/server_function.php';
    onClose($ser, $fd);
});

$server->on('finish', function ($ser, $fd) {
    return true;
});

$server->on('task', function(\swoole_websocket_server $server, $task_id, $src_worker_id, $data){
	App::initCommon();
	require_once __DIR__. '/server_function.php';
	onTask($server, $task_id, $src_worker_id, $data);
	return true;
});

$server->start();
~~~

首先，参考 https://www.tuicool.com/articles/emY3Ar  有了思路 ，然后阅读tp5源码 app 发现可以用静态方法将 映射调用某个类，因此。
将task message 映射到Task 的run  和 Message控制器 的 receive 方法里。

然后 定义数据格式为json 然后 反json后 动态op 参数调用内部方法。

消息的处理
经过讨论，为了方便客户端离线后台看到消息，我们设计了数据表 ws_message表。



业务消息必然和shop_id table_id 相关，然后保存 发送方from_client_id 和接受方to_client_id 并记录 发送消息设备类型 主还是副

经过讨论，主设备发送消息 无需记录， 消息 中data 和user_info 为序列化字段。

Message 类的组成

~~~
<?php
namespace app\index\controller;

use app\common\lib\SystemLog;
use app\index\model\WsDevices;
use app\index\model\WsMessage;
use app\index\model\WsOnlineClients;

class Message
{

    public function __construct()
    {
        config('default_return_type', 'json');
    }

    public $from_fd;
    public $server;
    public $date_format = 'Y-m-d H:i:s';

    public function success($info, $data = [])
    {
        debug('api_end');
        $push_data = [
            'code'      => 0,
            'msg'       => $info,
            'time'      => date($this->date_format, $_SERVER['REQUEST_TIME']),
            'data'      => $data,
            'ttfb_time' => debug('api_begin', 'api_end', 6) . 's',
        ];
        return $this->server->push($this->from_fd, json_encode($push_data, JSON_UNESCAPED_UNICODE));
    }

    public function error($info, $data = [])
    {
        debug('api_end');
        $push_data = [
            'code'      => 1,
            'msg'       => $info,
            'time'      => date($this->date_format, $_SERVER['REQUEST_TIME']),
            'data'      => $data,
            'ttfb_time' => debug('api_begin', 'api_end', 6) . 's',
        ];
        return $this->server->push($this->from_fd, json_encode($push_data, JSON_UNESCAPED_UNICODE));
    }

    public function receive($server, $frame)
    {
        debug('api_begin');
        $data = $frame->data;
        $this->from_fd = $frame->fd;
        $this->server = $server;
        echo $data . '\n';
        $data = json_decode($data, 1);
        if (is_array($data)) {
            if (method_exists($this, $data['op'])) {
                $call = $data['op'];
                unset($data['op']);
                $this->$call($server, $frame, $data);
            } else {
                goto rawMsg;
            }
        } else {
            rawMsg:
            $this->rawMsg($server, $frame, $frame->data);
        }
    }

    // 登录
    public function login($server, $frame, $data)
    {
        // dlert2("fd:#{$frame->fd}|shop_id:{$data['shop_id']}|client_id:{$data['client_id']}|type:{$data['type']}的设备登录了，".datetime());
        WsDevices::login($frame->fd, $data['shop_id'], $data['client_id'], $data['type']);
        if($data['type'] == '主'){
            // 登录后重发数据， 客户端重新链接后会重新拉去列表
            // $data = json_encode([
            //     'op'        => 'after_login',
            //     'client_id' => $data['client_id'],
            //     'from_fd'   => $frame->fd,
            // ], JSON_UNESCAPED_UNICODE);
            // $server->task($data);
        }
    }

    // 登出
    public function logout($server, $frame, $data)
    {
        $server->close($frame->fd);
    }

    // 加菜 退菜 打折 赠送 结账
    public function notify($server, $frame, $data)
    {
        if ($data['from_client_type'] == '主') {
            $sub_clients = WsDevices::getSubClientByShopId($data['shop_id']);
            if ($sub_clients) {
                $sub_client_ids = array_column($sub_clients, 'client_id');
                $fds = WsOnlineClients::where('client_id', 'in', $sub_client_ids)->column('fd');
                foreach ($fds as $fd) {
                    $server->push($fd, $data);
                }
            }
        } else {
            $main_clients = WsDevices::getMainClientByShopId($data['shop_id']);
            if ($main_clients) {
            	$ws_message_client_ids = [];
                foreach ($main_clients as $main_client) {
                    $id = WsMessage::add($data['shop_id'], $data['table_id'], $data['type'], $data['data'], $data['user_info'], $data['from_client_id'], $main_client['client_id'], '副', $data['status']);
                	$ws_message_client_ids[$main_client['client_id']] = $id;
                }
                $main_client_ids = array_column($main_clients, 'client_id');
              
                if ($main_client_ids) {
                    $fds = WsOnlineClients::where('client_id', 'in', $main_client_ids)->column('client_id,fd');
                    $online_messages = array_intersect_key($ws_message_client_ids, $fds);
                    foreach ($fds as $client_id=>$fd) {
                    	if(isset($online_messages[$client_id])){
                    		$msg_id = $online_messages[$client_id];
                    		$push_data = [
                                'id'       => $msg_id, 
                                'status'   => $data['status'], 
                                'table_id' => $data['table_id'], 
                                'type'     => $data['type'],
                                'title'    => "桌id：{$data['table_id']} {$data['type']}",
                            ];
                            $info = $server->connection_info($fd);
                            if($info['websocket_status'] == 3){
                                $ret = $server->push($fd, json_encode($push_data, JSON_UNESCAPED_UNICODE));
                                if($ret){
                                    WsMessage::where('id', $msg_id)->update(['is_delivered'=>1]);
                                }else{
                                    $fail_msg = sprintf('时间：%s，店铺id:%d下子设备 client_id:%s 向主设备client_id %s发送 【桌号id：%s，类型：%s，消息id：%d】的消息失败', datetime(),$data['shop_id'], $data['from_client_id'], $client_id, $data['table_id'], $data['type'], $msg_id);
                                    alert(__CLASS__.':'.__FUNCTION__.':L'.__LINE__.PHP_EOL.$fail_msg);
                                    dlert(__CLASS__.':'.__FUNCTION__.':L'.__LINE__.PHP_EOL.$fail_msg);
                                    SystemLog::error_log($fail_msg, __CLASS__.':'.__FUNCTION__.':L'.__LINE__, ERROR_LOG_TYPE);
                                }
                            }
                    	}
                    }
                }
            } else {
                $this->error('店铺主设备未记录，请先联系商家完成主设备初始化');
            }
        }
    }

    // 处理非序列化消息
    public function rawMsg($server, $frame, $msg)
    {
        $server->push($frame->fd, "{$frame->data}");
        // dlert2($msg);
        if (stripos($msg, '说') !== false) {
            $data = json_encode([
                'op' => 'say',
                'data' => $msg,
                'from_fd' => $frame->fd,
            ], JSON_UNESCAPED_UNICODE);
            $server->task($data);
        }

        // 获取特殊管理的消息
        if (stripos($msg, 'from_admin') !== false) {
            parse_str($msg, $params);
            dump($params);
            $op = $params['op'];
            switch ($op) {
                case 'reload':
                    echo 'reloading server';
                    $server->reload();
                    break;
                case 'get_connections':
                    $server->push($frame->fd, json_encode($server->connection_list() ?: [], JSON_UNESCAPED_UNICODE));
                    break;
                case 'send_messages':
                    $data = json_encode([
                        'op'      => 'admin_say',
                        'data'    => $params['content'],
                        'from_fd' => $frame->fd,
                        'to_fds'  => $params['to_fds'],
                    ], JSON_UNESCAPED_UNICODE);
                    $server->task($data);
                    break;
                default:
                    break;
            }
        }
    }
}
~~~
rawMsg  是用于不是json 格式的字符串，处理消息。用于客户端测试 echo服务器。和其他特殊命令
login  用于自定义登录消息，记录在线设备，更新设备状态
logout 下线（设备-删除ws_online_clients）记录。通过手动close fd 抓onClose里的 task 异步任务。

notify 主要逻辑 主要用于 产生消息记录，并广播至同店铺主设备（多个主设备比较复杂，需要二次同步，不实现）。push成功后更新is_delived 字段

http接口
1.获取消息列表（待处理-shop_id）ws.weiwoju.com/api.php/index/index/messageList/shop_id/{shop_id}
直接查询

2. 处理标记消息
ws.weiwoju.com/api.php/index/index/deal/{id:1,status}

3. 获取主设备在线状态
ws.weiwoju.com/api.php/index/index/check_online_main/shop_id/{shop_id}
其实就是查询online表和devices 表的

4. http 内请求websocket
ws.weiwoju.com/api.php/index/index/notify_main/ 参数见代码

和web端请求格式一致。

进程模型





ssl开启
生成证书：
SSL支持

本章将详细讲解如何制作证书以及如何开启Swoole的SSL的单向、双向认证。
准备工作
选择任意路径，执行如下命令创建文件夹结构
~~~
mkdir ca
cd ca
mkdir private
mkdir server
mkdir newcerts
~~~
在ca目录下创建openssl.conf文件，文件内容如下
~~~
[ ca ]  
default_ca      = foo                   # The default ca section  

[ foo ]  
dir            = /path/to/ca         # top dir  
database       = /path/to/ca/index.txt          # index file.  
new_certs_dir  = /path/to/ca/newcerts           # new certs dir  

certificate    = /path/to/ca/private/ca.crt         # The CA cert  
serial         = /path/to/ca/serial             # serial no file  
private_key    = /path/to/ca/private/ca.key  # CA private key  
RANDFILE       = /path/to/ca/private/.rand      # random number file  

default_days   = 365                     # how long to certify for  
default_crl_days= 30                     # how long before next CRL  
default_md     = md5                     # message digest method to use  
unique_subject = no                      # Set to 'no' to allow creation of  
                                         # several ctificates with same subject.  
policy         = policy_any              # default policy  

[ policy_any ]  
countryName = match  
stateOrProvinceName = match  
organizationName = match  
organizationalUnitName = match  
localityName            = optional  
commonName              = optional  
emailAddress            = optional
~~~
其中，/path/to/ca/是ca目录的绝对路径。
创建ca证书
在ca目录下创建一个shell脚本，命名为new_ca.sh。文件内容如下：
~~~
#!/bin/sh  
openssl genrsa -out private/ca.key  
openssl req -new -key private/ca.key -out private/ca.csr  
openssl x509 -req -days 365 -in private/ca.csr -signkey private/ca.key -out private/ca.crt  
echo FACE > serial  
touch index.txt  
openssl ca -gencrl -out private/ca.crl -crldays 7 -config "./openssl.conf"
~~~

执行sh new_ca.sh命令，创建ca证书。生成的证书存放于private目录中。
注意 在创建ca证书的过程中，需要输入一些信息。其中，countryName、stateOrProvinceName、organizationName、organizationalUnitName这四个选项的内容必须要填写，并且需要记住。在生成后续的证书过程中，要保证这四个选项的内容一致。
创建服务端证书
在ca目录下创建一个shell脚本，命名为new_server.sh。文件内容如下：
~~~
#!/bin/sh  
openssl genrsa -out server/server.key  
openssl req -new -key server/server.key -out server/server.csr  
openssl ca -in server/server.csr -cert private/ca.crt -keyfile private/ca.key -out server/server.crt -config "./openssl.conf"
~~~
执行sh new_ca.sh命令，创建ca证书。生成的证书存放于server目录中。
创建客户端证书
在ca目录下创建一个shell脚本，命名为new_client.sh。文件内容如下：
~~~
#!/bin/sh  

base="./"  
mkdir -p $base/users/  
openssl genrsa -des3 -out $base/users/client.key 1024  
openssl req -new -key $base/users/client.key -out $base/users/client.csr  
openssl ca -in $base/users/client.csr -cert $base/private/ca.crt -keyfile $base/private/ca.key -out $base/users/client.crt -config "./openssl.conf"  
openssl pkcs12 -export -clcerts -in $base/users/client.crt -inkey $base/users/client.key -out $base/users/client.p12
~~~
执行sh new_ca.sh命令，创建ca证书。生成的证书存放于users目录中。 进入users目录，可以看到有一个client.p12文件，这个就是客户端可用的证书了，但是这个证书是不能在php中使用的，因此需要做一次转换。命令如下：
~~~
openssl pkcs12 -clcerts -nokeys -out cer.pem -in client.p12
openssl pkcs12 -nocerts -out key.pem -in client.p12
~~~
以上两个命令会生成cer.pem和key.pem两个文件。其中，生成key.pem时会要求设置密码，这里记为client_pwd
注意 如果在创建客户端证书时，就已经给client.p12设置了密码，那么在转换格式的时候，需要输入密码进行转换
最终结果
以上步骤执行结束后，会得到不少文件，其中需要用的文件如下表所示：

| 文件名 | 路径 | 说明 | 
| --- | --- | --- |
| ca.crt | ca/private/ | ca证书 | 
| server.crt | ca/server/ | 服务器端证书 | 
| server.key | ca/server/ | 服务器端秘钥 | 
| cer.pem | ca/client/ | 客户端证书 |
| key.pem | ca/client/ | 客户端秘钥 |

SSL单向认证
Swoole开启SSL
Swoole开启SSL功能需要如下参数：
~~~
$server = new swoole_server("127.0.0.1", "9501" , SWOOLE_PROCESS, SWOOLE_SOCK_TCP | SWOOLE_SSL );
$server = new swoole_http_server("127.0.0.1", "9501" , SWOOLE_PROCESS, SWOOLE_SOCK_TCP | SWOOLE_SSL );
~~~
并在swoole的配置选项中增加如下两个选项：
~~~
$server->set(array(
    'ssl_cert_file' => '/path/to/server.crt',
    'ssl_key_file' =>  '/path/to/server.key',
));
~~~
这时，swoole服务器就已经开启了单向SSL认证，可以通过https://127.0.0.1:9501/进行访问。
SSL双向认证
服务器端设置
双向认证指服务器也要对发起请求的客户端进行认证，只有通过认证的客户端才能进行访问。 为了开启SSL双向认证，swoole需要额外的配置参数如下：
~~~
$server->set(array(
    'ssl_cert_file' => '/path/to/server.crt',
    'ssl_key_file' =>  '/path/to/server.key',
    'ssl_client_cert_file' => '/path/to/ca.crt',
    'ssl_verify_depth' => 10,
));
~~~
客户端设置
这里我们使用CURL进行https请求的发起。 首先，需要配置php.ini,增加如下配置：
`curl.cainfo=/path/to/ca.crt`
发起curl请求时，增加如下配置项：
~~~
$ch = curl_init();

curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, '2'); 
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);   // 只信任CA颁布的证书
curl_setopt($ch, CURLOPT_SSLCERT, "/path/to/cer.pem");
curl_setopt($ch, CURLOPT_SSLKEY,  "/path/to/key.pem");
curl_setopt($ch, CURLOPT_SSLCERTTYPE, 'PEM');
curl_setopt($ch, CURLOPT_SSLCERTPASSWD, '******'); // 创建客户端证书时标记的client_pwd密码
~~~
这时，就可以发起一次https请求，并且被swoole服务器验证通过了。

服务端域名 要开启那个ssl：

~~~
listen       443 ssl;
    ssl_certificate      server.crt;
    ssl_certificate_key  server.key;
    ssl_session_cache    shared:SSL:1m;
    ssl_session_timeout  5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers  on;
~~~

这样 443 后ssl  去掉ssl on  可以 混合访问

生成配置中的一些设置，经过测试不填host可以任意域名：

~~~
Country Name (2 letter code) []:CN
State or Province Name (full name) []:Zhejiang
Locality Name (eg, city) []:Hangzhou
Organization Name (eg, company) []:weiwoju
Organizational Unit Name (eg, section) []:ws
password = weiwoju

~~~
