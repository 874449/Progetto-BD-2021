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
    questions = current_quiz.questions

    # DEBUG
    print(questions)
    # forms
    question = Question()
    editor_form = EditorForm()

    if editor_form.validate_on_submit():
        pass
    if question.validate_on_submit():
        activable = False
        domanda = Domanda(question.question.data, question.activant.data, edit_id)
        # db.session.add(domanda)
        # db.session.commit()
    return render_template('editor.html', editor_form=editor_form, form=question, current_quiz=current_quiz)
