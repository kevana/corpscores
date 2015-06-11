# -*- coding: utf-8 -*-
"""
The app module, containing the app factory function.
"""

import os

from flask import Flask, render_template
from flask.ext.security import SQLAlchemyUserDatastore

from dci_notify import public, user
from dci_notify.admin import admin
from dci_notify.assets import assets
from dci_notify.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
    mail,
    sentry,
    security,
    api_manager
)
from dci_notify.settings import ProdConfig, DevConfig, TestConfig
from dci_notify.user.models import User, Role
from dci_notify.user.forms import RegisterForm
from dci_notify.api.views import init_api


def create_app(config_object=None):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """

    if not config_object:
        if os.environ.get('DCI_NOTIFY_ENV') == 'dev':
            config_object = DevConfig
            print('create_app using DevConfig based on DCI_NOTIFY_ENV')
        elif os.environ.get('DCI_NOTIFY_ENV') == 'test':
            config_object = TestConfig
            print('create_app using TestConfig based on DCI_NOTIFY_ENV')
        elif os.environ.get('DCI_NOTIFY_ENV') == 'prod':
            config_object = ProdConfig
            print('create_app using ProdConfig based on DCI_NOTIFY_ENV')
        else:
            config_object = ProdConfig
            print('create_app defaulting to ProdConfig')

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_loggers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    mail.init_app(app)
    mail.app = app
    api_manager.init_app(app, flask_sqlalchemy_db=db)
    api_manager.app = app
    init_api()

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=user_datastore, register_form=RegisterForm)
    if not app.debug:
        sentry.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_loggers(app):
    if not (app.debug or app.config.get('LOGGING_DISABLE', False)):
        import logging
        from logging import Formatter
        from logging.handlers import SMTPHandler

        mail_handler = SMTPHandler(mailhost=app.config['MAIL_SERVER'],
                                   fromaddr=app.config['LOGGING_SENDER'],
                                   toaddrs=app.config['ADMINS'],
                                   subject='CorpScores Server Error',
                                   credentials=(app.config['MAIL_USERNAME'],
                                                app.config['MAIL_PASSWORD']))
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter('''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s

            Message:

            %(message)s
        '''))
        app.logger.addHandler(mail_handler)
    return None
