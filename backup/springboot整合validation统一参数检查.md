

# 1.背景
﻿
实际开发中对参数进行检查,是常见
﻿
比如如下代码
﻿
~~~
/**
     * 参数检查测试(传统做法)
     *
     * @param dto
     * @return
     */
    @GetMapping("/paramCheckOld")
    public BaseResponse paramCheckOld(@RequestBody UserDTO dto) {
        // 参数检查
        if (StrUtil.isEmpty(dto.getWeChat())) {
            return ResponseBuilder.failed("微信号为空");
        }
        if (StrUtil.isEmpty(dto.getName())) {
            return ResponseBuilder.failed("姓名为空");
        }
﻿
        if (dto.getStatus() != null
                || dto.getStatus() != -1
                || dto.getStatus() != 0
                || dto.getStatus() != 1) {
            return ResponseBuilder.failed("状态为-1,0,1或者null");
        }
        // .....如果参数很多这里必然后崩溃..........
        // 调用业务方法
        // 响应结果
        System.out.println("dto=" + dto);
        return ResponseBuilder.success("统一参数检查.....");
    }
~~~
﻿

﻿
但是正确的做法应该是,这里其实只使用了一个@Validated注解就搞定了,太方便了.....
﻿

﻿
~~~
 /**
     * 统一参数检查(牛逼的做法)
     *
     * @param dto
     * @return
     */
    @GetMapping("/paramCheck")
    public BaseResponse paramCheck(@RequestBody @Validated UserDTO dto) {
        // 参数检查(已检查)
        // 调用业务方法
        // 响应结果
        System.out.println("dto=" + dto);
        return ResponseBuilder.success("统一参数检查.....");
    }
~~~
﻿

﻿
# 2.步骤
﻿
步骤一:引入jar包
﻿
~~~
 <!--  统一参数校验-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
~~~
﻿
步骤二:参数上贴标签
﻿

﻿
~~~
package com.ldp.user.entity.dto;
﻿
import com.ldp.user.common.validation.EnumValue;
import lombok.Data;
﻿
import javax.validation.constraints.NotBlank;
﻿
/**
 * @author 姿势帝-博客园
 * @address https://www.cnblogs.com/newAndHui/
 * @WeChat 851298348
 * @create 01/01 4:00
 * @description
 */
@Data
public class UserDTO {
    @NotBlank(message = "微信号不能为空")
    private String weChat;
﻿
    @NotBlank(message = "姓名不能为空")
    private String name;
    /**
     * 年龄
     */
    private Integer age;
    /**
     * 状态
     * -1:冻结用户 ,0:正常用户, 1:没有实名认证
     */
    @EnumValue(intValues = {-1, 0, 1}, message = "状态为-1,0,1或者null")
    private Integer status;
    /**
     * 地址
     */
    private String address;
}
~~~
﻿

﻿
步骤三:控制层方法上贴标签(当然在其他方法上也可以用的,只是一般我们用在控制层上)
﻿
﻿
~~~
/**
     * 统一参数检查(牛逼的做法)
     *
     * @param dto
     * @return
     */
    @GetMapping("/paramCheck")
    public BaseResponse paramCheck(@RequestBody @Validated UserDTO dto) {
        // 参数检查(已检查)
        // 调用业务方法
        // 响应结果
        System.out.println("dto=" + dto);
        return ResponseBuilder.success("统一参数检查.....");
    }
~~~
﻿
﻿
步骤四:统一参数检查不通过时提示消息获取
﻿
﻿
~~~
  /**
     * 参数异常捕获
     *
     * @param ex
     * @return
     */
    @ResponseBody
    @ExceptionHandler(value = ConstraintViolationException.class)
    public Object constraintViolationExceptionHandler(ConstraintViolationException ex) {
        Set<ConstraintViolation<?>> constraintViolations = ex.getConstraintViolations();
        Iterator<ConstraintViolation<?>> iterator = constraintViolations.iterator();
        List<String> msgList = new ArrayList<>();
        while (iterator.hasNext()) {
            ConstraintViolation<?> cvl = iterator.next();
            msgList.add(cvl.getMessageTemplate());
        }
        return ResponseBuilder.failed(msgList.toString());
    }
﻿
    @ExceptionHandler(BindException.class)
    @ResponseBody
    public Object getBindException(BindException ex) {
        List<ObjectError> objectErrors = ex.getBindingResult().getAllErrors();
        if (!CollectionUtils.isEmpty(objectErrors)) {
            StringBuilder msgBuilder = new StringBuilder();
            for (ObjectError objectError : objectErrors) {
                msgBuilder.append(objectError.getDefaultMessage()).append(",");
            }
            String errorMessage = msgBuilder.toString();
            if (errorMessage.length() > 1) {
                errorMessage = errorMessage.substring(0, errorMessage.length() - 1);
            }
            return ResponseBuilder.failed(errorMessage);
        }
        return ResponseBuilder.failed(ex.getMessage());
    }
~~~
﻿
﻿
步骤五测试
﻿
﻿
~~~
  @Test
    void paramCheck() {
        String url = urlLocal + "/userOrder/paramCheck";
        System.out.println("请求地址:" + url);
        HttpRequest request = HttpUtil.createRequest(Method.GET, url);
        Map<String, Object> map = new TreeMap<>();
        // 业务参数
      //  map.put("weChat", "851298348");
       // map.put("name", "李东平");
        map.put("age", "18");
        map.put("status", "0");
        map.put("address", "四川成都");
﻿
        // 公用参数
        map.put("appid", "1001");
        map.put("sequenceId", "seq" + System.currentTimeMillis());
        map.put("timeStamp", System.currentTimeMillis());
        map.put("sign", signApi(map, "123456"));
        String param = JSON.toJSONString(map);
        request.body(param);
        System.out.println("请求参数:" + param);
        request.header("Authorization", token);
        request.setConnectionTimeout(60 * 1000);
        String response = request.execute().body();
        System.out.println("请求结果:" + response);
    }
~~~
﻿
﻿
测试结果:
﻿
~~~
{"message":"微信号不能为空,姓名不能为空","code":900}
~~~
﻿
# 3.常用检查规则注解
﻿
![](https://img2020.cnblogs.com/blog/858186/202101/858186-20210101170015191-387263373.png)
﻿
﻿
~~~
JSR提供的校验注解：         
@Null   被注释的元素必须为 null    
@NotNull    被注释的元素必须不为 null    
@AssertTrue     被注释的元素必须为 true    
@AssertFalse    被注释的元素必须为 false    
@Min(value)     被注释的元素必须是一个数字，其值必须大于等于指定的最小值    
@Max(value)     被注释的元素必须是一个数字，其值必须小于等于指定的最大值    
@DecimalMin(value)  被注释的元素必须是一个数字，其值必须大于等于指定的最小值    
@DecimalMax(value)  被注释的元素必须是一个数字，其值必须小于等于指定的最大值    
@Size(max=, min=)   被注释的元素的大小必须在指定的范围内    
@Digits (integer, fraction)     被注释的元素必须是一个数字，其值必须在可接受的范围内    
@Past   被注释的元素必须是一个过去的日期    
@Future     被注释的元素必须是一个将来的日期    
@Pattern(regex=,flag=)  被注释的元素必须符合指定的正则表达式    
﻿
﻿
Hibernate Validator提供的校验注解：  
@NotBlank(message =)   验证字符串非null，且trim后长度必须大于0    
@Email  被注释的元素必须是电子邮箱地址    
@Length(min=,max=)  被注释的字符串的大小必须在指定的范围内    
@NotEmpty   被注释的字符串的必须非空    
@Range(min=,max=,message=)  被注释的元素必须在合适的范围内
~~~
﻿
﻿
# 4.自定义检查规则注解
﻿
如果这些注解还不能满足我们的需求,那么我么可以自己定义满足自己业务规则的注解
﻿
这里以自定义一个枚举值检查的注解,这个在实际生产中用的非常普遍
﻿
比如在传入用户状态时,只嗯传入-1,0,1或者null,其都是参数不合法的检查注解
﻿
[https://www.cnblogs.com/newAndHui/p/14185807.html](https://www.cnblogs.com/newAndHui/p/14185807.html)
﻿
# 完美!