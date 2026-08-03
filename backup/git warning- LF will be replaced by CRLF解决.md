初始化自己项目的时候，出现了N+个warning: LF will be replaced by CRLF，

git config --global core.autocrlf false

参考：http://stackoverflow.com/questions/1967370/git-is-saying-lf-will-be-replaced-by-crlf

看来存入缓存的时候，不同的操作系统文件结尾返回不一样，所以的CRLF会被替换为LF。但在取出的时候会被转换回CRLF,潜在的危险是二进制的改变·所以还是留为true吧。