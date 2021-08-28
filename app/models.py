"""
Nel file models.py è contenuto lo schema relazionale del DB.
In questo caso è stata utilizzata la libreria flask-SQLAlchemy basata sul modello ORM:
ciò vuol dire che ad ogni classe corrisponde una tabella del DB sottostante.
"""
from . import db
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from uuid import uuid4
from markdown import markdown
import bleach
from . import login_manager

'''
Concept:
la maggior parte delle classi ha un costruttore (il metodo '__init__') che viene utilizzato
per l'inserimento degli oggetti nel database.

Il metodo '__repr__' è stato definito per rappresentare come stringa le varie classi
ed è utilizzato per scopi di debug.
'''


# TODO: creare ruoli e permessi per:
#  admin - l'amministratore che può fare tutte le query e controllare ciò che fanno gli utenti
#  utente normale - può creare quiz, editarli e invitare al questionario gli altri utenti
#  utente anonimo - può solo visualizzare e compilare i quiz a cui è invitato
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role: {self.name}>'


# la classe User è figlia della classe UserMixin: una classe apposita che contiene implementazioni
# standard per semplificare la compatibilità con la libreria flask-login
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    quizzes = db.relationship('Questionario', cascade="all,delete", backref='owner', lazy='dynamic')

    '''
    per questioni di sicurezza l'attributo password non è direttamente accessibile, quindi
    la password viene letta e settata solo tramite hash
    '''
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User: {self.username} with email: {self.email}>'


class Questionario(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, default=uuid4())
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    description_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Domanda', cascade="all,delete", backref='in', lazy='dynamic')

    def __repr__(self):
        return f'<Questionario: {self.title} with {self.id}, owned by: {self.author_id}>'

    @staticmethod
    def on_changed_description(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'math']
        target.description_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Questionario.description, 'set', Questionario.on_changed_description)


# TODO: un trigger per quando si aggiunge una risposta alla domanda viene registrata la risposta anche qua
class RisposteQuestionario(db.Model):
    __tablename__ = 'quiz_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))


have_as_answer = db.Table('have_as_answer',
                          db.Column('possible_answer_id', db.Integer, primary_key=True),
                          db.Column('answer_to_questions_id', db.Integer, primary_key=True),
                          db.Column('question_id', db.Integer, primary_key=True),
                          db.ForeignKeyConstraint(['answer_to_questions_id', 'question_id'],
                                                  ['answers_to_questions.id', 'answers_to_questions.question_id'],
                                                  name='fk_answer_to_questions'),
                          db.ForeignKeyConstraint(['possible_answer_id'], ['possible_answers.id'],
                                                  name='fk_possible_answers')
                          )


class RispostaDomanda(db.Model):
    __tablename__ = 'answers_to_questions'
    id = db.Column(db.Integer, db.ForeignKey('quiz_answers.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    is_open = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.Text, nullable=True)
    text_html = db.Column(db.Text)
    have_as_answers = db.relationship('PossibileRisposta', secondary=have_as_answer,
                                      backref=db.backref('answers_to_questions', lazy='joined'))

    def __repr__(self):
        return f'Risposta: {self.text}'

    @staticmethod
    def on_changed_text(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'math']
        target.text_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(RispostaDomanda.text, 'set', RispostaDomanda.on_changed_text)


#class HannoComeRisposta(db.Model):
#    __tablename__ = 'have_as_answer'
#    possible_answers_id = db.Column(db.Integer, db.ForeignKey('possible_answers.id'), primary_key=True)
#    answers_to_questions_id = db.Column(db.Integer, primary_key=True)
#    question_id = db.Column(db.Integer, primary_key=True)
#    db.ForeignKeyConstraint(['answers_to_questions_id', 'question_id'],
#                            ['answers_to_questions.id', 'answers_to_questions.question_id'])


class Domanda(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    text_html = db.Column(db.Text)
    activant = db.Column(db.Boolean)
    activable_question = db.Column(db.Integer, db.ForeignKey('questions.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('questions_category.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('questions_type.id'))
    activant_answer_id = db.Column(db.Integer, db.ForeignKey('possible_answers.id'))
    #possible_answers = db.relationship('PossibileRisposta', cascade="all,delete", backref='domanda_a_scelta',
    #                                   lazy='dynamic', primaryjoin=id == PossibileRisposta.question_id)
    answers = db.relationship('RispostaDomanda', cascade="all,delete", backref='domanda', lazy='dynamic',
                              primaryjoin=id == RispostaDomanda.question_id)

    def __repr__(self):
        return f'<Domanda{self.id}: {self.text}>'

    @staticmethod
    def on_changed_text(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'math']
        target.text_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Domanda.text, 'set', Domanda.on_changed_text)


class PossibileRisposta(db.Model):
    __tablename__ = 'possible_answers'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    text_html = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    active_question = db.relationship('Domanda', backref='risposta_attivante',
                                      primaryjoin=id == Domanda.activant_answer_id)
    #answers_to_questions = db.relationship('RispostaDomanda', secondary=have_as_answer,
    #                                       backref=db.backref('possible_answers', lazy='joined'))

    @staticmethod
    def on_changed_text(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'math']
        target.text_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(PossibileRisposta.text, 'set', PossibileRisposta.on_changed_text)


class CategoriaDomanda(db.Model):
    __tablename__ = 'questions_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), default='No description')
    questions = db.relationship('Domanda', backref='categoria', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'Categoria Domanda: id = {self.id}, name = {self.name}'


class TipologiaDomanda(db.Model):
    __tablename__ = 'questions_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), default='No description')
    questions = db.relationship('Domanda', backref='tipologia', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'{self.id}'


# callback function for flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
