from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FormField, FieldList, IntegerField, Form
from wtforms.validators import Required, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_pagedown.fields import PageDownField
from wtforms import ValidationError
from ..models import *
from .. import db


# QUIZ CREATION
''' at the moment in DB:
dropdown_question_types:
    ('1', 'Aperta')
    ('2', 'A scelta multipla')
    ('3', 'A scelta singola')
    ('4', 'Numerica a interi')
'''

'''
Concept:
Dentro a editorForm vengono aggiunte le domande, quando schiaccio il + per una nuova domanda appare il module
per scegliere quale tipo di domanda fare e poi viene aggiunto il tipo corretto alla lista
'''


class Question(FlaskForm):
    text = PageDownField('Domanda', validators=[Required()])
    type_id = QuerySelectField('type',
                               validators=[Required()],
                               query_factory=lambda: TipologiaDomanda.query.all(),
                               get_label='name')
    activant = BooleanField('Attiva altre domande?')
    # category_id = QuerySelectField('Tag',
    #                               query_factory=lambda: CategoriaDomanda.query.all(),
    #                               get_label='name')
    submit = SubmitField('Crea')


class EditForm(FlaskForm):
    text = StringField('Testo')
    activant = BooleanField('Attivante')
    activable = BooleanField('Attivabile')


class EditorForm(FlaskForm):
    title = StringField('Titolo')
    description = PageDownField('Descrizione')
    # questions = FieldList(FormField(Question, default=lambda: Question()), min_entries=1)
    submit = SubmitField('Salva')


class NewQuestionnaire(FlaskForm):
    titolo = StringField('Titolo', validators=[Required()])
    descrizione = PageDownField('Descrizione')
    submit = SubmitField('Crea')


# QUESTIONS
class OpenQuestionForm(FlaskForm):
    answer = TextAreaField('Email', validators=[Required(), Length(1, 64)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class NumericQuestionForm(Question):
    answer = IntegerField('Inserisci un numero intero per rispondere')


class MultipleChoiceForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Register')
