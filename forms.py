from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание')
    price = FloatField('Цена', validators=[DataRequired()])
    image_url = StringField('Ссылка на изображение')
    category = SelectField('Категория', coerce=int)
    submit = SubmitField('Сохранить')