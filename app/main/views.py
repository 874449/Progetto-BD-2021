from flask import render_template, flash, url_for, redirect, session
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


@main.route('/delete/<int:quizID>', methods=['POST'])
@login_required
def delete(quizID):
    # print(f'[DELETING] {quizID}')
    quiz = Questionario.query.filter_by(id=quizID).first()
    db.session.delete(quiz)
    db.session.commit()
    flash('Questionario cancellato con successo', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    display_quiz = Questionario.query.filter_by(author_id=current_user.id).order_by(Questionario.id.desc()).all()
    nuovo_questionario_form = NewQuestionnaire()
    if nuovo_questionario_form.validate_on_submit():
        title = nuovo_questionario_form.titolo.data
        description = nuovo_questionario_form.descrizione.data
        nuovo = Questionario(title, description, current_user.id)
        db.session.add(nuovo)
        db.session.commit()
        flash('Questionario creato con successo', 'success')
        return redirect(url_for('quiz.editor', editID=nuovo.id))
    return render_template('dashboard.html', nuovo_questionario_form=nuovo_questionario_form, quizzes=display_quiz)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
