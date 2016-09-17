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
