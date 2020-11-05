#! -*- coding:utf-8 -*-

from celery import Celery
from ansible_runner import AnsibleRunner

celery = Celery('ansibletask',broker="redis://127.0.0.1:6379/0",backend="redis://127.0.0.1:6379/0")

@celery.task(name='ShellRun')
def ShellRun(iplist,cmd):
    shell_args = cmd
    ready_run = AnsibleRunner(forknum=10, remote_user='barney', conn_pass=123, root_pass=123, ipList=iplist, module_name='shell', module_args=shell_args)
    shell_result = ready_run.order_run()
    return shell_result
