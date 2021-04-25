"""
il file __init__.py serve per python a trovare i package di cui fare import.
Avendo fatto una cartella separata il file runner.py non può fare import create_app senza questo nome del file.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def create_app():
    """crea il server con flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret string'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # nelle seguenti linee stiamo creando le blueprint per dividere il progetto in più file
    from .main import main
    app.register_blueprint(main, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
