# -*- coding:utf-8 -*-

'''This module is used for deploying project to online environment.'''

__version__ = '0.0.1'


from fabric.api import env, local, cd, run
from fabric.main import load_settings
import os
import sys


def initialize_env(path):

    '''use the given file to set user's defined env.'''

    settings = load_settings(path)
    env.update(settings)


def optimize_file(project_path, compress_tool_path, opt=True):

    '''use tool to optiminze project files.'''

    project_path = os.path.abspath(project_path)
    if not os.path.exists(project_path):
        print "path %s does not exist." % project_path
        exit(0)
    build_dir = "/tmp/" + os.path.basename(project_path) + "_build"
    if os.path.exists(build_dir):
        try:
            local("rm -rf %s" % build_dir)
        except:
            pass
    os.mkdir(build_dir)
    print "create build path %s." % build_dir
    os.chdir(project_path)
    local("rsync -Cavz --exclude-from=.rsyncignore ./ %s" % build_dir)
    for dirpath, dirnames, filenames in os.walk(build_dir):
        os.chdir(dirpath)
        has_css = False
        has_js = False
        for file in filenames:
            has_css = file.endswith(".css")
            has_js = file.endswith(".js")
            if has_css and has_js:
                break
        if has_css:
            local("java -jar %s -o '.css$:.css' *.css" % compress_tool_path)
        if has_js:
            local("java -jar %s -o '.js$:.js' *.js" % compress_tool_path)
    os.chdir(build_dir)
    return build_dir


def runserver(workdir):

    '''run server in the specified dir.'''

    with cd(workdir):
        run("python ./server.py")


def upload_files(src, user, host, port, dst):

    '''upload files to remote server.'''

    if not os.path.exists(src):
        print "no upload path %s." % src
        exit(0)
    os.chdir(src)
    if isinstance(port, int):
        port = str(port)
    dst = user + '@' + host + ':' + dst
    shcmd = "'ssh -p %s'" % port
    local(("rsync -CrlptDcvz -e %s --exclude-from=.rsyncignore "
           "./ %s" % (shcmd, dst)))
    print "upload local %s to remote %s." % (src, dst)
    try:
        local("rm -rf %s" % src)
    except:
        pass


def main():

    pass
