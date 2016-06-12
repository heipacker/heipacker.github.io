---
layout: post
title:  "整合grafana， opentsdb"
author: heipacker
date:   2016-06-11 00:45:58 +0800
categories: jekyll update
tag: 技术,opentsdb,hbase,hadoop,grafana
---
&nbsp;&nbsp;&nbsp;&nbsp;本文记录本人学习整合grafana， opentsdb的笔记


前面一片学习了， 如何安装启动opentsdb， 这个主要是用来存储时间序列的监控数据的， 展示的话它也自带了一个<br/>
不过看起来还是挺难看的嘛。。。这个时候就要找一个好看点的嘛， 毕竟好美之心人皆有之！！！
这里就介绍一下如何用grafana这个很火的监控展示前端来展示opentsdb的监控数据

## 安装grafana:</br>
[http://docs.grafana.org/installation/debian/][grafana-download]到这里下载grafana的二进制安装包
![]({{ site.img_url }}/grafana_download.png)

tar -zxvf grafana*.tar.gz
这个时候到conf/目录下面吧default.ini配置文件相应的配置一下， 这里主要就是配置一些文件目录， 还有注意一下目录权限啥的。<br/>

这个时候就可以执行启动命令了， ./bin/grafana-server
![]({{ site.img_url }}/grafana_start_log.png)

然后就可以打开浏览器， 访问http://0.0.0.0:3000
![]({{ site.img_url }}/grafana_home_page.png)
这里默认的登录密码都是admin， 直接登录就行了

然后你会看到一个像这样的页面:
![]({{ site.img_url }}/grafana_home.png)

## 配置opentsdb:<br/>
这个时候需要把opentsdb的监控数据在这里展示出来， 你需要配置一个opentsdb数据源, 按照下面两个图来就行了
![]({{ site.img_url }}/grafana_config_datasource.png)

![]({{ site.img_url }}/grafana_config_datasource_opentsdb.png)
		
## 配置dashborad:<br/>
这样完事以后， 你需要创建一个dashboard
![]({{ site.img_url }}/grafana_setting.png)
然后你可以看ADD ROW的按钮， 你也可以看到左边有一个可以点击的东西
![]({{ site.img_url }}/grafana_config_start.png)

然后看下面这张图
![]({{ site.img_url }}/grafana_config_opentsdb.png)
选中opentsdb就行， 然后在上面的Graph里面点击Metrics
在这里就可以配置具体展示那个指标了(这里你要保证已经有指标了， 可以参照[上一篇文章][opentsdb-install])， 好了， 到这里配置结束了， 看下组后的效果图（这里有很多插件， 可以把你的这个borad搞得再漂亮点）
![]({{ site.img_url }}/grafana_last.png)

## 最后:<br/>
现在已经可以看监控了， 但是这个还是不好是吧， 因为你得去一个一个的配置每个指标， 这个需要好用还是要自己对这个grafana进行二次开发啥的， 比如左边用<br/>
树结构来展示你的指标， 再提供一个查询功能那就相当不错咯。。。然后把一些不要的东西去掉就行。。。

后面讲讲怎么搞报警， 毕竟如果只有监控没有报警那还要这个系统干毛线啊。。。。
		

参考文献:<br/>
1.[http://opentsdb.net/docs/build/html/installation.html#compiling-from-source][opentsdb-install]
2.[http://docs.grafana.org/installation/debian/][grafana-download]

[opentsdb-install]:http://heipacker.github.io/jekyll/update/2016/05/25/install-opentsdb.html
[grafana-download]:http://docs.grafana.org/installation/debian/
