# coding:utf-8
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        logging.debug("%s visit index." % self.current_user)
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        username = self.get_secure_cookie('username')
        userpy = self.get_secure_cookie('userpy')
        usermail = self.get_secure_cookie('usermail')
        usertel = self.get_secure_cookie('usertel')
        if userpy == "DMTest01" or userpy == "renfei":
            username = username + '(' + userpy + ')'
        command = "insert into login (time, userName, userPy, userMail, userTel) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (
        localtime, username, userpy, usermail, usertel)
        writevisit(command)
        self.render("index.html")
        return