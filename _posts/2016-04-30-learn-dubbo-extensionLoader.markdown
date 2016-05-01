---
layout: post
title:  "学习dubbo ExtensionLoader"
author: heipacker
date:   2016-04-30 12:25:58 +0800
categories: jekyll update
tag: 技术,dubbo
---
&nbsp;&nbsp;这个的作用就是来加载用户指定的类实现， 你给一个接口， 然后它给你换行你需要的实现。


&nbsp;&nbsp;&nbsp;&nbsp;说到extensionLoader, 肯定需要先说一下jdk里面自带这一个类似的东西， [ServiceLoader][serviceLoader-html]， 它的作用就是用来获取扩展的类， 举个例子： 我需要做一个读取远程文本的工具， 这个开始我只需要读取远程数据库里面的文本， 这个时候我， 会写一个接口RemoteLoader：
{% gist heipacker/8fd594ef7dbdbd86441f07fcabac717b  %}
&nbsp;&nbsp;然后再实现一个读取远程数据库的文本的RemoteDbLoader:
{% gist heipacker/5668b74a0b151ee8b0a52619c1794e9f  %}
&nbsp;&nbsp;这样用的时候new RemoteDbLoader()就行了， 如果这个时候产品告诉你还有一个从hadoop里面都文本的需求， 你又再实现一个RemoteHadoopLoader， 然后new一个， 用过spring的人可能会在这些实现上加一个@Service注解， 然后通过applicationContext.getBean(), 就能很爽的拿到想拿到的类实现了， 但是如果我不用spring呢， 这可怎么办， 这个时候简单一点自己实现一个类似spring的东西就行了（哈， 好简单啊）， 其实你可以更简单一点直接用java.util.ServiceLoader来获取， 要知道你遇到的问题sun的兄弟们早就遇到了， javaee里面很多设计都这个样子， 但是用的兄弟都会发现这个java.util.ServiceLoader实现的还是有点粗糙的， 比如：
1.它会把所有的都实例化了， 计算你没用到。。。
{% gist heipacker/32c7af1530f47d85c935b35c254c2b60  %}
&nbsp;&nbsp;你可以看到它返回的是一个ServiceLoader， 然后你要获取那个Class的话你还要用迭代器去拿， 所以没用到的都实例化了， 这个对那些实例化代价比较高的就有点难接受了。
2.它没法根据一个实现来获取具体的实现实例，比如我在上例中要获取Db的实现是不行的。。。跪了。
3.没法依赖注入， 比如A-->B, B-->C这种没法一次搞定。 需要自己编码在B实例化逻辑里加上依赖C。
可能还有被的不好用的地方， 但从另外一个角度想， 这个是sun搞的， 他们是最底层的角度， 做到这个份已经差不多了， 你还要人家给你来点具体的场景，估计最后就你用了。。别人没法用。


----------
----------


&nbsp;&nbsp;&nbsp;&nbsp;再来说ExtensionLoader这个dubbo里面的类似实现；这个的实现跟ServiceLoader类似， 除了可以从META-INF/services/读取还可以从多个目录读取扩展配置（META-INF/dubbo/, META-INF/dubbo/internal/）, 它会根据你的需要再去实例化， 不会想ServiceLoader那样都实例化， 基本上把上面提的一些缺点给解决了。
{% gist heipacker/f6fbe78e05bc32f35866a7e08fe27801  %}
&nbsp;&nbsp;上面是它最后获取到指定Class实现的逻辑， 可以看到它实例化以后还会做一些其他的事情injectExtension； 再来看这个方法
{% gist heipacker/62144005fe550b70c236fb78417acf97  %}
&nbsp;&nbsp;可以看到， 就是找set\*方法， 把属性名作为name用getExtension去获取扩展， 递归实例化。
做完injectExtension以后， 继续做wraper, 从cachedWrapperClasses里面获取所有wrapper包装当前instance； 然后返回。
这里看一下如何找到wrapperClasses的， 看下面代码：
{% gist heipacker/92c680b47746ae9801fdd4ba85bece31  %}
通过构造函数是不是只有一个当前type来判断这个是不是一个wrapper类。
&nbsp;&nbsp;&nbsp;&nbsp;再看一下ExtensionLoader里面的getAdaptiveExtension方法， 这个方法是用获取，这个方法主要是用来做适配的，做适配<br/>
大家都知道啥意思， 但是这个地方为啥要做适配呢， 开始一看不知道为啥， 我们看一下它干了什么
{% gist heipacker/6361f72f0cf5c724511dbc1f70a80a7e %}
再看一下createAdaptiveExtension方法干了什么
{% gist heipacker/cc8c0a46e138fc9be5cb6bf0d03e08e5 %}
可以看到， 这里会先调用getAdaptiveExtensionClass方法， 从字面意思就是获取自适应扩展的类Class， 然后调用newInstance，然后就是调用injectExtension<br/>
这里injectExtension方法我们上面讲过， 主要就是这个获取自适应扩展类的Class方法， 它干了什么呢， 同样看一下代码：
{% gist heipacker/0661db830334b9dfca31c9b53fdb86e3 %}
可以看到最后调用到了createAdaptiveExtensionClassCode这个方法来生成AdaptiveExtensionClass， 再看下它干了什么
{% gist heipacker/4cddcf739bc3de6369784bfddc03130d %}
这个代码有点长(这帮同志就不能把方法写短一点吗。。。。)， 删了一些， 要看详细的自己看代码吧， 代虽然很长，但是就做了一下wrap， 然后调用JavaCompiler去编译这段代码，看下它生成的代码:
{% gist heipacker/e1c1448122b77d513d267cba2c665696 %}
到这里就很明白了， 就是里面再去调用ExtensionLoader.getExtension, 这个作用就是把实例化的代价再延迟到你真正去调用方法的时候，看到这里是不是会觉得dubbo的代码还是很精髓的。。。这个比java.util.ServiceLoader有进一步优化了一下延迟加载了。


参考文献:<br/>
1.https://docs.oracle.com/javase/7/docs/api/java/util/ServiceLoader.html
2.http://dubbo.io/

[serviceLoader-html]:https://docs.oracle.com/javase/7/docs/api/java/util/ServiceLoader.html
