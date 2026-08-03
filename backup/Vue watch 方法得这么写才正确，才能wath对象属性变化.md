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