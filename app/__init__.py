from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from config import config

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
db = SQLAlchemy()


def create_app(config_name):
    """crea il server con flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    Session(app)
    login_manager.init_app(app)
    db.init_app(app)

    # nelle seguenti linee stiamo creando le blueprint per dividere il progetto in più file
    from .main import main
    app.register_blueprint(main, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .quiz import quiz
    app.register_blueprint(quiz, url_prefix='/quiz')

    from .commands import create_tables
    app.cli.add_command(create_tables)

    return app
