from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms import HiddenField


class NoteForm(FlaskForm):
    note_id = HiddenField('ID заметки')
    content = StringField('Название заметки', validators=[DataRequired()])
    info = TextAreaField('Основная информация', validators=[DataRequired()])
    is_task = BooleanField('Задача')
    timer = DateTimeField('Дедлайн', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField('Сохранить')
    