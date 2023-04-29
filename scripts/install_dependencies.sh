#!/bin/bash
yum -y update 
yum -y install gcc git pcre-devel python-devel python-pip tkinter postgresql postgresql-devel
mkdir /var/www
mkdir /var/www/html
mkdir /var/www/html/web2py
export WEB2PY_ROOT=/var/www/html/web2py
#git clone --recursive https://github.com/web2py/web2py.git $WEB2PY_ROOT  
#mv $WEB2PY_ROOT/handlers/ws
#gihandler.py $WEB2PY_ROOT  
groupadd web2py 
useradd -r -g web2py web2py
chown -R web2py:web2py $WEB2PY_ROOT
