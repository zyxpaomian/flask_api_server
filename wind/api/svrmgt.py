#! /usr/bin/env python3
#! -*- coding:utf -*-

from flask import Blueprint, g, jsonify, request
import logging
from wind.utils.conf import Config
from wind.controller.svrmgt import Svr_Mgt
from wind.base import token_required
import time
import json
#from flask_cors import CORS

logger = logging.getLogger('wind')

gettaskid_api = Blueprint('gettaskid_api',__name__)
@gettaskid_api.route('/api/v1/server/gettaskresult', methods=['POST'])
def gettaskid_route():
    resultid = g.request_data['resultid']
    result = Svr_Mgt().Get_Task_Result(resultid)
    return jsonify(result='SUCCESS', message=result)

gettaskstate_api = Blueprint('gettaskstate_api',__name__)
@gettaskstate_api.route('/api/v1/server/gettaskstate', methods=['POST'])
def gettaskstate_route():
    resultid = g.request_data['resultid']
    result = Svr_Mgt().Judge_Task_State(resultid)
    return jsonify(result='SUCCESS', message=result)

synctask_api = Blueprint('synctask_api',__name__)
@synctask_api.route('/api/v1/server/shellsynctask', methods=['POST'])
def synctask_route():
    cmd = g.request_data['cmd']
    iplist = g.request_data['iplist']
    result = Svr_Mgt().shell_Sync_Run(cmd,iplist)
    return jsonify(result='SUCCESS', message=result)


rsynctask_api = Blueprint('rsynctask_api',__name__)
@rsynctask_api.route('/api/v1/server/shellrsynctask', methods=['POST'])
def rsynctask_route():
    cmd = g.request_data['cmd']
    iplist = g.request_data['iplist']
    result = Svr_Mgt().shell_Rsync_Run(cmd,iplist)
    return jsonify(result='SUCCESS', message=result)




