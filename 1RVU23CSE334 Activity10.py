from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('store.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS products
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         price REAL, 
                         quantity INTEGER)''')

@app.route('/')
def home():
    with sqlite3.connect('store.db') as conn:
        products = conn.execute('SELECT * FROM products').fetchall()
    return render_template('store.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    with sqlite3.connect('store.db') as conn:
        conn.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_product():
    product_id = int(request.form['id'])
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    with sqlite3.connect('store.db') as conn:
        conn.execute('UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?', (name, price, quantity, product_id))
    return 'Product updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_product():
    product_id = int(request.form['id'])
    with sqlite3.connect('store.db') as conn:
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    return 'Product deleted successfully!'

@app.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('query', '')
    with sqlite3.connect('store.db') as conn:
        results = conn.execute('SELECT * FROM products WHERE name LIKE ?', (f'%{search_query}%',)).fetchall()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(port=9001)
