"""
In questo modulo si trovano tutte le route riguardandi l'autenticazione nel sito
"""
from flask import render_template, request, flash, redirect, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from . forms import LoginForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
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
