from flask import Flask, render_template

app = Flask(__name__)

products = [
    {"id": 1, "name": "Товар 1", "price": 100},
    {"id": 2, "name": "Товар 2", "price": 200},
    {"id": 3, "name": "Товар 3", "price": 300}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
