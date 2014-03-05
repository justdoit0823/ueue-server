# -*- coding:utf-8 -*-

'''This module provides many operations on the database server.'''

__version__ = '0.0.1'

from tornado import database

from tornado.options import define, options

#mysql define

define("mysql_host", default="127.0.0.1:3306", help="ueue database host")
define("mysql_database", default="yoez", help="ueue database name")
define("mysql_user", default="justdoit", help="ueue database user")
define("mysql_password", default=None, help="ueue database password")
define("noreply_password",
       default=None, help="signup email check account password")

dbsettings = {
    'host': mysql_host,
    'database': mysql_database,
    'user': mysql_user,
    'password': mysql_password,
    }


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
    def get_latest_works(start, offset=None):

        db = create_connection(**dbsettings)
        args = [start]
        worksql = ("select W.wid,W.title,W.type,W.content,W.teammates,"
                   "W.copysign,W.lable,W.time,W.view,W.review,W.support,"
                   "W.cover,W.describe,U.uid,U.img,U.account from work "
                   "as W join user as U on W.author_id=U.uid order by "
                   "W.timelimit %s")
        if offset is not None:
            args.append(offset)
            worksql = worksql + ",%s"
        return db.query(worksql, *args)


class RecordManager:

    pass


class UserManager:

    pass
