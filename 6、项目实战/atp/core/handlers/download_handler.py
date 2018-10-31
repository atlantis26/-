# coding:utf-8
import tornado.web


class DownLoadHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if self.request.arguments.has_key("project"):
            projectname = self.get_argument('project', 'this is a wrong project.')
        # projectname=eval(projectname)
        if self.request.arguments.has_key("time"):
            buildtime = self.get_argument('time', 'this is a wrong time.')
        # buildtime=eval(buildtime)
        table_log = projectname + '_log'
        command_create = "select * from %s where time=\'%s\'" % (table_log, buildtime)
        # tabledate, fields=self.readSqlite(command_create)
        tabledate = self.readSqlite(command_create)
        fields = [u'构建ID', u'构建时间', u'问题类型', u'问题模块', u'失败数量', u'失败原因', u'问题状态', u'闭环措施', u'闭环结果']
        ProblemClassify = {'Script': u'脚本问题', 'Environment': u'环境问题', 'ChangeRequest': u'需求变更',
                           'Introduction': u'修改引入缺陷', 'DemandDefect': u'新需求缺陷'}
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('problem_message', cell_overwrite_ok=True)
        for field in range(0, len(fields)):
            # sheet.write(0,field,fields[field][0])
            sheet.write(0, field, fields[field])
        row = 1
        col = 0
        for row in range(1, len(tabledate) + 1):
            for col in range(0, len(fields)):
                if col == 2:
                    sheet.write(row, col, u'%s' % ProblemClassify[tabledate[row - 1][col]])
                    continue
                sheet.write(row, col, u'%s' % tabledate[row - 1][col])
        workbook.save(r'./static/readout.xls')


    def readSqlite(self, command):
        conn = sqlite3.connect("tools/MG.db")
        cursor = conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        fields = cursor.description
        conn.commit()
        cursor.close()
        conn.close()
        return data
        # return data, fields