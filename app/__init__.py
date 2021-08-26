from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_moment import Moment
from flask_mail import Mail
from flask_pagedown import PageDown
from config import config

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
pagedown = PageDown()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    """crea l'app di flask, configura le sue variabili e crea le blueprint"""
    app = Flask(__name__)
    # configuro l'applicazione basandomi sulle classi costruite in config.py
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # costruttore per la gestione delle sessioni utente
    Session(app)
    login_manager.init_app(app)
    # collegamento del database all'app
    db.init_app(app)

    # libreria per l'invio di email
    mail.init_app(app)

    # aggiunta della libreria per la conversione del tempo UTC in locale
    moment.init_app(app)

    # aggiunta della libreria per l'editing con sintassi markdown
    pagedown.init_app(app)

    # nelle seguenti linee stiamo creando le blueprint per dividere il progetto in più file
    from .main import main
    app.register_blueprint(main, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .quiz import quiz
    app.register_blueprint(quiz, url_prefix='/quiz')

    # aggiungo ai comandi di flask quelli creati da me nel file commands.py
    from .commands import create_tables, populate_db, fill_qtypes_table, delete_db
    app.cli.add_command(create_tables)
    app.cli.add_command(populate_db)
    app.cli.add_command(fill_qtypes_table)
    app.cli.add_command(delete_db)

    return app
