# -*- coding: utf-8 -*-

'''
This module is about user's homepage and profile.

Meanwhile, this may handle user's relationship.


'''


from __init__ import BaseHandler, USER_STATUS, DEFAULT_TEXT

import tornado.web

import re


class UserSpaceHandler(BaseHandler):
    def get(self, id):
        uid = int(id)
        cuser = self.get_current_user()
        worklist = {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 0}
        user_sql = "select * from user where uid=%d" % uid
        user = self.db.get(user_sql)
        if not user:
            return self.write('sorry!the page you request does not exists.')
        event_sql = ("select * from user join work on work.author_id=user.uid "
                     "where work.author_id=%d order by work.time desc") % uid
        contact_sql = ("select * from contactinfo join basicinfo on "
                       "con_id=bsc_id where con_id=%d") % uid
        rows = self.db.query(event_sql)
        conrow = self.db.get(contact_sql)
        worklist['-1'] = len(rows)
        for one in rows:
            worklist[one.type] += 1
        userself = cuser and (cuser.uid == user.uid)
        followed = False
        if not userself and cuser:
            flwsql = ("select * from follow where fid=%d and "
                      "flwid=%d") % (cuser.uid, uid)
            flwrst = self.db.get(flwsql)
            followed = flwrst and int(flwrst.relation)
        is_authenticate = int(user.status) == USER_STATUS["authenticate"]
        self.render('yoez1.0beta/homepage-people-show-1.html', user=user,
                    cuser=cuser, rows=rows, conrow=conrow, userself=userself,
                    followed=followed, is_auth=is_authenticate,
                    deftxt=DEFAULT_TEXT, worklist=worklist)


class UserPsldomainHandler(BaseHandler):

    def get(self, idf, ids):
        domain = idf+ids
        cuser = self.get_current_user()
        usersql = ("select * from contactinfo join basicinfo on con_id=bsc_id "
                   "where psldomain='%s'") % domain
        conrow = self.db.get(usersql)
        if not conrow:
            return self.write('sorry!the page you request does not exists.')
        usersql = "select * from user where uid=%d" % conrow.con_id
        user = self.db.get(usersql)
        if not user:
            return self.write('sorry!the page you request does not exists.')
        event_sql = ("select * from user join work on work.author_id"
                     "=user.uid where work.author_id=%d order by "
                     "work.time desc") % user.uid
        rows = self.db.query(event_sql)
        userself = cuser and (cuser.uid == user.uid)
        worklist = {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 0}
        self.render('yoez1.0beta/homepage-people-show-1.html', user=user,
                    cuser=cuser, rows=rows, conrow=conrow, userself=userself,
                    followed=False, worklist=worklist)


class UserMessageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        msgsql = "select * from message where muid=%d" % cuser.uid
        msgs = self.db.query(msgsql)
        self.render("user1.0beta/message-1.html", cuser=cuser, msgs=msgs)


class UserMessagesHandler(BaseHandler):

    '''The msgtype 0 for newmsg(default),1 for systemmsg,
    2 for replymsg and 3 for commercialmsg'''

    @tornado.web.authenticated
    def get(self):
        msgtype = self.get_argument("msgtype", "0")
        #self.render("user1.0beta/message-1.html",cuser=cuser)


class UserFocusHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        which = self.get_argument("type", "1")
        basicsql = ("select * from basicinfo join property on basicinfo.bsc_id"
                    "=property.proper_id where bsc_id=%d") % cuser.uid
        basic = self.db.get(basicsql)
        self.render("yoez1.0beta/homepage-people-focus-"+which+".html",
                    cuser=cuser, basic=basic)


class UserProfileHandler(BaseHandler):
    def get(self, id):
        followed = False
        sanwei = None
        uid = int(id)
        cuser = self.get_current_user()
        user_sql = ("select * from user join contactinfo on user.uid="
                    "contactinfo.con_id where user.uid=%d") % uid
        user = self.db.get(user_sql)
        if not user:
            return self.write('sorry!the page you request does not exists.')
        userself = cuser and (user.uid == cuser.uid)
        basicsql = ("select * from basicinfo join property on basicinfo."
                    "bsc_id=property.proper_id where bsc_id=%d") % uid
        basic = self.db.get(basicsql)
        is_authenticate = int(user.status) == USER_STATUS["authenticate"]
        if not userself and cuser:
            flwsql = ("select * from follow where fid=%d and "
                      "flwid=%d") % (cuser.uid, uid)
            flwrst = self.db.get(flwsql)
            followed = flwrst and int(flwrst.relation)
        if basic.extend:
            sanwei = basic.extend.split("&")[0]
            if sanwei:
                sanwei = sanwei.split("-")
        #print sanwei
        self.render("yoez1.0beta/homepage-people-info-1.html", user=user,
                    cuser=cuser, userself=userself, basic=basic,
                    is_auth=is_authenticate, followed=followed,
                    deftxt=DEFAULT_TEXT, sanwei=sanwei)


HandlerList = [
    (r"/([0-9]+)", UserSpaceHandler),
    (r"/u/([^0-9/]+)([^/]+)", UserPsldomainHandler),
    (r"/user/message", UserMessageHandler),
    (r"/user/messages", UserMessagesHandler),
    (r"/user/focus", UserFocusHandler),
    (r"/([0-9]+)/profile", UserProfileHandler),
    ]
