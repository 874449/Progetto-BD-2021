from flask import render_template, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import case

from .. models import *
from .. import db, moment
from ..quiz.forms import NewQuestionnaire
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
        scelte = PossibileRisposta.query.filter_by(question_id=domanda.id).all()
        for scelta in scelte:
            db.session.delete(scelta)
    db.session.commit()
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
        return redirect(url_for('quiz.editor', edit_uuid=nuovo.uuid))
    return render_template('main/dashboard.html', nuovo_questionario_form=nuovo_questionario_form, quizzes=display_quiz)


@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username)

    return render_template('main/profile.html', user=user)


@main.route('/quizzes')
@login_required
def quizzes():
    # TODO: view con la lista di tutti i questionari pubblici fatti dagli altri utenti.
    #  DECIDERE SE CREARE LA CONDIVISIONE PRIVATA DEI QUIZ!

    query = db.session.\
        query(
            Questionario.title, Questionario.description, Questionario.description_html,
            Questionario.timestamp, Questionario.uuid, User.username).\
        join(
            Questionario, User.id == Questionario.author_id)

    return render_template('main/quizzes.html', questionari=query)


@main.route('/responses/<quiz_id>')
@login_required
def responses(quiz_id):
    overview = get_overview(quiz_id)
    risposte = get_singole(quiz_id)
    return render_template('responses.html', overview=overview, risposte=risposte)


@main.route('/responses_overview/')
@login_required
def responses_overview():
    display_quiz = Questionario.query.filter_by(author_id=current_user.id).order_by(Questionario.id.desc()).all()
    return render_template('responses_overview.html', questionari=display_quiz)


def get_overview(quiz_id):
    subquery = db.session.query(RisposteQuestionario.id).filter(RisposteQuestionario.quiz_id == quiz_id)
    # , RisposteQuestionario.id == 1)
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
    print("RISPOSTE QUESTIONARIO: _------------------------------------------")
    print(risposte_questionario)
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
