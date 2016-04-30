---
layout: post
title:  "学习dubbo ExtensionLoader"
author: heipacker
date:   2016-04-30 12:25:58 +0800
categories: jekyll update
tag: 技术,dubbo
---
这个的作用就是来加载用户指定的类实现， 你给一个接口， 然后它给你换行你需要的实现。


说到extensionLoader, 肯定需要先说一下jdk里面自带这一个类似的东西， [ServiceLoader][serviceLoader-html]， 它的作用就是用来获取扩展的类， 举个例子： 我需要做一个读取远程文本的工具， 这个开始我只需要读取远程数据库里面的文本， 这个时候我， 会写一个接口RemoteLoader：
{% gist heipacker/8fd594ef7dbdbd86441f07fcabac717b  %}
然后再实现一个读取远程数据库的文本的RemoteDbLoader:
{% gist heipacker/5668b74a0b151ee8b0a52619c1794e9f  %}
这样用的时候new RemoteDbLoader()就行了， 如果这个时候产品告诉你还有一个从hadoop里面都文本的需求， 你又再实现一个RemoteHadoopLoader， 然后new一个， 用过spring的人可能会在这些实现上加一个@Service注解， 然后通过applicationContext.getBean(), 就能很爽的拿到想拿到的类实现了， 但是如果我不用spring呢， 这可怎么办， 这个时候简单一点自己实现一个类似spring的东西就行了（哈， 好简单啊）， 其实你可以更简单一点直接用java.util.ServiceLoader来获取， 要知道你遇到的问题sun的兄弟们早就遇到了， javaee里面很多设计都这个样子， 但是用的兄弟都会发现这个java.util.ServiceLoader实现的还是有点粗糙的， 比如：
1.它会把所有的都实例化了， 计算你没用到。。。
{% gist heipacker/32c7af1530f47d85c935b35c254c2b60  %}
你可以看到它返回的是一个ServiceLoader， 然后你要获取那个Class的话你还要用迭代器去拿， 所以没用到的都实例化了， 这个对那些实例化代价比较高的就有点难接受了。
2.它没法根据一个实现来获取具体的实现实例，比如我在上例中要获取Db的实现是不行的。。。跪了。
3.没法依赖注入， 比如A-->B, B-->C这种没法一次搞定。 需要自己编码在B实例化逻辑里加上依赖C。
可能还有被的不好用的地方， 但从另外一个角度想， 这个是sun搞的， 他们是最底层的角度， 做到这个份已经差不多了， 你还要人家给你来点具体的场景，估计最后就你用了。。别人没法用。


----------


再来说ExtensionLoader这个dubbo里面的类似实现；这个的实现跟ServiceLoader类似， 除了可以从META-INF/services/读取还可以从多个目录读取扩展配置（META-INF/dubbo/, META-INF/dubbo/internal/）, 它会根据你的需要再去实例化， 不会想ServiceLoader那样都实例化， 基本上把上面提的一些缺点给解决了。
{% gist heipacker/f6fbe78e05bc32f35866a7e08fe27801  %}
上面是它最后获取到指定Class实现的逻辑， 可以看到它实例化以后还会做一些其他的事情injectExtension； 再来看这个方法
{% gist heipacker/62144005fe550b70c236fb78417acf97  %}
可以看到， 就是找set\*方法， 把属性名作为name用getExtension去获取扩展， 递归实例化。
做完injectExtension以后， 继续做wraper, 从cachedWrapperClasses里面获取所有wrapper包装当前instance； 然后返回。
这里看一下如何找到wrapperClasses的， 看下面代码：
{% gist heipacker/92c680b47746ae9801fdd4ba85bece31  %}
通过构造函数是不是只有一个当前type来判断这个是不是一个wrapper类。

参考文献:<br/>
1.https://docs.oracle.com/javase/7/docs/api/java/util/ServiceLoader.html
2.http://dubbo.io/

[serviceLoader-html]:https://docs.oracle.com/javase/7/docs/api/java/util/ServiceLoader.html
