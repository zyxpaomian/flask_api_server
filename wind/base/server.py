#! /usr/bin/env python3
#! -*- coding:utf-8 -*-




from flask import Flask, request, jsonify, session, g
import datetime
import json
from wind.api.user import auth_api,user_create_api
from wind.api.svrmgt import *
from wind.base import register_errors
from wind.utils.log import register_logging
from wind.utils.conf import Config


from oslo_config import cfg

CONF = cfg.CONF
_APP = None

MODULES = [
    (user_auth_api,''),
    (user_create_api,''),
]


'''
蓝本注册管理
'''
def configure_blueprints(app,modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

'''
创建app，指定一些静态文件和模板的路径
'''
def make_app():
    global _APP
    if _APP is False:
        return _APP

    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 1024000000
    app.secret_key = 'saaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    configure_blueprints(app, MODULES)
    _APP = app
    return app

def before_run():
    app = make_app()
    app.permanent_session_lifetime = datetime.timedelta(days=1)

    '''
    注册错误码
    '''
    register_errors(app)

    '''
    初始化日志
    '''
    register_logging()

    '''
    拦截请求，在请求前对参数做检查，只接收json数据
    '''
    @app.before_request
    def before_request():
        try:
            g.request_data = {}
        #if str(request.data,encoding='utf-8') != '' or request.data != "" or len(request.data) != 0:
            if len(request.data) != 0:
                g.request_data = json.loads(str(request.data,encoding='utf-8'))
            elif len(request.values) == 0:
                g.request_data = {}
            else:
                try:
                    for k, v in request.values.iteritems():
                        g.request_data[k] = v
                except:
                    g.request_data = {}
        except:
            return json.dumps(
               dict(msg='Wrong Param,Need Json Type')
            ),401
    return app

def create_app():
    app = before_run()
    return app
