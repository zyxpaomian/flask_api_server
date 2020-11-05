#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

import configparser

class Dictionary(dict):
    '''
    将ini配置文件转换为dict
    '''
    def __getattr__(self,keyname):
        return self.get(keyname,"配置文件中没有找到Key")

class Config():
    def __init__(self,cfg_name='conf/default.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(cfg_name)
        for section in self.config.sections():
            setattr(self,section,Dictionary())
            for keyname,value in self.config.items(section):
                setattr(getattr(self,section),keyname,value)

    def getconf(self,section):
        if section not in self.config.sections():
            exit(111)
        return getattr(self, section)
