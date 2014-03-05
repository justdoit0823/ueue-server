# -*- coding: utf-8 -*-

'''
The is a main server module,with some application settings
 to change server behaviour.After this,start the sever loop.

'''


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys
import re
import os
import time
from __init__ import BaseHandler, USER_STATUS
import works
import events
import userspace
import setting
import useraction
import module
import signal
import logging

from tornado.options import define, options

define("server_port0", default=10000, help="run on the given port", type=int)
define("server_port1", default=10001, help="run on the given port", type=int)
define("server_port2", default=10002, help="run on the given port", type=int)
define("server_port3", default=10003, help="run on the given port", type=int)
define("pid_file", default=None, help="pid file for the daemon process",
       type=str)

#rewrite RequestHandler

BUF_READ_SIZE = 4096


class HomeHandler(BaseHandler):
    def get(self):
        print self.request
        if self.is_db_connected is False:
            return self.write("connect to mysql server failed.")
        cuser = self.get_current_user()
        work_sql = ("select * from user join work on work.author_id=user.uid "
                    "order by work.time desc")
        rows = self.db.query(work_sql)
        event_sql = ("select * from user join event on event.author_id="
                     "user.uid order by event.time desc limit 0,4")
        ls = self.db.query(event_sql)
        review_sql = ("select * from user join eventreview on "
                      "eventreview.reviewuid=user.uid order by "
                      "eventreview.time desc limit 0,4")
        rvls = self.db.query(review_sql)
        kwargs = dict(cuser=cuser, sf=self, rows=rows, ls=ls, rvls=rvls)
        self.render("yoez1.0beta/index.html", **kwargs)


class ProfessionalHandler(BaseHandler):
    def get(self):
        cuser = self.get_current_user()
        usersql = ("select * from user join basicinfo on uid=bsc_id where "
                   "status >= %s")
        rows = self.db.query(usersql, USER_STATUS["infoset"])
        self.render("yoez1.0beta/user-search.html", cuser=cuser, rows=rows)


class ClubHandler(BaseHandler):
    def get(self):
        #cuser=self.get_current_user()
        self.write("Sorry!The page you request does not exist.Wait a moment!")


class IndexHandler(BaseHandler):
    def get(self):
        tab = self.get_argument("tab", "works")
        self.render("yoez1.0beta/index-"+tab+".html")


class StaticImgHandler(BaseHandler):
    def get(self, filename):
        imgfmt = filename.split(".")[1]
        path = os.path.dirname(sys.argv[0])+"/static/img/"+filename
        buf = ""
        try:
            f = file(path, "rb")
            while True:
                rd = f.read(BUF_READ_SIZE)
                if not rd:
                    break
                else:
                    buf += rd
            f.close()
        finally:
            if f:
                f.close()
            else:
                print "open file "+path+" error!"
        print buf
        if buf:
            self.set_header("Content-Type", "image/"+imgfmt)
            self.write(buf)
        else:
            self.write("img read error!")


class UserStatementHandler(BaseHandler):

    def get(self):
        self.render("other1.0beta/other-1.html")

#rewrite Application


class MyApplication(tornado.web.Application):
    def __init__(self):
        HandlerList = [
            (r"/", HomeHandler),
            (r"/index", IndexHandler),
            (r"/professional", ProfessionalHandler),
            (r"/vane", ClubHandler),
            (r"/user/statement", UserStatementHandler),
            #(r"/static/img/([a-zA-Z0-9.]+)", StaticImgHandler),
            ]
        import_modules = [works, events, userspace, useraction, setting]
        for m in import_modules:
            if hasattr(m, "HandlerList"):
                HandlerList += m.HandlerList
        workdir = os.path.dirname(sys.argv[0])
        settings = dict(
            template_path=os.path.join(workdir, "template"),
            static_path=os.path.join(workdir, "static"),
            cookie_secret=("sdjkfdSKFJ8K07JDWEOSLSGaYdkL5gemGeJKFuYh2y5g"
                           "d8tu6N0k$;Kfe"),
            login_url="/user/action/login",
            xsrf_cookies=True,
            ui_modules=module.modules,
            autoescape=None,
            gzip=True,
            #debug=True,
            handlers=HandlerList
            )
        tornado.web.Application.__init__(self, **settings)


def serverquit(signum, frame):
    '''quit signal handler'''

    logging.info("server stop.")
    exit(0)


def daemonize():
    '''daemonize the call process'''
    pid = os.fork()
    if pid < 0:
        logging.error("fork error!")
    elif pid > 0:
        os._exit(0)
    os.setsid()
    fd = os.open("/dev/null", os.O_RDWR)
    os.dup2(fd, 0)
    os.dup2(fd, 1)
    os.dup2(fd, 2)


def main():

    config_file = os.path.join(os.path.dirname(sys.argv[0]), "server.conf")
    tornado.options.parse_config_file(config_file)
    tornado.options.parse_command_line()
    signal.signal(signal.SIGQUIT, serverquit)
    #initdbpsw()
    #daemonize()
    application = MyApplication()
    http_server0 = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server0.bind(options.server_port0)
    http_server0.start(4)
    pid = os.getpid()
    port = options.server_port0
    logging.info("process: "+str(pid)+" listen port "+str(port))
    #http_server1 = tornado.httpserver.HTTPServer(application,xheaders=True)
    #http_server1.listen(options.port1)
    #http_server2 = tornado.httpserver.HTTPServer(application,xheaders=True)
    #http_server2.listen(options.port2)
    #http_server3 = tornado.httpserver.HTTPServer(application,xheaders=True)
    #http_server3.listen(options.port3)
    logging.info("server start and press key Ctrl+\ to stop...")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
