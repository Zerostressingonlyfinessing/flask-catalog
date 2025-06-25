from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Добавить')
