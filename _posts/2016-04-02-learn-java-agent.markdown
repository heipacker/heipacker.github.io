---
layout: post
title:  "学习java agent"
author: heipacker
date:   2016-04-02 13:25:58 +0800
categories: jekyll update
tag: 技术
---
  这两天看了下java的agent，这个东西功能看起来很高级，功能很多， 比如：<br/>
<ul>
<li>
  1.可以在加载class文件之前做拦截，对字节码做修改;<br/>
</li>
<li>
2.可以在运行期对已加载类的字节码做变更;<br/>
</li>
<li>
3.获取所有已经加载过的类;<br/>
</li>
<li>
4.获取所有已经初始化过的类（执行过clinit方法，是上面的一个子集）;<br/>
</li>
<li>
5.获取某个对象的大小;<br/>
</li>
<li>
6.将某个jar加入到bootstrap classpath里作为高优先级被bootstrapClassloader加载;<br/>
</li>
<li>
7.将某个jar加入到classpath里供AppClassloard去加载;<br/>
</li>
<li>
8.设置某些native方法的前缀，主要在查找native方法的时候做规则匹配;<br/>
</li>
</ul>
这里第一第二条算主要作用，其他的重要性比较低， 因为要做其他的性价比比较低;<br/>
javaagent这个东西主要涉及到jdk里的java.lang.instrument这个包， 还有jdk目录下面的tools.jar这个包；

  agent从字面意思上来理解就是代理用户的一些行为，如果你需要在程序运行前对程序的代码做一些操作， 比如修改字节码，做一些性能检测等， 还可以在运行的时候attach到jdk进程中去， 获取一些程序运行情况， 比如堆的监控， gc的信息； 相信大家在日常的工作中一般出现问题都会去dump一下， 比如jstack的时候就会经常会看到Signal Dispatcher和 Attach Listener线程这连个线程。

javaagent的入口premain或者agentmain， 类似正常java的正常入口main，如下：
{% gist heipacker/2ce631f95e22d1f348a3e10b183ba067 %}
从上面代码里可以看到主要有两种方式：
第一种:程序启动是attach，通过设置vm options 例如：-javaagent:/agent-jar/target/agent-jar-1.0-SNAPSHOT.jar， 这里-javaagent可以有多个， 但是必须放在执行类的前面， 如果放在后面是无效的；
然后就可以在程序中执行下面的程序获取Instrumentation
{% gist heipacker/67240c6bfb28ef783701e017c0c51f00 %}
然后就可以执行下面的代码为所欲为了：
{% gist heipacker/4be207245fc34938891966083d773c3c %}

第二种:程序启动后attach；
第二种就是要用户自己来attach进进程， 如下:
{% gist heipacker/de35ba118e472bc93cb0d6be53981c2e %}
这个需要先获取到进程的pid， 有很多中方法， 随便搞，然后就是将agent-jar.jar包attach进程；然后就可以类似第一种方式的后续操作；
先获取Instrumentation， 然后就可以修改字节码啊，插入一些日志， 性能测试代码等等；

能看到两种方式都是为了获取到java.lang.instrument.Instrumentation这个类， 用户能做的也都是操作这个类来做的，这里具体的api大家可以找找这个类的api接口,也可以看看下面贴的代码， 还有很多具体的代码待完善哈。

例子:[https://github.com/heipacker/agentTest.git][agent-example]

参考文献:<br/>
1.[http://www.infoq.com/cn/articles/javaagent-illustrated][javaagent-illustrated]<br/>
2.[http://nijiaben.iteye.com/blog/1846595][nijiaben.iteye]

[javaagent-illustrated]: http://www.infoq.com/cn/articles/javaagent-illustrated
[agent-example]: https://github.com/heipacker/agentTest.git
[nijiaben.iteye]: http://nijiaben.iteye.com/blog/1846595
