from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, FormField
from wtforms.validators import Required, Length, Regexp
from wtforms import ValidationError
from ..models import *
from .. import db

# QUIZ CREATION
dropdown_question_types = [
    ('1', 'Aperta'),
    ('2', 'Aperta obbligatoria'),
    ('3', 'A scelta singola'),
    ('4', 'A scelta multipla'),
    ('5', 'Numerica a interi'),
    ('6', 'Numerica floating point'),
    ('7', 'Data')
]


class NewQuestion(FlaskForm):
    # dropdown_question_types = TipologiaDomanda.query.all()
    question = StringField('Domanda')
    selection = SelectField('type', validators=[Required()], choices=dropdown_question_types)
    activable = BooleanField('Domanda attivabile', validators=[])
    submit = SubmitField('Create')


class NewQuestionnaire(FlaskForm):
    titolo = StringField('Titolo', validators=[Required()])
    descrizione = TextAreaField('Descrizione')
    submit = SubmitField('Crea')


# QUESTIONS
class MandatoryQuestionForm(NewQuestion):
    question = StringField('Domanda', validators=[Required()])


class OpenQuestionForm(FlaskForm):
    answer = TextAreaField('Email', validators=[Required(), Length(1, 64)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class MultipleChoiceForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Register')