# -*- coding: utf-8 -*-


'''
This module mainly handles user basic actions.

Details of request are login,logout,sign up,init,active...

'''


'''
status for the user:

0 ---- unactive

1 ---- locked

2 ---- uninit

3 ---- normal

4 ---- infoset

5 ---- unauthenticate

6 ---- authenticate

'''

from __init__ import BaseHandler, send, set_image_size
from __init__ import WWW_COOKIE_DOMAIN, USER_STATUS

import time
import random
import sys
import os
from hashlib import sha224, md5
import tornado.web
from tornado.options import define, options

import UserManager

define("noreply_account", default="noreply@ueue.cc",
       help="signup email check account")


def check_password(input_psw, salt, check_psw):

    return (sha224(input_psw + salt).hexdigest() == check_psw)


class UserLoginHandler(BaseHandler):

    def get(self):
        self.render("register1.0beta/login.html")

    def post(self):
        email = self.get_argument("email")
        psw = self.get_argument("password")
        go = self.get_argument("next", "/")
        result = UserManager.get_user_withmail(email)
        json = {}
        if result:
            salt = ""
            check = check_password(psw, salt, result.password)
            if check:
                if(result.status > USER_STATUS["unactive"]):
                    if(result.status == USER_STATUS["lock"]):
                        json = dict(error=1, msg='你的帐号以被暂停使用，请联系客服', url=go)
                    else:
                        self.set_secure_cookie("_yoez_uid",
                                               str(result.uid), expires_days=7,
                                               domain=WWW_COOKIE_DOMAIN)
                        json = dict(error=0, msg='', url=go)
                else:
                    tip = "请完成邮箱激活"
                    json = dict(error=1, msg=tip, url='/user/action/login')
            else:
                tip = "密码错误"
                json = dict(error=1, msg=tip, url='/user/action/login')
        else:
            tip = "用户不存在"
            json = dict(error=1, msg=tip, url='/user/action/login')
        self.write(json)


class UserLogoutHandler(BaseHandler):

    def get(self):
        self.clear_current_user()
        go = self.get_argument("next", "/")
        self.redirect(go)


class UserSignupHandler(BaseHandler):

    def get(self):
        self.render("register1.0beta/register-1.html")

    def post(self):
        act = self.get_argument("nick")
        mail = self.get_argument("email")
        psw = self.get_argument("password")
        psw = sha224(psw).hexdigest()
        num = random.randint(1, 10)
        img = "/static/img/common/avt"+str(num)+".jpg"
        reg_time = time.strftime("%Y-%m-%d %X", time.localtime())
        uid = 0
        while(1):
            uid = random.randint(1000000, 10000000)
            chk_sql = "select * from user where uid=%d" % uid
            rt = self.db.get(chk_sql)
            if not rt:
                break
        code = md5(str(uid)+reg_time).hexdigest()
        msg = self.render_string("register1.0beta/config_email.htm",
                                 act=act, co=code)
        sub = "请完成账号激活"
        send(options.noreply_account, mail, sub, msg)
        args = (uid, act, mail, psw, img, reg_time, code)
        UserManager.new_user(*args)
        left, right = mail.split('@')
        rlft, rght = right.split('.')
        if rlft == "gmail":
            right = "google."+rght
        mailpath = "mail."+right
        #self.set_secure_cookie("_yoez_uid",str(uid),expires_days=7)
        self.render('register1.0beta/register-2.html', actname=act,
                    mailpath=mailpath, code=code)


class UserResendmailHandler(BaseHandler):
    def get(self):
        code = self.get_argument('code')
        user_sql = "select * from user where code='%s'" % code
        rt = self.db.get(user_sql)
        if not rt:
            msg = 'send error!pleae contact Customer Services.'
            kwargs = dict(status=0, msg=msg)
            return self.write()
        msg = self.render_string("register1.0beta/config_email.htm",
                                 act=rt.account, co=code)
        sub = "请完成账号激活"
        send(options.noreply_account, rt.email, sub, msg)
        self.write(dict(status=1, msg='go to email and for your active.'))


class UserActiveHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        #cuid=int(self.get_secure_cookie("_yoez_uid"))
        code = self.get_argument("code")
        check_sql = "select * from user where code='%s'" % code
        result = self.db.get(check_sql)
        if(result):
            if result.status == USER_STATUS["unactive"]:
                self.set_secure_cookie("_yoez_uid", str(result.uid), 7,
                                       domain=WWW_COOKIE_DOMAIN)
                active_sql = ("update user set status=%d where "
                              "uid='%d'") % (USER_STATUS["uninit"], result.uid)
                self.db.execute(active_sql)
                print sys.argv[0]
                print sys.argv
                workdir = os.path.dirname(sys.argv[0])
                path = "%s/static/img/user/%d" % (workdir, result.uid)
                print os.path.dirname(sys.argv[0])
                print path
                os.mkdir(path)
                self.render("register1.0beta/register-3.html")
            else:
                self.write(('''你的账户已经激活,请<a href="/user/action/login">'''
                            '''点此登陆</a>'''))
        else:
            self.write(('''验证错误，请检查地址有错误没。如果还是不行，请<a href='''
                        '''"mailto:noreply@ueue.cc">联系我们</a>,'''
                        '''我们会为你解决的。'''))


class UserConfirmHandler(BaseHandler):
    def post(self):
        data = self.get_argument("user_d", "")
        tp = self.get_argument("type", "")
        sql = "SELECT * from user where %s='%s'" % (tp, data)
        result = self.db.get(sql)
        if result:
            if tp == "email":
                tip = "该邮箱已注册，请换一个!"
            else:
                tip = "该用户名已存在，请换一个!"
        else:
            if tp == "email":
                tip = "你可以使用该邮箱注册"
            else:
                tip = "你可以使用该用户名"
        self.write(tip)


class UserInitializeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        if(cuser.status >= USER_STATUS["normal"]):
            return self.redirect("/user/set-basic")
        self.render("user1.0beta/user-beginning-1.html", cuser=cuser)

    def post(self):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        usertype = self.get_argument("type", "0")
        sex = self.get_argument("sex", "0")
        img = self.get_argument("avatar")
        setrst = set_image_size((200, 200), img)
        upd_sql = ("update user set img='%s',status=%d where "
                   "uid=%d") % (img, USER_STATUS["normal"], cuid)
        chk_sql = "select proper_id from  property where proper_id=%d" % cuid
        chk = self.db.get(chk_sql)
        if not chk:
            pro_sql = ("insert into property(proper_id,ptype,sex) values "
                       "(%d,'%s','%s')") % (cuid, usertype, sex)
            bsc_sql = "insert into basicinfo(bsc_id) values(%d)" % (cuid)
            con_sql = "insert into contactinfo(con_id) values(%d)" % (cuid)
            self.db.execute(pro_sql)
            self.db.execute(bsc_sql)
            self.db.execute(con_sql)
        if setrst:
            self.db.execute(upd_sql)
            result = dict(url="/"+str(cuid), status=1, code='')
        else:
            result = dict(url="/", status=0, code='set image error!')
        self.write(result)


# SUPPORT_ACTIONS = dict(follow=follow, cancel=cancel)


class UserFollowHandler(BaseHandler):

    def follow(self, flwid):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        chksql = "select * from follow where flwid=%d" % (flwid)
        result = self.db.get(chksql)
        if result:
            if int(result.relation):
                print "repeat follow"
            else:
                updsql = ("update follow set relation='1' where fid=%d "
                          "and flwid=%d") % (cuid, flwid)
                self.db.execute(updsql)
        else:
            addsql = ("insert into follow(fid,flwid,relation) values "
                      "(%d,%d,'1')") % (cuid, flwid)
            self.db.execute(addsql)

    def cancel(self, flwid):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        chksql = "select * from follow where flwid=%d" % flwid
        result = self.db.get(chksql)
        if result:
            if int(result.relation):
                updsql = ("update follow set relation='0' where fid=%d "
                          "and flwid=%d") % (cuid, flwid)
                self.db.execute(updsql)
            else:
                print "cancel error!"
        else:
            print "cancel error!"

    def post(self):
        action = self.get_argument("action", None)
        flwid = int(self.get_argument("flwid", None))
        result = {}
        if not action:
            result = dict(status=0, msg="unknow action!")
            return self.write(result)
        if not flwid:
            result = dict(status=0, msg="argument action!")
            return self.write(result)
        UserFollowHandler.SUPPORT_ACTIONS[action](self, flwid)
        result = dict(status=1, msg="action success!")
        self.write(result)


class UserPostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.render("editor1.0beta/editor-loading.html")


class UserAuthbindHandler(BaseHandler):

    def get(self):

        self.render("register1.0beta/register-4.html")


HandlerList = [
    (r"/user/action/login", UserLoginHandler),
    (r"/user/action/logout", UserLogoutHandler),
    (r"/user/action/signup", UserSignupHandler),
    (r"/user/action/resendmail", UserResendmailHandler),
    (r"/user/account/active", UserActiveHandler),
    (r"/user/action/confirm", UserConfirmHandler),
    (r"/user/action/init", UserInitializeHandler),
    (r"/user/action/follow", UserFollowHandler),
    (r"/user/action/post", UserPostHandler),
    (r"/user/action/authbind", UserAuthbindHandler),
    ]
