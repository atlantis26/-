# coding:utf-8
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        # name = tornado.escape.xhtml_escape(self.current_user)
        self.redirect("index.html")
        return