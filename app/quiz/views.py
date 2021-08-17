from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .forms import Question, EditorForm, EditForm
from . import quiz
from ..models import *
from .. import db, moment


@quiz.route('/editor/<edit_id>', methods=['GET', 'POST'])
@login_required
def editor(edit_id):
    # queries
    current_quiz = Questionario.query.filter_by(id=edit_id).first()
    tipi_domanda = TipologiaDomanda.query.all()

    # forms
    question = Question()
    editor_form = EditorForm(obj=current_quiz)

    if question.validate_on_submit():
        domanda = Domanda(text=question.text.data, type_id=question.type_id.data.id,
                          activant=question.activant.data, quiz_id=edit_id)
        db.session.add(domanda)
        db.session.commit()
        flash('Nuova domanda creata', 'success')
        return redirect(url_for('quiz.editor', edit_id=current_quiz.id))

    if editor_form.validate_on_submit():
        editor_form.populate_obj(current_quiz)
        db.session.commit()
        flash("Saved changes", 'success')

    return render_template('editor.html', editor_form=editor_form,
                           form=question, current_quiz=current_quiz, tipi_domanda=tipi_domanda)


@quiz.route('/editor/<quiz_id>/<question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(quiz_id, question_id):
    current_question = Domanda.query.filter_by(id=question_id)
    form = EditForm(obj=current_question)
    if form.validate_on_submit():
        return redirect(url_for('quiz.edit_question', quiz_id=quiz_id, question_id=question_id))
    return render_template('question_editor.html', form=form, current_question=current_question, quiz_id=quiz_id)


@quiz.route('/delete/<domanda_id>', methods=['POST'])
@login_required
def delete(domanda_id):
    query1 = Domanda.query.filter_by(id=domanda_id).first()
    query2 = Questionario.query.filter_by(id=query1.quiz_id).first()
    if query1 and query2 and current_user.id == query2.author_id:
        db.session.delete(query1)
        db.session.commit()
        flash('Domanda rimossa', 'success')
        return redirect(url_for('quiz.editor', edit_id=query1.quiz_id))
    else:
        flash('Operazione invalida', 'danger')
        abort(403)


@quiz.route('/view/<questionnaire_id>', methods=['GET', 'POST'])
def render(questionnaire_id):
    # query
    current_quiz = Questionario.query.filter_by(id=questionnaire_id).first()

    return render_template('visualize.html')
