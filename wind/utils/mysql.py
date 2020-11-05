#! /usr/bin/env python3
#! -*- coding:utf-8 -*-
import MySQLdb
from wind.utils.conf import Config
import logging

logger = logging.getLogger('wind')

class DB():
    def __init__(self,host=None,port=None,username=None,password=None,schema=None):
        self.conf = Config()
        self.host = host or self.conf.getconf("mysql").host
        self.port = port or self.conf.getconf("mysql").port
        self.username = host or self.conf.getconf("mysql").username
        self.password = host or self.conf.getconf("mysql").password
        self.schema = host or self.conf.getconf("mysql").schema

    def __enter__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = MySQLdb.connect(host=self.host,
                                        port=int(self.port),
                                        user=self.username,
                                        passwd=self.password,
                                        db=self.schema,
                                        charset='utf8',
                                        connect_timeout=5)
            self.conn.autocommit(False)
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except Exception as e:
            logger.exception(e)
        finally:
            return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn:
                self.conn.commit()
        except Exception as e:
            logger.exception(e)

        try:
            if self.cursor:
                self.cursor.close()
        except Exception as e:
            logger.exception(e)

        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.exception(e)
