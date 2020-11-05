#! -*- coding:utf-8 -*-
from oslo_config import cfg  
import oslo_messaging  
import time  
from ansible_task import *
from celery.result import AsyncResult
  
CONF = cfg.CONF  
  
class ServerControlEndpoint(object):  
    target = oslo_messaging.Target(namespace='control',  
                                   version='1.0')  
  
    def __init__(self, server):  
        self.server = server  
  
    def stop(self, ctx):  
        if self.server:  
            self.server.stop()  

class BasicEndpoint(object):

    def GetTaskResult(self, ctx, myarg):
        resultid = myarg["resultid"]
        execresult=ShellRun.AsyncResult(resultid).get()
        return execresult

    def JudgeTaskStatus(self, ctx, myarg):
        resultid = myarg["resultid"]
        return ShellRun.AsyncResult(resultid).ready()
       
class ShellEndpoint(object):
 
    def shellRun(self, ctx, myarg):
        cmd = myarg["cmd"]
        ipstr = myarg["iplist"]
        result = ShellRun(ipstr,cmd)
        return result


    def shellDelayRun(self, ctx, myarg):
        cmd = myarg["cmd"]
        ipstr = myarg["iplist"]
        result = ShellRun.delay(ipstr,cmd)
        return {"resultid":str(result)}


transport_url = 'rabbit://wind:wind@192.168.118.171:5672/'
transport = oslo_messaging.get_transport(cfg.CONF,transport_url)  
target = oslo_messaging.Target(topic='wind_rpc', server='wind_rpc_server')  
endpoints = [  
    ServerControlEndpoint(None),
    BasicEndpoint(),
    ShellEndpoint(), 
]  
server=oslo_messaging.get_rpc_server(transport,target, endpoints,executor='blocking')  

try:  
    server.start()  
    while True:  
        time.sleep(1)  
except KeyboardInterrupt:
    print("stop server")
    server.stop()
server.wait()
