# coding:utf-8
import tornado.web


class MiguLibHander(tornado.web.RequestHandler):
    def get(self):
        self.redirect("static/migu_library.html")
        return
