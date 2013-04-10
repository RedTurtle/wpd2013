from fabric.api import run, cd, env
from fabric.utils import abort
from fabric.colors import green

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

def buildout():
    """Pull buildout, run bin/buildount, touch wsgi"""
    with cd(env.directory):
        run("git pull")
        run("./bin/buildout -NU")
        run("touch parts/mod_wsgi/wsgi")
