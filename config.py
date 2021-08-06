"""
Il modulo config è un file di configurazione per le variabili d'ambiente dell'applicazione flask.
All'interno del modulo vengono definite diverse classi per diversificare le variabili a seconda del contesto:

- Config è la classe genitore che contiene alcune variabili comuni a tutti i setup
- DevelopmentConfig è il setup per far eseguire l'applicazione flask in locale
- ProductionConfig è la configurazione per il porting online della webapp
"""
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_RECORD_QUERIES = True
    SESSION_PERMANENT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # per far girare il DB locale collegato a flask si deve cambiare la url con
    # 'postgresql://<pg_username>:<pg_password>@localhost/<db_name>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://matteo:password@localhost/postgres'


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database.db')


class HerokuProdConfig(Config):
    DEBUG = False
    # la variabile HEROKU_DATABASE_URL è stata settata nell'ambiente di Heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_DATABASE_URL')
    SSL_REDIRECT = True if os.environ.get('DYNO') else False


config = {
    'development': DevelopmentConfig,
    'production': HerokuProdConfig,
    'test': TestingConfig,

    # a seconda delle necessità si può cambiare il valore della chiave 'default'
    # per un setup rapido è già settato a TestingConfig
    'default': TestingConfig
}
