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
from tornado import database

from email.mime.text import MIMEText

from getpass import getpass

import PIL.Image


#mysql define

define("mysql_host", default="127.0.0.1:3306", help="ueue database host")
define("mysql_database", default="yoez", help="ueue database name")
define("mysql_user", default="justdoit", help="ueue database user")
define("mysql_password", default=None, help="ueue database password")

# define site server hosts

ADMIN_HOST = "siteadmin.ueue.cc"

WEB_HOST = "www.ueue.cc"

STATIC_HOST = "static.ueue.cc"

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


# define authorize options

AUTHORIZE_OPTIONS = {
    "0": "授权公开",
    "1": "仅对我关注的人公开",
    "2": "保密"
    }

# define default show text

DEFAULT_TEXT = "未被授权显示"

#rewrite requesthandler

USER_CACHE = dict()


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):

        self.db = database.Connection(host=options.mysql_host,
                                      user=options.mysql_user,
                                      database=options.mysql_database,
                                      password=options.mysql_password)

    @property
    def is_db_connected(self):

        return self.db is not None

    def get_current_user(self):

        cuser = self.get_secure_cookie("_yoez_uid")
        if(cuser):
            user_sql = ("select account,uid,img,status,time from user "
                        "where uid=%s")
            user = self.db.get(user_sql, cuser)
            #USER_CACHE[cuser]=user
            return user
        else:
            return None

    def clear_current_user(self):

        self.clear_cookie("_yoez_uid")

    def get_dynum(self, user):
        dnum = 0
        sql = ("select COUNT(id) as nid from dynamic where dyner='%s' "
               "and handle=0")
        dyn = self.db.get(sql, user)
        if(dyn):
            dnum = dyn.nid
        return dnum


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


#get the database password from the terminal

def initdbpsw():

    options.mysql_password = getpass("User database password:")
    print "init database connection"
    options.noreply_password = getpass("User noreply email password:")


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
