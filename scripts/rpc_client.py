#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

import oslo_messaging as messaging  
from oslo_context import context  
from oslo_config import cfg  
from oslo_log import log as logging  
      
CONF = cfg.CONF  
#LOG = logging.getLogger(__name__) 
#logging.register_options(CONF)  
#logging.setup(CONF, "myservice")  
#CONF(default_config_files=['app.conf'])  
     
ctxt = {}  
#arg = {'a':'b'}  
def aaa(**kwargs):
#def aaa():
    arglist = []
    #for k ,v in kwargs.items():
    #    argstring = "{0}={1}".format(k,v)
    #    arglist.append(argstring)
    #clientargstring = ','.join(arglist)
    transport_url = 'rabbit://wind:wind@192.168.118.171:5672/'      
    transport = messaging.get_transport(cfg.CONF,transport_url)  
    target = messaging.Target(topic='wind_rpc')  
    client = messaging.RPCClient(transport, target)  
    #result = client.call(ctxt, 'add', arg=arg)
    result = client.call(ctxt, 'shellRun', myarg=kwargs)
    print(result)
    #client.cast({}, 'stop')
    cctxt = client.prepare(namespace='control',version='1.0')
    cctxt.cast({}, 'stop')

aaa(cmd='uptime',iplist='127.0.0.1,')
