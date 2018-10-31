# coding:utf-8
import tornado.web

class setEmailHandler(tornado.web.RequestHandler):
    # def get_current_user( self ):
    # return self.get_secure_cookie('username')
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # if not self.current_user:
        # return
        if self.request.arguments.has_key("project"):
            project = self.get_argument('project', 'this is a wrong project.')
        else:
            project = "bigdata"
        command = "select * from mail where project=\'%s\'" % (project)
        data, fields = self.mailsqlite(command)
        info = [data[0][0], str(data[0][1]), str(data[0][2])]
        jinfo = json.dumps(info)
        self.write(jinfo)

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # if not self.current_user:
        #    return
        # else:
        #    log.debug(self.current_user+"post mail")
        if self.request.arguments.has_key("project"):
            project = self.get_argument('project', 'this is a wrong project.')
        if self.request.arguments.has_key("sendmail"):
            sendmail = self.get_argument('sendmail', 'this is a wrong project.')
        if self.request.arguments.has_key("ccmail"):
            ccmail = self.get_argument('ccmail', 'this is a wrong project.')
        command = "update mail set sendmail=\'%s\', ccmail=\'%s\' where project=\'%s\'" % (sendmail, ccmail, project)
        logging.debug(command)
        self.mailsqlite(command)

    def mailsqlite(self, command):
        conn = sqlite3.connect("email/email.db")
        cursor = conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        fields = cursor.description
        conn.commit()
        cursor.close()
        conn.close()
        return data, fields

