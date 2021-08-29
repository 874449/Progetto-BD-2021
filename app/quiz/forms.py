from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import Required, Length, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_pagedown.fields import PageDownField
from wtforms import widgets
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
    text = StringField('Testo della risposta...')
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


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
