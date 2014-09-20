from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['medusa-node1.vsnet.gmu.edu']
env.user = 'akalburg'

'''
def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()
'''
def deploy():
    code_dir = '/home/akalburg/github'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone  https://github.com/anupkalburgi/cs675-assign1.git %s" % code_dir)
	    run('python %s/dameon_start.py'%code_dir)
'''
    with cd(code_dir):
     
        run("python bootstrap_node.py",pty=False )
        #run("touch app.wsgi")
'''
