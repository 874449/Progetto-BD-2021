from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import Question, EditorForm, OpenQuestionForm, MandatoryQuestionForm
from . import quiz
from ..models import *
from .. import db, moment


@quiz.route('/editor/<edit_id>', methods=['GET', 'POST'])
@login_required
def editor(edit_id):
    # queries
    current_quiz = Questionario.query.filter_by(id=edit_id).first()
    questions = Domanda.query.filter_by(quiz_id=edit_id).all()

    if not questions:
        db.session.add(Domanda(text='', type_id=1, activant=False, quiz_id=edit_id))
        db.session.commit()

    # forms
    question = Question()
    editor_form = EditorForm(obj=current_quiz)

    if editor_form.validate_on_submit():
        # editor_form.populate_obj(current_quiz)  --- it doesn't work
        current_quiz.title = editor_form.title.data
        current_quiz.description = editor_form.description.data
        i = 0
        max_len = len(current_quiz.questions.all())
        for elem in editor_form.questions.data:
            if i < max_len:
                setattr(current_quiz.questions[i], 'text', elem['text'])
                setattr(current_quiz.questions[i], 'type_id', str(elem['type_id']))
                setattr(current_quiz.questions[i], 'activant', elem['activant'])
                i = i + 1
            else:
                domanda = Domanda(text=elem['text'],
                                  type_id=str(elem['type_id']),
                                  activant=elem['activant'],
                                  quiz_id=edit_id)
                db.session.add(domanda)

        db.session.commit()
        flash("Saved changes", 'success')

    return render_template('editor.html', editor_form=editor_form,
                           form=question, current_quiz=current_quiz)


@quiz.route('/view/<questionnaire_id>', methods=['GET', 'POST'])
def render(questionnaire_id):
    # query
    current_quiz = Questionario.query.filter_by(id=questionnaire_id).first()
    quiz_questions = Domanda.query.filter_by(quiz_id=questionnaire_id).all()

    return render_template('visualize.html')
