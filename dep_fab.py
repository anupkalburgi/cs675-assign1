from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'akalburg'
env.password = ''
env.always_use_pty = False
code_dir = '/home/akalburg/github'

def nodes():
    env.hosts = ['medusa-node2.vsnet.gmu.edu',\
                 'medusa-node3.vsnet.gmu.edu',\
                 'medusa-node4.vsnet.gmu.edu',\
                 'medusa-node5.vsnet.gmu.edu']


def bootstrap():
    env.hosts = ['medusa-node1.vsnet.gmu.edu']


def update():
    with settings(warn_only=True):
        if not run("test -d %s" % code_dir).failed:
            run('rm -rf %s' % code_dir)
        run("git clone  https://github.com/anupkalburgi/cs675-assign1.git %s" % code_dir)
        run("sleep 1")
        run("cd %s;mkdir -p logs;touch logs/errors.log" % code_dir)


def bootstrap_deploy():
    #TODO--Before starting of with command check if the directoy exists
    with settings(warn_only=True):
        #run('export PYRO_SERIALIZERS_ACCEPTED=serpent,json,marshal,pickle') Right now i have it my \
        # in my bash_profile, that will not work at scale
        # Right way of doing it is http://stackoverflow.com/questions/8313238/best-way-to-add-an-environment-variable-in-fabric
        run("pyro4-ns --host=%s >& /dev/null < /dev/null &" %env.hosts[0] )
        run("cd %s;python bootstrap_node.py >& /dev/null < /dev/null &" %code_dir)
        #run("nohup python %s/bootstrap_node.py >& /dev/null < /dev/null &" %code_dir)


def node_deploy():
    run("cd %s;python start_node.py >& /dev/null < /dev/null &" %code_dir)


def kill():
    run("fuser -k 5150/tcp;sleep 1")


def stop():
    run("fuser -k 9090/tcp;sleep 1")



