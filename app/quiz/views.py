from flask import render_template, flash, redirect, request, url_for, abort
from flask_login import login_required, current_user
from .forms import Question, EditorForm, EditForm, SingleAnswerForm
from . import quiz
from ..models import *
from .. import db, moment

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectMultipleField, SubmitField, FormField, FieldList, RadioField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField


@quiz.route('/editor/<edit_uuid>', methods=['GET', 'POST'])
@login_required
def editor(edit_uuid):
    # queries
    current_quiz = Questionario.query.filter_by(uuid=edit_uuid).first()
    tipi_domanda = TipologiaDomanda.query.all()
    subquery = db.session.query(TipologiaDomanda.id).filter(TipologiaDomanda.name == "Scelta")
    # attivante = db.session.query(Domanda.id, Domanda.text, PossibileRisposta.id, PossibileRisposta.text)\
    #    .join(PossibileRisposta).filter(Domanda.type_id.in_(subquery), Domanda.quiz_id == current_quiz)
    #print(current_quiz.id)
    attivante = db.session.query(Domanda.id, Domanda.text).filter(Domanda.type_id.in_(subquery),
                                                                  Domanda.quiz_id == current_quiz.id)
    attivante_list = [(i.id, i.text) for i in attivante]


    # forms
    question = Question()
    question.activant.choices = attivante_list
    editor_form = EditorForm(obj=current_quiz)

    if question.validate_on_submit():
        domanda = Domanda(text=question.text.data, type_id=question.type_id.data.id,
                          activant=question.is_activated.data, quiz_id=current_quiz.id)
        db.session.add(domanda)
        db.session.commit()
        flash('Nuova domanda creata', 'success')
        return redirect(url_for('quiz.editor', edit_uuid=current_quiz.uuid))

    if editor_form.validate_on_submit():
        editor_form.populate_obj(current_quiz)
        db.session.commit()
        flash("Modifiche salvate", 'success')

    return render_template('quiz/editor.html', editor_form=editor_form,
                           form=question, current_quiz=current_quiz, tipi_domanda=tipi_domanda)


@quiz.route('/editor/<quiz_uuid>/<question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(quiz_uuid, question_id):
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
        return redirect(url_for('quiz.edit_question', quiz_uuid=quiz_uuid, question_id=question_id))

    if form_dom.submit.data and form_dom.validate():
        form_dom.populate_obj(current_question)
        db.session.commit()
        flash('Modifiche salvate', 'success')

    return render_template('quiz/question_editor.html', form=form_dom, risposte=risposte,
                           current_question=current_question, risposte_form=risposte_form,
                           quiz_uuid=quiz_uuid)


@quiz.route('/delete/<domanda_id>', methods=['POST'])
@login_required
def delete(domanda_id):
    # TODO security check proprietary role
    query1 = Domanda.query.filter_by(id=domanda_id).first()
    query2 = Questionario.query.filter_by(id=query1.quiz_id).first()
    query3 = PossibileRisposta.query.filter_by(question_id=domanda_id).all()

    if query1 and query2 and current_user.id == query2.author_id:
        for elem in query3:
            db.session.delete(elem)
        db.session.commit()
        db.session.delete(query1)
        db.session.commit()
        flash('Domanda rimossa', 'success')
        return redirect(url_for('quiz.editor', edit_uuid=query2.uuid))
    else:
        flash('Operazione invalida', 'danger')
        abort(403)


@quiz.route('/remove/<quiz_uuid>/<answer_id>', methods=['POST'])
@login_required
def delete_answer(answer_id, quiz_uuid):
    query = PossibileRisposta.query.filter_by(id=answer_id).first()
    db.session.delete(query)
    db.session.commit()

    return redirect(url_for('quiz.edit_question', quiz_uuid=quiz_uuid, question_id=query.question_id))


@quiz.route('/view/<questionnaire_uuid>', methods=['GET', 'POST'])
def render(questionnaire_uuid):

    class CompilationForm(FlaskForm):
        submit = SubmitField('Invia', render_kw={'class': 'btn btn-info'})

    # query
    current_quiz = Questionario.query.filter_by(uuid=questionnaire_uuid).first()

    domande = current_quiz.questions.all()
    print('\nDEBUG domande')
    print(f'quante domande appartengono al questionario: {len(domande)}')
    print(domande)

    iterator = 0
    for domanda in domande:
        if domanda.type_id == 1:
            setattr(CompilationForm, 'domanda' + str(iterator), TextAreaField('Risposta aperta',
                                                                              render_kw={'class': 'form-control'})
                    )
        elif domanda.type_id == 3:
            setattr(CompilationForm, 'domanda' + str(iterator), RadioField(
                choices=[(q.id, q.text) for q in PossibileRisposta.query.filter_by(question_id=domanda.id)],
                render_kw={'class': 'form-check', 'type': 'radio'}
            ))
        else:
            setattr(CompilationForm, 'domanda' + str(iterator), SelectMultipleField(
                choices=[(q.id, q.text) for q in PossibileRisposta.query.filter_by(question_id=domanda.id)],
                render_kw={'class': 'form-select'}
            ))
        iterator += 1

    risposte_possibili = PossibileRisposta.query.all()

    form = CompilationForm()

    if form.validate_on_submit():
        iterator = 0
        for dom in domande:
            print(request.form.get('domanda' + str(iterator)))
            if dom.type_id == 1:
                db.session.add(RispostaDomanda(
                    question_id=dom.id, is_open=True, text=request.form.get('domanda' + str(iterator))
                ))
            else:
                db.session.add(RispostaDomanda(
                    question_id=dom.id, is_open=False
                ))
            iterator += 1
        # db.session.add(RisposteQuestionario(quiz_id=current_quiz.id))
        # db.session.commit()

    return render_template('visualize.html', current_quiz=current_quiz, domande=domande,
                           risposte_possibili=risposte_possibili, form=form, dim=len(domande))
