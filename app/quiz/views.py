from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . forms import Question, EditorForm, OpenQuestionForm, MandatoryQuestionForm
from . import quiz
from ..models import *
from .. import db


@quiz.route('/editor/<edit_id>', methods=['GET', 'POST'])
@login_required
def editor(edit_id):
    # queries
    current_quiz = Questionario.query.filter_by(id=edit_id).first()
    questions = Domanda.query.filter_by(quiz_id=edit_id).all()

    if not questions:
        db.session.add(Domanda('Testo di default', 1, False, edit_id))
        db.session.commit()

    # forms
    question = Question()
    editor_form = EditorForm(obj=current_quiz)

    if editor_form.validate_on_submit():
        editor_form.populate_obj(current_quiz)
        db.session.commit()
        flash("Saved changes", 'success')

    return render_template('editor.html', editor_form=editor_form,
                           form=question, current_quiz=current_quiz)


@quiz.route('/delete/question/<id_domanda>', methods=['POST'])
def delete_question(id_domanda):
    domanda = Domanda.query.filter_by(id=id_domanda).first()
    db.session.delete(domanda)
    db.session.commit()
    flash('Domanda cancellata', 'success')
    return redirect(url_for('quiz.editor', edit_id=domanda.quiz_id))


@quiz.route('/view/<questionnaire_id>', methods=['GET', 'POST'])
def render(questionnaire_id):
    # query
    current_quiz = Questionario.query.filter_by(id=questionnaire_id).first()
    quiz_questions = Domanda.query.filter_by(quiz_id=questionnaire_id).all()

    return render_template('visualize.html')
