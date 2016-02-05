import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = 'MyFirstApp'
    SECRET_KEY = 'randomnubersandletters123'
    SALTY_KEY = 'randomnubersandletters123'
    LISTINGS_PER_PAGE = 20

    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'add_salt_123_hard_one'
    SECURITY_CONFIRMABLE = True

    # SendGrid
    SENDGRID_API_KEY = 'xxxxxxxxx_API_KEY_HERE_xxxxxxxxxx'

    # Used by flask security
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'user'
    MAIL_PASSWORD = 'password'
    DEFAULT_MAIL_SENDER = 'notifications@yourcompany.com'
    SECURITY_EMAIL_SENDER = 'notifications@yourcompany.com'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost:3306/database_name'
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    DEBUG = True
