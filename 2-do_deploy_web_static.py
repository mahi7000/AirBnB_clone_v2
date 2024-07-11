#!/usr/bin/python3
"""Distributes an archive to your web servers"""

from fabric.api import *
from os.path import exists
env.hosts = ['35.175.130.143', '54.237.93.121']


def do_deploy(archive_path):
    """function that distributes archive to web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split('/')[-1]
        n = file_n.split('.')[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(file_n, path, n))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, n))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, n))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
