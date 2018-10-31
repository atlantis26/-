# coding:utf-8
import tornado.web


class GetMonthHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if self.request.arguments.has_key("endtime"):
            endtime = self.get_argument('endtime', 'this is a wrong project.')
        else:
            endtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if self.request.arguments.has_key("starttime"):
            starttime = self.get_argument('starttime', 'this is a wrong project.')
        if locals().has_key('starttime'):
            datelist = dateRange(endtime, starttime)
        else:
            datelist = dateRange(endtime)
        datelist.reverse()
        visitlist = ['charts', 'login', 'knowledge']
        visitdata = []
        visitdata.append(datelist)
        for table in visitlist:
            page = []
            command = "select * from %s where time<=\'%s\' and time >= \'%s\' order by time asc" % (
            table, endtime + '#', datelist[0])
            sqlite, fields = readvisit(command)
            for i in datelist:
                page.append(str(sqlite).count(i))
            visitdata.append(page)
        jinfo = json.dumps(visitdata)
        self.write(jinfo)

