---
title: "Vue watch 方法得这么写才正确，才能wath对象属性变化"
date: 2017-07-10
tags: ["blog", "javascript", "vue"]
summary: "js"
---

``` js
var app = new Vue({
    el: '#app',
    data: {
        form: {
            param: {
                cleanup: false,
                useInlineStylesBlock: false,
                stripOriginalStyleTags: false,
                excludeMediaQueries: true,
                excludeConditionalInlineStylesBlock: true,
            },
            style: '',
            content: '',
        },
        afterParse:''
    },
    watch: {
        form: {
            handler:function (newVal, oldVal) {
                    axios.post($('[name=form]').attr('action'), {
                        param:this.form
                    })
                    .then(function (response) {
                        this.afterParse = response;
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('网络出错了');
                    });
                },
                deep:true
        }
    }
})  
```
