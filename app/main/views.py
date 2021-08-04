from flask import render_template, request, url_for, redirect, session
from flask_login import login_required, current_user
from .. models import *
from .. import db
from ..quiz.forms import NewQuestionnaire
from . import main


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template("index.html")


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    nuovo_questionario_form = NewQuestionnaire()
    if nuovo_questionario_form.validate_on_submit():
        title = nuovo_questionario_form.titolo.data
        description = nuovo_questionario_form.descrizione.data
        nuovo = Questionario(title, description, current_user.id)
        db.session.add(nuovo)
        db.session.commit()
        return redirect(url_for('quiz.editor'))
    return render_template('dashboard.html', nuovo_questionario_form=nuovo_questionario_form)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')