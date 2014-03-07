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

    '''use tool to optimize project files.'''

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
    if opt:
        os.chdir(build_dir)
        local("find ./ -name \*.css -exec java -jar %s -o '.css$:.css' {} \;" %
              compress_tool_path)
        local("find ./ -name \*.js -exec java -jar %s -o '.js$:.js' {} \;" %
              compress_tool_path)
        print "optimize css and javascript files success."
    return build_dir


def runserver(workdir, servercmd, runserver=True):

    '''run server in the specified dir.'''

    if runserver:
        with cd(workdir):
            run(servercmd)


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
    print "upload local %s to remote %s success." % (src, dst)
    try:
        local("rm -rf %s" % src)
    except:
        pass


def set_libjs_version(path, version):

    '''set the js libary's version with the given version.'''

    os.chdir(path)
    local(("find ./ -name \*.js -exec sed -i 's/jquery-[0-9.].js/jquery-%s.js'"
           "{} \;") % version)
    print "set js libary success."


def deploy_static(config_file):

    initialize_env(config_file)
    build_path = optimize_file(env.srcpath, env.optool, bool(env.optimize))
    upload_files(build_path, env.user, env.host, env.port, env.dstpath)


def deploy_www(config_file):

    initialize_env(config_file)
    build_path = optimize_file(env.srcpath, env.optool, bool(env.optimize))
    upload_files(build_path, env.user, env.host, env.port, env.dstpath)
    runserver(env.dstpath, env.servercmd, bool(env.runserver))


def deploy(config_file):

    '''common deploy function,invoke with different config file'''

    initialize_env(config_file)
    build_path = optimize_file(env.srcpath, env.optool, bool(env.optimize))
    upload_files(build_path, env.user, env.host, env.port, env.dstpath)
    runserver(env.dstpath, env.servercmd, bool(env.runserver))


def main():

    deploy(sys.argv[1])


if __name__ == '__main__':

    main()
