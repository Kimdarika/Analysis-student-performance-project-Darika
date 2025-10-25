from flask import Flask, render_template, request, redirect, url_for, session, g
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

# --- Flask Setup ---
app = Flask(__name__)
app.secret_key = "secret123"

# --- MySQL Config ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'student_performance'

# --- MySQL Connection Shim ---
class MySQLShim:
    def __init__(self, app):
        self.app = app

    @property
    def connection(self):
        if 'mysql_conn' not in g:
            cfg = self.app.config
            g.mysql_conn = pymysql.connect(
                host=cfg.get('MYSQL_HOST', 'localhost'),
                user=cfg.get('MYSQL_USER', ''),
                password=cfg.get('MYSQL_PASSWORD', ''),
                database=cfg.get('MYSQL_DB', ''),
                cursorclass=pymysql.cursors.Cursor,
                autocommit=True
            )
        return g.mysql_conn

def close_mysql_connection(exception=None):
    conn = g.pop('mysql_conn', None)
    if conn is not None:
        conn.close()

mysql = MySQLShim(app)
app.teardown_appcontext(close_mysql_connection)

# --- Routes ---

# Home redirects to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']
        role = request.form['role']
        full_name = request.form.get('full_name')
        email = request.form.get('email')

        if password != confirm:
            message = "❌ Passwords do not match!"
        elif not username or not password or not role:
            message = "❌ Please fill in all required fields!"
        else:
            hashed_password = generate_password_hash(password)
            try:
                conn = mysql.connection
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO users (username, password, role, full_name, email)
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, hashed_password, role, full_name, email))
                conn.commit()
                cur.close()
                message = "✅ Registration successful! <a href='/login'>Login here</a>"
            except pymysql.err.IntegrityError:
                message = "❌ Username already exists!"
            except Exception as e:
                message = f"❌ Error: {str(e)}"

    return render_template('register.html', message=message)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT password, role FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            session['role'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            message = "❌ Invalid username or password!"

    return render_template('login.html', message=message)

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
