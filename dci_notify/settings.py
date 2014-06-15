# -*- coding: utf-8 -*-
import os
import urlparse


class Config(object):
    SECRET_KEY = '117E9348-0CB8-4127-AA48-8E6FD1057CF7'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    # FlaskMail and logging
    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'postmaster@sandbox17422.mailgun.org'
    MAIL_PASSWORD = '9vwwg5ysiqf0'
    MAIL_DEFAULT_SENDER = 'sms@sandbox17422.mailgun.org'
    # Logging setup
    ADMINS = ['kevan@kevanahlquist.com']
    LOGGING_SENDER = 'dci-notify-server-error@sandbox17422.mailgun.org'
    MAIL_SUPPRESS_SEND = False


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/app')
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
