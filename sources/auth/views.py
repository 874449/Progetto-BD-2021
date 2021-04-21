"""
In questo modulo si trovano tutte le route riguardandi l'autenticazione nel sito
"""
from flask import render_template
from . import auth


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return render_template("index.html")


@auth.route('/signup')
def sign_up():
    """
    TODO: creare pagina html corretta e gestire gli input salvandoli nel database,
          eventualmente mandando email di conferma
    """
    return render_template("index.html")
