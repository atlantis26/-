# coding:utf-8
import tornado.web


class VisitHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render("template/visit.html")
        # self.redirect("visit.html")
        # return
