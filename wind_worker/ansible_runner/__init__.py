#! -*- coding:utf-8 -*-
#from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
#from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
import json

#Ansible返回结果
class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

#Ansible并发执行
class AnsibleRunner:
    def __init__(self, forknum=None, remote_user=None, conn_pass=None, module_name=None, module_args=None, root_pass=None, ipList=None):
        self.forknum = forknum
        self.remote_user = remote_user
        self.conn_pass = conn_pass
        self.root_pass = root_pass
        self.ipList = ipList
        self.callback = None
        self.module_name = module_name
        self.module_args = module_args
        self.results_raw = {'success':[],
                             'failed'  :[],
                             'unreachable':[]
                            }
    def order_run(self):
        Options = namedtuple('Options',
            ['connection',
            'module_path', 
            'forks',
            'become',
            'become_method',
            'become_user',
            'timeout',
            'remote_user',
            'become_pass',
            'check',
            'diff'])

        loader = DataLoader()

        myoptions = Options(
            connection='smart',
            module_path=None,
            forks=int(self.forknum),
            become=True,
            become_method='su',
            become_user='root',
            timeout=5,
            remote_user=self.remote_user,
            become_pass=self.root_pass,
            check=False,
            diff=False)

        passwords = dict(vault_pass='secret', conn_pass=self.conn_pass, become_pass=self.root_pass)

        inventory = InventoryManager(loader=loader, sources=self.ipList)

        variable_manager = VariableManager(loader=loader, inventory=inventory)

        play_source =  dict(
            name = "Ansible Exec",
            hosts = self.ipList,
            gather_facts = 'no',
            tasks = [
                #dict(action=dict(module='ping', args='')),
                dict(action=dict(module=self.module_name, args=self.module_args),register='shell_out'),
        ]
        )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        tqm = None
        self.callback = ResultsCollector()
        try:
            tqm = TaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=myoptions,
                    passwords=passwords
                #stdout_callback=callback,
            )
            tqm._stdout_callback = self.callback
            result = tqm.run(play)

            for host, result in tqm._stdout_callback.host_ok.items():
                if self.module_name == 'copy':
                    self.results_raw['success'].append({'host':host,'msg':'Copy File Success','module_name':self.module_name})
                elif self.module_name == 'yum':
                    self.results_raw['success'].append({'host':host,'msg':'YUM Update Success','module_name':self.module_name})
                else:
                #    print(result._result)
                    self.results_raw['success'].append({'host':host,'msg':result._result['stdout'],'module_name':self.module_name})

            for host, result in tqm._stdout_callback.host_failed.items():
                self.results_raw['failed'].append({'host':host,'msg':result._result[u'msg'],'module_name':self.module_name})
            for host, result in tqm._stdout_callback.host_unreachable.items():
                self.results_raw['unreachable'].append({'host':host,'msg':result._result[u'msg'],'module_name':self.module_name})
        finally:
            if tqm is not None:
                tqm.cleanup()
        return self.results_raw 


#
#shell_args='whoami'
#ready_run = AnsibleRunner(forknum=10, remote_user='barney', conn_pass=123, root_pass=123, ipList='127.0.0.1,192.168.118.171,', module_name='shell', module_args=shell_args)
#shell_result = ready_run.order_run()
#print(shell_result)
#
