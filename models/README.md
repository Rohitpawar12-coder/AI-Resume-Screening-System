# AI Resume Screening and Job Matching System

## Overview

The AI Resume Screening and Job Matching System is a web application that helps recruiters and job seekers by automatically analyzing resumes and matching candidates with suitable job descriptions using Natural Language Processing (NLP) and Machine Learning.

---

## Features

- Upload resumes in PDF or DOCX format
- Extract candidate information
  - Name
  - Email
  - Phone Number
  - LinkedIn Profile
  - GitHub Profile
  - Skills
  - Education
  - Experience
- Match resumes with job descriptions
- Calculate resume-job match percentage
- Display matching results on a dashboard
- Simple and responsive web interface

---

## Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Libraries
- PyPDF2
- python-docx
- pandas
- scikit-learn
- nltk
- spacy
- regex

---

## Project Structure

```
AI_Resume_Screening_System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── parser/
├── matching/
├── utils/
├── database/
├── templates/
├── static/
├── jobs/
├── datasets/
└── tests/
```

---

## Installation

1. Clone the repository

```
git clone <repository-url>
```

2. Navigate to the project folder

```
cd AI_Resume_Screening_System
```

3. Create a virtual environment

```
python -m venv venv
```

4. Activate the virtual environment

Windows

```
venv\Scripts\activate
```

Linux/Mac

```
source venv/bin/activate
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Run the application

```
python app.py
```

---

## Workflow

1. User uploads a resume.
2. Resume text is extracted.
3. Candidate information is parsed.
4. Skills are identified.
5. Resume is compared with job descriptions.
6. Matching score is calculated.
7. Results are displayed.

---

## Future Enhancements

- AI chatbot for career guidance
- Resume ranking
- Interview scheduling
- Email notifications
- Multiple job recommendations
- Admin dashboard
- Resume feedback suggestions

---

## Author

Rohit Pawar

Computer Engineering Student

Data Science | AI | Machine Learning