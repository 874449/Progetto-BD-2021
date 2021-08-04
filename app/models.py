"""
Nel file models.py è contenuto lo schema relazionale del DB.
In questo caso è stata utilizzata la libreria flask-SQLAlchemy basata sul modello ORM:
ciò vuol dire che ad ogni classe corrisponde una tabella del DB sottostante.
"""
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

'''
Concept:
la maggior parte delle classi ha un costruttore (il metodo '__init__') che viene utilizzato
per l'inserimento degli oggetti nel database.

Il metodo '__repr__' è stato definito per rappresentare come stringa le varie classi
ed è utilizzato per scopi di debug.
'''


# TODO: è necessaria la tabella role?
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
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    quizzes = db.relationship('Questionario', backref='owner', lazy='dynamic')

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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User: {self.username} with email: {self.email}>'


class Questionario(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Domanda', backref='in', lazy='dynamic')
    answers = db.relationship('RispostaDomanda', backref='questionario', lazy='dynamic')  # TODO da rimuovere, è di test

    def __init__(self, title, description, owner_id):
        self.title = title
        self.description = description
        self.author_id = owner_id

    def __repr__(self):
        return f'<Questionario: {self.title} with {self.id}, owned by: {self.author_id}>'


class Domanda(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    choice_question = db.Column(db.Boolean, nullable=False)
    activant = db.Column(db.Boolean, nullable=False)
    activable_question = db.Column(db.Integer, db.ForeignKey('questions.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('questions_category.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('questions_type.id'))
    answers = db.relationship('RispostaDomanda', backref='domanda', lazy='dynamic')

    def __init__(self, text, activable, quiz_id):
        self.text = text
        self.activable_question = activable
        self.quiz_id = quiz_id

    def __repr__(self):
        return f'<Domanda{self.id}: {self.text}>'


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
        return f'Tipologia Domanda: id = {self.id}, name = {self.name}'


# TODO: idea! non sarebbe possibile integrare questa tabella direttamente nelle risposteDomande
#  e poi richiamare le domande per essere scelte dall'utente nel form?
class PossibileRisposta(db.Model):
    __tablename__ = 'possible_answers'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))


class RispostaDomanda(db.Model):
    __tablename__ = 'answers_to_questions'
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.Text, nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))  # TODO da rimuovere, è una FK per test

    def __init__(self, is_open, text):
        self.text = text
        self.is_open = is_open

    def __repr__(self):
        return f'Risposta: {self.text}'


# callback function for flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
