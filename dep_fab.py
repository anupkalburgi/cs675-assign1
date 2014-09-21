from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'akalburg'
env.always_use_pty = False
code_dir = '/home/akalburg/github'

def nodes():
    env.hosts = ['129.174.94.98',\
                 '129.174.94.97',\
                 '129.174.94.96',\
                 '129.174.94.95']



def bootstrap():
    env.hosts = ['129.174.94.99']

def get_code():
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone  https://github.com/anupkalburgi/cs675-assign1.git %s" % code_dir)

def refresh_code():
    with settings(warn_only=True):
        if not run("test -d %s" % code_dir).failed:
            run('rm -rf %s' %code_dir)


def deploy():
    #run('python %s/dameon_start.py'%code_dir)
    run('nohup python %s/bootstrap_node.py >& /dev/null < /dev/null &' %code_dir)

def node_deploy():
    run('nohup python %s/start_node.py >& /dev/null < /dev/null &' %code_dir)

def kill():
    run("fuser -k 5150/tcp;sleep 1")



