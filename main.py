from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    description = data['description']
    amount = data['amount']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (description, amount) VALUES (?, ?)', (description, amount))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/transactions')
def transactions():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()

    return jsonify([{'description': row[1], 'amount': row[2]} for row in transactions])

if __name__ == '__main__':
    app.run(debug=True)
