#! /usr/bin/env python3
#! -*- coding:utf -*-

from flask import abort
from wind.dao.user import UserDao
import logging
import uuid


logger = logging.getLogger('wind')

class User_Mgt():
    def __init__(self):
        super(User_Mgt, self).__init__()
        self.userdb = UserDao()

    def create_token(self,username,password):
        userdata = self.userdb.user_auth(username,password)
        if len(userdata) == 0:
            abort(401)
        else:
            token = uuid.uuid4().hex
            self.userdb.token_save(token,username)
            return token

    def get_user_by_token(self,token):
        username = self.userdb.get_token(token)
        if len(username) == 0:
            abort(401)
        else:
            return username[0]['username']

    def create_user(self,username,password,groupid):
        self.userdb.create_user(username,password,groupid)
        return True
    
