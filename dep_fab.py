from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'akalburg'
env.always_use_pty = False
code_dir = '/home/akalburg/github'

def nodes():
    env.hosts = ['medusa-node2.vsnet.gmu.edu',\
                 'medusa-node3.vsnet.gmu.edu',\
                 'medusa-node4.vsnet.gmu.edu',\
                 'medusa-node5.vsnet.gmu.edu']



def bootstrap():
    env.hosts = ['medusa-node1.vsnet.gmu.edu']


def get_code():
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone  https://github.com/anupkalburgi/cs675-assign1.git %s" % code_dir)

def refresh_code():
    with settings(warn_only=True):
        if not run("test -d %s" % code_dir).failed:
            run('rm -rf %s' %code_dir)


def bootstrap_deploy():
    #run('python %s/dameon_start.py'%code_dir)
    #TODO--Before starting of with command check if the directoy exists
    with settings(warn_only=True):
        run("pyro4-ns --host=%s >& /dev/null < /dev/null &;sleep 2" %env.hosts[0] )
        run('nohup python %s/bootstrap_node.py >& /dev/null < /dev/null &' %code_dir)

def node_deploy():
    run('nohup python %s/start_node.py >& /dev/null < /dev/null &' %code_dir)

def kill():
    run("fuser -k 5150/tcp;sleep 1")



