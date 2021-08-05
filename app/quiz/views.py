from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . forms import NewQuestion, OpenQuestionForm, MandatoryQuestionForm
from . import quiz
from ..models import *
from .. import db


@quiz.route('/editor/<int:editID>', methods=['GET', 'POST'])
@login_required
def editor(editID):
    form = NewQuestion()
    # print(f'[EDITING] QUIZ n {editID}')
    if form.validate_on_submit():
        activable = False
        domanda = Domanda(form.question.data, form.activant.data, editID)
        db.session.add(domanda)
    return render_template('editor.html', form=form)

