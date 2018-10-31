# coding:utf-8
import tornado.web


class EmailConfHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.redirect("static/email-conf-vue.html")
        return
