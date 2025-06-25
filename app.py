from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from forms import ProductForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import Product

@app.route('/')
def home():
    return '<h1>Главная страница</h1><a href="/add">Добавить товар</a> | <a href="/login">Вход</a> | <a href="/logout">Выход</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == app.config['ADMIN_PASSWORD']:
            session['admin'] = True
            return redirect(url_for('add_product'))
        else:
            error = 'Неверный пароль'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin'):
        return redirect(url_for('login'))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_product.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
