#!/usr/bin/python3
"""Distributes an archive to your web servers"""

from fabric.api import *
from os.path import exists
from datetime import datetime
env.hosts = ['35.175.130.143', '54.237.93.121']


def do_pack():
    """make archive"""
    t = datetime.now()
    archive = 'web_static_{}.tgz'.format(t.strftime("%Y%m%d%H%M%S"))
    local('mkdir -p versions')
    c = local('tar -cvzf versions/{} web_static'.format(archive))
    if c is not None:
        return archive
    else:
        return None


def do_deploy(archive_path):
    """function that distributes archive to web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split('/')[-1]
        n = file_n.split('.')[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, n))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, n))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, n))
        run('rm -rf {}{}/web_static'.format(path, n))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, n))
        return True
    except:
        return False


def deploy():
    """Gets archive path and deploys"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
