from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    is_published = BooleanField('Опубликовано')
    submit = SubmitField('Добавить')


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Текст')
    category_id = SelectField('Категория', choices=[])
    is_published = BooleanField('Опубликовано')
    submit = SubmitField('Добавить')
