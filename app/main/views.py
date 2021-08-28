from flask import render_template, flash, url_for, redirect, Response
from flask_login import login_required, current_user
from sqlalchemy import case
import io
import csv

from .. models import *
from .. import db, moment
from ..quiz.forms import NewQuestionnaire
from . forms import EditProfileForm
from . import main
from sqlalchemy.dialects import postgresql


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main/index.html')
    return render_template("main/index.html")


@main.route('/delete/<quiz_uuid>', methods=['POST'])
@login_required
def delete(quiz_uuid):
    # TODO tripla query annidata, bisognerebbe sistemare il file models per far funzionare il delete on cascade...
    quiz = Questionario.query.filter_by(uuid=quiz_uuid).first()
    domande = Domanda.query.filter_by(quiz_id=quiz.id).all()
    for domanda in domande:
        statement = have_as_answer.delete().values(
            question_id=domanda.id
        )
        db.session.execute(statement)
        db.session.flush()
        # PossibileRisposta.query.filter_by(question_id=domanda.id).delete()

    RisposteQuestionario.query.filter_by(quiz_id=quiz.id).delete()
    db.session.delete(quiz)
    db.session.commit()
    flash('Questionario cancellato', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # query per prendere tutti i questionari dell'utente
    display_quiz = Questionario.query.filter_by(author_id=current_user.id).order_by(Questionario.id.desc()).all()

    # form
    nuovo_questionario_form = NewQuestionnaire()
    if nuovo_questionario_form.validate_on_submit():
        # registrazione dei dati passati dal form al db
        title = nuovo_questionario_form.titolo.data
        description = nuovo_questionario_form.descrizione.data
        nuovo = Questionario(title=title, description=description, author_id=current_user.id)
        db.session.add(nuovo)
        db.session.commit()
        flash('Questionario creato con successo', 'success')
        # una volta creato il questionario si viene reindirizzati all'editor
        return redirect(url_for('quiz.editor', edit_uuid=nuovo.uuid))
    return render_template('main/dashboard.html', nuovo_questionario_form=nuovo_questionario_form, quizzes=display_quiz)


@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Modifiche salvate.', 'success')
        return redirect(url_for('.profile', username=current_user.username))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.location.data = current_user.location
    return render_template('main/profile.html', form=form)


@main.route('/quizzes')
@login_required
def quizzes():
    query = db.session.\
        query(
            Questionario.title, Questionario.description, Questionario.description_html,
            Questionario.timestamp, Questionario.uuid, User.username).\
        join(
            Questionario, User.id == Questionario.author_id)

    return render_template('main/quizzes.html', questionari=query)


@main.route('/responses/<quiz_uuid>')
@login_required
def responses(quiz_uuid):
    current_quiz = Questionario.query.filter_by(uuid=quiz_uuid).first()
    overview = get_overview(current_quiz.id)
    risposte = get_singole(current_quiz.id)
    return render_template('responses.html', current_quiz=current_quiz, overview=overview, risposte=risposte)


@main.route('/responses_overview/')
@login_required
def responses_overview():
    display_quiz = Questionario.query.filter_by(author_id=current_user.id).order_by(Questionario.id.desc()).all()
    return render_template('responses_overview.html', questionari=display_quiz)


def get_overview(quiz_id):
    subquery = db.session.query(RisposteQuestionario.id).filter(RisposteQuestionario.quiz_id == quiz_id)
    risposte = db.session.query(Domanda.text.label('Domanda'), Domanda.type_id.label('Tipo'),
                                Domanda.id.label('Id_domanda'),
                                case((RispostaDomanda.is_open, RispostaDomanda.text),
                                     else_=PossibileRisposta.text).label('Risposta')).join(RispostaDomanda) \
        .outerjoin(RispostaDomanda.have_as_answers).filter(RispostaDomanda.id.in_(subquery)) \
        .order_by(Domanda.id, RispostaDomanda.id)
    # print(str(risposte.statement.compile(dialect=postgresql.dialect())))
    overview = {}
    # formato dizionario:{("Domanda1","Tipo_di_domanda"):{"Risposta1":numero di risposte,"Risposta2":numero_di_risposte)
    # inizializzazione del dizionario
    # 1 = aperta
    # 2 = scelta
    # 3 = multipla
    for i in risposte:
        overview[(i.Domanda, i.Tipo)] = {}
        if i.Tipo != 1:
            possibili_risposte = PossibileRisposta.query.filter(PossibileRisposta.question_id == i.Id_domanda).all()
            for j in possibili_risposte:
                overview[(i.Domanda, i.Tipo)][j.text] = 0
    # valorizzazione delle riposte multiple nel dizionario
    for i in risposte:
        if i.Tipo == 1:
            overview[(i.Domanda, i.Tipo)][i.Risposta] = 1
        else:
            overview[(i.Domanda, i.Tipo)][i.Risposta] += 1
    return overview


def get_singole(quiz_id):
    risposte_questionario = db.session.query(RisposteQuestionario.id).filter(RisposteQuestionario.quiz_id == quiz_id).all()
    risposte_singole = {}
    for r in risposte_questionario:
        i = r.id
        print(i)
        subquery = db.session.query(RisposteQuestionario.id).filter(RisposteQuestionario.quiz_id == quiz_id,
                                                                    RisposteQuestionario.id == i)
        risposte = db.session.query(Domanda.text.label('Domanda'),
                                    case((RispostaDomanda.is_open, RispostaDomanda.text),
                                         else_=PossibileRisposta.text).label('Risposta')).join(RispostaDomanda) \
            .outerjoin(RispostaDomanda.have_as_answers).filter(RispostaDomanda.id.in_(subquery)) \
            .order_by(Domanda.id, RispostaDomanda.id)
        for j in risposte:
            risposte_singole[i] = {}
        for j in risposte:
            if j.Domanda not in risposte_singole[i]:
                risposte_singole[i][j.Domanda] = [j.Risposta]
            else:
                risposte_singole[i][j.Domanda].append(j.Risposta)
    print(risposte_singole)
    return risposte_singole


@main.route('/download/csv/<uuid>')
@login_required
def download(uuid):
    # query per prendere il database e le risposte
    current_quiz = Questionario.query.filter_by(uuid=uuid).first()
    risposte = RisposteQuestionario.query.filter_by(quiz_id=current_quiz.id).all()

    # get singole restituisce un dizionario con le risposte ad ogni domanda nel formato
    # { key = risposta.id, value = dizionario{ domanda: risposta } }
    data = get_singole(current_quiz.id)

    '''
    generazione della lista con gli id delle risposte:
        dal momento che la variabile
    '''
    lista_risposte_id = [r.id for r in risposte]

    # stream output
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[lista_risposte_id[0]].keys())

    writer.writeheader()
    for i in range(0, len(data)):
        writer.writerow(data[lista_risposte_id[i]])

    output.seek(0)
    return Response(output,
                    mimetype="text/csv",
                    headers={f"Content-Disposition": f"attachment;filename={current_quiz.title}.csv"})
