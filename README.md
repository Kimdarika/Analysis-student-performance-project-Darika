# Student Performance Tracking System

A comprehensive Flask-based web application for tracking student performance across multiple terms, subjects, and assessment types.

## Features

- Track student performance across 2 terms (6 months)
- Multiple subjects per term (BCU, English for IT, General English, PL, Logic, Design, Web Design, Algorithm)
- Multiple assessment types (Quiz, Homework, Exam, Project)
- Visual analytics with interactive charts
- Hard skills and soft skills tracking
- Performance trends and improvement graphs

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### Setup Instructions

1. **Clone or extract the project files**

2. **Install Python dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Set up MySQL Database**

   - Start your MySQL server
   - Create the database and tables:
   \`\`\`bash
   mysql -u root -p < database/schema.sql
   \`\`\`
   
   - Insert sample data:
   \`\`\`bash
   mysql -u root -p < database/seed_data.sql
   \`\`\`

4. **Configure Database Connection**

   Edit `app.py` and update the MySQL configuration:
   \`\`\`python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'your_password'
   app.config['MYSQL_DB'] = 'student_performance'
   \`\`\`

5. **Run the Application**
\`\`\`bash
python app.py
\`\`\`

6. **Access the Application**

   Open your browser and go to: `http://localhost:5000`

## Usage

### Adding Students

Students can be added through the database or by extending the API with a student registration form.

### Recording Assessments

1. Select a student from the dropdown
2. Choose the term (Term 1 or Term 2)
3. Select the subject
4. Choose assessment type (Quiz, Homework, Exam, or Project)
5. Enter the score and maximum score
6. Add optional notes
7. Click "Add Assessment"

### Viewing Analytics

After selecting a student, you'll see:
- Performance by term (line chart)
- Performance by subject (bar chart)
- Performance by assessment type (doughnut chart)
- Hard skills vs soft skills (radar chart)
- Detailed performance table

## Project Structure

\`\`\`
student-performance-tracker/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── database/
│   ├── schema.sql         # Database schema
│   └── seed_data.sql      # Sample data
├── static/
│   ├── css/
│   │   └── style.css      # Styles
│   └── js/
│       └── dashboard.js   # Dashboard functionality
└── templates/
    ├── index.html         # Home page
    └── dashboard.html     # Dashboard page
\`\`\`

## API Endpoints

- `GET /api/students` - Get all students
- `POST /api/students` - Add new student
- `GET /api/subjects/<term>` - Get subjects for a term
- `POST /api/assessments` - Add assessment score
- `GET /api/performance/<student_id>` - Get student performance data
- `GET /api/analytics/<student_id>` - Get analytics data

## Customization

### Adding More Subjects

Edit `database/seed_data.sql` and add new subjects:
\`\`\`sql
INSERT INTO subjects (subject_code, name, term_number, skill_type) VALUES
('NEW101', 'New Subject', 1, 'hard_skill');
\`\`\`

### Modifying Assessment Types

Assessment types are defined in the database schema as an ENUM. To add more types, modify the schema.

### Changing Color Scheme

Edit `static/css/style.css` and modify the CSS variables in the `:root` selector.

## Troubleshooting

**Database Connection Error:**
- Verify MySQL is running
- Check username and password in `app.py`
- Ensure database exists

**Charts Not Displaying:**
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible

**No Data Showing:**
- Verify sample data was inserted
- Check API endpoints are returning data

## Future Enhancements

- User authentication system
- Export reports to PDF
- Email notifications
- Attendance tracking
- Parent portal
- Mobile app

## License

This project is open source and available for educational purposes.
