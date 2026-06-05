---
title: Smart Resume Screening
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Smart Resume Screening and Job Matching System

A FastAPI-based application that performs resume screening, ATS scoring, semantic matching, and job recommendations.
# Smart Resume Screening & Job Matching System

## Overview

The Smart Resume Screening & Job Matching System is an AI-powered recruitment platform developed to automate resume analysis, candidate screening, and job recommendation. The system uses Natural Language Processing (NLP), Machine Learning techniques, and Applicant Tracking System (ATS) concepts to evaluate resumes against job descriptions and recommend suitable job roles.

The platform supports both Job Seekers and HR Recruiters through dedicated dashboards, enabling efficient resume screening, candidate ranking, and recruitment management.

---

## Problem Statement

Recruiters often spend significant time manually reviewing resumes to identify suitable candidates. Traditional screening processes can be time-consuming, inconsistent, and prone to human error.

This project addresses these challenges by automating resume parsing, skill extraction, ATS scoring, semantic matching, and job recommendations using AI and NLP techniques.

---

## Objectives

* Automate resume screening and evaluation.
* Extract candidate skills using NLP techniques.
* Match resumes with job descriptions.
* Calculate ATS compatibility scores.
* Recommend suitable job roles.
* Rank candidates based on relevance scores.
* Provide HR recruiters with bulk resume screening capabilities.
* Store screening history and generate reports.

---

## Features

### Candidate Features

* User Registration & Login
* Resume Upload (PDF and DOCX)
* Resume Parsing
* AI-Based Skill Extraction
* ATS Score Calculation
* Semantic Match Analysis
* Missing Skill Identification
* Improvement Suggestions
* Job Recommendations
* Screening History
* Profile Management
* Report Generation & Export

### HR Features

* HR Registration & Login
* Bulk Resume Screening
* Candidate Ranking
* Candidate Management Dashboard
* Screening History
* Recruitment Analytics
* Profile Management

### AI Features

* NLP-Based Skill Extraction
* Gemini LLM Skill Analysis
* ATS Resume Evaluation
* Semantic Similarity Matching
* Automated Job Recommendation Engine

---

## Technology Stack

### Backend

* FastAPI
* Python

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite
* SQLAlchemy ORM

### Natural Language Processing

* spaCy
* Sentence Transformers
* Scikit-Learn

### Resume Processing

* PyMuPDF
* pdfplumber
* python-docx
* pytesseract
* Pillow

### AI Integration

* Google Gemini API

### Reporting

* ReportLab
* OpenPyXL

---

## System Architecture

```text
User / HR
     │
     ▼
Frontend Interface
(HTML, CSS, JavaScript)
     │
     ▼
FastAPI Backend
     │
     ├── Authentication Module
     ├── Resume Parser
     ├── Skill Extraction Engine
     ├── ATS Scoring Engine
     ├── Semantic Matching Engine
     ├── Job Recommendation Engine
     ├── Report Generation Module
     │
     ▼
SQLite Database
```

---

## Project Structure

```text
app/
│
├── static/
│   ├── consumer/
│   ├── hr/
│   ├── profile_photos/
│   ├── home.html
│   ├── login.html
│   └── signup.html
│
├── uploads/
│
├── __init__.py
├── ats_engine.py
├── auth.py
├── database.py
├── extraction.py
├── llm_skills.py
├── main.py
├── models.py
├── skills.py
│
├── job_descriptions.csv
├── resume_screening.db
└── requirements.txt
```

---

## Workflow

### Candidate Workflow

1. Register/Login
2. Upload Resume
3. Enter Job Title
4. Enter Job Description
5. Resume Text Extraction
6. Skill Extraction
7. ATS Score Calculation
8. Semantic Matching
9. Job Recommendations
10. Results Stored in Database

### HR Workflow

1. Login
2. Upload Multiple Resumes
3. Enter Job Description
4. Bulk Screening Process
5. Candidate Ranking
6. Dashboard Analytics
7. Candidate Management

---

## ATS Evaluation Parameters

The ATS Engine evaluates resumes using:

* Skill Match Percentage
* Semantic Similarity Score
* Required Skills Coverage
* Missing Skills Analysis
* Resume Relevance Score

The final ATS score is generated based on the compatibility between the resume and the job description.

---

## Database Tables

### User Table

Stores:

* User ID
* Username
* Email
* Password
* User Role (Candidate / HR)
* Profile Information

### ResumeHistory Table

Stores:

* Resume Information
* ATS Score
* Semantic Match Score
* Recommendations
* Generated Reports

### Candidate Table

Stores:

* Candidate Information
* Resume Scores
* HR Reference
* Recommendation Status

---

## API Endpoints

### Authentication

```http
POST /api/signup
POST /api/login
```

### Resume Screening

```http
POST /api/screen-resume
POST /api/bulk-screen
```

### Candidate Dashboard

```http
GET /api/user-dashboard/{user_id}
GET /api/history/{user_id}
```

### HR Dashboard

```http
GET /api/hr-dashboard/{user_id}
GET /api/hr-history/{user_id}
GET /api/candidates/{hr_id}
```

### Reports

```http
GET /api/report/{history_id}
GET /api/export-report/{report_id}
```

---

## Installation Guide

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Smart-Resume-Screening-System
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### Step 4: Configure Gemini API Key

Create an environment variable:

```bash
GEMINI_API_KEY=your_api_key
```

### Step 5: Run Application

```bash
uvicorn app.main:app --reload
```

### Step 6: Open Browser

```text
http://localhost:8000
```

---

## Expected Outputs

* ATS Score
* Skill Match Score
* Semantic Match Score
* Matched Skills
* Missing Skills
* Improvement Suggestions
* Recommended Job Roles
* Ranked Candidate List

---

## Future Enhancements

* JWT Authentication
* Email Notifications
* Interview Recommendation System
* Advanced Recruitment Analytics
* Cloud Storage Integration
* Resume Improvement Generator
* Multi-language Resume Support
* Real-time Job Portal Integration

---

## Conclusion

The Smart Resume Screening & Job Matching System successfully automates the recruitment process by combining Artificial Intelligence, Natural Language Processing, and ATS methodologies. The platform improves hiring efficiency by reducing manual effort, enhancing candidate evaluation accuracy, and providing intelligent job recommendations for job seekers and recruiters.

---

## Developed Using

* Python
* FastAPI
* Natural Language Processing (NLP)
* Machine Learning
* SQLite Database
* HTML, CSS, JavaScript
* Google Gemini AI

## Author

Name: Navya Sree

Degree: M.Sc. Data Science (Minor in Big Data Analytics)

Project: Smart Resume Screening & Job Matching System

## Deployment

Platform: Render

Application URL:
https://your-app-name.onrender.com
