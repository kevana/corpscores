#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from dci_notify.app import create_app
from dci_notify.user.models import User
from dci_notify.settings import DevConfig, ProdConfig
from dci_notify.database import db


if os.environ.get("DCI_NOTIFY_ENV") == 'prod':
    app = create_app(ProdConfig)
    print('Manager app created with ProdConfig')
else:
    app = create_app(DevConfig)
    print('Manager app created with DevConfig')

manager = Manager(app)
TEST_CMD = 'foreman run py.test tests'


@manager.command
def test():
    """Run the tests."""
    os.environ['DCI_NOTIFY_ENV'] = 'test'
    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)


@manager.command
def debug_server():
    '''Run server with development config.'''
    os.environ['DCI_NOTIFY_ENV'] = 'dev'
    status = subprocess.call('foreman start', shell=True)
    sys.exit(status)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
