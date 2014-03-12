# -*- coding:utf-8 -*-

'''This module provides many operations on the database server.'''

__version__ = '0.0.1'

from tornado import database

from tornado.options import define, options

import logging


def create_connection(**kwargs):

    '''keys in argument kwargs.
    host: mysql server host's ip address or name
    database: use a database in mysql server
    user: user connect to mysql server
    passwrod: user's password connect to mysql server
    max_idle_time: max idle time for a connection
    '''

    return database.Connection(**kwargs)


class WorkManager:

    @staticmethod
    def get_latest_works(limit, offset=None):

        args = [limit]
        worksql = ("select W.wid,W.title,W.type,W.content,W.teammates,"
                   "W.copysign,W.lable,W.time,W.view,W.review,W.support,"
                   "W.cover,W.wdescribe,U.uid,U.img,U.account from user "
                   "as U join work as W on W.author_id=U.uid order by "
                   "W.time desc limit %s")
        if offset is not None:
            args.insert(0, offset)
            worksql = worksql + ",%s"
        try:
            con = create_connection(**options.dbsettings)

            return con.query(worksql, *args)
        except:

            return None

    @staticmethod
    def get_work():

        pass


class RecordManager:

    @staticmethod
    def get_recordlist(uid, type=-1):

        '''Get user's records'''

        args = [uid]

        if(type > -1):
            args.append(type)
            sql = ("select E.eid,E.title,E.content,E.type,E.place,E.lable,"
                   "E.time from event as E where E.author_id=%s and E.type=%s "
                   "order by E.time desc")
        else:
            sql = ("select E.eid,E.title,E.content,E.type,E.place,E.lable,"
                   "E.time from event as E where E.author_id=%s order by "
                   "E.time desc")
        try:

            con = create_connection(**options.dbsettings)

            return con.query(sql, *args)

        except:
            return None

    @staticmethod
    def get_latest_records(limit, offset=None):

        '''Get latest records'''

        args = [limit]

        sql = ("select U.uid,U.account,E.eid,E.title,E.type,E.time from user "
               "as U join event as E on U.uid=E.author_id order by E.time "
               "limit %s")
        if offset is not None:

            args.insert(0, offset)
            sql += ",%s"
        try:

            con = create_connection(**options.dbsettings)
            return con.query(sql, *args)
        except:

            return None

    @staticmethod
    def get_user_record(rid):

        sql = ("select U.uid,U.account,U.img,E.title,E.content,E.picture,"
               "E.lable,E.type,E.view,E.review,E.support,E.time from user "
               "as U join event as E on U.uid=E.author_id where E.eid=%s")
        try:

            con = create_connection(**options.dbsettings)

            return con.get(sql, rid)

        except:

            return None


class UserManager:

    @staticmethod
    def has_user(uid):
        '''check the user exists'''

        sql = "select uid from user where uid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.get(con, uid)

        except:

            return None

    @staticmethod
    def get_user_withid(uid):

        sql = ("select uid,account,img,status,email,password,status,time from "
               "user where uid=%s")

        try:
            con = create_connection(**options.dbsettings)

            return con.get(sql, uid)
        except:

            return None

    def get_user_withmail(mail):

        sql = ("select uid,account,img,status,password,status from user "
               "where email=%s")

        try:
            con = create_connection(**options.dbsettings)

            return con.get(sql, mail)
        except:

            return None


class ReviewManager:

    @staticmethod
    def get_latest_reviews(limit, offset=None):

        args = [limit]

        sql = ("select U.uid,U.account,ER.content,ER.time from eventreview as "
               "ER join user as U on ER.reviewuid=U.uid order by ER.time desc "
               "limit %s")
        if offset is not None:
            sql += ",%s"
            args.insert(0, offset)
        try:

            con = create_connection(**options.dbsettings)
            return con.query(sql, *args)
        except:

            return None
