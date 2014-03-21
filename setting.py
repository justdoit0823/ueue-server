# -*- coding:utf-8 -*-


'''
This module mainly handle user's settings,which include
 basic information and contact information.
Also,the 3th auth and user confirm are here.

'''


from __init__ import BaseHandler
from __init__ import USER_STATUS, AUTHORIZE_OPTIONS, set_image_size

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
        if(cuser.status >= USER_STATUS["normal"]):
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
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        img = self.get_argument("avatar")
        setrst = set_image_size((200, 200), img)
        upd_sql = "update user set img='%s' where uid=%d" % (img, cuid)
        img_sql = "select img from user where uid=%d" % cuid
        if setrst:
            oldimg = self.db.get(img_sql).img
            self.db.execute(upd_sql)
            path = os.path.dirname(sys.argv[0])+oldimg
            #print path
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
            args.append(cuid)
            BasicManager.update_basic(*args)
            if cuser.status < options.userstatus["infoset"]:
                UserManager.update_user_status(options.userstatus["infoset"],
                                               cuser.uid)
        else:
            args.insert(0, cuid)
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
        args = list(self.get_values((("agent", 0), ("phone", ""),
                                     ("mail", ""), ("address", ""),
                                     ("sina", ""), ("tqq", ""),
                                     ("qq", ""), ("qzone", ""), ("renren", "")
                                     ("douban", ""))))
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
            is_domain_set = self.db.get(("select con_id from contactinfo "
                                         "where con_id=%d") % cuid)
            if not is_domain_set:
                addsql = ("insert into contactinfo(con_id,psldomain) values"
                          "(%d,'%s')") % (cuid, domain)
                self.db.execute(updsql)
                result = dict(status=1, msg="设置成功")
            else:
                chksql = ("select psldomain from contactinfo where psldomain"
                          "='%s'") % domain
                chkrst = self.db.get(chksql)
                if chkrst:
                    result = dict(status=0, msg="该域名已存在，请再选一个")
                else:
                    updsql = ("update contactinfo set psldomain='%s' where "
                              "con_id=%d") % (domain, cuid)
                    self.db.execute(updsql)
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
