# coding:utf-8
import tornado.web


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
        return

    def post(self, *args, **kwargs):
        args = dict((k, v[-1]) for k, v in self.request.arguments.items())
        # logging.debug("%s" %args)
        args["password"] = toRsa(args["password"])
        args["type"] = "0"
        data_str = json.dumps(args)
        # logging.debug("%s" %data_str)
        headers = {'Content-type': 'application/json'}
        r = requests.post(_MIGU_AUTH_URL, data=data_str, headers=headers, verify=False)
        userinfo = r.json()
        logging.info("zhe visit user INFO : %s" % userinfo)
        if userinfo["code"] != 200:
            self.redirect("/login")
            return
        if userinfo["code"] == 200:
            if userinfo["userName"]:
                self.set_secure_cookie('username', userinfo["userName"], expires_days=None)
                self.set_secure_cookie('userpy', userinfo["userPy"], expires_days=None)
                self.set_secure_cookie('usermail', userinfo["userMail"], expires_days=None)
                self.set_secure_cookie('usertel', userinfo["userTel"], expires_days=None)
            self.redirect("/")
            return
