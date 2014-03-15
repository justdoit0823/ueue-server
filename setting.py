# -*- coding:utf-8 -*-


'''
This module mainly handle user's settings,which include
 basic information and contact information.
Also,the 3th auth and user confirm are here.

'''


from __init__ import BaseHandler
from __init__ import USER_STATUS, AUTHORIZE_OPTIONS, set_image_size

import tornado.web

from hashlib import sha224

import os
import sys

JOB_NUM = 3

JOB_ORDER = ["第一职业", "第二职业", "第三职业"]

JOB_ID_ORDER = ["user-job-first", "user-job-second", "user-job-third"]


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
        prosql = "select * from property where proper_id=%d" % cuser.uid
        infosql = "select * from basicinfo where bsc_id=%d" % cuser.uid
        pro = self.db.get(prosql)
        info = self.db.get(infosql)
        is_woman = int(pro.sex)
        joblen = 0
        if(not info.job or info.job == "--"):
            info.job = []
        else:
            info.job = info.job.split("+")
        if info.organ:
            info.organ = info.organ.split("&")
        if info.birth:
            info.birth = info.birth.split("&")
        if info.weight:
            info.weight = info.weight.split("&")
        if info.height:
            info.height = info.height.split("&")
        joblen = len(info.job)
        url = self.get_previous_url()
        self.render("user1.0beta/user-2.html", cuser=cuser, is_woman=is_woman,
                    info=info, options=AUTHORIZE_OPTIONS, jobnum=JOB_NUM,
                    joborder=JOB_ORDER, jobid=JOB_ID_ORDER, joblen=joblen,
                    url=url)

    def post(self):
        name = self.get_argument("name", "--")
        area = self.get_argument("area", "--")
        organ = self.get_argument("organ", "--")
        job = self.get_argument("job", "--")
        height = self.get_argument("height", "--")
        weight = self.get_argument("weight", "--")
        birth = self.get_argument("birth", "--")
        extend = self.get_argument("extend", "--")
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        is_set = self.db.get(("select bsc_id,status from basicinfo join user "
                              "on basicinfo.bsc_id=user.uid where bsc_id=%d")
                             % cuid)
        result = dict()
        if is_set:
            updsql = ("update basicinfo set uname='%s',area='%s',organ='%s',"
                      "job='%s',height='%s',weight='%s',birth='%s',extend='%s'"
                      " where bsc_id=%d") % (name, area, organ, job, height,
                                             weight, birth, extend, cuid)
            self.db.execute(updsql)
            if is_set.status < USER_STATUS["infoset"]:
                updusr = ("update user set status=%d where "
                          "uid=%d") % (USER_STATUS["infoset"], cuid)
                self.db.execute(updusr)
            result = dict(status=1, msg='')
        else:
            addsql = ("insert into basicinfo(bsc_id,uname,area,organ,job,"
                      "height,weight,birth,extend) values(%d,'%s','%s','%s',"
                      "'%s','%s','%s','%s','%s')") % (cuid, name, area, organ,
                                                      job, height, weight,
                                                      birth, extend)
            updusr = ("update user set status=%d where "
                      "uid=%d") % (USER_STATUS["infoset"], cuid)
            self.db.execute(addsql)
            self.db.execute(updusr)
            result = dict(status=1, msg='')
        self.write(result)


class SetContactHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        is_authenticate = int(cuser.status) == USER_STATUS["authenticate"]
        info_sql = "select * from contactinfo where con_id=%d" % cuser.uid
        info = self.db.get(info_sql)
        if info.telphone:
            info.telphone = info.telphone.split("&")
        if info.conmail:
            info.conmail = info.conmail.split("&")
        if info.conaddress:
            info.conaddress = info.conaddress.split("&")
        if info.sinawb:
            info.sinawb = info.sinawb.split("&")
        if info.qqwb:
            info.qqwb = info.qqwb.split("&")
        if info.qq:
            info.qq = info.qq.split("&")
        if info.qzone:
            info.qzone = info.qzone.split("&")
        if info.renren:
            info.renren = info.renren.split("&")
        if info.douban:
            info.douban = info.douban.split("&")
        url = self.get_previous_url()
        self.render("user1.0beta/user-3.html", cuser=cuser,
                    is_auth=is_authenticate, info=info,
                    options=AUTHORIZE_OPTIONS, url=url)

    def post(self):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        agent = int(self.get_argument("agent", 0))
        phone = self.get_argument("phone", "")
        mail = self.get_argument("mail", "")
        address = self.get_argument("address", "")
        sina = self.get_argument("sina", "")
        tqq = self.get_argument("tqq", "")
        qq = self.get_argument("qq", "")
        qzone = self.get_argument("qzone", "")
        renren = self.get_argument("renren", "")
        douban = self.get_argument("douban", "")
        domain = str(cuid)
        is_contact_set = self.db.get(("select con_id from contactinfo where "
                                      "con_id=%d") % cuid)
        if is_contact_set:
            upd_sql = ("update contactinfo set agent_id=%d,telphone='%s',"
                       "conmail='%s',conaddress='%s',sinawb='%s',qqwb='%s',"
                       "qq='%s',qzone='%s',renren='%s',douban='%s' where "
                       "con_id=%d") % (agent, phone, mail, address, sina,
                                       tqq, qq, qzone, renren, douban, cuid)
            self.db.execute(upd_sql)
            result = dict(status=1, code='')
        else:
            add_sql = ("insert into contactinfo(con_id,agent_id,telphone,"
                       "conmail,conaddress,sinawb,qqwb,qq,qzone,renren,douban,"
                       "psldomain) values(%d,%d,'%s','%s','%s','%s','%s','%s',"
                       "'%s','%s','%s','%s')") % (cuid, agent, phone, mail,
                                                  address, sina, tqq, qq,
                                                  qzone, renren, douban,
                                                  domain)
            self.db.execute(add_sql)
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
        chksql = ("select account from user where uid=%d and password"
                  "='%s'") % (cuser.uid, oldpsw)
        chkresult = self.db.get(chksql)
        result = {}
        if chkresult:
            updatesql = ("update user set password='%s' where "
                         "uid=%d") % (newpsw, cuser.uid)
            self.db.execute(updatesql)
            result = dict(status=1, code='')
        else:
            result = dict(status=0, code='你无权修改他人密码')
        self.write(result)


class SetDomainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        dmsql = "select * from contactinfo where con_id=%d" % cuser.uid
        domain = self.db.get(dmsql)
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
