from flask import Flask, render_template, request, redirect, url_for
from models import db, Product
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
db.init_app(app)

ADMIN_PASSWORD = "admin123"

@app.route('/')
def index():
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    products = Product.query

    if category:
        products = products.filter_by(category=category)
    if min_price:
        products = products.filter(Product.price >= min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)

    products = products.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != ADMIN_PASSWORD:
            return "Unauthorized", 403
        name = request.form['name']
        price = int(request.form['price'])
        description = request.form['description']
        category = request.form['category']
        image = request.files['image']
        filename = image.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)

        product = Product(name=name, price=price, description=description, category=category, image=filename)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
