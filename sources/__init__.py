"""
il file __init__.py serve per python a trovare i package di cui fare import.
Avendo fatto una cartella separata il file runner.py non può fare import create_app senza questo nome del file.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import config
from flask_login import LoginManager

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

    return app
