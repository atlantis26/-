# coding:utf-8
import tornado.web


class UnfinishHander(tornado.web.RequestHandler):
    def get(self):
        # self.render( "static/under_construction.html" )
        # self.redirect( "static/Robot_Framework.html")
        self.redirect("static/miguhelp.html")
        return
