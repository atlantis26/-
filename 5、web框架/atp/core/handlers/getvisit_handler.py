# coding:utf-8
import tornado.web


class GetVisitHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        newtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        wktime = time.strftime("%a", time.localtime())
        wk = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
        thiswktime = datetime.datetime.strftime(
            datetime.datetime.strptime(newtime, '%Y-%m-%d') - datetime.timedelta(wk[wktime]), '%Y-%m-%d')
        today = {'pv': 0, 'uv': 0}
        tswk = {'pv': 0, 'uv': 0}
        amount = {'pv': 0, 'uv': 0}
        visitlist = ['charts', 'login', 'knowledge']
        username = []
        usercount = []
        for table in visitlist:
            command = "select * from %s" % table
            sqlite, fields = readvisit(command)
            todayuser = []
            wkuser = []
            for i in sqlite:
                if thiswktime <= i[0] and table != 'knowledge':
                    wkuser.append(i[1])
                    tswk['pv'] += 1
                if table == 'knowledge':
                    if thiswktime <= i[1]:
                        tswk['pv'] += 1
                        tswk['uv'] += 1
                    continue
                if newtime in i[0]:
                    todayuser.append(i[1])
                    today['pv'] += 1
                username.append(i[1])
            today['uv'] += len(list(set(todayuser)))
            tswk['uv'] += len(list(set(wkuser)))
            amount['pv'] += len(sqlite)
            for user in list(set(username)):
                usercount.append(username.count(user))
            amount['uv'] += len(usercount)
        jinfo = [today, tswk, amount]
        jinfo = json.dumps(jinfo)
        self.write(jinfo)

