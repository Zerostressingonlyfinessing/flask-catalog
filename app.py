from flask import Flask, render_template, redirect, url_for, request, session
from models import db, Product, Category
from forms import ProductForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    if not Category.query.first():
        db.session.add(Category(name="Одежда"))
        db.session.add(Category(name="Электроника"))
        db.session.add(Category(name="Книги"))
        db.session.commit()

@app.route('/')
def home():
    return redirect(url_for('catalog'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == app.config['ADMIN_PASSWORD']:
            session['admin'] = True
            return redirect(url_for('catalog'))
        return 'Неверный пароль', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('catalog'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin'):
        return redirect(url_for('login'))
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data,
            category_id=form.category.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('catalog'))
    return render_template('add_product.html', form=form)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image_url = form.image_url.data
        product.category_id = form.category.data
        db.session.commit()
        return redirect(url_for('catalog'))
    return render_template('edit_product.html', form=form)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    db.session.delete(Product.query.get_or_404(product_id))
    db.session.commit()
    return redirect(url_for('catalog'))

@app.route('/catalog')
def catalog():
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category_id:
        query = query.filter_by(category_id=category_id)
    products = query.all()
    categories = Category.query.all()
    return render_template('catalog.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(host='0.0.0.0', port=8000)