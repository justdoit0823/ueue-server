# -*- coding:utf-8 -*-


'''
This module mainly handle user's settings,which include
 basic information and contact information.
Also,the 3th auth and user confirm are here.

'''


from __init__ import BaseHandler
from __init__ import AUTHORIZE_OPTIONS, set_image_size

import tornado.web

from tornado.options import options

from hashlib import sha224

import os
import sys

from manage import BasicManager, ContactManager, PropertyManager

from manage import UserManager

JOB_NUM = 3

JOB_ORDER = ("第一职业", "第二职业", "第三职业")

JOB_ID_ORDER = ("user-job-first", "user-job-second", "user-job-third")


def split_values(values):

    _d = '&'
    for k in values:
        v = values[k]
        if isinstance(v, tuple) and v:
            _d = v[1]
            v = v[0]
        if v:
            values[k] = v.split(_d)


class SettingHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        if(cuser.status >= options.userstatus['normal']):
            self.redirect("/user/set-basic")
        else:
            self.redirect("/user/action/init")


class SetAvatarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url()
        return self.render("user1.0beta/user-1.html", cuser=cuser, url=url)

    def post(self):
        cuser = self.get_current_user()
        img = self.get_argument("avatar")
        setrst = set_image_size((200, 200), img)
        if setrst:
            oldimg = cuser.img
            UserManager.update_user(cuser.uid, **{'img': img})
            path = os.path.dirname(sys.argv[0])+oldimg
            os.remove(path)
            result = dict(url="/"+str(cuid), status=1, code='')
        else:
            result = dict(url="/", status=0, code='set image error!')
        self.write(result)


class SetBasicHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        pro = PropertyManager.get_property(cuser.uid)
        info = BasicManager.get_basic(cuser.uid)
        is_woman = int(pro.sex)
        joblen = 0
        infotmp = info.copy()
        infotmp.pop('uname')
        infotmp.pop('area')
        if(not infotmp['job'] or infotmp['job'] == "--"):
            infotmp['job'] = ()
        else:
            infotmp['job'] = infotmp['job'].replace('+', '&')
        split_values(infotmp)
        info.update(infotmp)
        joblen = len(info.job)
        url = self.get_previous_url()
        self.render("user1.0beta/user-2.html", cuser=cuser, is_woman=is_woman,
                    info=info, options=AUTHORIZE_OPTIONS, jobnum=JOB_NUM,
                    joborder=JOB_ORDER, jobid=JOB_ID_ORDER, joblen=joblen,
                    url=url)

    def post(self):

        args = list(self.get_values((("name", "--"), ("area", "--"),
                                     ("organ", "--"), ("job", "--"),
                                     ("height", "--"), ("weight", "--"),
                                     ("birth", "--"), ("extend", "--"))))
        cuser = self.get_current_user()
        is_set = BasicManager.check_basic(cuser.uid)
        if is_set:
            args.append(cuser.uid)
            BasicManager.update_basic(*args)
            if cuser.status < options.userstatus["infoset"]:
                UserManager.update_user_status(options.userstatus["infoset"],
                                               cuser.uid)
        else:
            args.insert(0, cuser.uid)
            BasicManager.new_basic(*args)
            UserManager.update_user_status(options.userstatus["infoset"],
                                           cuser.uid)
        result = dict(status=1, msg='')
        self.write(result)


class SetContactHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        is_auth = int(cuser.status) == options.userstatus["authenticate"]
        info = ContactManager.get_contact(cuser.uid)
        split_values(info)
        url = self.get_previous_url()
        self.render("user1.0beta/user-3.html", cuser=cuser,
                    is_auth=is_auth, info=info,
                    options=AUTHORIZE_OPTIONS, url=url)

    def post(self):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        args = list(self.get_values((("phone", ""), ("mail", ""),
                                     ("address", ""))))
        domain = str(cuid)
        is_contact_set = ContactManager.check_contact(cuid)
        if is_contact_set:
            args.append(cuid)
            ContactManager.update_contact(*args)
            result = dict(status=1, code='')
        else:
            args.insert(0, cuid)
            ContactManager.new_contact(*args)
            result = dict(status=1, code='')
        self.write(result)


class SetPasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url()
        return self.render("user1.0beta/user-4.html", cuser=cuser, url=url)

    def post(self):
        cuser = self.get_current_user()
        oldpsw = sha224(self.get_argument("oldpsw")).hexdigest()
        newpsw = sha224(self.get_argument("newpsw")).hexdigest()
        if cuser and cuser.password == oldpsw:
            UserManager.update_user_psw(newpsw, cuser.uid)
            result = dict(status=1, code='')
        else:
            result = dict(status=0, code='你无权修改他人密码')
        self.write(result)


class SetDomainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        domain = ContactManager.get_domain(cuser.uid)
        url = self.get_previous_url()
        return self.render("user1.0beta/user-5.html",
                           cuser=cuser, domain=domain, url=url)

    def post(self):
        domain = self.get_argument("domain", None)
        result = dict(status=0, msg="缺少参数")
        if domain:
            cuid = int(self.get_secure_cookie("_yoez_uid"))
            is_domain_set = ContactManager(cuid)
            if not is_domain_set:
                args = [None] * 12
                args[0] = cuid
                args[11] = domain
                ContactManager.new_contact(*args)
                result = dict(status=1, msg="设置成功")
            else:
                chkrst = ContactManager.check_domain(domain)
                if chkrst:
                    result = dict(status=0, msg="该域名已存在，请再选一个")
                else:
                    ContactManager.update_domain(cuid, domain)
                    result = dict(status=1, msg="设置成功")
        self.write(result)


class SetAuthHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url()
        self.render("user1.0beta/user-6.html", cuser=cuser, url=url)


class SetConfirmHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url()
        self.render("user1.0beta/user-7.html", cuser=cuser, url=url)


class SetRealnameConfirmHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url()
        self.render("user1.0beta/user-7-1-1.html", cuser=cuser, url=url)


HandlerList = [
    (r"/user/setting", SettingHandler),
    (r"/user/set-avatar", SetAvatarHandler),
    (r"/user/set-basic", SetBasicHandler),
    (r"/user/set-contact", SetContactHandler),
    (r"/user/set-password", SetPasswordHandler),
    (r"/user/set-domain", SetDomainHandler),
    (r"/user/set-auth", SetAuthHandler),
    (r"/user/set-confirm", SetConfirmHandler),
    (r"/user/set/confirm-realname", SetRealnameConfirmHandler),
    ]
