# coding:utf-8
import tornado.web

class GetDataHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if self.request.arguments.has_key("project"):
            projectName = self.get_argument('project', 'this is a wrong project.')
        else:
            raise keyerror('project is wrong.')
        # if projectName == "rate":
        if self.request.arguments.has_key("starttime"):
            starttime = self.get_argument('starttime', 'this is a wrong project.')
        if self.request.arguments.has_key("endtime"):
            endtime = self.get_argument('endtime', 'this is a wrong project.')
        sqname = projectName + "_output"
        # print sqname
        # conn = sqlite3.connect("tools/MG.db")
        # cursor = conn.cursor()
        if projectName == "rate":
            if self.request.arguments.has_key("month"):
                month = self.get_argument('month', 'this is a wrong month')
                month = month.replace("-", "")
                command = ("select * from monthdata where month=\'%s\'" % month)
            else:
                command = "select * from monthdata order by month desc"
            results, fields = self.readSqlite(command)
            projectlist = []
            rate = []
            increment = []
            incrementrate = []
            for i in xrange(2, len(fields)):
                projectlist.append(fields[i][0])
            for row in xrange(0, len(results)):
                if results[row][1] == 'increment':
                    for j in xrange(2, len(results[row])):
                        increment.append(results[row][j])
                if results[row][1] == 'ratedata':
                    for j in xrange(2, len(results[row])):
                        rate.append(results[row][j])
                if results[row][1] == 'addrate':
                    for j in xrange(2, len(results[row])):
                        incrementrate.append(results[row][j])
            data = [rate, incrementrate, increment, projectlist]
            # data=results
            jinfo = json.dumps(data)
        elif locals().has_key('starttime'):
            starttime = starttime.replace("-", "")
            starttime = starttime + '_'
            if locals().has_key('endtime'):
                endtime = endtime.replace("-", "")
                endtime = endtime + '_?'
                command = ("select * from %s where time >= \'%s\' and time < \'%s\' order by time asc" % (
                sqname, starttime, endtime))
            else:
                command = ("select * from %s where time >= \'%s\' order by time asc" % (sqname, starttime))
            data, fields = self.readSqlite(command)
            # data.reverse()
            fail = []
            passdata = []
            rate = []
            time = []
            casedata = []
            for i in xrange(0, len(data)):
                time.append(str(data[i][5]))
                fail.append(data[i][2])
                passdata.append(data[i][1])
                rate.append(data[i][3])
                casedata.append({'objid': str(data[i][10]), 'coverage': data[i][11], 'version': str(data[i][12]),
                                 'buildtime': str(data[i][5]), 'all': data[i][0], 'pass': data[i][1],
                                 'fail': data[i][2], 'Feedback': data[i][9], 'Nofeedback': 0})
            casedata.reverse()
            info = [time, fail, passdata, rate, casedata]
            # self.write([time,fail,passdata,rate])
            # return
            jinfo = json.dumps(info)
        else:
            command = ("select * from %s order by time desc limit 10" % sqname)
            data, fields = self.readSqlite(command)
            data.reverse()
            fail = []
            passdata = []
            rate = []
            time = []
            casedata = []
            for i in xrange(0, len(data)):
                time.append(str(data[i][5]))
                fail.append(data[i][2])
                passdata.append(data[i][1])
                rate.append(data[i][3])
                casedata.append({'objid': str(data[i][10]), 'coverage': str(data[i][11]), 'version': str(data[i][12]),
                                 'buildtime': str(data[i][5]), 'all': data[i][0], 'pass': data[i][1],
                                 'fail': data[i][2], 'Feedback': data[i][9], 'Nofeedback': 0})
            casedata.reverse()
            info = [time, fail, passdata, rate, casedata]
            # info = [{"name": projectName, "time": data[0][5], "data": data[0][0:3], "softwareproblem": data[0][6], "script": data[0][7], "environmental":data[0][8], "other":data[0][9]}]
            jinfo = json.dumps(info)
        self.write(jinfo)

    def readSqlite(self, command):
        conn = sqlite3.connect("tools/MG.db")
        cursor = conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        fields = cursor.description
        cursor.close()
        conn.close()
        return data, fields