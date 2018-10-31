# coding:utf-8
import tornado.web
import tornado.escape
import logging
import time


class ChartsHander(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        logging.debug("zhe user %s visit charts.html" % self.current_user)
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        username = self.get_secure_cookie('username')
        userpy = self.get_secure_cookie('userpy')
        usermail = self.get_secure_cookie('usermail')
        usertel = self.get_secure_cookie('usertel')
        if userpy == "DMTest01" or userpy == "renfei":
            username = username + '(' + userpy + ')'
        command = "insert into charts (time, userName, userPy, userMail, userTel) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (
        localtime, username, userpy, usermail, usertel)
        writevisit(command)
        return self.render("template/charts.html")
