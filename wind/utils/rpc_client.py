#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

import oslo_messaging
from wind.utils.conf import Config
from oslo_config import cfg  
 
CONF = cfg.CONF  

def Rpc_Client(funcname, **kwargs):
    ctxt = {}
    conf = Config()
    rabbit_user = conf.getconf("rpc").rabbitmq_user
    rabbit_passwd = conf.getconf("rpc").rabbitmq_passwd
    rabbit_url = conf.getconf("rpc").rabbitmq_url
    transport_url = "rabbit://{0}:{1}@{2}".format(rabbit_user,rabbit_passwd,rabbit_url)
    transport = oslo_messaging.get_transport(cfg.CONF,transport_url)
    target = oslo_messaging.Target(topic=conf.getconf("rpc").rpc_topic)
    client = oslo_messaging.RPCClient(transport, target)
    result = client.call(ctxt, funcname, myarg=kwargs)
    cctxt = client.prepare(namespace='control',version='1.0')
    cctxt.cast({}, 'stop')
    return result