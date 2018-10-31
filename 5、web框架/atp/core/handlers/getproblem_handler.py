# coding:utf-8
import tornado.web


class GetProblemHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if self.request.arguments.has_key("project"):
            projectName = self.get_argument('project', 'this is a wrong project.')
        if self.request.arguments.has_key("buildtime"):
            buildtime = self.get_argument('buildtime', 'this is a wrong project.')
        projectname = projectName + '_log'
        command = ("select * from %s order by time asc" % (projectname))
        data = self.readSqlite(command)
        info = {'ObjId': 0, 'Time': 0, 'Script': 0, 'Environment': 0, 'ChangeRequest': 0, 'Introduction': 0,
                'DemandDefect': 0, 'Total': 0}
        jinfo = []
        for i in xrange(0, len(data)):
            if i == 0 or data[i][1] == data[i - 1][1]:
                info['ObjId'] = data[i][0]
                info['Time'] = data[i][1]
                info[data[i][2]] += data[i][4]
            else:
                jinfo.append(copy.deepcopy(info))
                info['ObjId'] = data[i][0]
                info['Time'] = data[i][1]
                info['Script'] = 0
                info['Environment'] = 0
                info['ChangeRequest'] = 0
                info['Introduction'] = 0
                info['DemandDefect'] = 0
                info['Total'] = 0
                info[data[i][2]] = data[i][4]
            if i + 1 == len(data):
                jinfo.append(copy.deepcopy(info))
        jinfo.reverse()
        jinfo = json.dumps(jinfo)
        self.write(jinfo)

    def readSqlite(self, command):
        conn = sqlite3.connect("tools/MG.db")
        cursor = conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

