---
layout: post
title:  "nginx配置auth认证模块"
author: heipacker
date:   2016-09-09 00:45:58 +0800
categories: jekyll update
tag: 技术,nginx,authToken,upload
---
&nbsp;&nbsp;&nbsp;&nbsp;本文记录本人配置auth认证模块所学

# 一.前言
  这段时间工作很忙, 由于工作需要, 我们项目涉及到文件的上传下载, 类似七牛云, 这个就需要一个对接口的
认证机制, 对于web的认证, 用户认证的本质, 用户认证分为会话控制(authentication)和权限控制(authorization)。要实现会话控制，就需要一个身份认证的过程：<br/>
1.客户端提供认证凭证。eg：username password<br/>
2.服务器核对<br/>
3.核对失败则返回失败信息。核对成功则返回成功标识，传统的方式是使用session，设置客户端cookie<br/>
4.客户端请求需要认证的网址。传统的方式是由浏览器自动发送cookie到服务器端，服务器端核对sessionid<br/>

现在基本两个思路:<br/>
## 1.通过session来做认证 ##<br/>
  session的机制的话主要就是利用http的协议了, session基于cookies来实现，每次访问都把特定的cookie
带上. 这种方式现在基本没有了，它的优缺点也都很明显．<br/>
## 2.一个是通过token来认证 ##<br/>
优点：<br/>
*   跨域。ajax设置"Authorization header" and "Bearer<br/>
*   状态无关。天然适合restful services<br/>
*   CDN。 专注api<br/>
*   解耦。token可以随时生成，随处验证<br/>
*   移动适用。移动端cookie支持不好<br/>
*   CSRF。这个需要具体情况具体分析<br/>
*   性能。连接数据库查询session比对token进行解密更费时间<br/>
*   标准化。 JSON WEB TOKEN (JWT) http://jwt.io/
缺点：<br/>
*   对于reftful 客户端， 将其设置成GET或POST参数即可<br/>
*   对于传统web。可存储在cookie里由浏览器自动传送，会有跨域问题<br/>
*   或者存储在localsotrage里, 或者url里，或者放在页面里。需要用js手动取出，拼接到url里。这会加大工作量。适用范围有限<br/>
*   利用"Authorization header" and "Bearer<br/>

# 二.authToken设计：<br/>
token的认证思路:<br/><br/>
  客户端请求nginx对外的接口, 然后nginx-auth-request-module模块, 将token设置到header里面,<br/>
然后auth接口对这个token进行验证, 成功返回200, 失败返回401, 如果返回200则跳转到用户请求的接口, <br/>
如果返回401则，直接返回给用户显示为认证成功.<br/>

token结构:<br/>
  accessKey:sigin:params<br/>
用户端逻辑(用户端通过其他方式获取accessKey, secretKey, 比如注册以后服务端返给用户):<br/>
  accessKey, secretKey, 用户对参数params通过进行编码, 一般是base64, 这个一般不是为了认证, 主要
是为了防止特殊字符, 导致传输过程有问题，然后通过服务端给的secretKey进行一定规则加密，然后凭借成token
的结构, 通过header发生到服务端．<br/>

服务端处理：<br/>
  服务端通过解析token, 获取accessKey获取用户的secretKey, 然后使用相同规则对token里的params进行
签名，然后跟客户端传过来的sign比对, 判断用户是否认证通过．<br/>

# 三.nginx配置:<br/>




参考文献:<br/>
1.[http://www.jianshu.com/p/10fe9aebfed0][http://www.jianshu.com/p/10fe9aebfed0]
2.[http://www.infoq.com/cn/articles/how-to-design-a-good-restful-api][http://www.infoq.com/cn/articles/how-to-design-a-good-restful-api]
3.[https://github.com/perusio/nginx-auth-request-module][https://github.com/perusio/nginx-auth-request-module]
