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


def formate_errmsg(args):

    if isinstance(args, str):

        return args
    msg = [str(arg) for arg in args]

    return " ".join(args)


def log_mysql_error(args):

    if args:

        error_prefix = "mysql error " + str(args[0]) + ": "

        error_msg = error_prefix + formate_errmsg(args[1:])

        logging.error(error_msg)


def do_query_request(sql, *args):

    '''do real db request with sql and args'''

    try:
        con = create_connection(**options.dbsettings)
        return con.query(sql, *args)
    except Exception, e:

        log_mysql_error(e)
        return None


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
            worksql = ','.join((worksql, '%s'))
        return do_query_request(worksql, *args)

    @staticmethod
    def get_work_byid(wid):

        sql = ("select W.wid,W.title,W.type,W.content,W.teammates,"
               "W.copysign,W.lable,W.time,W.view,W.review,W.support,"
               "W.cover,W.wdescribe,U.uid,U.img,U.account from user "
               "as U join work as W on W.author_id=U.uid where W.wid=%s")
        try:

            con = create_connection(**options.dbsettings)
            return con.get(sql, wid)
        except Exception, e:

            log_mysql_error(e)
            return None

    @staticmethod
    def get_user_works(uid, type=-1):

        args = [uid]
        if type == -1:
            sql = ("select W.wid,W.title,W.type,W.content,W.teammates,"
                   "W.copysign,W.lable,W.time,W.view,W.review,W.support,"
                   "W.cover,W.wdescribe,U.uid,U.img,U.account from user "
                   "as U join work as W on W.author_id=U.uid where U.uid=%s"
                   " order by W.time desc")
        else:
            sql = ("select W.wid,W.title,W.type,W.content,W.teammates,"
                   "W.copysign,W.lable,W.time,W.view,W.review,W.support,"
                   "W.cover,W.wdescribe,U.uid,U.img,U.account from user "
                   "as U join work as W on W.author_id=U.uid where U.uid=%s"
                   " and W.type=%s order by W.time desc")
            args.append(type)
        return do_query_request(sql, *args)

    @staticmethod
    def update_work_view(wid, num):

        sql = "update work set view=view+%s where wid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.execute(sql, *(num, wid))

        except Exception, e:

            log_mysql_error(0)
            return 0

    @staticmethod
    def update_work_review(wid, num):

        sql = "update work set review=review+%s where wid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.execute(sql, *(num, wid))

        except Exception, e:

            log_mysql_error(0)
            return 0

    @staticmethod
    def update_work_support(wid, num):

        sql = "update work set support=support+%s where wid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.execute(sql, *(num, wid))

        except Exception, e:

            log_mysql_error(0)
            return 0

    @staticmethod
    def new_work(*args):

        sql = ("insert into work (author_id,type,title,content,wdescribe,"
               "cover,lable,copysign,teammates,time) values(%s,%s,%s,%s,%s,"
               "%s,%s,%s,%s,%s)")

        try:
            con = create_connection(**options.dbsettings)
            return con.execute(sql, *args)
        except Exception, e:

            log_mysql_error(e)
            return 0


class RecordManager:

    @staticmethod
    def get_user_records(uid, type=-1):

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
        return do_query_request(sql, *args)

    @staticmethod
    def get_latest_records(limit, offset=None):

        '''Get latest records'''

        args = [limit]

        sql = ("select U.uid,U.account,E.eid,E.title,E.type,E.time from user "
               "as U join event as E on U.uid=E.author_id order by E.time "
               "limit %s")
        if offset is not None:

            args.insert(0, offset)
            sql = ','.join((sql, '%s'))
        return do_query_request(sql, *args)

    @staticmethod
    def get_record_byid(rid):

        sql = ("select U.uid,U.account,U.img,E.title,E.content,E.picture,"
               "E.lable,E.type,E.view,E.review,E.support,E.time from user "
               "as U join event as E on U.uid=E.author_id where E.eid=%s")
        try:

            con = create_connection(**options.dbsettings)

            return con.get(sql, rid)

        except Exception, e:
            log_mysql_error(e)
            return None

    @staticmethod
    def update_record_view(rid, num):

        sql = "update event set view=view+%s where eid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.execute(sql, *(num, rid))

        except Exception, e:

            log_mysql_error(0)
            return 0

    @staticmethod
    def update_record_review(rid, num):

        sql = "update event set review=review+%s where eid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.execute(sql, *(num, rid))

        except Exception, e:

            log_mysql_error(0)
            return 0

    @staticmethod
    def update_record_support(rid, num):

        sql = "update event set support=support+%s where eid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.execute(sql, *(num, rid))

        except Exception, e:

            log_mysql_error(0)
            return 0

    @staticmethod
    def new_record(*args):

        sql = ("insert into event (author_id,type,title,content,picture,place,"
               "lable,time) values(%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            con = create_connection(**options.dbsettings)

            return con.execute(*args)
        except Exception, e:
            log_mysql_error(e)
            return 0


class UserManager:

    @staticmethod
    def has_user(uid):
        '''check the user exists'''

        sql = "select uid from user where uid=%s"

        try:

            con = create_connection(**options.dbsettings)

            return con.get(con, uid)

        except Exception, e:
            log_mysql_error(e)
            return None

    @staticmethod
    def get_user_withid(uid):

        sql = ("select uid,account,img,status,email,password,status,time from "
               "user where uid=%s")

        try:
            con = create_connection(**options.dbsettings)

            return con.get(sql, uid)
        except Exception, e:
            log_mysql_error(e)
            return None

    @staticmethod
    def get_user_withmail(mail):

        sql = ("select uid,account,img,status,password,status from user "
               "where email=%s")

        try:
            con = create_connection(**options.dbsettings)

            return con.get(sql, mail)
        except Exception, e:
            log_mysql_error(e)
            return None

    @staticmethod
    def get_pro_users():

        sql = ("select U.uid,U.account,U.img,U.status,U.time,BI.job,BI.area "
               "from user as U join basicinfo as BI on U.uid=BI.bsc_id where "
               "U.status >= %s")
        return do_query_request(sql, options.userstatus['infoset'])

    @staticmethod
    def get_latest_users(limit, offset=None):

        args = [options.userstatus['normal'], limit]
        sql = ("select uid,account,img from user where status >= %s order by "
               "time limit %s")
        if offset:
            args.insert(1, offset)
            sql = ','.join((sql, '%s'))
        return do_query_request(sql, *args)

    @staticmethod
    def new_user(*args):

        sql = ("insert into user(uid,account,email,password,img,"
               "time,code) values (%s,%s,%s,%s,%s,%s,%s)")
        try:
            con = create_connection(**options.dbsettings)
            return con.execute(sql, *args)
        except Exception, e:

            log_mysql_error(e)
            return 0

    @staticmethod
    def get_user_basic(uid):

        sql = ("select U.uid,U.account,U.img,U.status,U.time,BI.job,BI.area "
               "from user as U join basicinfo as BI on U.uid=BI.bsc_id where "
               "U.uid=%s")
        try:
            con = create_connection(**options.dbsettings)
            return con.get(sql, uid)
        except Exception, e:

            log_mysql_error(e)
            return None

    @staticmethod
    def get_full_basic(uid):

        sql = ("select U.uid,U.account,U.img,U.status,U.time,BI.uname,BI.job,"
               "BI.area,BI.organ,BI.height,BI.weight,BI.birth,BI.extend from "
               "user as U join basicinfo as BI on U.uid=BI.bsc_id where "
               "U.uid=%s")
        try:
            con = create_connection(**options.dbsettings)
            return con.get(sql, uid)
        except Exception, e:

            log_mysql_error(e)
            return None

    @staticmethod
    def get_contact_property(uid):

        sql = ("select CI.telphone,CI.conmail,CI.conaddress,P.ptype,P.sex "
               "from contactinfo as CI join property as P on "
               "CI.con_id=P.proper_id where CI.con_id=%s")
        try:
            con = create_connection(**options.dbsettings)
            return con.get(sql, uid)
        except Exception, e:
            log_mysql_error(e)
            return None


class ReviewManager:

    @staticmethod
    def get_latest_reviews(limit, offset=None):

        args = [limit]

        sql = ("select U.uid,U.account,ER.content,ER.time from eventreview as "
               "ER join user as U on ER.reviewuid=U.uid order by ER.time desc "
               "limit %s")
        if offset is not None:
            sql = ','.join((sql, '%s'))
            args.insert(0, offset)
        return do_query_request(sql, *args)

    @staticmethod
    def new_record_review(*args):

        sql = ("insert into eventreview (revieweid,reviewuid,content,time "
               "values(%s,%s,%s,%s)")
        try:
            con = create_connection(**options.dbsettings)

            return con.execute(sql, *args)
        except Exception, e:
            log_mysql_error(e)
            return 0

    @staticmethod
    def get_record_reviews(rid):

        sql = ("select ER.content,ER.time,U.uid,U.account,U.img from "
               "eventreview as ER join user as U on ER.reviewuid=U.uid "
               "where ER.revieweid=%s")
        return do_query_request(sql, rid)

    @staticmethod
    def new_work_review(*args):

        sql = ("insert into workreview (reviewwid,reviewuid,content,time "
               "values(%s,%s,%s,%s)")
        try:
            con = create_connection(**options.dbsettings)

            return con.execute(sql, *args)
        except Exception, e:
            log_mysql_error(e)
            return 0

    @staticmethod
    def get_work_reviews(wid):

        sql = ("select WR.content,WR.time,U.uid,U.account,U.img from "
               "workreview as WR join user as U on WR.reviewuid=U.uid "
               "where WR.reviewwid=%s")
        return do_query_request(sql, wid)


class ViewManager:

    @staticmethod
    def user_view_record(uid, rid):

        sql = ("select viewuid from eventview where vieweid=%s and "
               "viewuid=%s")
        try:
            con = create_connection(**options.dbsettings)
            return con.get(sql, *(rid, uid))
        except Exception, e:
            log_mysql_error(e)
            return None

    @staticmethod
    def new_record_view(*args):

        sql = ("insert into eventview (vieweid,viewuid,time) values(%s,%s,%s)")
        try:
            con = create_connection(**options.dbsettings)
            return con.execute(sql, *args)
        except Exception, e:
            log_mysql_error(e)
            return 0

    @staticmethod
    def new_record_view(*args):

        sql = ("insert into workview (viewwid,viewuid,time) values(%s,%s,%s)")
        try:
            con = create_connection(**options.dbsettings)
            return con.execute(sql, *args)
        except Exception, e:
            log_mysql_error(e)
            return 0
