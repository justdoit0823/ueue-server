# -*- coding: utf-8 -*-

'''
This module handles all requests about work and self-define data.

The details are view,search,post,edit,delete...

'''


from __init__ import BaseHandler, USER_STATUS

from userspace import DEFAULT_TEXT

import tornado.web
import tornado.escape
import module


import time
import os
import sys
import re

from hashlib import md5

from manage import WorkManager, UserManager, ReviewManager


'''The typevalue -1 is for all(default),0 for video,1 for music,
2 for picture,3 for article.'''

SUPORT_WORKS = ('video', 'music', 'picture', 'article')

SUPORT_IMAGES = ('jpg', 'png', 'jpeg')

SUPORT_WORK_MARKS = ('不标记知识共享协议', '署名-非商业性使用-禁止演绎', '署名-非商业性使用-相同方式共享',
                     '署名-非商业性使用', '署名-禁止演绎', '署名-相同方式共享', '署名')


SAERCHBASE = ("select work.wid,work.title,work.type,work.content,"
              "work.teammates,work.copysign,work.lable,work.time,"
              "work.view,work.support,work.review,work.cover,"
              "work.wdescribe,user.uid,user.img,user.account from "
              "work join user on work.author_id=user.uid")

USERSEARCH = ("select uid from user join basicinfo on user.uid="
              "basicinfo.bsc_id ")


ORDERS = ("view", "support", "review")


CONDITIONS = {
    "trade": "basicinfo.job like %s",
    "type": "work.type=%s ",
    "user": "user.status=%s ",
    "lable": "work.lable like %s"
}


'''
status for the work:

0 ---- secure publish

1 ---- unverifyed

2 ---- unsure

3 ---- verifyed

'''


class WorksHandler(BaseHandler):

    def get(self):
        schargs = self.request.uri.split("?")
        if len(schargs) < 2:
            schcond = []
        else:
            schcond = schargs[1].split("&")
        schsql = ""
        usrsql = ""
        wrkwhcond = ""
        usrwhcond = ""
        ordcond = ""
        args1 = []
        args2 = []
        for i in schcond:
            left, right = i.split("=")
            if left == "type":
                if int(right) > -1:
                    if not wrkwhcond:
                        wrkwhcond = "  "+CONDITIONS[left]
                    else:
                        wrkwhcond += " and "+CONDITIONS[left]
                    args2.append(right)
            elif left == "user":
                if int(right) > -1:
                    if not usrwhcond:
                        usrwhcond = " where "+CONDITIONS[left]
                    else:
                        usrwhcond += " and "+CONDITIONS[left]
                    args1.append(right)
            elif left == "trade":
                #print right, type(right)
                right = tornado.escape.url_unescape(right)
                #print right, type(right)
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
                if not wrkwhcond:
                    wrkwhcond = "  "+CONDITIONS[left]
                else:
                    wrkwhcond += " and "+CONDITIONS[left]
                args2.append(right)
            elif left == "hotsort":
                ordcond = " order by work."+ORDERS[int(right)-1]+" desc"
        if not ordcond:
            ordcond = " order by work.time desc"
        usrsql = USERSEARCH+usrwhcond
        if not usrwhcond:
            if wrkwhcond:
                wrkwhcond = " where "+wrkwhcond
        else:
            if wrkwhcond:
                wrkwhcond = " where user.uid in ("+usrsql+") and "+wrkwhcond
            else:
                wrkwhcond = " where user.uid in ("+usrsql+") "
        schsql = SAERCHBASE+wrkwhcond+ordcond
        print schsql, args1+args2
        rows = self.db.query(schsql, *(args1+args2))
        cuser = self.get_current_user()
        self.render("yoez1.0beta/work-search.html", cuser=cuser, rows=rows)


class UserWorksHandler(BaseHandler):

    def get(self, id):
        uid = int(id)
        cuser = self.get_current_user()
        type = int(self.get_argument("type", -1))
        worklist = {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 0}
        user = UserManager.get_user_basic(uid)
        if user is None:
            return self.write("sorry!the page you request does not exists.")
        rows = WorkManager.get_user_works(uid, type)
        worklist['-1'] = len(rows)
        for one in rows:
            worklist[one.type] += 1
            one.contet = one.content.replace("\'", "'")
        userself = cuser and (cuser.uid == uid)
        is_authenticate = int(user.status) == USER_STATUS["authenticate"]
        followed = False
        if not userself and cuser:
            flwsql = ("select * from follow where fid=%d and "
                      "flwid=%d") % (cuser.uid, uid)
            flwrst = self.db.get(flwsql)
            followed = flwrst and int(flwrst.relation)
        self.render("yoez1.0beta/homepage-people-show-1.html", cuser=cuser,
                    user=user, rows=rows, userself=userself,
                    is_auth=is_authenticate, followed=followed,
                    deftxt=DEFAULT_TEXT, worklist=worklist)


class WorkDetailHandler(BaseHandler):
    def get(self, id):
        wid = int(id)
        cuser = self.get_current_user()
        WorkManager.update_work_view(wid, 1)
        row = WorkManager.get_work_byid(wid)
        row.contet = row.content.replace("\'", "'")
        copysign = SUPORT_WORK_MARKS[int(row.copysign)]
        if(row.type == '1'):
            mid = re.search("([0-9]+)", row.content).group(0)
        else:
            mid = None
        is_follow = False
        if cuser:
            if cuser.uid == row.uid:
                is_follow = True
            else:
                flwsql = ("select * from follow where fid=%d and "
                          "flwid=%d") % (cuser.uid, row.uid)
                flwrst = self.db.get(flwsql)
                is_follow = flwrst and int(flwrst.relation)
        reviews = ReviewManager.get_work_reviews(wid)
        work = SUPORT_WORKS[int(row.type)]
        self.render("yoez1.0beta/work-content-"+work+".html", cuser=cuser,
                    row=row, copysign=copysign, mid=mid, is_follow=is_follow,
                    reviews=reviews)

    def post(self, id):
        wid = int(id)
        cuser = self.get_current_user()
        content = self.get_argument("rcontent")
        content = content.replace("'", "\'")
        at = time.strftime("%Y-%m-%d %X", time.localtime())
        ReviewManager.new_work_review(*(wid, cuser.uid, content, at))
        WorkManager.update_work_review(wid, 1)
        one = dict(uid=cuser.uid, img=cuser.img, account=cuser.account,
                   content=content.replace("\'", "'"), time=at)
        rmsg = self.render_string("modules/user_review_content.html", one=one)
        result = dict(status=1, msg=rmsg)
        self.write(result)


class UserPostVideoworkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url("/")
        self.render('editor1.0beta/editor-work-2.html', cuser=cuser, url=url)

    def post(self):
        cuid = self.get_secure_cookie("_yoez_uid")
        type = '0'
        values = self.get_values(('title', 'content', ('describe', ''),
                                  'cover', 'lable', 'copysign',
                                  ('teammates', '')))
        if not values:
            return self.write({'status': 0, 'code': "missing argument."})
        at = time.strftime("%Y-%m-%d %X", time.localtime())
        args = (cuid, type) + values + (at,)
        WorkManager.new_work(*args)
        result = dict(status=1, code='')
        self.write(result)


class UserPostMusicworkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url("/")
        self.render('editor1.0beta/editor-work-3.html', cuser=cuser, url=url)

    def post(self):
        cuid = self.get_secure_cookie("_yoez_uid")
        type = '1'
        values = self.get_values(('title', 'content', ('describe', ''),
                                  ('cover', ''), 'lable', 'copysign',
                                  ('teammates', '')))
        if not values:
            return self.write({'status': 0, 'code': "missing argument."})
        at = time.strftime("%Y-%m-%d %X", time.localtime())
        args = (cuid, type) + values + (at,)
        WorkManager.new_work(*args)
        result = dict(status=1, code='')
        self.write(result)


class UserPostArticleworkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url("/")
        self.render('editor1.0beta/editor-work-4.html', cuser=cuser, url=url)

    def post(self):
        cuid = self.get_secure_cookie("_yoez_uid")
        type = '3'
        values = self.get_values(('title', 'content', ('describe', ''),
                                  ('cover', ''), 'lable', 'copysign',
                                  ('teammates', '')))
        if not values:
            return self.write({'status': 0, 'code': "missing argument."})
        at = time.strftime("%Y-%m-%d %X", time.localtime())
        args = (cuid, type) + values + (at,)
        WorkManager.new_work(*args)
        result = dict(status=1, code='')
        self.write(result)


class UserPostPictureworkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        url = self.get_previous_url("/")
        self.render('editor1.0beta/editor-work-1.html', cuser=cuser, url=url)

    def post(self):
        cuid = self.get_secure_cookie("_yoez_uid")
        type = '2'
        values = self.get_values(('title', 'content', ('describe', ''),
                                  'cover', 'lable', 'copysign',
                                  ('teammates', '')))
        if not values:
            return self.write({'status': 0, 'code': "missing argument."})
        at = time.strftime("%Y-%m-%d %X", time.localtime())
        args = (cuid, type) + values + (at,)
        WorkManager.new_work(*args)
        result = dict(status=1, code='')
        self.write(result)


class WorksPicuploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        cuser = self.get_current_user()
        workdir = os.path.dirname(sys.argv[0])
        for i in self.request.files:
            print i
            fname, ext = os.path.splitext(self.request.files[i][0]["filename"])
            if ext.lower() not in SUPORT_IMAGES:
                result = dict(status=0, code="unsupport image type")
                print result
                return self.write(result)
            timestamp = time.strftime("%Y%m%d%X", time.localtime())
            fname = fname.encode("utf-8") + ext
            fname = md5(fname).hexdigest()
            fname += "."+ext
            path = "%s/static/img/user/%d/%s" % (workdir, cuser.uid, fname)
            try:
                f = file(path, "wb+")
                f.write(self.request.files[i][0]["body"])
                f.close()
                src = "/static/img/user/%d/%s" % (cuser.uid, fname)
                result = dict(status=1, path=src)
            except:
                result = dict(status=0, code="upload error!")
            finally:
                if f:
                    f.close()
            print result
            self.write(result)


class WorksMultiPicuploadHandler(BaseHandler):

    ''' The videowork'type is 1 and the picturework'type is 0 '''

    def check_xsrf_cookie(self):

        xsrf_cookie = self.get_argument("_xsrf_cookie", None)
        xsrf = self.get_argument("_xsrf", None)
        if xsrf is None or xsrf_cookie is None:
            err_msg = "_xsrf argument  missing from POST"
            raise tornado.web.HTTPError(403, err_msg)
        if xsrf_cookie != xsrf:
            err_msg = "USER cookie does not match POST argument"
            raise tornado.web.HTTPError(403, err_msg)

    def post(self):
        uid_value = self.get_argument("_yoez_uid", None)
        uid = self.get_secure_cookie("_yoez_uid", value=uid_value)
        if uid is None:
            err_msg = "_yoez_uid argument missing from POST"
            raise tornado.web.HTTPError(403, err_msg)
        cuser = UserManager.get_user_withid(uid)
        if cuser is None:
            raise tornado.web.HTTPError(403, "USER authenticated error!")
        workdir = os.path.dirname(sys.argv[0])
        for i in self.request.files:
            for j in self.request.files[i]:
                fname, ext = os.path.splitext(j["filename"])
                timestamp = time.strftime("%Y%m%d%X", time.localtime())
                fname = fname.encode("utf-8") + timestamp
                fname = md5(fname).hexdigest()
                fname += "."+ext
                path = "%s/static/img/user/%d/%s" % (workdir, cuser.uid, fname)
                try:
                    f = file(path, "wb+")
                    f.write(j["body"])
                    f.close()
                except:
                    result = dict(status=0, code="upload error!")
                finally:
                    if f:
                        f.close()
                src = "/static/img/user/%d/%s" % (cuser.uid, fname)
                result = dict(status=1, path=src)
                self.write(result)


class WorkDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self, wid):
        cuid = int(self.get_secure_cookie("_yoez_uid"))
        wid = int(wid)
        idx = self.get_argument("index")
        chksql = ("select wid from work where wid=%d and "
                  "author_id=%d") % (wid, cuid)
        chkrst = self.db.get(chksql)
        hdlrst = {}
        if chkrst:
            delsql = "delete from work where wid=%d" % wid
            self.db.execute(delsql)
            hdlrst = dict(status=1, index=idx, msg="delete success!")
        else:
            hdlrst = dict(status=0, msg="delete failure!")
        self.write(hdlrst)


HandlerList = [
    (r"/works", WorksHandler),
    #(r"/worksearch",WorkSearchHandler),
    (r"/([0-9]+)/works", UserWorksHandler),
    (r"/work/([0-9]+)", WorkDetailHandler),
    (r"/user/postwork/video", UserPostVideoworkHandler),
    (r"/user/postwork/music", UserPostMusicworkHandler),
    (r"/user/postwork/article", UserPostArticleworkHandler),
    (r"/user/postwork/picture", UserPostPictureworkHandler),
    (r"/user/works/picupload", WorksPicuploadHandler),
    (r"/user/works/multipicupload", WorksMultiPicuploadHandler),
    (r"/work/([0-9]+)/delete", WorkDeleteHandler),
    ]
