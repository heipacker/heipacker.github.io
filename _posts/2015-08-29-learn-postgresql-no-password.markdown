---
layout: post
title:  "pg数据库配置无需交互式输入密码连接服务端"
date:   2015-08-29 13:25:58 +0800
categories: jekyll update
tags: 技术
---

&emsp;&emsp;最近在做一个etl导入插件, 因为公司有写部门用了[postgresql]数据库, 这个数据库从mysql被oralce收购以后号称最好的开始数据库。<br/>
<br/>
&emsp;&emsp;大家可以看一下这个他们之间的区别[sqllit-mysql-postgresql]; 我们需要通过psql客户端去连服务端，但是它不像mysql那样输入:<br/>
mysql -h127.0.0.1-udev -p123456 -P 3306 <br/>
postgres它不能直接输入密码，需要交互式的输入：<br/>
psql -U username -h 127.0.0.1 -p 5432 -t -d database<br/>
这个时候你需要手动输入密码, 但是没地方可以输入这个密码， 所以需要搞一个自动的形式,  看了一些postgres数据库，支持这种，发现有两种方法（还有别的方法，希望周知一下）<br/>

第一种：配置一个环境变量PGPASSWORD，这个只需要在执行psql命令之前执行：export PGPASSWORD=password

第二种：配置一个配置文件.pgpass文件，格式像下面这样就行：127.0.0.1:5432:\*:postgres:postgres <br/>

&emsp;&emsp;这种方式需要你去配置一个文件，注意这个需要放在用户主目录下面下，～/.pgpass，还需要注意这个文件的权限，至少当前用户能读取到这个文件吧，这个很容易理解吧;<br/>
还有就是需要权限配成0600，命令：sudo chmod 0600 ~/.pgpass




[sqllit-mysql-postgresql]: http://www.infoq.com/cn/news/2014/04/sqlite-mysql-postgresql
[postgresql]: http://www.postgres.cn/docs/9.3/

