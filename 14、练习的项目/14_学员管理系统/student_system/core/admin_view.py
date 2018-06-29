# coding:utf-8
from model.db_handler import create_user


class AdminView(object):
    def create_user(self, name, account, password1, password2, qq, role_id):
        if

        rsp = create_user(name, account, password1, password2, qq, role_id)
        print(rsp.msg)


    def delete_user(self):
        pass


    def modify_user(self):
        pass


    def detail_user(self):
        pass


    def list_user(self):
        pass
