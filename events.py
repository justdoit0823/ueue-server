# -*- coding: utf-8 -*-

'''
This module handles all about record.

Actions are view,search,post...


'''


from __init__ import BaseHandler

import tornado.web

import tornado.escape

import time

import os

import sys

import module

from hashlib import md5

from manage import RecordManager, UserManager, ReviewManager

from manage import ViewManager, FollowManager, SupportManager

SUPPORT_EVENTS = ["pubwelfare", "job", "award",
                  "recruit", "declare", "media",
                  "experience", "games", "official"]

EVENTLIKEY = ("公益参与", "通告媒体", "获奖荣誉",
              "机构招募", "发表声明", "媒体报道",
              "经验分享", "赛事活动", "官方发布")

SAERCHBASE = ("select event.eid,event.title,event.type,event.place,"
              "event.lable,event.time,event.view,event.support,"
              "event.review,event.picture,user.uid,user.img,user.account "
              "from event join user on event.author_id=user.uid")

USERSEARCH = ("select uid from user join basicinfo on "
              "user.uid=basicinfo.bsc_id ")


ORDERS = ("view", "support", "review")


CONDITIONS = {
    "trade": "basicinfo.job like %s",
    "type": "event.type=%s ",
    "user": "user.status=%s ",
    "lable": "event.lable like %s"
}


'''
status for the work:

0 ---- secure publish

1 ---- unverifyed

2 ---- unsure

3 ---- verifyed

'''


class UserPostHandler(BaseHandler):

    def do_record_add(self, etype):

        time = self.get_argument('time')
        place = self.get_argument('place')
        lable = self.get_argument('lable')
        title = self.get_argument('title')
        pic = self.get_argument("uploadpic", None)
        content = self.get_argument('content')
        content = content.replace("'", "\'")
        cuid = self.get_secure_cookie("_yoez_uid")
        RecordManager.new_record()


def do_record_add(request, rtype):

    #content = content.replace("'", "\'")
    cuid = request.get_secure_cookie("_yoez_uid")
    values = request.get_values(('title', 'content', ('uploadpic', ''),
                                 'place', 'lable', 'time'))
    args = (cuid, rtype) + values
    RecordManager.new_record(*args)


class RecordHandler(BaseHandler):

    def get(self):
        schargs = self.request.uri.split("?")
        if(len(schargs) < 2):
            schcond = []
        else:
            schcond = [l for l in schargs[1].split("&") if l]
        schsql = ""
        usrsql = ""
        rcdwhcond = ""
        usrwhcond = ""
        ordcond = ""
        args1 = []
        args2 = []
        for i in schcond:
            left, right = i.split("=")
            if left == "type":
                if int(right) > -1:
                    if not rcdwhcond:
                        rcdwhcond = "  "+CONDITIONS[left]
                    else:
                        rcdwhcond += " and "+CONDITIONS[left]
                    args2.append(right)
            elif left == "user":
                if int(right) > -1:
                    if not usrwhcond:
                        usrwhcond = " where "+CONDITIONS[left]
                    else:
                        usrwhcond += " and "+CONDITIONS[left]
                    args1.append(right)
            elif left == "trade":
                right = tornado.escape.url_unescape(right)
                right = u"%" + right + u"%"
                #print right
                if not usrwhcond:
                    usrwhcond = " where "+CONDITIONS[left]
                else:
                    usrwhcond += " and "+CONDITIONS[left]
                args1.append(right)
            elif left == "lable":
                right = tornado.escape.url_unescape(right)
                right = u"%" + right + u"%"
                #print right
                if not rcdwhcond:
                    rcdwhcond = "  "+CONDITIONS[left]
                else:
                    rcdwhcond += " and "+CONDITIONS[left]
                args2.append(right)
            elif left == "hotsort":
                ordcond = " order by event."+ORDERS[int(right)-1]+" desc"
        if not ordcond:
            ordcond = " order by event.time desc"
        usrsql = USERSEARCH+usrwhcond
        if not usrwhcond:
            if rcdwhcond:
                rcdwhcond = " where "+rcdwhcond
        else:
            if rcdwhcond:
                rcdwhcond = " where user.uid in ("+usrsql+") and "+rcdwhcond
            else:
                rcdwhcond = " where user.uid in ("+usrsql+") "
        schsql = SAERCHBASE+rcdwhcond+ordcond
        print schsql, args1+args2
        rows = self.db.query(schsql, *(args1+args2))
        cuser = self.get_current_user()
        tips = self.get_tool_tips(('top', 'tip'))
        self.render("yoez1.0beta/event-search.html", cuser=cuser, rows=rows,
                    tips=tips)


class UserEventsHandler(BaseHandler):
    def get(self, id):
        uid = int(id)
        type = int(self.get_argument("type", -1))
        cuser = self.get_current_user()
        user = UserManager.get_user_basic(uid)
        if user is None:
            return self.write("sorry!the page you request does not exists.")
        rows = RecordManager.get_user_records(uid, type)
        for one in rows:
            one.contet = one.content.replace("\'", "'")
        userself = cuser and (uid == cuser.uid)
        followed = False
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, user=user, rows=rows, userself=userself,
                      tips=tips)
        self.render("yoez1.0beta/homepage-people-event-1.html", **kwargs)


class EventDetailHandler(BaseHandler):
    def get(self, id):
        eid = int(id)
        cuser = self.get_current_user()
        if cuser:
            rt = SupportManager.check_event_support(*(cuser.uid, eid))
            is_support = (rt is not None)
        else:
            is_support = False
        row = RecordManager.get_record_byid(eid)
        if row is None:
            return self.write("sorry!the page you request does not exists.")
        row.contet = row.content.replace("\'", "'")
        reviews = ReviewManager.get_record_reviews(eid)
        for i in reviews:
            i.content = i.content.replace("\'", "'")
        if not cuser:
            RecordManager.update_record_view(eid, 1)
        else:
            if not (cuser.uid == row.uid):
                rt = ViewManager.user_view_record(cuser.uid, eid)
                if not rt:
                    at = time.strftime("%Y-%m-%d %X", time.localtime())
                    ViewManager.new_record_view(*(eid, cuser.uid, at))
                    RecordManager.update_record_view(eid, 1)
        is_follow = False
        if cuser:
            if(cuser.uid == row.uid):
                is_follow = True
            else:
                flwrst = FollowManager.get_follow_uid(*(cuser.uid, row.uid))
                is_follow = flwrst and int(flwrst.relation)
        piclist = []
        j = 0
        if row.picture:
            for i in row.picture.split(";"):
                piclist.append(dict(num=j, src=i))
                j += 1
        tips = self.get_tool_tips(('top', 'tip', 'del', 'open'))
        if(int(row.type) == 3):
            kwargs = dict(cuser=cuser, row=row, reviews=reviews,
                          is_support=is_support, tips=tips,
                          type=EVENTLIKEY[int(row.type)],
                          email=row.place.split("&")[0],
                          place=row.place.split("&")[1],
                          is_follow=is_follow, piclist=piclist)
            self.render("yoez1.0beta/event-zhaopin-content.html", **kwargs)
        else:
            kwargs = dict(cuser=cuser, row=row, reviews=reviews,
                          is_support=is_support, tips=tips,
                          type=EVENTLIKEY[int(row.type)],
                          is_follow=is_follow, piclist=piclist)
            self.render("yoez1.0beta/event-content.html", **kwargs)

    def post(self, id):
        eid = int(id)
        cuser = self.get_current_user()
        content = self.get_argument("rcontent")
        content = content.replace("'", "\'")
        at = time.strftime("%Y-%m-%d %X", time.localtime())
        args = (eid, cuser.uid, content, at)
        ReviewManager.new_record_review(*args)
        ReviewManager.update_record_review(eid, 1)
        one = dict(uid=cuser.uid, img=cuser.img, account=cuser.account,
                   content=content.replace("\'", "'"), time=at)
        rmsg = self.render_string("modules/user_review_content.html", one=one)
        result = dict(status=1, msg=rmsg)
        self.write(result)


class EventsAgreeHandler(BaseHandler):
    def post(self, id):
        eid = int(id)
        cuser = self.get_current_user()
        upview = "update event set agree=agree+1 where eid=%d" % eid
        result = {}
        if(not cuser.account == event.author):
            chksql = ("select * from eventagree where agrer='%s' "
                      "and agreid=%d") % (cuser.account, eid)
            rt = self.db.get(chksql)
            if not rt:
                at = time.strftime("%Y-%m-%d %X", time.localtime())
                addsql = ("insert into eventagree (agreid,agrer,time) "
                          "values(%d,'%s','%s')") % (eid, cuser.account, at)
                self.db.execute(addsql)
                self.db.execute(upview)
                result = dict(status=1, code="")
        else:
            result = dict(status=0, code="我们更希望看到大家的支持哦！")
        self.write(result)


class UserPosteventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        self.render('editor1.0beta/editor-event-default.html', cuser=cuser)


class UserPostPubwelfareventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[0], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-0.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '0')
        self.write(dict(status=1, code=''))


class UserPostJobeventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[1], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-1.html', **kwargs)

    def post(self):

        do_record_add(self, '1')
        self.write(dict(status=1, code=''))


class UserPostAwardeventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[2], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-2.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '2')
        self.write(dict(status=1, code=''))


class UserPostRecruiteventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[3], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-3.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '3')
        self.write(dict(status=1, code=''))


class UserPostDeclareventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[4], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-4.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '4')
        self.write(dict(status=1, code=''))


class UserPostMediaeventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[5], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-5.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '5')
        self.write(dict(status=1, code=''))


class UserPostMediaeventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[5], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-5.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '5')
        self.write(dict(status=1, code=''))


class UserPostExpeventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[6], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-6.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '6')
        self.write(dict(status=1, code=''))


class UserPostGameseventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[7], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-7.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '7')
        self.write(dict(status=1, code=''))


class UserPostOfficialeventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        cuser = self.get_current_user()
        url = self.get_previous_url()
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, eventxt=EVENTLIKEY[8], url=url, tips=tips)
        self.render('editor1.0beta/editor-event-8.html', **kwargs)

    def post(self):

        cuid = self.get_secure_cookie("_yoez_uid")
        do_record_add(self, '8')
        self.write(dict(status=1, code=''))


class EventsPicuploadHandler(BaseHandler):
    def get(self):

        self.render("yoez1.0beta/event-picupload.html")

    def post(self):

        cuser = self.get_current_user()
        workdir = os.path.dirname(sys.argv[0])
        for i in self.request.files:
            fname, ext = os.path.splitext(self.request.files[i][0]["filename"])
            timestamp = time.strftime("%Y%m%d%X", time.localtime())
            fname = md5(fname.encode("utf-8") + timestamp).hexdigest()
            fname += ext
            path = "%s/static/img/user/%d/%s" % (workdir, cuser.uid, fname)
            try:
                f = file(path, "wb+")
                f.write(self.request.files[i][0]["body"])
                f.close()
            finally:
                if f:
                    f.close()
                result = dict(status=1, code="upload error.")
        src = "/static/img/user/%d/%s" % (cuser.uid, fname)
        result = dict(status=1, path=src)
        self.write(result)


class EventsCalendarHandler(BaseHandler):
    def get(self):

        time_default = time.asctime(time.localtime())
        year = int(self.get_argument("year", time_default[0]))
        month = int(self.get_argument("month", time_default[1]))
        md = module.CalendarModule(self)
        self.write(md.render(year, month))


HandlerList = [
    (r"/records", RecordHandler),
    (r"/([0-9]+)/records", UserEventsHandler),
    (r"/record/([0-9]+)", EventDetailHandler),
    (r"/user/postevent", UserPosteventHandler),
    (r"/user/postevent/pubwelfare", UserPostPubwelfareventHandler),
    (r"/user/postevent/job", UserPostJobeventHandler),
    (r"/user/postevent/award", UserPostAwardeventHandler),
    (r"/user/postevent/recruit", UserPostRecruiteventHandler),
    (r"/user/postevent/declare", UserPostDeclareventHandler),
    (r"/user/postevent/media", UserPostMediaeventHandler),
    (r"/user/postevent/experience", UserPostExpeventHandler),
    (r"/user/postevent/games", UserPostGameseventHandler),
    (r"/user/postevent/official", UserPostOfficialeventHandler),
    (r"/user/events/picupload", EventsPicuploadHandler),
    (r"/events/([0-9]+)/agree", EventsAgreeHandler),
    (r"/events/calendar", EventsCalendarHandler),
    ]
