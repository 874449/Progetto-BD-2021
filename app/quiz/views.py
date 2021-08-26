from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .forms import Question, EditorForm, EditForm, SingleAnswerForm
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
        flash("Modifiche salvate", 'success')

    return render_template('editor.html', editor_form=editor_form,
                           form=question, current_quiz=current_quiz, tipi_domanda=tipi_domanda)


@quiz.route('/editor/<quiz_id>/<question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(quiz_id, question_id):
    # query
    current_question = Domanda.query.filter_by(id=question_id).first()
    risposte = PossibileRisposta.query.filter_by(question_id=question_id).all()

    # forms
    risposte_form = SingleAnswerForm()
    form_dom = EditForm(obj=current_question)

    if risposte_form.add.data and risposte_form.validate():
        nuova_risp = PossibileRisposta(text=risposte_form.text.data, question_id=question_id)
        db.session.add(nuova_risp)
        db.session.commit()
        flash('Risposta aggiunta', 'success')
        return redirect(url_for('quiz.edit_question', quiz_id=quiz_id, question_id=question_id))

    if form_dom.submit.data and form_dom.validate():
        form_dom.populate_obj(current_question)
        db.session.commit()
        flash('Modifiche salvate', 'success')

    return render_template('question_editor.html', form=form_dom, risposte=risposte,
                           current_question=current_question, risposte_form=risposte_form,
                           quiz_id=quiz_id)


@quiz.route('/delete/<domanda_id>', methods=['POST'])
@login_required
def delete(domanda_id):
    # TODO security check proprietary role
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


@quiz.route('/remove/<quiz_id>/<answer_id>', methods=['POST'])
@login_required
def delete_answer(answer_id, quiz_id):
    query = PossibileRisposta.query.filter_by(id=answer_id).first()
    db.session.delete(query)
    db.session.commit()

    return redirect(url_for('quiz.edit_question', quiz_id=quiz_id, question_id=query.question_id))


@quiz.route('/view/<questionnaire_uuid>', methods=['GET', 'POST'])
def render(questionnaire_uuid):
    # query
    current_quiz = Questionario.query.filter_by(id=questionnaire_uuid).first()

    return render_template('visualize.html')
