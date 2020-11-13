import os


class Config(object):
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = 'dfgDfgDFGdFGDfG53RE'
    # URI используемая для подключения к базе данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'           #os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sevg78@gmail.com'
    MAIL_PASSWORD = 'ss101325270878SS'
    MAIL_DEFAULT_SENDER = '"Admin" <sevg78@gmail.com>'

    BABEL_TRANSLATION_DIRECTORIES = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'translations/')

    BABEL_DEFAULT_LOCALE = 'ru_RU'

    APP_NAME = 'Coins'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
