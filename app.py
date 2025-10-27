import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# REQUIRED: Set a secret key for session management
app.secret_key = 'safer_key_for_no_keyerror' 

# --- Dummy Data (Simulates Database) ---
# Credentials for testing: student@school.edu / password123
DUMMY_USERS = {"student@school.edu": "password123"} 
STUDENT_DATA = {
    "name": "Alex Johnson",
    "overall_gpa": 3.75,
    # Mock data for the summary cards
    "total_students": 120,
    "average_score": 82.5,
    "top_performer": "Sokha",
    "pass_rate": 91.6,
    # Detailed course data for the table and charts
    "courses": [
        {"name": "Calculus I", "grade": "A", "score": 92},
        {"name": "Computer Science", "grade": "A-", "score": 89},
        {"name": "English Literature", "grade": "B+", "score": 87},
        {"name": "Physics", "grade": "C+", "score": 75},
        {"name": "Chemistry", "grade": "B-", "score": 79},
        {"name": "Web Design", "grade": "A+", "score": 95},
    ]
}

# --- Utility Function for Placeholder Routes ---
def placeholder_page(title):
    """Helper to return simple HTML for unbuilt pages, inheriting the base template."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('content.html', title=title) # Renders a simple content page
    
# --- Authentication Routes ---

@app.route('/index')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in DUMMY_USERS and DUMMY_USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
            
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in DUMMY_USERS:
            error = 'User already exists!'
            return render_template('register.html', error=error)
        
        DUMMY_USERS[username] = password
        return redirect(url_for('login'))
        
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.clear() # Clears all session data
    return redirect(url_for('login'))

# --- Application Routes ---

@app.route('/dashboard') 
def dashboard():
    # Authentication Guard
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # 1. Prepare data for JavaScript charts
    course_labels = [course["name"] for course in STUDENT_DATA["courses"]]
    course_scores = [course["score"] for course in STUDENT_DATA["courses"]]
    
    # 2. Serialize data to JSON strings for safe transmission to the HTML template
    course_labels_json = json.dumps(course_labels)
    course_scores_json = json.dumps(course_scores)
    
    # 3. Pass all data to the template
    return render_template(
        'dashboard.html', 
        student=STUDENT_DATA,
        current_page='dashboard', # Passed for setting active navbar link
        course_labels_json=course_labels_json,
        course_scores_json=course_scores_json
    )

@app.route('/student-profile')
def student_profile(): 
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Pass the specific student data to the profile template
    return render_template('student-profile.html', student=STUDENT_DATA, current_page='student_profile')


# Placeholder routes using the utility function and passing the page title
@app.route('/subject-analysis')
def subject_analysis(): 
    return render_template("subject-analysis.html")
    # return placeholder_page("Subject Analysis")

@app.route('/comparison')
def comparison(): 
    return render_template("comparison.html")

@app.route('/prediction')
def prediction():
    return render_template("prediction.html")

@app.route('/reports')
def reports(): 
    return render_template("reports.html")

@app.route('/teacher-insights')
def teacher_insights(): 
    return render_template("teacher-insights.html")

@app.route('/trends')
def trends(): 
    return render_template("trends.html")


# 


# --- Application Entry Point ---
if __name__ == '__main__':
    app.run(debug=True)

