# -*- coding: utf-8 -*-

'''
This module is about user's homepage and profile.

Meanwhile, this may handle user's relationship.


'''


from __init__ import BaseHandler, USER_STATUS, DEFAULT_TEXT

import tornado.web

import re

from manage import WorkManager, UserManager, FollowManager


def formate_sanwei_str(swstr):

    if not swstr:
        return DEFAULT_TEXT
    sanwei_prefix = ['B/', 'W/', 'H/']
    sw = swstr.split('-')
    swlist = []
    for i, s in enumerate(sw):
        swlist.append(''.join((sanwei_prefix[i], s)))
    return ' '.join(swlist)


class UserSpaceHandler(BaseHandler):
    def get(self, id):
        uid = int(id)
        cuser = self.get_current_user()
        worklist = {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 0}
        user = UserManager.get_user_basic(uid)
        if not user:
            return self.html404()
        rows = WorkManager.get_user_works(uid)
        worklist['-1'] = len(rows)
        for one in rows:
            worklist[one.type] += 1
        userself = cuser and (cuser.uid == user.uid)
        followed = False
        if not userself and cuser:
            flwrst = FollowManager.get_user_relation(*(cuser.uid, uid))
            followed = flwrst and int(flwrst.relation)
        is_auth = int(user.status) == USER_STATUS["authenticate"]
        tips = self.get_tool_tips(('top', 'tip'))
        self.render('yoez1.0beta/homepage-people-show-1.html', user=user,
                    cuser=cuser, rows=rows, userself=userself,
                    followed=followed, is_auth=is_auth, tips=tips,
                    deftxt=DEFAULT_TEXT, worklist=worklist)


class UserPsldomainHandler(BaseHandler):

    def get(self, idf, ids):
        domain = idf+ids
        cuser = self.get_current_user()
        conrow = None
        if not conrow:
            return self.html404()
        user = UserManager.get_user_withid(conrow.con_id)
        if not user:
            return self.html404()
        rows = WorkManager.get_user_works(user.uid)
        userself = cuser and (cuser.uid == user.uid)
        worklist = {'-1': 0, '0': 0, '1': 0, '2': 0, '3': 0}
        tips = self.get_tool_tips(('top', 'tip'))
        self.render('yoez1.0beta/homepage-people-show-1.html', user=user,
                    cuser=cuser, rows=rows, conrow=conrow, userself=userself,
                    followed=False, worklist=worklist, tips=tips)


class UserMessageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cuser = self.get_current_user()
        msgs = []
        url = self.get_previous_url()
        self.render("user1.0beta/message-1.html", cuser=cuser, msgs=msgs,
                    url=url)


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
        user = UserManager.get_user_basic(cuser.uid)
        which = self.get_argument("type", "1")
        tips = self.get_tool_tips(('top', 'tip'))
        self.render("yoez1.0beta/homepage-people-focus-"+which+".html",
                    cuser=cuser, user=user, tips=tips)


class UserProfileHandler(BaseHandler):
    def get(self, id):
        followed = False
        sanweistr = ''
        uid = int(id)
        user = UserManager.get_full_basic(uid)
        if not user:
            return self.html404()
        cuser = self.get_current_user()
        userself = cuser and (user.uid == cuser.uid)
        contact = UserManager.get_contact_property(uid)
        is_authenticate = int(user.status) == USER_STATUS["authenticate"]
        if not userself and cuser:
            flwrst = FollowManager.get_user_relation(*(cuser.uid, uid))
            followed = flwrst and int(flwrst.relation)
        isw = int(contact.sex)
        if isw and user.extend:
            sanwei = user.extend.split("&")[0]
            sanweistr = formate_sanwei_str(sanwei)
        tips = self.get_tool_tips(('top', 'tip'))
        self.render("yoez1.0beta/homepage-people-info-1.html", user=user,
                    cuser=cuser, userself=userself, contact=contact,
                    is_auth=is_authenticate, followed=followed, tips=tips,
                    deftxt=DEFAULT_TEXT, isw=isw, sanweistr=sanweistr)


HandlerList = [
    (r"/([0-9]+)", UserSpaceHandler),
    #(r"/u/([^0-9/]+)([^/]+)", UserPsldomainHandler),
    (r"/user/message", UserMessageHandler),
    (r"/user/messages", UserMessagesHandler),
    (r"/user/focus", UserFocusHandler),
    (r"/([0-9]+)/profile", UserProfileHandler),
    ]
