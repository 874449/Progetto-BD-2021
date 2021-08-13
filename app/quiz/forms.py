from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FormField, FieldList, IntegerField, Form
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


class Question(Form):
    text = StringField('Domanda', validators=[Required()])
    # type_id = QuerySelectField('type',
    #                           validators=[Required()],
    #                           query_factory=lambda: TipologiaDomanda.query.all(),
    #                           get_label='name')
    activant = BooleanField('Attiva altre domande?')
    # category_id = QuerySelectField('Tag',
    #                               query_factory=lambda: CategoriaDomanda.query.all(),
    #                               get_label='name')


class NewQuestion(FlaskForm):
    query = QuerySelectField('type',
                             validators=[Required()],
                             query_factory=lambda: TipologiaDomanda.query.all(),
                             get_label='name')
    # text = TextAreaField('Testo della domanda', validators=[Required()])
    submit = SubmitField('Create')


class EditorForm(FlaskForm):
    title = StringField('Titolo')
    description = TextAreaField('Descrizione')
    questions = FieldList(FormField(Question, default=lambda: Question()), min_entries=1)
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


class NumericQuestionForm(Question):
    answer = IntegerField('Inserisci un numero intero per rispondere')


class MultipleChoiceForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Register')