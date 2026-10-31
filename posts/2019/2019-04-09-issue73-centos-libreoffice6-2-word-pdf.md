---
title: "centos 安装最新libreoffice6.2 来进行word转pdf"
date: 2019-04-09
tags: []
summary: "源码安装python3.6"
---

# 源码安装python3.6
## 安装setuptools 和pip3

python3 setup.py build
python3 setup.py install

https://www.cnblogs.com/wenchengxiaopenyou/p/5709218.html

# 卸载旧版本libreoffice

1、卸载系统当前的libreoffice
执行如下命令：sudo yum erase libreoffice\*（centos、ubuntu均有效）
或者尝试：sudo yum remove libreoffice-*（未能成功）

2. libreoffice 下载

LibreOffice_6.2.2_Linux_x86-64_rpm.tar.gz
LibreOffice_6.2.2_Linux_x86-64_rpm_sdk.tar.gz
LibreOffice_6.2.2_Linux_x86-64_rpm_langpack_zh-CN.tar.gz
cd /usr/libreoffice/LibreOffice_6.0.3_Linux_x86-64_rpm/RPMS

yum localinstall *.rpm

3. 安装一些库
yum -y groupinstall Development tools
yum -y install cairo 
yum -y install libSM 
yum install ibus
yum install libreoffice-headless

 version `GLIBC_2.14' not found (required by /opt/libreoffice6.2/program/libpython3.5m.so.1.0

参考 ：http://get.ftqq.com/9143.get

linux系统下的缺失 libstdc++.so.6: version’GLIBCXX_3.4.20’的问题
参考：http://get.ftqq.com/9144.get

/lib64/libdbus-1.so.3: no version information available
同上：
Connector : couldn't connect to socket (Connection refused)


 libsystemd.so.0: cannot open shared object file
