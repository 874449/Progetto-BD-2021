"""
In questo modulo si trovano tutte le route riguardanti l'autenticazione nel sito
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . forms import LoginForm, RegistrationForm
from . import auth
from ..models import User
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Password o E-Mail invalida.', 'warning')
    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sei stato disconnesso con successo.', 'warning')
    return redirect('/')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    TODO: creare conferma attraverso token con invio della mail
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulazioni, registrazione avvenuta con successo!', 'success')
        return redirect(url_for('auth.login'))
    """
    TODO: username potrebbe anche non essere unico quindi potrebbe anche avere doppioni nel database, trovare
    il modo per dire a flask di non validare il campo username.
    """
    if form.username.errors:
        flash(form.username.errors[0], 'warning')
    if form.email.errors:
        flash(form.email.errors[0], 'warning')
    if form.password.errors:
        flash(form.password.errors[0], 'warning')
    if form.password2.errors:
        flash(form.password2.errors[0], 'warning')
    # if form.errors:
    #    for i in form.errors:
    #        flash(i, 'warning')
    return render_template('register.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
