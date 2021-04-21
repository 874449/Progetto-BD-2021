"""
il file __init__.py serve per python a trovare i package di cui fare import.
Avendo fatto una cartella separata il file main.py non può fare import create_app senza questo nome del file.
"""

from flask import Flask


def create_app():
    """crea il server con flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret string'

    # nelle seguenti linee stiamo creando le blueprint per dividere il progetto in più file
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,  url_prefix='/')

    return app
