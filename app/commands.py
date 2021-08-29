"""
Il seguente modulo contiene dei comandi personalizzati eseguibili da flask
tramite CLI:
per richiamare un comando basterà digitare

    flask `nome_comando`

ciò semplifica alcune funzioni come la creazione delle tabelle del DB
o il popolamento di queste.
Il vantaggio è che non è necessario importare i moduli o le librerie al di
fuori di flask, in quanto i comandi di questo modulo vengono eseguiti nel contesto
dell'applicazione flask.
"""
import click
from . import fake
from flask.cli import with_appcontext

from . models import *


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    """create_tables è un wrapper per la creazione delle tabelle del DB"""
    db.create_all()
    print("Your DB has been created")


@click.command(name='delete_db')
@with_appcontext
def delete_db():
    """drop all tables of the database"""
    db.drop_all()
    print("DB Deleted")


@click.command(name='fill_qtypes_table')
@with_appcontext
def fill_qtypes_table():
    tipologie = [TipologiaDomanda('Aperta', 'Domanda aperta'),
                 TipologiaDomanda('Multi-scelta', 'Domanda a risposta multipla'),
                 TipologiaDomanda('Scelta', 'Domanda a scelta che prevede una singola scelta')]

    for elem in tipologie:
        print(f'[INFO] Adding {elem} to db')
        db.session.add(elem)

    db.session.commit()
    print('[SUCCESS] TipologiaDomande table has been filled successfully')


@click.command(name='faker')
@with_appcontext
def faker():
    print('[INFO] generating fake users')
    fake.users(100)
    print('[INFO] generating fake quizzes')
    fake.questionari(200)
    print('[SUCCESS] DONE')
