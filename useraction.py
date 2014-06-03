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
from __init__ import WWW_COOKIE_DOMAIN

import time
import random
import sys
import os
from hashlib import sha224, md5
import tornado.web
import logging
from tornado.options import define, options

from manage import UserManager, PropertyManager

from manage import BasicManager, ContactManager, FollowManager

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
                if(result.status > options.userstatus['unactive']):
                    if(result.status == options.userstatus['lock']):
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
            rt = UserManager.has_user(uid)
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
        rt = UserManager.get_user_withcode(code)
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
        result = UserManager.get_user_withcode(code)
        if(result):
            if result.status == options.userstatus['unactive']:
                self.set_secure_cookie("_yoez_uid", str(result.uid), 7,
                                       domain=WWW_COOKIE_DOMAIN)
                UserManager.update_user_status(options.userstatus['uninit'],
                                               result.uid)
                workdir = os.path.dirname(sys.argv[0])
                path = "%s/static/img/user/%d" % (workdir, result.uid)
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
        if tp == "email":
            result = UserManager.get_user_withmail(data)
            if result:
                tip = "该邮箱已注册，请换一个!"
            else:
                tip = "你可以使用该邮箱注册"
        else:
            result = UserManager.get_user_withid(data)
            if result:
                tip = "该用户名已存在，请换一个!"
            else:
                tip = "你可以使用该用户名"
        self.write(tip)


class UserInitializeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        if(cuser.status >= options.userstatus['normal']):
            return self.redirect("/user/set-basic")
        self.render("user1.0beta/user-beginning-1.html", cuser=cuser)

    def post(self):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        usertype = self.get_argument("type", "0")
        sex = self.get_argument("sex", "0")
        img = self.get_argument("avatar")
        chk = PropertyManager.get_property(cuid)
        if not chk:
            args = [None] * 12
            args[0] = cuid
            PropertyManager.new_property(*(cuid, usertype, sex))
            BasicManager.new_basic(*(args[:9]))
            ContactManager.new_contact(*args)
        kwargs = {'img': img, 'status': options.userstatus['normal']}
        UserManager.update_user(cuid, **kwargs)
        result = dict(url=img, status=1)
        self.write(result)


class UserFollowHandler(BaseHandler):

    def follow(self, flwid):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        result = FollowManager.get_user_relation(cuid, flwid)
        if result:
            if int(result.relation):
                logging.warn("repeat follow at UserFollowHandler")
            else:
                FollowManager.update_user_relation(cuid, flwid)
        else:
            FollowManager.new_user_relation(cuid, flwid, 1)

    def cancel(self, flwid):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        result = FollowManager.get_user_relation(cuid, flwid)
        if result:
            if int(result.relation):
                FollowManager.update_user_relation(cuid, flwid, 0)
            else:
                logging.warn("don't need to cancel!")
        else:
            logging.warn("don't need to cancel!")

    def post(self):
        action = self.get_argument("action", None)
        flwid = int(self.get_argument("flwid", None))
        if not action:
            result = dict(status=0, msg="unknow action!")
            return self.write(result)
        if not flwid:
            result = dict(status=0, msg="argument action!")
            return self.write(result)
        if action == 'follow':
            self.follow(flwid)
        else:
            self.cancel(flwid)
        result = dict(status=1, msg="action success!")
        self.write(result)


class UserPostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.render("editor1.0beta/editor-loading.html")


class UserAuthbindHandler(BaseHandler):

    def get(self):

        self.render("register1.0beta/register-4.html")


class UserAvatarUploadHandler(BaseHandler):

    def post(self):

        from storage import get_rootpath, validate_image, uploadToUpyun

        imgcontent = self.request.files['file'][0]['body']
        val = validate_image(imgcontent, (200, 200))
        if(val == 1):
            result = dict(status=0, code="image size is too small")
        elif(val == -1):
            result = dict(status=0, code="upload image error")
        else:
            rootpath = get_rootpath("user")
            imgname = self.request.files['file'][0]["filename"]
            cuser = self.get_current_user()
            headers = {'x-gmkerl-type': 'fix_both',
                       'x-gmkerl-value': '200x200'}
            upres = uploadToUpyun(cuser.uid, imgcontent, rootpath, imgname,
                                  headers)
            if upres:
                result = dict(status=1, path=upres)
            else:
                result = dict(status=0, code='upload error')
        self.write(result)

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
    (r"/user/avatar/upload", UserAvatarUploadHandler),
    ]
