from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    start_datetime = DateTimeField('Дата и время начала', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Дата и время окончания', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Место', validators=[Length(max=200)])
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')