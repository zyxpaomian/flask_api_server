from wind.utils.mysql import DB
import logging

logger = logging.getLogger('wind')

class UserDao():
    def __init__(self):
        super(UserDao, self).__init__()

    def user_auth(self, username, password):
        with DB() as db:
            sql = "select username,password from user where username = \'{0}\' and password = MD5({1})".format(username,password)
            db.execute(sql)
            data = db.fetchall()
            return data

    def token_save(self,token,username):
        with DB() as db:
            sql = "insert into tokens(token,username,expire_time) values (\'{0}\',\'{1}\',date_sub(NOW(),interval -1 day));".format(token,username)
            db.execute(sql)
                
    def create_user(self, username, password, groupid):
        with DB() as db:
            sql = "insert into user(username,password,create_time,group_id) values (\'{0}\',MD5({1}),NOW(),{2});".format(username,password,groupid)
            db.execute(sql)
    
    def get_token(self, token):
        with DB() as db:
            sql = "select username from tokens where token=\'{0}\';".format(token)
            db.execute(sql)
            data = db.fetchall()
            return data
    