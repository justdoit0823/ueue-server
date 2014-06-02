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


def formate_update_sql(tb, **kwargs):

    _str = []
    _val = []
    _sql = ['update', tb, 'set']
    for k in kwargs:
        _str.appned(k + '=%s')
        _val.append(kwargs[k])
    _sql .append(','.join(_str))
    return (' '.join(_sql), _val)


def log_mysql_error(args):

    if args:

        error_prefix = "mysql error " + str(args[0]) + ": "

        error_msg = error_prefix + formate_errmsg(args[1:])

        logging.error(error_msg)


def do_query_request(sql, *args):

    '''do real db request with sql and args'''

    try:
        con = create_connection(**options.dbsettings)
        result = con.query(sql, *args)
    except Exception, e:

        log_mysql_error(e)
        result = None
    finally:
        con.close()
        return result


def do_execute_request(sql, *args):

    '''do real db request with sql and args'''

    try:
        con = create_connection(**options.dbsettings)
        result = con.execute(sql, *args)
    except Exception, e:

        log_mysql_error(e)
        result = -1
    finally:
        con.close()
        return result


def do_get_request(sql, *args):

    '''do real db request with sql and args'''

    try:
        con = create_connection(**options.dbsettings)
        result = con.get(sql, *args)
    except Exception, e:
        log_mysql_error(e)
        result = None
    finally:
        con.close()
        return result


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
        return do_get_request(sql, wid)

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

        return do_execute_request(sql, *(num, wid))

    @staticmethod
    def update_work_review(wid, num):

        sql = "update work set review=review+%s where wid=%s"

        return do_execute_request(sql, *(num, wid))

    @staticmethod
    def update_work_support(wid, num):

        sql = "update work set support=support+%s where wid=%s"

        return do_execute_request(sql, *(num, wid))

    @staticmethod
    def new_work(*args):

        sql = ("insert into work (author_id,type,title,content,wdescribe,"
               "cover,lable,copysign,teammates,time) values(%s,%s,%s,%s,%s,"
               "%s,%s,%s,%s,%s)")
        return do_execute_request(sql, *args)

    @staticmethod
    def del_work(wid):

        sql = "delete from work where wid=%s"

        return do_execute_request(sql, wid)

    @staticmethod
    def check_user_work(uid, wid):

        sql = "select wid from work where wid=%s and author_id=%s"

        return do_get_request(sql, wid, uid)


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
               "desc limit %s")
        if offset is not None:

            args.insert(0, offset)
            sql = ','.join((sql, '%s'))
        return do_query_request(sql, *args)

    @staticmethod
    def get_records(limit, offset=None):

        '''Get latest records'''

        args = [limit]

        sql = ("select U.uid,U.account,U.img,E.eid,E.title,E.picture,E.type,"
               "E.lable,E.time from user as U join event as E on "
               "U.uid=E.author_id order by E.time desc limit %s")
        if offset is not None:

            args.insert(0, offset)
            sql = ','.join((sql, '%s'))
        return do_query_request(sql, *args)

    @staticmethod
    def get_record_byid(rid):

        sql = ("select U.uid,U.account,U.img,E.title,E.content,E.picture,"
               "E.lable,E.type,E.view,E.review,E.support,E.time from user "
               "as U join event as E on U.uid=E.author_id where E.eid=%s")
        return do_get_request(sql, rid)

    @staticmethod
    def update_record_view(rid, num):

        sql = "update event set view=view+%s where eid=%s"

        return do_execute_request(sql, *(num, rid))

    @staticmethod
    def update_record_review(rid, num):

        sql = "update event set review=review+%s where eid=%s"

        return do_execute_request(sql, *(num, rid))

    @staticmethod
    def update_record_support(rid, num):

        sql = "update event set support=support+%s where eid=%s"

        return do_execute_request(sql, *(num, rid))

    @staticmethod
    def new_record(*args):

        sql = ("insert into event (author_id,type,title,content,picture,place,"
               "lable,time) values(%s,%s,%s,%s,%s,%s,%s,%s)")

        return do_execute_request(sql, *args)


class UserManager:

    @staticmethod
    def has_user(uid):
        '''check the user exists'''

        sql = "select uid from user where uid=%s"
        return do_get_request(sql, uid)

    @staticmethod
    def update_user(uid, **kwargs):

        sql_prefix, args = formate_update_sql('user', **kwargs)
        whcase = 'where uid=%s'
        sql = ' '.join(sql_prefix, whcase)
        args.append(uid)
        return do_execute_request(sql, *args)

    @staticmethod
    def update_user_psw(psw, uid):

        sql = "update user set password=%s where uid=%s"
        do_execute_request(sql, psw, uid)

    @staticmethod
    def update_user_status(st, uid):
        sql = "update user set status=%s where uid=%s"
        do_execute_request(sql, st, uid)

    @staticmethod
    def get_user_withid(uid):

        sql = ("select uid,account,img,status,email,password,status,time from "
               "user where uid=%s")
        return do_get_request(sql, uid)

    @staticmethod
    def get_user_withmail(mail):

        sql = ("select uid,account,img,status,password,status from user "
               "where email=%s")
        return do_get_request(sql, mail)

    @staticmethod
    def get_user_withcode(code):

        sql = "select uid,account,email,status from user where code=%s"

        return do_get_request(sql, code)

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

        return do_execute_request(sql, *args)

    @staticmethod
    def get_user_basic(uid):

        sql = ("select U.uid,U.account,U.img,U.status,U.time,BI.job,BI.area "
               "from user as U join basicinfo as BI on U.uid=BI.bsc_id where "
               "U.uid=%s")
        return do_get_request(sql, uid)

    @staticmethod
    def get_full_basic(uid):

        sql = ("select U.uid,U.account,U.img,U.status,U.time,BI.uname,BI.job,"
               "BI.area,BI.organ,BI.height,BI.weight,BI.birth,BI.extend from "
               "user as U join basicinfo as BI on U.uid=BI.bsc_id where "
               "U.uid=%s")
        return do_get_request(sql, uid)

    @staticmethod
    def get_contact_property(uid):

        sql = ("select CI.telphone,CI.conmail,CI.conaddress,P.ptype,P.sex "
               "from contactinfo as CI join property as P on "
               "CI.con_id=P.proper_id where CI.con_id=%s")
        return do_get_request(sql, uid)


class ReviewManager:

    @staticmethod
    def get_latest_workreviews(limit, offset=None):

        args = [limit]

        sql = ("select U.uid,U.account,WR.reviewwid as wid,WR.content,WR.time "
               "from workreview as WR join user as U on WR.reviewuid=U.uid "
               "order by WR.time desc limit %s")
        if offset is not None:
            sql = ','.join((sql, '%s'))
            args.insert(0, offset)
        return do_query_request(sql, *args)

    @staticmethod
    def get_latest_recordreviews(limit, offset=None):

        args = [limit]

        sql = ("select U.uid,U.account,ER.revieweid as rid,ER.content,ER.time "
               "from eventreview as ER join user as U on ER.reviewuid=U.uid "
               "order by ER.time desc limit %s")
        if offset is not None:
            sql = ','.join((sql, '%s'))
            args.insert(0, offset)
        return do_query_request(sql, *args)

    @staticmethod
    def new_record_review(*args):

        sql = ("insert into eventreview (revieweid,reviewuid,content,time) "
               "values(%s,%s,%s,%s)")

        return do_execute_request(sql, *args)

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

        return do_execute_request(sql, *args)

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
        return do_get_request(sql, *(rid, uid))

    @staticmethod
    def new_record_view(*args):

        sql = ("insert into eventview (vieweid,viewuid,time) values(%s,%s,%s)")

        return do_execute_request(sql, *args)

    @staticmethod
    def new_record_view(*args):

        sql = ("insert into eventview (vieweid,viewuid,time) values(%s,%s,%s)")

        return do_execute_request(sql, *args)


class FollowManager:

    @staticmethod
    def get_user_relation(fid, flwid):

        sql = "select fid,relation from follow where fid=%s and flwid=%s"
        return do_get_request(sql, fid, flwid)

    @staticmethod
    def update_user_relation(fid, flwid, relation=1):

        sql = "update follow set relation=%s where fid=%s and flwid=%s"
        return do_execute_request(sql, relation, fid, flwid)

    @staticmethod
    def new_user_relation(fid, flwid, relation=1):

        sql = "insert into follow(fid,flwid,relation) values (%s,%s,%s)"
        return do_execute_request(sql, fid, flwid, relation)


class SupportManager:

    @staticmethod
    def check_event_support(*args):

        sql = "select esid from eventsupport where supuid=%s and supeid=%s"

        return do_get_request(sql, *args)

    @staticmethod
    def new_event_support(*args):

        sql = "insert into eventsupport (supeid,supuid,time) values(%s,%s,%s)"

        return do_execute_request(sql, *args)


class BasicManager:

    @staticmethod
    def new_basic(*args):

        sql = ("insert into basicinfo(bsc_id,uname,area,organ,job,height,"
               "weight,birth,extend) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        return do_execute_request(sql, *args)

    @staticmethod
    def update_basic(*args):

        sql = ("update basicinfo set uname=%s,area=%s,organ=%s,job=%s,"
               "height=%s,weight=%s,birth=%s,extend=%s where bsc_id=%s")
        return do_execute_request(sql, *args)

    @staticmethod
    def check_basic(bid):

        sql = "select bsc_id from basicinfo where bsc_id=%s"

        return do_get_request(sql, bid)

    @staticmethod
    def get_basic(bid):

        sql = ("select uname,area,organ,job,height,weight,birth,extend from "
               "basicinfo where bsc_id=%s")
        return do_get_request(sql, bid)


class ContactManager:

    @staticmethod
    def check_contact(cid):

        sql = "select con_id from contactinfo where con_id=%s"

        return do_get_request(sql, cid)

    @staticmethod
    def new_contact(*args):

        sql = ("insert into contactinfo(con_id,agent_id,telphone,conmail,"
               "conaddress,sinawb,qqwb,qq,qzone,renren,douban,psldomain) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        return do_execute_request(sql, *args)

    @staticmethod
    def update_contact(*args):

        sql = ("update contactinfo set agent_id=%s,telphone=%s,conmail=%s,"
               "conaddress=%s,sinawb=%s,qqwb=%s,qq=%s,qzone=%s,renren=%s,"
               "douban=%s where con_id=%s")

        return do_execute_request(sql, *args)

    @staticmethod
    def get_contact(cid):

        sql = ("select telphone,conmail,conaddress,psldomain from "
               "contactinfo where con_id=%s")
        return do_get_request(sql, cid)

    @staticmethod
    def get_domain(cid):

        sql = "select psldomain from contactinfo where con_id=%s"

        return do_get_request(sql, cid)

    @staticmethod
    def update_domain(cid, dm):

        sql = "update contactinfo set psldomain=%s where con_id=%s"

        return do_execute_request(sql, dm, cid)

    @staticmethod
    def check_domain(dm):

        sql = "select psldomain from contactinfo where psldomain=%s"
        return do_get_request(sql, dm)


class PropertyManager:

    @staticmethod
    def get_property(pid):

        sql = "select proper_id,ptype,sex from property where proper_id=%s"

        return do_get_request(sql, pid)

    @staticmethod
    def new_property(*args):

        sql = "insert into property(proper_id,ptype,sex) values(%s,%s,%s)"

        return do_query_request(sql, *args)
