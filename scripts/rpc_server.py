#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

from oslo_config import cfg  
import oslo_messaging  
#from oslo_log import log as logging  
import time  
  
CONF = cfg.CONF  
#LOG = logging.getLogger(__name__)
 
#logging.register_options(CONF)  
#logging.setup(CONF, "myservice")  
#CONF(default_config_files=['app.conf'])  
  
class ServerControlEndpoint(object):  
    target = oslo_messaging.Target(namespace='control',  
                                   version='1.0')  
  
    def __init__(self, server):  
        self.server = server  
  
    def stop(self, ctx):  
        if self.server:  
            self.server.stop()  
  
class TestEndpoint(object):  
    def test(self, ctx, arg):  
        print("test")
        print(arg)
        return arg 

class Test2Endpoint(object):
   # target = oslo_messaging.Target(namespace='test2',  
                                   #version='1.0')  
    def add(self, ctx, myarg):
        a = map(lambda x:int(x),myarg.values())
        return sum(a)
        #print("test")
        #print(arg)
        
        #return a+b

transport_url = 'rabbit://wind:wind@192.168.118.162:5672/'
transport = oslo_messaging.get_transport(cfg.CONF,transport_url)  
target = oslo_messaging.Target(topic='wind_rpc', server='wind_rpc_server')  
endpoints = [  
    ServerControlEndpoint(None),  
    TestEndpoint(), 
    Test2Endpoint(), 
]  
server=oslo_messaging.get_rpc_server(transport,target, endpoints,executor='blocking')  
#server.start()
#time.sleep(5)
#server.stop()
#server.wait()
try:  
    server.start()  
    while True:  
        time.sleep(1)  
except KeyboardInterrupt:
    print("stop server")
    server.stop()
server.wait()