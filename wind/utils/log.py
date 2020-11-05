#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

import logging
from wind.utils.conf import Config

def register_logging():
    conf = Config()
    logname = conf.getconf("server").logname
    logger = logging.getLogger('wind')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logname)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s=>%(module)s=>%(funcName)s]: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)