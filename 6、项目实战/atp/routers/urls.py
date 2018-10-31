# coding:utf-8
from core import *

url_patterns = [
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/migulib", MiguLibHander),
    (r"/charts", ChartsHander),
    (r"/unfinish", UnfinishHander),
    (r"/*", IndexHandler),
    (r"/getdata", GetDataHandler),
    (r"/postdata", PostDataHandler),
    (r"/getproblem", GetProblemHandler),
    (r"/download", DownLoadHandler),
    (r"/visit", VisitHandler),
    (r"/getuser", GetUserHandler),
    (r"/getmonth", GetMonthHandler),
    (r"/getvisit", GetVisitHandler),
    (r"/email", setEmailHandler),
    (r"/emailconf", EmailConfHandler),
]
