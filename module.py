# -*- coding:utf-8 -*-

'''
This module rewrites many view submodules,
which are reused in other template files.

'''


import tornado.web
import time
import calendar

from __init__ import DEFAULT_TEXT, USER_STATUS

MonthList = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

WORKLICONTENT = ("<img src='cover' width='298' height='185'><span></span>",
                 "<span></span>", "<img src='cover' width='298' height='185'>",
                 "<p>content</p>")

WORKLIKEY = ("cover", "title", "cover", "content")

WORKTYPEKEY = ('video', 'voice', 'pic', 'txt')

EVENTLIKEY = ("公益参与", "通告媒体", "获奖荣誉", "机构招募", "发表声明",
              "媒体报道", "经验分享", "赛事活动", "官方发布")

MESSAGES = ("系统消息", "回复通知", "商业消息")

MESSAGECLASS = ("system", "reply", "other")


class UserModule(tornado.web.UIModule):

    def render(self, cuser, wh='/', dftmsg=0):
        init = cuser and (cuser.status >= USER_STATUS["normal"])
        #print init
        kwargs = dict(cuser=cuser, wh=wh, msg=dftmsg, level=init)
        return self.render_string('modules/yoez_user.html', **kwargs)


class IndexRecordliModule(tornado.web.UIModule):

    def render(self, l):

        kwargs = dict(type=EVENTLIKEY[int(l.type)], l=l)
        return self.render_string("modules/index_record_li.html", **kwargs)


class IndexReviewliModule(tornado.web.UIModule):

    def render(self, rvl):

        return self.render_string("modules/index_review_li.html", rvl=rvl)


class UeHeaderModule(tornado.web.UIModule):

    def render(self, cuser, url='/', dftmsg=0):

        kwargs = dict(cuser=cuser, url=url, msg=dftmsg)
        return self.render_string('modules/yoez_header.html', **kwargs)


class SettingHeaderModule(tornado.web.UIModule):

    def render(self, cuser, url='/', dftmsg=0):

        kwargs = dict(cuser=cuser, url=url, msg=dftmsg)
        return self.render_string('modules/setting_header.html', **kwargs)


class UeEditorHeaderModule(tornado.web.UIModule):

    def render(self, url='/'):

        return self.render_string('modules/yoez_editor_header.html', url=url)


class EventSearchliModule(tornado.web.UIModule):

    def render(self, row):
        type = EVENTLIKEY[int(row.type)]
        if int(row.type) == 3:
            row.place = row.place.split("&")[1]
        if row.picture:
            row.picture = row.picture.split(";")
            j = min(len(row.picture), 2)
        else:
            j = 0
        kwargs = dict(row=row, type=type, j=j)
        return self.render_string('modules/event_search_content.html',
                                  **kwargs)


class UserEventliModule(tornado.web.UIModule):

    def render(self, row):

        return self.render_string('modules/user_event_content.html', row=row)


class UserSearchliModule(tornado.web.UIModule):

    def render(self, row):

        return self.render_string('modules/user_search_content.html',
                                  row=row, deftxt=DEFAULT_TEXT)


class UserReviewliModule(tornado.web.UIModule):

    def render(self, one):

        return self.render_string('modules/user_review_content.html', one=one)


class EventHomepageliModule(tornado.web.UIModule):

    def render(self, row, userself):
        i = int(row.type)
        type = EVENTLIKEY[i]
        if i == 3:
            row.place = row.place.split("&")[1]
            row.content = row.content.split(";")[0].split("&")[1]
        curtime = time.strftime("%Y:%m:%d %X", time.localtime())
        if row.time > curtime:
            bgclsname = "yz-hp-event-nohappened"
        else:
            bgclsname = "yz-hp-event-happened"
        return self.render_string('modules/event_homepage_content.html',
                                  row=row, type=type, userself=userself,
                                  bgclsname=bgclsname)


class MainFooterModule(tornado.web.UIModule):

    def render(self, tips):

        return self.render_string("modules/main_footer.html", tips=tips)


class WhiteFooterModule(tornado.web.UIModule):

    def render(self):

        return self.render_string("modules/white_footer.html")


class BlackFooterModule(tornado.web.UIModule):

    def render(self, user, tips):

        return self.render_string("modules/black_footer.html", user=user,
                                  tips=tips)


class HomepageContentModule(tornado.web.UIModule):

    def render(self, user, userself=True, followed=False):

        return self.render_string("modules/homepage_content.html", user=user,
                                  followed=followed, userself=userself)


class UserMessageModule(tornado.web.UIModule):

    def render(self, msg):

        return self.render_string('modules/user_message_content.html', msg=msg,
                                  msgtype=MESSAGES[int(msg.type)],
                                  msgclstype=MESSAGECLASS[int(msg.type)])


class WorkSearchliModule(tornado.web.UIModule):

    def render(self, row):
        i = int(row.type)
        j = WORKLIKEY[i]
        content = WORKLICONTENT[i].replace(WORKLIKEY[i], row[j])
        typeclass = WORKTYPEKEY[i]
        return self.render_string('modules/work_search_content.html', row=row,
                                  content=content, typeclass=typeclass)


class WorkHomepageliModule(tornado.web.UIModule):

    def render(self, row, userself):
        i = int(row.type)
        j = WORKLIKEY[i]
        content = WORKLICONTENT[i].replace(WORKLIKEY[i], row[j])
        typeclass = WORKTYPEKEY[i]
        return self.render_string('modules/work_homepage_content.html',
                                  row=row, content=content,
                                  typeclass=typeclass, userself=userself)


class MessageModule(tornado.web.UIModule):

    def render(self, msg):

        return self.render_string('modules/message_content.html', msg=msg)


class CalendarModule(tornado.web.UIModule):

    def render(self, year=None, month=None):
        if(not year):
            year = time.localtime()[0]
        if(not month):
            month = time.localtime()[1]
        mchr = MonthList[month-1]
        cld = calendar.Calendar(0)
        itm = cld.itermonthdates(year, month)
        begin = calendar.monthrange(year, month)[0]
        cal = []
        for i in itm:
            if(i.month == month):
                cal.append(i.day)
        mon = ''
        if(month < 10):
            mon = '0'+str(month)
        else:
            mon = str(month)
        return self.render_string("modules/calendar.html", year=year, mon=mon,
                                  cal=cal, begin=begin, mchr=mchr)


class UeDescribeModule(tornado.web.UIModule):

    def render(self):

        thisyear = time.localtime().tm_year
        return self.render_string('modules/ue_describe_content.html',
                                  thisyear=thisyear)


class UeDocprotocolModule(tornado.web.UIModule):

    def render(self):

        return self.render_string('modules/ue_docprotocol_content.html')


class UeAddlableModule(tornado.web.UIModule):

    def render(self, tiptext=''):

        return self.render_string('modules/ue_addlable_content.html',
                                  tiptext=tiptext)


class RecentpostModule(tornado.web.UIModule):

    def render(self):

        return self.render_string('modules/recentpost_content.html')


class SetlistModule(tornado.web.UIModule):

    def render(self):

        return self.render_string('modules/setlist_content.html')


class EditorUploadpicModule(tornado.web.UIModule):

    def render(self, tiptxt=""):

        return self.render_string('modules/editor_uploadpicture.html',
                                  tiptxt=tiptxt)


class EditorUploadvideoModule(tornado.web.UIModule):

    def render(self, is_change=False):

        return self.render_string('modules/editor_uploadvideo.html',
                                  is_change=is_change)


modules = dict(
    User=UserModule,
    Header=UeHeaderModule,
    EventSearch=EventSearchliModule,
    EventHomepage=EventHomepageliModule,
    UserEvent=UserEventliModule,
    UserSearch=UserSearchliModule,
    UserReview=UserReviewliModule,
    UserMeaage=UserMessageModule,
    WorkSearch=WorkSearchliModule,
    WorkHomepage=WorkHomepageliModule,
    Calendar=CalendarModule,
    MainFooter=MainFooterModule,
    WhiteFooter=WhiteFooterModule,
    BlackFooter=BlackFooterModule,
    HomepageContent=HomepageContentModule,
    Message=MessageModule,
    UeDescribe=UeDescribeModule,
    EditorHeader=UeEditorHeaderModule,
    UeDocprotocol=UeDocprotocolModule,
    UeAddlable=UeAddlableModule,
    Recentpost=RecentpostModule,
    Setlist=SetlistModule,
    EditorUploadpic=EditorUploadpicModule,
    EditorUploadvideo=EditorUploadvideoModule,
    SettingHeader=SettingHeaderModule,
    IndexRecordli=IndexRecordliModule,
    IndexReviewli=IndexReviewliModule,
    )
