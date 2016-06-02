---
layout: post
title:  "启动opentsdb"
author: heipacker
date:   2016-05-26 00:45:58 +0800
categories: jekyll update
tag: 技术,opentsdb,hbase,hadoop
---
&nbsp;&nbsp;&nbsp;&nbsp;本文记录本人学习安装opentsdb的笔记


如果要安装opentsdb， 首先就的看看官网咯[安装文档][opentsdb-install],<br/>
这里说了安装前提：<br/>
1.A Linux system<br/>
2.Java Runtime Environment 1.6 or later<br/>
3.HBase 0.92 or later<br/>
4.GnuPlot 4.2 or later<br/>
没啥说的， 第三步参考[hbase安装][hbase-install]， 当然安装hbase也有前提， hadoop，zk啊这些， 文档都很齐全，参考一下就行了。<br/>
<br/>
然后就是安装了， 这里有几种方式可以安装，从tar.gz包来安装， 从deb来安装， 从source来安装<br/>
这里主要讲一下从source安装<br/>
<br/>
到制定目录(/home/heipacker/IdeaProjects/)执行<br/>
git clone https://github.com/OpenTSDB/opentsdb.git<br/>

然后cd到opentsdb目录<br/>
执行<br/>
./build.sh<br/>
<br/>
这个你可能需要安装autoconf这个工具， 一般sudo apt-get install autoconf就行， 然后继续./build.sh<br/>
<br/>
安装完以后你会发现有一个build文件夹, cd进去, 会发现有一个tsdb文件<br/>
然后执行./build/tsdb这个命令， 不过这个命令有一些参数需要填写， 可以用下面的命令<br/>
./build/tsdb tsd<br/>
当然执行了这个命令后， 你会发现并未卵<br/>
会报没有其他的什么文件啥的， 这个你就的找到./src/opentsdb.conf这个文件了， 配置一下里面的参数:<br/>
tsd.http.cachedir - Path to write temporary files to<br/>
tsd.http.staticroot - Path to the static GUI files found in ./build/staticroot<br/>
tsd.storage.hbase.zk\_quorum - If HBase and Zookeeper are not running on the same machine, specify the host and port here.<br/>
主要配置这个就行了([完整的参数配置][all-config])<br/>

tsdtmp=${TMPDIR-'/tmp'}/tsd    # For best performance, make sure<br/>
mkdir -p "$tsdtmp"             # your temporary directory uses tmpfs<br/>
./build/tsdb tsd --port=4242 --staticroot=build/staticroot --cachedir="$tsdtmp" --zkquorum=localhost:2181<br/>
你也可以直接执行上面这个命令指定具体的参数， 然后你可能会发现/var/log/opentsdb文件夹不存在什么的， 这个就自己去创建一下<br/>
启动以后就可以看看界面了， 不过好像不对哈， 还没有创建hbase表呢。。。。<br/>
env COMPRESSION=NONE HBASE\_HOME=/home/heipacker/software/hbase-1.2.1 ./src/create\_table.sh<br/>
把表创建后就可以启动了。。。， 然后查看页面<br/>
http://127.0.0.1:4242/<br/>
然后就可以看图了， 如下：<br/>
![]({{ site.img_url }}/opentsdb-ui-screenshot.png)

到这里就可以了，这里你如果想看图的话的安装一下tcollector来采集数据， 还得安装GnuPlot这个来展示图， 这里主要想集成grafana所以这个GnuPlot大家自己去装咯。。。 下一篇讲讲怎么集成grafana图形界面。

参考文献:<br/>
1.[http://opentsdb.net/docs/build/html/installation.html#compiling-from-source][opentsdb-install]
2.[http://hbase.apache.org/book.html#quickstart_pseudo][hbase-install]
3.[http://opentsdb.net/docs/build/html/user_guide/configuration.html][all-config]

[opentsdb-install]:http://opentsdb.net/docs/build/html/installation.html#compiling-from-source
[hbase-install]:http://hbase.apache.org/book.html#quickstart_pseudo
[all-config]:http://opentsdb.net/docs/build/html/user_guide/configuration.html
