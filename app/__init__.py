import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_babelex import Babel
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager
from flask_moment import Moment

from .database import db

login_manager = LoginManager()
bootstrap = Bootstrap()
csrf_protect = CSRFProtect()
mail = Mail()
babel = Babel()
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'users.log'

    bootstrap.init_app(app)

    babel.init_app(app)

    mail.init_app(app)

    csrf_protect.init_app(app)

    moment.init_app(app)

    import app.users.controllers as users
    app.register_blueprint(users.module)

    return app
