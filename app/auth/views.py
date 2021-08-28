"""
In questo modulo si trovano tutte le route riguardanti l'autenticazione nel sito
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . forms import LoginForm, RegistrationForm
from . import auth
from ..models import User
from ..email import send_email
from .. import db


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Password o E-Mail invalida.', 'warning')
    return render_template("auth/login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sei stato disconnesso con successo.', 'warning')
    return redirect('/')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # genera token per confermare l'email
        token = user.generate_confirmation_token()
        send_email(user.email, 'Conferma Account',
                   'auth/email/confirm', user=user, token=token)
        flash('Congratulazioni, registrazione avvenuta con successo!\n\
        Ti abbiamo mandato un link per confermare il tuo account al tuo indirizzo email.', 'success')
        return redirect(url_for('auth.login'))

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
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Grazie per aver confermato il tuo account!')
    else:
        flash('Il link che hai usato non è valido o è scaduto.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Conferma account',
               'auth/email/confirm', user=current_user, token=token)
    flash('Ti abbiamo appena inviato un link per confermare il tuo account al tuo indirizzo email.')
    return redirect(url_for('main.index'))