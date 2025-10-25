from flask import Flask, render_template, request, jsonify, redirect, url_for, g
import pymysql
import pymysql.cursors
class MySQLShim:
    def __init__(self, app):
        self.app = app

    @property
    def connection(self):
        # reuse connection per request
        if 'mysql_conn' not in g:
            cfg = self.app.config
            g.mysql_conn = pymysql.connect(
                host=cfg.get('MYSQL_HOST', 'localhost'),
                user=cfg.get('MYSQL_USER', ''),
                password=cfg.get('MYSQL_PASSWORD', ''),
                database=cfg.get('MYSQL_DB', ''),
                cursorclass=pymysql.cursors.Cursor,
                autocommit=False,
            )
        return g.mysql_conn

def close_mysql_connection(exception=None):
    conn = g.pop('mysql_conn', None)
    if conn is not None:
        try:
            conn.close()
        except Exception:
            pass

from datetime import datetime
import json

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'student_performance'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize shim and teardown
mysql = MySQLShim(app)
app.teardown_appcontext(close_mysql_connection)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students ORDER BY name")
        students = cur.fetchall()
        cur.close()
        
        student_list = []
        for student in students:
            student_list.append({
                'id': student[0],
                'student_id': student[1],
                'name': student[2],
                'email': student[3],
                'program': student[4],
                'enrollment_date': student[5].strftime('%Y-%m-%d') if student[5] else None
            })
        
        return jsonify(student_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add new student
@app.route('/api/students', methods=['POST'])
def add_student():
    try:
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO students (student_id, name, email, program, enrollment_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['student_id'], data['name'], data['email'], data['program'], data['enrollment_date']))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get subjects by term
@app.route('/api/subjects/<int:term>', methods=['GET'])
def get_subjects(term):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM subjects WHERE term_number = %s", (term,))
        subjects = cur.fetchall()
        cur.close()
        
        subject_list = []
        for subject in subjects:
            subject_list.append({
                'id': subject[0],
                'code': subject[1],
                'name': subject[2],
                'term': subject[3],
                'skill_type': subject[4]
            })
        
        return jsonify(subject_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add assessment score
@app.route('/api/assessments', methods=['POST'])
def add_assessment():
    try:
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO assessments (student_id, subject_id, term_number, assessment_type, score, max_score, date, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['student_id'], data['subject_id'], data['term_number'], 
              data['assessment_type'], data['score'], data['max_score'], 
              data['date'], data.get('notes', '')))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Assessment added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get student performance data
@app.route('/api/performance/<int:student_id>', methods=['GET'])
def get_performance(student_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT a.*, s.name as subject_name, s.skill_type
            FROM assessments a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = %s
            ORDER BY a.date
        """, (student_id,))
        assessments = cur.fetchall()
        cur.close()
        
        performance_data = []
        for assessment in assessments:
            performance_data.append({
                'id': assessment[0],
                'subject_id': assessment[2],
                'subject_name': assessment[9],
                'term': assessment[3],
                'type': assessment[4],
                'score': float(assessment[5]),
                'max_score': float(assessment[6]),
                'percentage': round((float(assessment[5]) / float(assessment[6])) * 100, 2),
                'date': assessment[7].strftime('%Y-%m-%d'),
                'skill_type': assessment[10]
            })
        
        return jsonify(performance_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get analytics data
@app.route('/api/analytics/<int:student_id>', methods=['GET'])
def get_analytics(student_id):
    try:
        cur = mysql.connection.cursor()
        
        # Get overall performance by term
        cur.execute("""
            SELECT term_number, AVG((score/max_score)*100) as avg_percentage
            FROM assessments
            WHERE student_id = %s
            GROUP BY term_number
        """, (student_id,))
        term_performance = cur.fetchall()
        
        # Get performance by subject
        cur.execute("""
            SELECT s.name, AVG((a.score/a.max_score)*100) as avg_percentage
            FROM assessments a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = %s
            GROUP BY s.name
        """, (student_id,))
        subject_performance = cur.fetchall()
        
        # Get performance by assessment type
        cur.execute("""
            SELECT assessment_type, AVG((score/max_score)*100) as avg_percentage
            FROM assessments
            WHERE student_id = %s
            GROUP BY assessment_type
        """, (student_id,))
        assessment_performance = cur.fetchall()
        
        # Get skills performance
        cur.execute("""
            SELECT s.skill_type, AVG((a.score/a.max_score)*100) as avg_percentage
            FROM assessments a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = %s AND s.skill_type IS NOT NULL
            GROUP BY s.skill_type
        """, (student_id,))
        skills_performance = cur.fetchall()
        
        cur.close()
        
        analytics = {
            'term_performance': [{'term': t[0], 'percentage': round(float(t[1]), 2)} for t in term_performance],
            'subject_performance': [{'subject': s[0], 'percentage': round(float(s[1]), 2)} for s in subject_performance],
            'assessment_performance': [{'type': a[0], 'percentage': round(float(a[1]), 2)} for a in assessment_performance],
            'skills_performance': [{'skill': sk[0], 'percentage': round(float(sk[1]), 2)} for sk in skills_performance]
        }
        
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
