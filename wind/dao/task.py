from wind.utils.mysql import DB
import logging

logger = logging.getLogger('wind')

class TaskDao():
    def __init__(self):
        super(TaskDao, self).__init__()

    def get_synctask_list(self,taskmod):
        with DB() as db:
            sql = "select taskname,taskurl,taskargs,taskmod  from tasks_model where taskmod = \'{0}\'".format(taskmod)
            db.execute(sql)
            data = db.fetchall()
            return data

    def get_synctask(self,taskmod):
        with DB() as db:
            sql = "select taskname,taskurl,taskargs,taskmod from tasks_model where taskmod = \'{0}\'".format(taskmod)
            db.execute(sql)
            data = db.fetchall()
            return data            

    def add_task(self,taskname,taskurl,taskargs,tasktype):
        with DB() as db:
            sql = "insert into server_tasks_model (`taskname`,`taskurl`,`taskargs`,`tasktype`) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\');".format(taskname,taskurl,taskargs,tasktype)
            #sql = "insert into user(username,password,create_time,group_id) values (\'{0}\',MD5({1}),NOW(),{2});".format(username,password,groupid)
            db.execute(sql)
            #data = db.fetchall()