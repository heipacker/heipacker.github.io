---
layout: post
title:  "单机版pinpoint部署"
date:   2016-04-07 13:25:58 +0800
categories: jekyll update
tags: 技术
---

[https://github.com/naver/pinpoint][pinpoint-git]<br/>

这个主要用来查看系统性能， 及服务的一些运行状态， 当前服务调用情况等（盗图一张）
 ![]({{ site.img_url }}/ss_server-map.png)
1.现在有一个单击版的pinpoint， 在127.0.0.1机器上面， 

2.启动步骤：

Download & Start - Run quickstart/bin/start-hbase.sh

Initialize Tables - Run quickstart/bin/init-hbase.sh

Collector - Run quickstart/bin/start-collector.sh

Web UI - Run quickstart/bin/start-web.sh

TestApp - Run quickstart/bin/start-testapp.sh

查看：
Web UI - http://127.0.0.1:28080
TestApp - http://127.0.0.1:28081
Stopping
HBase - Run quickstart/bin/stop-hbase.sh

Collector - Run quickstart/bin/stop-collector.sh

Web UI - Run quickstart/bin/stop-web.sh

TestApp - Run quickstart/bin/stop-testapp.sh

应用接入pinpoint

将这个pinpoint-agent.tar.gz 解压到/home/fupan/pinpoint-agent

配置pinpoint.config中的collector

profiler.collector.ip=127.0.0.1(这里最好配置成你本机在局域网里的ip)

设置环境变量vim /etc/profile

追加export AGENT\_PATH=/home/fupan/pinpoint-agent

source /etc/profile

配置cmd:

-javaagent:$AGENT\_PATH/pinpoint-bootstrap-1.5.2-SNAPSHOT.jar -Dpinpoint.agentId=testApp-agent -Dpinpoint.applicationName=uidApp

启动应用即可

[pinpoint-git]: https://github.com/naver/pinpoint
