xstream 基本用法是对应类对象 转为xml
但是 不支持  `<a href="">aa</a>`  这种(我需要的是<p><img wi=""/></p>)。
找了半天说要用转换器

```
package com.paizhi.component.utils.cpc.entity.coventor;

import com.paizhi.component.utils.cpc.entity.xml.img;
import com.paizhi.component.utils.cpc.entity.xml.p;
import com.thoughtworks.xstream.converters.Converter;
import com.thoughtworks.xstream.converters.MarshallingContext;
import com.thoughtworks.xstream.converters.UnmarshallingContext;
import com.thoughtworks.xstream.io.HierarchicalStreamReader;
import com.thoughtworks.xstream.io.HierarchicalStreamWriter;

public class PConventor implements Converter{
    //定义转换器能转换的JavaBean类型
    @Override
    public boolean canConvert(Class type) {
        return type.equals(p.class);
    }

    //把对象序列化成XML或JSON
    @Override
    public void marshal(Object value, HierarchicalStreamWriter writer, MarshallingContext context) {
        p p = (p) value;
//        writer.startNode("p");
        writer.addAttribute("id", p.getId());
        writer.addAttribute("num", p.getNum().toString());

        // 文字
        if(p.getImg() == null){
            writer.addAttribute("Italic", "0");
            writer.setValue(p.getValue());
        }else{
            img img = p.getImg();
             String newImgStr = imgStr.format("<img wi=\"%s\" he=\"%s\" file=\"%s\" img-format=\"jpg\" img-content=\"drawing\" orientation=\"%s\" inline=\"no\"/>",
                img.getWi(),
                img.getHe(),
                img.getFile(),
                img.getOrientation()
            );
            writer.setValue(newImgStr);
        }
//        writer.endNode();
    }

    //把XML或JSON反序列化成对象
    @Override
    public Object unmarshal(HierarchicalStreamReader reader, UnmarshallingContext context) {
        return null;
    }
}

```
于是写了个转换器
开始想的是用setValue 来将img节点当字符串设为p节点的值。
万万没想到 输出的时候 给我转义了。

后来就想着怎么不转义。
试了几种都不行。

后来发现 转换器里 可以 写字节点。多写几对 startNode endNode 就行了。 一个不写 就是给当前节点加属性 设值。

```
    //把对象序列化成XML或JSON
    @Override
    public void marshal(Object value, HierarchicalStreamWriter writer, MarshallingContext context) {
        p p = (p) value;
//        writer.startNode("p");
        writer.addAttribute("id", p.getId());
        writer.addAttribute("num", p.getNum().toString());

        // 文字
        if(p.getImg() == null){
            writer.addAttribute("Italic", "0");
            writer.setValue(p.getValue());
        }else{
            img img = p.getImg();
            writer.startNode("img");
            writer.addAttribute("wi", img.getWi().toString());
            writer.addAttribute("he", img.getHe().toString());
            writer.addAttribute("file", img.getFile());
            writer.addAttribute("img-format", "jpg");
            writer.addAttribute("img-content", "drawing");
            writer.addAttribute("orientation", img.getOrientation());
            writer.addAttribute("inline", "no");
            writer.endNode();
        }
//        writer.endNode();
    }
```
