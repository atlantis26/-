# coding:utf-8
import tornado.web


class GetUserHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        visitlist = ['charts', 'login']
        usernames = []
        usercount = []
        for table in visitlist:
            command = "select * from %s" % table
            sqlite, fields = readvisit(command)
            for i in sqlite:
                usernames.append(i[1])
        username = list(set(usernames))
        for user in username:
            tmp = {'value': '', 'name': ''}
            tmp['name'] = user
            tmp['value'] = usernames.count(user)
            usercount.append(tmp)
        jinfo = json.dumps(usercount)
        self.write(jinfo)
