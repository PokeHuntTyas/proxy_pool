# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyApi.py  
   Description :  
   Author :       JHao
   date：          2016/12/4
-------------------------------------------------
   Change Activity:
                   2016/12/4: 
-------------------------------------------------
"""
__author__ = 'JHao'

import sys

sys.path.append('../')

from flask import Flask, jsonify, request
from Util.GetConfig import GetConfig



from Manager.ProxyManager import ProxyManager

app = Flask(__name__)


api_list = {
    'get': u'get a usable proxy',
    # 'refresh': u'refresh proxy pool',
    'get_all': u'get all proxies from the proxy pool',
    'delete?proxy=127.0.0.1:8080': u'delete a bad proxy',
    'get_status': u'proxy statistics'
}

def check_auth(username, password):
   config = GetConfig()
   return username == config.username and password = config.password

def authenticate():
    return Response(
    'You\'re not allowed here.\n'
    'Password not right', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/get/')
@requires_auth
def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'


@app.route('/refresh/')
def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，暂不使用
    # ProxyManager().refresh()
    pass
    return 'success'


@app.route('/get_all/')
@requires_auth
def getAll():
    proxies = ProxyManager().getAll()
    return jsonify(proxies)


@app.route('/delete/', methods=['GET'])
@requires_auth
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@app.route('/get_status/')
@requires_auth
def getStatus():
    status = ProxyManager().getNumber()
    return jsonify(status)


def run():
    config = GetConfig()
    app.run(host=config.host_ip, port=config.host_port)

if __name__ == '__main__':
    run()
