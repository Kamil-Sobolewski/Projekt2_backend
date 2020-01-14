import os

basedir = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = "qwerty123456"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('DJANGO_EMAIL')
    MAIL_PASSWORD = os.environ.get('DJANGO_EMAIL_PASS')
    UPLOAD_FOLDER = f'{basedir}/photos'
    JWT_SECRET_KEY = "qwerty123456"
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_CSRF_PROTECT = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev-db.sqlite")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
