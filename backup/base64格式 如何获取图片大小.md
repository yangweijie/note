
今天 微信群友问了一句 base64格式 如何获取图片大小，我想了下 有个`getimagesizefromstring` 函数 可以获取，让他看手册，结果他说能不能不存获取。我想可以啊，就自己封装了个函数 实验了下。可以

~~~php
function get_img_info_from_base64($base64_image_content){
    if (preg_match('/^(data:\s*image\/(\w+);base64,)/', $base64_image_content, $result)){
        $file_content = base64_decode(str_replace($result[1], '', $base64_image_content));
        return getimagesizefromstring($file_content);
    }else{
        return false;
    }
}

~~~

测试

~~~php
 public function test_base64_img_info(){
        $image_file = 'https://www.baidu.com/img/bd_logo1.png';
        $image_info = getimagesize($image_file);
        $base64_image_content = "data:{$image_info['mime']};base64," . chunk_split(base64_encode(file_get_contents($image_file)));
        $ret = get_img_info_from_base64($base64_image_content);
        return json($ret);
    }

~~~

如果是文件存储大小，strlen一下个那个file_content 就行了，我拿百度logo测试了一下 7877 一样的。