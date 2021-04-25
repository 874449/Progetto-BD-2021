"""
In questo modulo si trovano tutte le route riguardandi l'autenticazione nel sito
"""
from flask import render_template, request, flash, redirect, session
# from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
# @login_required
def logout():
    # logout_user()
    session["email"] = None
    flash('You have been logged out.')
    return redirect('/')


@auth.route('/signup')
def sign_up():
    """
    TODO: creare pagina html corretta e gestire gli input salvandoli nel database,
          eventualmente mandando email di conferma
    """
    return render_template("index.html")


@auth.route('/success', methods=['POST'])
def success():
    name = request.form.get("email")
    password = request.form.get("password")
    session["email"] = name
    return redirect('/')
    #  return render_template("success.html", name=name, password=password)
