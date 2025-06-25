from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    price = FloatField('Цена', validators=[DataRequired()])
    image_url = StringField('Ссылка на изображение')
    submit = SubmitField('Добавить')
