# coding:utf-8
import tornado.web


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('username')
        self.redirect("/login")
        # self.render( "login.html" )
        return
