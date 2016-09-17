---
layout: post
title:  "nginx配置auth认证模块"
author: heipacker
date:   2016-09-09 00:45:58 +0800
categories: jekyll update
tag: 技术,nginx,authToken,upload
---
&nbsp;&nbsp;&nbsp;&nbsp;本文记录本人配置auth认证模块了解的知识点, 这里记录一下。

# 一.前言
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这段时间工作很忙, 由于工作需要, 我们项目涉及到文件的上传下载, 类似七牛云, 这个就需要一个对接口的
认证机制, 对于web的认证, 用户认证的本质, 用户认证分为会话控制(authentication)和权限控制(authorization)。要实现会话控制，就需要一个身份认证的过程：<br/>
1.客户端提供认证凭证。eg：username password<br/>
2.服务器核对<br/>
3.核对失败则返回失败信息。核对成功则返回成功标识，传统的方式是使用session，设置客户端cookie<br/>
4.客户端请求需要认证的网址。传统的方式是由浏览器自动发送cookie到服务器端，服务器端核对sessionid<br/>

## 现在基本两个思路:<br/>
### 1.通过session来做认证<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;session的机制的话主要就是利用http的协议了, session基于cookies来实现，每次访问都把特定的cookie
带上. 这种方式现在基本没有了，它的优缺点也都很明显．<br/>
### 2.一个是通过token来认证 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token的机制有很多介绍的文章,大家自己去搜下看看。
优点：<br/>
*   跨域; ajax设置"Authorization header" and "Bearer<br/>
*   状态无关; 天然适合restful services<br/>
*   CDN; 专注api<br/>
*   解耦; token可以随时生成，随处验证<br/>
*   移动适用; 移动端cookie支持不好<br/>
*   CSRF; 这个需要具体情况具体分析<br/>
*   性能; 连接数据库查询session比对token进行解密更费时间<br/>
*   标准化; JSON WEB TOKEN (JWT) http://jwt.io/
缺点：<br/>
*   对于reftful 客户端， 将其设置成GET或POST参数即可<br/>
*   对于传统web; 可存储在cookie里由浏览器自动传送，会有跨域问题<br/>
*   或者存储在localsotrage里, 或者url里，或者放在页面里。需要用js手动取出，拼接到url里。这会加大工作量。适用范围有限<br/>
*   利用"Authorization header" and "Bearer"<br/>

# 二.authToken设计：<br/>
token的认证思路:<br/><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;客户端请求nginx对外的接口, 然后nginx-auth-request-module模块, 将token设置到header里面,<br/>
然后auth接口对这个token进行验证, 成功返回200, 失败返回401, 如果返回200则跳转到用户请求的接口, <br/>
如果返回401则，直接返回给用户显示为认证成功.<br/>

token结构:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;accessKey:sigin:params<br/>
客户端逻辑(客户端通过其他方式获取accessKey, secretKey, 比如注册以后服务端返给用户):<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;accessKey, secretKey, 用户对参数params通过进行编码, 一般是base64, 这个一般不是为了认证, 主要
是为了防止特殊字符, 导致传输过程有问题，然后通过服务端给的secretKey进行一定规则加密，然后凭借成token
的结构, 通过header发生到服务端．<br/>

服务端处理：<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;服务端通过解析token, 获取accessKey获取用户的secretKey, 然后使用相同规则对token里的params进行
签名，然后跟客户端传过来的sign比对, 判断用户是否认证通过．<br/>

# 三.nginx安装:<br/>
<p>安装过程写了个脚本:</p>
<pre><code>
# -*- coding: utf-8 -*-

import os
import sys

if __name__ == '__main__':
	cur_dir = os.getcwd()
	os.system('wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.39.tar.gz && tar -zxf pcre-8.39.tar.gz && cd pcre-8.39 && ./configure && make && sudo make install && cd ../')
	# install zlib lib
	os.system('wget http://zlib.net/zlib-1.2.8.tar.gz && tar -zxf zlib-1.2.8.tar.gz && cd zlib-1.2.8 && ./configure && make && sudo make install && cd ../')
	# install openSsl lib
	os.system('wget http://www.openssl.org/source/openssl-1.0.2f.tar.gz && tar -zxf openssl-1.0.2f.tar.gz && cd openssl-1.0.2f && ./config --prefix=/usr && make && sudo make install && cd ../')
	# install upload lib
	os.system('wget https://github.com/vkholodkov/nginx-upload-module/archive/2.2.zip && mv 2.2.zip nginx-upload-module-2.2.zip && unzip nginx-upload-module-2.2.zip && cd ../')

	os.system('wget https://github.com/perusio/nginx-auth-request-module/archive/master.zip && unzip master.zip && mv nginx-auth-request-module-master nginx-auth-request-module && cd ../')
	# install nginx
	os.system('wget https://nginx.org/download/nginx-1.11.1.tar.gz && tar -zxvf nginx-1.11.1.tar.gz && ln -s nginx-1.11.1 nginx && cd nginx && mkdir 3party_module && cd 3party_module && touch config && cd ../')
	os.system('./configure --sbin-path=' + cur_dir + '/nginx/nginx --conf-path=' + cur_dir + '/nginx/conf/nginx.conf --pid-path=' + cur_dir + '/nginx/nginx.pid --with-pcre=../pcre-8.39 --with-zlib=../zlib-1.2.8 --with-threads --with-file-aio --with-http_v2_module --with-http_gzip_static_module --with-http_slice_module --with-stream --add-module=' + cur_dir + '/nginx-upload-module-2.2 --add-module=' + cur_dir + '/nginx-auth-request-module --add-dynamic-module=' + cur_dir + '/nginx/3party_module && make && sudo make install')
	os.system('mkdir -p logs')
	os.system('./nginx')
	print 'done'
	sys.exit(0)
</code></pre>

# 四.nginx配置:<br/>
<p>下面是nginx的配置信息:</p>

<pre><code>

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
	worker_connections  1024;
}


http {
	include       mime.types;
	default_type  application/octet-stream;

#log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
#                  '$status $body_bytes_sent "$http_referer" '
#                  '"$http_user_agent" "$http_x_forwarded_for"';

#access_log  logs/access.log  main;

	sendfile        on;
#tcp_nopush     on;

#keepalive_timeout  0;
	keepalive_timeout  65;

#gzip  on;

	server {
		listen       80;
		server_name  192.168.62.102;

#charset koi8-r;

#access_log  logs/host.access.log  main;

		client_max_body_size 500m;

		location / {
			root   html;
			index  index.html index.htm;
		}

# Upload form should be submitted to this location
		location /cloudservice {
# Pass altered request body to this location
			upload_pass   /v1/cloudservice;
			upload_resumable	on;
			upload_pass_args	on;

# Store files to this directory
# The directory is hashed, subdirectories 0 1 2 3 4 5 6 7 8 9 should exist
			upload_store /data/nginx_data 1;

			upload_state_store /data/nginx_data/state 1;

# Allow uploaded files to be read only by user
			upload_store_access user:r;

# Set specified fields in request body
			upload_set_form_field $upload_field_name.name "$upload_file_name";
			upload_set_form_field $upload_field_name.content_type "$upload_content_type";
			upload_set_form_field $upload_field_name.path "$upload_tmp_path";

# Inform backend about hash and size of a file
			upload_aggregate_form_field "$upload_field_name.md5" "$upload_file_md5";
			upload_aggregate_form_field "$upload_field_name.size" "$upload_file_size";

			upload_pass_form_field "^submit$|^description$";

			upload_cleanup 400 404 499 500-505;
		}

# Pass altered request body to a backend
		location /v1/cloudservice {
			proxy_pass   http://192.168.62.107:9909/v1/cloudservice/file/;
		}
#error_page  404              /404.html;

# redirect server error pages to the static page /50x.html
#
		error_page   500 502 503 504  /50x.html;
		location = /50x.html {
			root   html;
		}

# proxy the PHP scripts to Apache listening on 127.0.0.1:80
#
#location ~ \.php$ {
#    proxy_pass   http://127.0.0.1;
#}

# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
#
#location ~ \.php$ {
#    root           html;
#    fastcgi_pass   127.0.0.1:9000;
#    fastcgi_index  index.php;
#    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
#    include        fastcgi_params;
#}

# deny access to .htaccess files, if Apache's document root
# concurs with nginx's one
#
#location ~ /\.ht {
#    deny  all;
#}
	}


# another virtual host using mix of IP-, name-, and port-based configuration
#
#server {
#    listen       8000;
#    listen       somename:8080;
#    server_name  somename  alias  another.alias;

#    location / {
#        root   html;
#        index  index.html index.htm;
#    }
#}


# HTTPS server
#
#server {
#    listen       443 ssl;
#    server_name  localhost;

#    ssl_certificate      cert.pem;
#    ssl_certificate_key  cert.key;

#    ssl_session_cache    shared:SSL:1m;
#    ssl_session_timeout  5m;

#    ssl_ciphers  HIGH:!aNULL:!MD5;
#    ssl_prefer_server_ciphers  on;

#    location / {
#        root   html;
#        index  index.html index.htm;
#    }
#}

}

</code></pre>

参考文献:<br/>
1.[http://www.jianshu.com/p/10fe9aebfed0][http://www.jianshu.com/p/10fe9aebfed0]
2.[http://www.infoq.com/cn/articles/how-to-design-a-good-restful-api][http://www.infoq.com/cn/articles/how-to-design-a-good-restful-api]
3.[https://github.com/perusio/nginx-auth-request-module][https://github.com/perusio/nginx-auth-request-module]
