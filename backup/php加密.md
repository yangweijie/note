~~~ shell
composer require phpseclib/phpseclib
~~~
# AES

~~~ php
use phpseclib3\Crypt\AES;

  # 加密
  $aesKey= md5(uniqid(rand(), true));
  $iv          = self::IV;
  // AES加密
  $aes = new AES('CBC');
  $aes->setKey($aesKey);
  $aes->setIV($iv);
  $dataJson = is_array($data) ? json_encode($data, JSON_THROW_ON_ERROR) : $data;
  $encode   = $aes->encrypt($dataJson);
  $encodeStr = strtoupper(bin2hex($encode));


  # 解密
  $iv          = self::IV;
  $data        = hex2bin(strtolower($data));
  // AES解密
  $aes = new AES('CBC');
  $aes->setKey($aesKey);
  $aes->setIV($iv);
  $encode = $aes->decrypt($data);
~~~
# RSA
~~~ php
# 加密
  public static function RsaEncode($publicKey, $data, $padding = RSA::ENCRYPTION_OAEP){
      $key = PublicKeyLoader::load(file_get_contents($publicKey), $password);
      $key->withPadding($padding);
      return base64_encode($key->encrypt($data));
  }

  public static function RsaDecode($privateKey, $data, $padding = RSA::ENCRYPTION_OAEP){
      $key = PublicKeyLoader::load(file_get_contents($privateKey), $password);
      $key->withPadding($padding);
      return $key->decrypt(base64_decode($data));
  }
# 解密
~~~

# SM3

~~~ shell
composer require ch4o5/sm3-php
~~~

~~~php
$sm3 = sm3('abc');
~~~

# 证书转换
有的时候客户发的是p12 证书 可以去[网站](https://myssl.com/cert_convert.html) 上转换
