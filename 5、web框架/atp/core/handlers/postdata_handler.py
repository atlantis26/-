# coding:utf-8
import tornado.web


class PostDataHandler(tornado.web.RequestHandler):
    # def get(self):
    # self.set_header("Access-Control-Allow-Origin", "*")
    # if self.request.arguments.has_key("data"):
    #    data = self.get_argument('data', 'this is a wrong data.')
    # print data
    def get_current_user(self):
        return self.get_secure_cookie('username')

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if not self.current_user:
            self.redirect("/login")
            return
        if self.request.arguments.has_key("data"):
            logdata = self.get_argument('data', 'this is a wrong data.')
        logdata = eval(logdata)
        # print type(logdata),logdata
        buildtime = logdata["Time"]
        tablename = logdata["projectname"] + '_log'

        table_output = logdata["projectname"] + '_output'
        command_Feedback = "select * from %s where time=\'%s\'" % (table_output, buildtime)
        Feedback = self.readSqlite(command_Feedback)
        Feedbackdata = int(Feedback[0][9]) + int(logdata['CaseNum'])
        command_output = "update %s set other=\'%s\' where time=\'%s\'" % (table_output, Feedbackdata, buildtime)
        self.readSqlite(command_output)
        # checkcommand = "select * from %s where time = \'%s\' and ProblemClassify=\'%s\'" %(tablename, buildtime, logdata["ProblemClassify"])
        # isHave = self.readSqlite(checkcommand)
        # if isHave is not None and len(isHave):
        # command = "update %s set ModuleName=\'%s\', CaseNum=\'%s\', FailureCause=\'%s\', ProblemStatus=\'%s\', LoopMeasures=\'%s\', LoopResults=\'%s\' where Time=\'%s\' and ProblemClassify=\'%s\'" %(tablename, logdata["ModuleName"], str(logdata["CaseNum"]), logdata["FailureCause"], logdata["ProblemStatus"], logdata["LoopMeasures"], logdata["LoopResults"], buildtime, logdata["ProblemClassify"])
        # self.readSqlite(command)
        # else:
        command = "insert into %s (ObjId, Time, ProblemClassify, ModuleName, CaseNum, FailureCause, ProblemStatus, LoopMeasures, LoopResults, author) values (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (
        tablename, logdata["ObjId"], buildtime, logdata["ProblemClassify"], logdata["ModuleName"], logdata["CaseNum"],
        logdata["FailureCause"], logdata["ProblemStatus"], logdata["LoopMeasures"], logdata["LoopResults"],
        self.current_user)
        self.readSqlite(command)

    def readSqlite(self, command):
        conn = sqlite3.connect("tools/MG.db")
        cursor = conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return data

