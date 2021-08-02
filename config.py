"""
Il modulo config è un file di configurazione per le variabili d'ambiente dell'applicazione flask.
All'interno del modulo vengono definite diverse classi per diversificare le variabili a seconda del contesto:

- Config è la classe genitore che contiene alcune variabili comuni a tutti i setup
- DevelopmentConfig è il setup per far eseguire l'applicazione flask in locale
"""
import os
import secrets


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SESSION_PERMANENT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    # per far girare il DB locale collegato a flask si deve cambiare la url con
    # 'postgresql://<pg_username>:<pg_password>@localhost/<db_name>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://matteo:password@localhost/postgres'


class ProductionConfig(Config):
    DEBUG = False
    SESSION_TYPE = 'filesystem'
    # la variabile HEROKU_DATABASE_URL è stata settata nell'ambiente di Heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
