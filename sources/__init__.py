"""
il file __init__.py serve per python a trovare i package di cui fare import.
Avendo fatto una cartella separata il file runner.py non può fare import create_app senza questo nome del file.
"""

from flask import Flask
# TODO: configurare il database
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


def create_app():
    """crea il server con flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret string'
    # db.init_app(auth)

    # nelle seguenti linee stiamo creando le blueprint per dividere il progetto in più file
    from .main import main
    app.register_blueprint(main, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
