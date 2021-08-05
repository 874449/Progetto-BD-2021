from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, FormField, FieldList
from wtforms.validators import Required, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import ValidationError
from ..models import *
from .. import db


# QUIZ CREATION
'''dropdown_question_types = [
    ('1', 'Aperta'),
    ('2', 'Aperta obbligatoria'),
    ('3', 'A scelta singola'),
    ('4', 'A scelta multipla'),
    ('5', 'Numerica a interi'),
    ('6', 'Numerica floating point'),
    ('7', 'Data')
]'''

'''
Concept:
Dentro a editorForm vengono aggiunte le domande, quando schiaccio il + per una nuova domanda appare il module
per scegliere quale tipo di domanda fare e poi viene aggiunto il tipo corretto alla lista
'''


class Question(FlaskForm):
    question = StringField('Domanda')
    selection = QuerySelectField('type',
                                 validators=[Required()],
                                 query_factory=lambda: TipologiaDomanda.query.all(),
                                 get_label='name')
    activant = BooleanField('Attiva altre domande?')
    submit = SubmitField('Create')


class NewQuestion(FlaskForm):
    query = QuerySelectField('type')
    text = TextAreaField('Testo della domanda', validators=[Required()])


class EditorForm(FlaskForm):
    fields = FieldList(FormField(Question, default=lambda: Question()))
    submit = SubmitField('Salva')


class NewQuestionnaire(FlaskForm):
    titolo = StringField('Titolo', validators=[Required()])
    descrizione = TextAreaField('Descrizione')
    submit = SubmitField('Crea')


# QUESTIONS
class MandatoryQuestionForm(Question):
    question = StringField('Domanda', validators=[Required()])


class OpenQuestionForm(FlaskForm):
    answer = TextAreaField('Email', validators=[Required(), Length(1, 64)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class MultipleChoiceForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Register')