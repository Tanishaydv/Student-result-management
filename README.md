# ResultHub — Student Result Management System

A beginner-friendly web application built with **HTML, CSS, Python, Flask, and SQLite**. It helps manage student details, record subject marks, and calculate academic results.

## Features

- Add, view, edit, and delete student records
- Search students by name or roll number
- Store records in a local SQLite database
- Automatically calculate total marks, percentage, grade, and pass/fail status
- Responsive dashboard with student statistics
- Subject-wise performance bars
- Print-friendly result report

## Tech stack

- **Frontend:** HTML5, CSS3, Jinja templates
- **Backend:** Python 3, Flask
- **Database:** SQLite (built into Python)

## Project structure

```text
student-result-management/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── student_form.html
│   └── result.html
└── static/
    └── style.css
```

The `students.db` database file is created automatically when you run the app. It is intentionally ignored by Git so your local data is not uploaded.

## Run locally

### 1. Install Python
Install Python 3.10 or newer and confirm it is available:

```bash
python --version
```

### 2. Open the project folder in a terminal

### 3. Create and activate a virtual environment (recommended)

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Result rules

- Maximum marks: 100 per subject; 500 total
- A student passes only if they score at least 33 in every subject
- Grades: A+ (90%+), A (80–89%), B (70–79%), C (60–69%), D (50–59%), E (33–49%), F (fail)

These are sample rules for this learning project and can be changed to match your institution.

## Upload to GitHub

1. Create a new repository on GitHub named `student-result-management`.
2. Keep the repository public if you want to showcase it in your portfolio.
3. Upload the project files and folders, or use Git from your terminal:

```bash
git init
git add .
git commit -m "Build student result management system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-result-management.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not upload passwords, private student data, or your local `students.db` file.

## Future improvements

- Add login and role-based access for teachers/admins
- Export reports to CSV or PDF
- Add charts for class performance
- Add pagination for large student lists
- Add automated tests

## Learning note

This project is intended for practice and demonstration. It is not production-ready and does not include authentication or authorization. Do not enter real or sensitive student records.
