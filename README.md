# Student Performance Tracking System
![Dashboard](https://i.pinimg.com/736x/b2/b9/7f/b2b97fab420adedeb0f6c43592a6105a.jpg)
A comprehensive Flask-based web application for tracking student performance across multiple terms, subjects, and assessment types.

## Features

- Track student performance across 2 terms (6 months)
- Multiple subjects per term (BCU, English for IT, General English, PL, Logic, Design, Web Design, Algorithm)
- Multiple assessment types (Quiz, Homework, Exam, Project)
- Visual analytics with interactive charts
- Hard skills and soft skills tracking
- Performance trends and improvement graphs

## Technology Stack
![Dashboard](https://i.pinimg.com/1200x/f5/30/b3/f530b397fb4005953bcf373d845f8090.jpg)

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** js

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)


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

![Dashboard](https://i.pinimg.com/1200x/d8/fa/9f/d8fa9fa02d25d7c04a941b6f67792ffc.jpg)

<!-- \`\`\`
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
\`\`\` -->

### Modifying Assessment Types

Assessment types are defined in the database schema as an ENUM. To add more types, modify the schema.

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



## Project Description

![Dashboard](https://i.pinimg.com/736x/65/5b/81/655b81dc33c00f9fd29ce510700bdebf.jpg)

This project analyzes student performance data for two academic terms. It helps teachers and administrators understand students’ progress, identify weak areas, and make data-driven decisions. The analysis includes grades, attendance, and subject-specific performance.

---

## Features
- Input student data for Term 1 and Term 2  
- Visualize performance per subject  
- Compare overall performance across terms  
- Generate reports for individual students or entire classes  
- Identify trends and potential areas for improvement  

---

## Input Data / Dataset
The project requires structured input data for each student, which can be provided via CSV, form, or database.

![Dashboard](https://i.pinimg.com/736x/80/10/5a/80105a6c3ce0d5528d06aa3e85ac19ba.jpg)

### General Information
- `Student ID` – Unique identifier for each student  
- `Full Name` – Student’s full name  
- `Class` – Grade or class  
- `Attendance` – Percentage or number of days attended per term  

### Term 1 Subjects
- `BCU` – Business Computing & Utilization  
- `English for IT`  
- `General English`  
- `Logic`  
- `PL` – Programming Language  
- `Design`  

### Term 2 Subjects
- `English for IT`  
- `General English`  
- `Algorithm`  
- `PL` – Programming Language  
- `Web Design`  

## Website us of Analysis student performance

https://github.com/Kimdarika/Analysis-student-performance-project-Darika

## 👩‍🦰  *Project Owner & Developer*

Thanks goes to these wonderful people:

<a href="https://github.com/Kimdarika">
  <img src="https://avatars.githubusercontent.com/u/214124108?v=4" width="80" style="border-radius:50%"/>
</a>
