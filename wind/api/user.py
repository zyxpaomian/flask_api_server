#! /usr/bin/env python3
#! -*- coding:utf -*-

from flask import Blueprint, g, jsonify, request
import logging
from wind.utils.conf import Config
from wind.controller.user import User_Mgt
from wind.base import token_required

logger = logging.getLogger('wind')

auth_api = Blueprint('auth_api',__name__)
@auth_api.route('/api/v1/user/gettoken', methods=['POST'])
def gettoken():
    username = g.request_data['username']
    password = g.request_data['password']
    token = User_Mgt().create_token(username,password)
    logger.info("user: {0} auth successful".format(username))
    return jsonify(result='SUCCESS', token=token)


user_create_api = Blueprint('user_create_api',__name__)
@user_create_api.route('/api/v1/user/createuser', methods=['POST'])
@token_required
def createuser():
    username = g.request_data['username']
    password = g.request_data['password']
    groupid = g.request_data['groupid']
    if User_Mgt().create_user(username,password,groupid):
        logger.info("create user {0}".format(username))
    return jsonify(result='SUCCESS', message='create user successful')
