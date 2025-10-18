from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('ticket.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    movie TEXT,
                    seat TEXT,
                    snacks TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        movie = request.form['movie']
        seat = request.form['seat']
        snacks = ', '.join(request.form.getlist('snacks'))

        conn = sqlite3.connect('ticket.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, movie, seat, snacks) VALUES (?, ?, ?, ?)",
                  (name, movie, seat, snacks))
        conn.commit()
        conn.close()

        return redirect(url_for('success', name=name))
    return render_template('book.html')

@app.route('/success/<name>')
def success(name):
    return render_template('success.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
