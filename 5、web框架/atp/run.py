# coding=utf-8
from routers.urls import url_patterns
from settings import cookie_secret
import tornado.web
import tornado.ioloop
import tornado.escape
import os


application = tornado.web.Application(handlers=url_patterns,
                                      template_path=os.path.join(os.path.dirname(__file__), "views"),
                                      static_path=os.path.join(os.path.dirname(__file__), "static"),
                                      templates_path=os.path.join(os.path.dirname(__file__), "template"),
                                      autoreload=True,
                                      cookie_secret=cookie_secret,)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
