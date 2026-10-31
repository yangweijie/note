---
title: "给通过书签给chrome控制台添加jquery支持"
date: 2017-07-10
tags: ["blog"]
summary: "~~~ javascript"
---

~~~ javascript
javascript:(function(){ var jq = document.createElement('script');  jq.src = "http://apps.bdimg.com/libs/jquery/1.8.3/jquery.min.js"; document.getElementsByTagName('head')[0].appendChild(jq);  jQuery.noConflict();})();
~~~
