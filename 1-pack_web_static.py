#!/usr/bin/python3
"""Fabric script generates a .tgz archive from web_static"""

from fabric.api import *
from datetime import datetime


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
