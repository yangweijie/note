官方api里 pc.trade.pay 默认生成的是form 表单，不是原来php端支持的iframe 嵌入二维码的字符串返回，需要手动构建。

～～～java 命名空间引入
import com.alipay.easysdk.factory.Factory;
import com.alipay.easysdk.kernel.Client;
import com.aliyun.tea.TeaConverter;
import com.aliyun.tea.TeaPair;
～～～
~~~ 获取alipay的配置
 private Config getAliOptions() {
        Config config = new Config();
        config.protocol = "https";
//        config.gatewayHost = "openapi.alipay.com";
//        config.gatewayHost = env.equals("master")? "openapi.alipay.com": "openapi.alipaydev.com";
        SysConfig sc = null;
        sc = sysConfigService.detail("ali_pay_config");
        String scValue = null;
        scValue = sc.getValue();
        HashMap<String,String> scObject =  JSON.parseObject(scValue, HashMap.class);

        config.gatewayHost = scObject.get("dev").equals("0")  ? "openapi.alipay.com":"openapi.alipaydev.com";
        config.signType = "RSA2";

        config.appId = scObject.get("appid"); 

        // 为避免私钥随源码泄露，推荐从文件中读取私钥字符串而不是写入源码中
        config.merchantPrivateKey = scObject.get("privateKey"); 

        //注：证书文件路径支持设置为文件系统中的路径或CLASS_PATH中的路径，优先从文件系统中加载，加载失败后会继续尝试从CLASS_PATH中加载
//        config.merchantCertPath = "<-- 请填写您的应用公钥证书文件路径，例如：/foo/appCertPublicKey_2019051064521003.crt -->";
//        config.alipayCertPath = "<-- 请填写您的支付宝公钥证书文件路径，例如：/foo/alipayCertPublicKey_RSA2.crt -->";
//        config.alipayRootCertPath = "<-- 请填写您的支付宝根证书文件路径，例如：/foo/alipayRootCert.crt -->";

        //注：如果采用非证书模式，则无需赋值上面的三个证书路径，改为赋值如下的支付宝公钥字符串即可
         config.alipayPublicKey = scObject.get("publicKey"); 

        //可设置异步通知接收服务地址（可选）
        config.notifyUrl = scObject.get("notifyUrl");

        if(scObject.get("encryptKey") != null && !scObject.get("encryptKey").isEmpty()){
            //可设置AES密钥，调用AES加解密相关接口时需要（可选）
            config.encryptKey = scObject.get("encryptKey");

        return config;
    }
~~~

～～～ 发起订单
private Result aliThirdPay(BigDecimal moneyValue, Integer dId){
        // 1. 设置参数（全局只需设置一次）
        Config config = getAliOptions();
        Factory.setOptions(config);
        String notify_url = config.notifyUrl;
//        String notify_url = "https://xxxx.com/web/open/alipayCallback";
        String out_trade_no = SnowflakeIdWorker.nextId(1L) + "-" + dId;

        try {
            // 2. 发起API调用（以创建当面付收款二维码为例）
//            AlipayTradePrecreateResponse a = null;
            Client _kernel = Factory.Payment.Page()._kernel;

            Map<String, String> systemParams = TeaConverter.buildMap(
                new TeaPair("method", "alipay.trade.page.pay"),
                new TeaPair("app_id", _kernel.getConfig("appId")),
                new TeaPair("timestamp", _kernel.getTimestamp()),
                new TeaPair("format", "json"),
                new TeaPair("version", "1.0"),
                new TeaPair("alipay_sdk", _kernel.getSdkVersion()),
                new TeaPair("charset", "UTF-8"),
                new TeaPair("sign_type", _kernel.getConfig("signType")),
                new TeaPair("app_cert_sn", _kernel.getMerchantCertSN()),
                new TeaPair("alipay_root_cert_sn", _kernel.getAlipayRootCertSN())
            );

            Map<String, Object> bizParams = TeaConverter.buildMap(
                new TeaPair("body", "充值"),
                new TeaPair("qr_pay_mode", "4"),
                new TeaPair("qrcode_width", "100"),
                new TeaPair("subject", "充值订单"),
                new TeaPair("out_trade_no", out_trade_no),
                new TeaPair("total_amount", moneyValue),
                new TeaPair("product_code", "FAST_INSTANT_TRADE_PAY")
            );

            Map<String, String> textParams = TeaConverter.buildMap(
                new TeaPair("notify_url", notify_url)
            );

            String sign = _kernel.sign(systemParams, bizParams, textParams, _kernel.getConfig("merchantPrivateKey"));

            String url = _kernel.generatePage("GET", systemParams, bizParams, textParams, sign);

            Map<String, Object> resultMap = new HashMap<>();
            resultMap.put("url", url);
            resultMap.put("chargeWay", 0);
            return Result.ok(resultMap);
        } catch (Exception e) {
            System.err.println("调用遭遇异常，原因：" + e.getMessage());
            return Result.failed(e.getMessage());
        }
    }
～～～