from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product
from forms import ProductForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['PRODUCT_ADD_PASSWORD'] = '1234'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        if form.password.data != app.config['PRODUCT_ADD_PASSWORD']:
            flash('Неверный пароль', 'danger')
            return render_template('add_product.html', form=form)

        new_product = Product(name=form.name.data, price=form.price.data)
        db.session.add(new_product)
        db.session.commit()
        flash('Товар добавлен', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)