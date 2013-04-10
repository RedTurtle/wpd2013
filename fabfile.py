from fabric.api import sudo, cd, env
from fabric.utils import abort
from fabric.colors import green
from fabric.contrib.files import exists

def staging():
    """Use staging server"""
    if not 'wpd2013.staging.server' in env \
            or not 'wpd2013.staging.dir' in env \
            or not 'wpd2013.staging.user' in env:
        abort('You don\'t have proper staging ENV. '
              'Please check your ~/.fabricrc '
              'and ensure that you have two entries:\n' + \
              green('wpd2013.staging.server = example.com\n') + \
              green('wpd2013.staging.user = user\n') + \
              green('wpd2013.staging.dir = /opt/my_dir'))

    env.directory = env['wpd2013.staging.dir']
    env.hosts = [env['wpd2013.staging.server']]
    env.user = env['wpd2013.staging.user']

def freshdb():
    """If Data.fs_fresh is available it will be used as a new ZODB"""
    if exists('%s/var/filestorage/Data.fs_fresh' % env.directory, use_sudo=True):
        with cd(env.directory):
            sudo("./bin/instance stop")
        with cd('%s/var/filestorage' % env.directory):
            sudo("mv Data.fs Data.fs.old")
            sudo("cp Data.fs_fresh Data.fs")
            sudo("chown plone: ./ -R")
        with cd(env.directory):
            sudo("./bin/instance start")

def buildout():
    """Pull buildout, run bin/buildount, touch wsgi"""
    with cd(env.directory):
        sudo("git pull")
        sudo("./bin/instance stop")
        sudo("./bin/buildout -NU")
        sudo("./bin/instance start")
