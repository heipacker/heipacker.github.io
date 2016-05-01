---
layout: post
title:  "学习dubbo Consumer启动过程"
author: heipacker
date:   2016-05-02 04:25:58 +0800
categories: jekyll update
tag: 技术,dubbo
---
&nbsp;&nbsp;&nbsp;&nbsp;本文记录本人学习Consumer的启动过程的笔记， 我们从ReferenceBean的实例化讲起，这个ReferenceBean它实现了FactoryBean这个类，<br/>
大家应该知道这个类是spring用来提供实例化bean的一个工厂, 比如我们需要实例化一个类时，<br/>
它可能会有一些前置逻辑，可能你会有很多其他的方法，<br/>
这里提供一个简单点的思路， 你可以实现一下FactoryBean这个类， 然后把这个实现类注入， 然后用@Resource注解就可以拿到了。<br/>
&nbsp;&nbsp;重点讲解一下ReferenceBean的实例化， 看下代码吧:
{% gist heipacker/83ff77e84f4f4e3c451ff740f7c13bd9 %}
这段代码把前面获取配置信息的代码删除了， 大家看下后面的
{% gist heipacker/97f80a179a4c2da166da19227239a25b %}
这里最后调用到了createProxy这个方法
{% gist heipacker/34cca718d82acfc0c57b8e6da6b5f839 %}
这个代码理解起来就有点困难了，首先需要看一下ExtensionLoader的代码，<br/> 
大家可以看下[上一篇文章， dubbo ExtensionLoader加载][learn-dubbo-extension]的分析文章<br/>
重点注意一下上篇文章里面的Protocol$Adaptive生成的适配类中的refer方法， 其实跟export是一样的。
{% gist heipacker/c9936ddba79ad8b61753785c6ecf52e8 %}
还得看下这段代码， 这个是ExtensionLoader里面生成的Cluster的适配类
现在说一下这个createProxy方法里面涉及到consumer启动的大概逻辑， 首先获取每个注册中心的urls， 然后这里面的refprotocol.refer方法获取到Invoker<br/>
这个refer会拿到一个MockClusterInvoker的类，这个类就是一个包装类里面保证DubboInvoker类了， 然后接下来就是cluster.join这个调用， cluster的实现<br/>
就是上面生成的Cluster$Adaptive类了， 看到代码里面会调用默认的failover的Cluster实现，所以最后生成了一个Proxy， 里面默认包装了failover的Cluster<br/>
实现， 里面包装了多个invoker， 这个里面会包含路由， 负载均衡等逻辑。具体的再分析了。上面就是consumer的启动过程了， 主要得理解ExtensionLoader里面的Adaptive逻辑， 整个dubbo的扩展机制都是基于这个ExtensionLoader实现， 所以要了解dubbo， 需要好好研究这个了。


参考文献:<br/>
1.[http://dubbo.io/][dubbo-io]

[learn-dubbo-extension]:http://heipacker.github.io/jekyll/update/2016/04/30/learn-dubbo-extensionLoader.html
[dubbo-io]:http://dubbo.io/
