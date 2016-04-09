---
layout: post
title:  "学习byte buddy 一个字节码修改框架"
author: heipacker
date:   2016-04-02 13:25:58 +0800
categories: jekyll update
tag: 技术
---
  接上一片java agent， 之前只实现了java agent attach到jvm里面去的部分， 但是
  attach进去以后能做的并没有讲，
  上一篇也说了这个java agent具体能做说明， 本篇就举一个例子， 拦截所有的方法
  在每个方法执行时记录一下执行，就是一个执行记录；

  这个主要就是在获取到Instrumentation这个实例以后， 通过Instrumentation.addTransformer方法， 如下：
{% gist heipacker/81183110d73606f4a31b2b0fb8b37b79 %}
然后我们的重点就是实现这个ClassFileTransformer接口了; 这里方法有很多， 你可以简单的实现一下， 如下：
{% gist heipacker/dc219bff58e614a091cf0f989fe28d65 %}
这个实现确实简单， 但是并没有什么很大作用； 所以要想一点其他的方法， 比如可以用asm, cglib, javaassist, jdk proxy
这些东西来修改修改你的字节码什么的，公司里链路跟踪系统我看用的是asm来修改字节码， 这个需要去认真学习一下java的字节码了；
这里就用另外一个框架byte buddy， 这个同事推荐， 而且官方给的性能测试也是相当不错[http://bytebuddy.net/#/tutorial][byte-buddy-benmark]
这里就贴一下具体的实现， 如下：
{% gist heipacker/1cf23e119f625924675f08a61c2d8ff3 %}

{% gist heipacker/c71507842ac2507a87891b4784f88e0e %}
然后就执行下面的，如下:
{% gist heipacker/4439f791e202288c97f70e9c7b271bb3 %}
查看输出了, 如下:
{% gist heipacker/d27a450ffa3cbee5e5ed3246d281d3b2 %}
大家能看到， 在sayHello前面有一行logging， 这个就是在DelagateLogging类里面的logging方法， 
这个方法会在HelloWorld类里面的sayHello方法前执行

  byte buddy这个框架还有很多其他的使用例子， 具体大家看看byte buddy的官网吧, 例子很多，在看byte buddy的时候
看到byte buddy里面对classLoader的处理， 突然就想到这个星期一个同事有一个场景， 就是现在我通过代码自动生成了一个
类文件， 然后编译以后， 这个class文件怎么能够让system classLoader获取lanuch classLoader来加载到呢， 这个一般你是可以
提供一个参数， 然后把这个.class文件生成到指定的文件目录， 比如tomcat里面的webapps/ROOT/WEB-INF/classes/目录下面， 这个
方法没啥问题， 但是这个有点不方便嘛， 还要用户来提供这个目录， 这个不是把自己的实现困难的负担转嫁给用户吗（一位同事说的真理）
, 确实这个负担转嫁给用户了，大功告成， 普天同庆， 可是有没有好一点的方法呢， 今天看到byte buddy的实现确实是有更加优美的方法，
byte buddy用的方法是利用java agent来新增system classLoader/lanuch classLoader的搜索路径，代码如下:
{% gist heipacker/ef641b43b52979f9c2c0320cc83a10d3 %}
这里可以看到， 先是打包.class文件为jar包， 然后调用target注入这个jar包， 这个target的两个实现就是下面的哪两个类加载器(BOOTSTRAP/SYSTEM)
其实内部就是让这两个类加载器， 可以多扫描这个jar， 其实就是相当于把这个jar放到classpath里面去了， 这个方法是不是更完美呢？ 到底是不是就要
看这个的代价了。。。哈哈

具体实例代码:[https://github.com/heipacker/agentTest.git][agent-example]

参考文献:<br/>
1.[http://www.infoq.com/cn/articles/Easily-Create-Java-Agents-with-ByteBuddy][byte-buddy-explain]

[byte-buddy-explain]: http://www.infoq.com/cn/articles/Easily-Create-Java-Agents-with-ByteBuddy
[byte-buddy-benmark]: http://bytebuddy.net/#/tutorial
