# -*- coding: utf-8 -*-

'''
This is a init module.Define some data and function for future use.

'''

__version__ = "0.0.1"

import tornado.web
from tornado.options import define, options
import sys
import smtplib
import os
import email.utils

from email.mime.text import MIMEText

from getpass import getpass

import PIL.Image

import manage

import logging

define("mysql_host", default="127.0.0.1:3306", help="ueue database host")
define("mysql_database", default="yoez", help="ueue database name")
define("mysql_user", default="justdoit", help="ueue database user")
define("mysql_password", default='', help="ueue database password")
define("dbsettings", default={}, help="ueue database settings", type=dict)
define("noreply_password",
       default='', help="signup email check account password")

define("server_port0", default=10000, help="run on the given port", type=int)
define("server_port1", default=10001, help="run on the given port", type=int)
define("server_port2", default=10002, help="run on the given port", type=int)
define("server_port3", default=10003, help="run on the given port", type=int)
define("pidfile", default=None, help="pid file for the daemon process",
       type=str)


define("userstatus", default={}, help="user status dict", type=dict)
# define site server hosts

ROOT_HOST = "ueue.cc"

ROOT_URL = "http://ueue.cc/"

ADMIN_HOST = "siteadmin.ueue.cc"

ADMIN_URL = "http://siteadmin.ueue.cc/"

WEB_HOST = "www.ueue.cc"

WWW_URL = "http://www.ueue.cc/"

STATIC_HOST = "static.ueue.cc"

STATIC_URL = "http://static.ueue.cc/"

IMAGE_HOST = "iamge1.ueue.cc"

IMAGE_URL = "http://image1.ueue.cc/"

# define the userstatus table

USER_STATUS = {
    "unactive": 0,
    "lock": 1,
    "uninit": 2,
    "normal": 3,
    "infoset": 4,
    "unauthenticate": 5,
    "authenticate": 6
    }

# define profession table

userprofessions = {
    "0": "a",
    "1": "b",
    "2": "c",
    "3": "d",
    "4": "e",
    "5": "f"
    }


# define tooltips

TOOL_TIPS = {
    'top': '<a href="#" title="回到顶部" id="ue-main-gotop"></a>',
    'tip': '<a href="#" title="侵权举报" id="ue-main-tip"></a>',
    'edit': '<a href="#" title="编辑" id="ue-main-edit"></a>',
    'del': '<a href="#" title="删除" id="ue-main-del"></a>',
    'open': '<a href="#" title="设置为公开" id="ue-main-open"></a>',
    'close': '<a href="#" title="设置为保密" id="ue-main-close"></a>'
    }


# define authorize options

AUTHORIZE_OPTIONS = {
    "0": "授权公开",
    "1": "仅对我关注的人公开",
    "2": "保密"
    }

# define default show text

DEFAULT_TEXT = "未被授权显示"

# define www cookie domain

WWW_COOKIE_DOMAIN = "www.ueue.cc"


#rewrite requesthandler


class BaseHandler(tornado.web.RequestHandler):

    def html404(self):

        cuser = self.get_current_user()
        rows = manage.WorkManager.get_latest_works(30)
        ls = manage.RecordManager.get_latest_records(4)
        rvls = manage.ReviewManager.get_latest_workreviews(4)
        tips = self.get_tool_tips(('top', 'tip'))
        kwargs = dict(cuser=cuser, sf=self, rows=rows, ls=ls, rvls=rvls,
                      tips=tips)
        self.render("yoez1.0beta/404.html", **kwargs)

    def get_user_cookie(self, cookie):

        return self.get_secure_cookie(cookie)

    def get_current_user(self):

        cuser = self.get_user_cookie("_yoez_uid")
        if cuser:
            user = manage.UserManager.get_user_withid(cuser)
            return user
        else:
            return None

    def clear_current_user(self):

        self.clear_cookie("_yoez_uid", domain=WWW_COOKIE_DOMAIN)

    def get_values(self, names):

        '''get values of item in names list.'''

        values = []
        for name in names:
            kwargs = {}
            if isinstance(name, tuple):
                if len(name) > 1:
                    kwargs['default'] = name[1]
                arg = name[0]
            else:
                arg = name
            try:
                value = self.get_argument(arg, **kwargs)
                values.append(value)
                if 'default' in kwargs:
                    kwargs.pop('default')
            except:
                logging.error("get argument %s's value error" % arg)
                return ()
        return tuple(values)

    def get_previous_url(self, default=WWW_URL):

        '''use the Referer in http header to indicate the previous url'''

        url = self.request.headers.get("Referer", default)
        if url.find(ROOT_HOST) == -1:
            url = default
        return url

    def get_tool_tips(self, tiplist):

        tl = []
        for t in tiplist:
            tl.append(TOOL_TIPS[t])
        return '\n'.join(tl)


#send email

def send(fr, to, sub, msg, passwd=None):

    mail = MIMEText(msg, 'html', 'utf-8')
    mail["from"] = fr
    mail["to"] = to
    mail["Subject"] = sub.decode("utf-8")
    mail["Date"] = email.utils.formatdate(localtime=1)
    mail["Message-ID"] = email.utils.make_msgid()
    message = mail.as_string()
    user, server = fr.split('@')
    server = "smtp."+server
    print user, server
    try:
        s = smtplib.SMTP(host=server)
        #s.starttls()
        if passwd is None:
            passwd = options.noreply_password
        s.login(fr, passwd)
        s.sendmail(fr, to, message)
        s.quit()
    except Exception, e:
        print e


def initconfig(path):

    '''init the options with the config file'''

    tornado.options.parse_config_file(path)
    tornado.options.parse_command_line()
    options.dbsettings = {
        'host': options.mysql_host,
        'database': options.mysql_database,
        'user': options.mysql_user,
        'password': options.mysql_password,
    }
    options.userstatus = USER_STATUS


#set image size

def set_image_size(size, img):
    path = os.path.dirname(sys.argv[0])+img
    #print path
    try:
        im = PIL.Image.open(path)
        wh = im.size[0]
        hg = im.size[1]
        if wh*1.0/hg < size[0]*1.0/size[1]:
            nwh = size[0]
            nhg = int(hg/(wh*1.0/nwh))
        else:
            nhg = size[1]
            nwh = int(wh/(hg*1.0/nhg))
        #print im
        im.thumbnail((nwh, nhg))
        im.save(path, im.format, quality=100)
        nwh = im.size[0]
        nhg = im.size[1]
        if nwh > nhg:
            start = ((nwh-200)/2, 0)
        else:
            start = (0, (nhg-200)/2)
        im = im.crop((start[0], start[1], size[0]+start[0], size[1]+start[1]))
        im.save(path, im.format, quality=100)
        #print im
        return True
    except:
        print "set image size error."
        return False
