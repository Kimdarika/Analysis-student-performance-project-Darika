from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ------------------- Flask App Setup -------------------
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'student_performance'

# ------------------- MySQL Shim -------------------
class MySQLShim:
    def __init__(self, app):
        self.app = app

    @property
    def connection(self):
        if 'mysql_conn' not in g:
            cfg = self.app.config
            g.mysql_conn = pymysql.connect(
                host=cfg['MYSQL_HOST'],
                user=cfg['MYSQL_USER'],
                password=cfg['MYSQL_PASSWORD'],
                database=cfg['MYSQL_DB'],
                cursorclass=pymysql.cursors.Cursor,
                autocommit=True
            )
        return g.mysql_conn

def close_mysql_connection(exception=None):
    conn = g.pop('mysql_conn', None)
    if conn:
        conn.close()

mysql = MySQLShim(app)
app.teardown_appcontext(close_mysql_connection)

# ------------------- User Authentication -------------------

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        full_name = request.form.get('full_name', '')
        email = request.form.get('email', '')

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                flash("Username already exists!", "error")
                return redirect(url_for('register'))

            cur.execute("""
                INSERT INTO users (username, password_hash, role, full_name, email, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, hashed_password, role, full_name, email, datetime.now()))
            mysql.connection.commit()
            flash("✅ Registration successful! You can login now.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('register'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, password_hash, role FROM users WHERE username=%s", (username,))
            user = cur.fetchone()
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                session['username'] = username
                session['role'] = user[2]
                flash(f"Welcome {username}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password.", "error")
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

# ------------------- Protected Dashboard -------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

# ------------------- Home -------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ------------------- Run Flask -------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
