#! /usr/bin/env python3
#! -*- coding:utf -*-

from flask import abort
import logging
from wind.utils.rpc_client import Rpc_Client
from wind.dao.task import TaskDao


logger = logging.getLogger('wind')

class Svr_Mgt():
    def __init__(self):
        super(Svr_Mgt, self).__init__()
        self.taskdb = TaskDao()

    def Get_Task_Result(self,resultid):
        rpcresult = Rpc_Client(funcname='GetTaskResult',resultid=resultid)
        return rpcresult

    def Judge_Task_State(self,resultid):
        rpcresult = Rpc_Client(funcname='JudgeTaskStatus',resultid=resultid)
        if rpcresult == True:
            return "finished"
        else:
            return "processing"

    def shell_Sync_Run(self,cmd,iplist):
        rpcresult = Rpc_Client(funcname='shellRun',cmd=cmd,iplist=iplist)
        return rpcresult

    def shell_Rsync_Run(self,cmd,iplist):
        rpcresultid = Rpc_Client(funcname='shellDelayRun',cmd=cmd,iplist=iplist)
        return rpcresultid


        
