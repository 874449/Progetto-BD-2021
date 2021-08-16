from flask import render_template, flash, url_for, redirect
from flask_login import login_required, current_user
from .. models import *
from .. import db, moment
from ..quiz.forms import NewQuestionnaire
from . import main


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template("index.html")


@main.route('/delete/<quiz_id>', methods=['POST'])
@login_required
def delete(quiz_id):
    quiz = Questionario.query.filter_by(id=quiz_id).first()
    db.session.delete(quiz)
    db.session.commit()
    flash('Questionario cancellato', 'success')
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
        return redirect(url_for('quiz.editor', edit_id=nuovo.id))
    return render_template('dashboard.html', nuovo_questionario_form=nuovo_questionario_form, quizzes=display_quiz)


@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username)

    return render_template('profile.html')


@main.route('/quizzes')
@login_required
def quizzes():
    # TODO: view con la lista di tutti i questionari pubblici fatti dagli altri utenti.
    #  Sostanzialmente in pseudocodice dovrebbe essere una cosa tipo:
    #  1 - query per prendere tutti i quiz
    #  2 - if quiz in query is public:
    #  3 -  visualizza il quiz nell'elenco
    #  poi ci sarà un pulsante per entrare nel quiz e dare la propria risposta
    if current_user.is_authenticated:
        return render_template('quizzes.html')


@main.route('/responses/<quiz_id>')
@login_required
def responses(quiz_id):
    #risposte = session.query(User, Questionario).join(Questionario)
    return render_template('responses.html')
