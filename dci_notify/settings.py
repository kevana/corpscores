# -*- coding: utf-8 -*-
import os
import urlparse


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'NOT_A_SECRET_KEY')
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
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'postmaster@example.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '<example_password>')
    MAIL_DEFAULT_SENDER = 'noreply@kevanahlquist.com'
    SMS_DEFAULT_SENDER = 'sms@kevanahlquist.com'
    # Logging setup
    ADMINS = ['kevan@kevanahlquist.com']
    LOGGING_SENDER = 'CorpScores-server-error@kevanahlquist.com'
    MAIL_SUPPRESS_SEND = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/app')
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    API_KEY = os.environ.get('API_KEY', 'API_KEY')


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    MAIL_SUPPRESS_SEND = True
