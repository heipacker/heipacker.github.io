---
layout: post
title:  "collectd源码安装"
author: heipacker
date:   2016-11-20 00:15:58 +0800
categories: jekyll update
tag: 技术,collectd
---
&nbsp;&nbsp;&nbsp;&nbsp;这段时间项目也已经上线了，但是监控方面还是很欠缺，系统一直在裸奔，挂了都不知道，还在睡大觉，所以准备搭建一个监控系统，大概的思路是使用graphite来做后端存储, collectd来做基础数据收集，grafana来做前端监控图的展示, 最终要的就是报警了，准备使用seyren来报警，这篇文件先讲怎么安装collectd。

# 简介:
&nbsp;&nbsp;&nbsp;&nbsp;collectd是一个用来收集系统性能以及提供多种存储方式来存储不同性能值的守护进程。它会周期性统计系统的相关统计信息，并且可以利用这些信息发现当前系统性能的瓶颈和预测系统未来的load。</br>

### 1、安装相关依赖
```
#centos 6.x 32位
rpm -ivh "http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm"
#如果是centos 6.x 64位执行下面命令
#rpm -ivh "http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
yum -y install libcurl libcurl-devel rrdtool rrdtool-devel perl-rrdtool rrdtool-prel libgcrypt-devel gcc make gcc-c++ liboping liboping-devel perl-CPAN net-snmp net-snmp-devel
```

### 2、下载Collectd，并解压、编译和安装
```
wget http://collectd.org/files/collectd-5.4.1.tar.gz
wget http://update.secon.me/collectd-5.4.1.tar.gz
tar zxvf collectd-5.4.1.tar.gz
cd collectd-5.4.1
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --libdir=/usr/lib --mandir=/usr/share/man
make && make install
```

### 3、添加启动脚本和开机启动项
```
#复制启动脚本
cp contrib/redhat/init.d-collectd /etc/init.d/collectd
chmod +x /etc/init.d/collectd
#添加开机启动项
chkconfig --add collectd
chkconfig collectd on
```
### 4、更改配置文件/etc/collectd.conf,以采集CPU、内存、硬盘和网卡流量发送到graphite为例
```
Hostname "BIGLog"

LoadPlugin cpu
LoadPlugin aggregation
LoadPlugin load
LoadPlugin disk
LoadPlugin df
LoadPlugin interface
LoadPlugin memory
LoadPlugin swap
LoadPlugin write_graphite

<Plugin interface>
  IgnoreSelected true
</Plugin>

<Plugin aggregation>
    <Aggregation>
        Plugin "cpu"
        Type "cpu"
        GroupBy "Host"
        GroupBy "TypeInstance"
        CalculateSum true
        CalculateAverage true
    </Aggregation>
</Plugin>

<Plugin df>
  FSType "devtmpfs"
  FSType "tmpfs"
  IgnoreSelected true
  ReportByDevice true
  ReportReserved true
</Plugin>

<Plugin "write_graphite">
 <Node "example">
   Host "sys.biglog.cn"  #graphite地址
   Port "2003"  #graphite的端口号
   Protocol "tcp"
   Prefix "biglog."
   EscapeCharacter "_"
   SeparateInstances true
   StoreRates false
   AlwaysAppendDS false
 </Node>
</Plugin>
```

### 5、启动服务
```
service collectd start
```
