#!/usr/bin/python3
"""Fabric script generates a .tgz archive from web_static"""

from fabric.api import *
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['35.175.130.143', '54.237.93.121']


def do_pack():
    """make archive"""
    try:
        t = datetime.now()
        if isdir('versions') is False:
            local("mkdir versions")
        archive = 'versions/web_static_{}.tgz'.format(t.strftime("%Y%m%d%H%M%S"))
        local('tar -cvzf {} web_static'.format(archive))
        return archive
    except:
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
    """Gets path and deploys"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
