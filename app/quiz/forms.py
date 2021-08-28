from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FormField, FieldList, IntegerField, \
    SelectField, validators
from wtforms.validators import Required, Length, Optional
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
    is_activated = BooleanField('E\' attivata da altre domande?', id='is_activated')
    activant = SelectField('Domanda che attiva questa domanda', coerce=int, id='select_activant', validators=[Optional()])  # , validators=[Required()])
    id_activant_answer = SelectField('Risposta che deve attivare questa domanda', coerce=int,
                                     id='select_id_activant_answer', validators=[Optional()])  # , validators=[Required()])
    # category_id = QuerySelectField('Tag',
    #                               query_factory=lambda: CategoriaDomanda.query.all(),
    #                               get_label='name')
    invia = SubmitField('Crea')


class SingleAnswerForm(FlaskForm):
    text = PageDownField('Testo della risposta...')
    add = SubmitField('Aggiungi')


class EditForm(FlaskForm):
    text = PageDownField('Testo', validators=[Required()])
    # type_id = QuerySelectField('type',
    #                           validators=[Required()],
    #                           query_factory=lambda: TipologiaDomanda.query.all(),
    #                           get_label='name')
    # category_id = QuerySelectField('Tag',
    #                               query_factory=lambda: CategoriaDomanda.query.all(),
    #                               get_label='name')
    # activant = BooleanField('Attivante')
    # activable = BooleanField('Attivabile')
    # possible_answers = FieldList(FormField(PossibleAnswerForm, default=lambda: PossibileRisposta(), min_entries=1))
    submit = SubmitField('Salva')


class EditorForm(FlaskForm):
    title = StringField('Titolo')
    description = PageDownField('Descrizione')
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


# TODO da implementare
class MultipleChoiceForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Register')
