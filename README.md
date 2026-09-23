
# 🏙️ CivicAI – AI-Based Civic Issue Detection, Prioritization and Resolution System

CivicAI is an AI-powered civic issue management platform that allows citizens to report problems such as potholes, damaged roads, garbage accumulation, broken streetlights, water leakage, and other civic issues.

The system combines **AI-assisted issue analysis, Generative AI, duplicate detection, priority scoring, automatic department assignment, acknowledgement tracking, deadline monitoring, escalation, and resolution management** into a single end-to-end workflow.

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Project Workflow](#-project-workflow)
- [AI Components](#-ai-components)
- [System Architecture](#-system-architecture)
- [User Roles](#-user-roles)
- [Project Structure](#-project-structure)
- [Installation](#️-installation)
- [Usage](#-usage)
- [Testing](#-testing)
- [Limitations](#-limitations)
- [Future Scope](#-future-scope)

---

## 📖 About the Project

Civic issue reporting is often manual, unstructured, and difficult to track. Citizens may not know whether their complaint has been received, complaints can be duplicated, and urgent issues may not receive appropriate priority.

CivicAI addresses these problems through an integrated digital workflow.

Citizens can submit an issue with:

- 📷 Image
- 📝 Description
- 📍 Location

The system then analyzes the issue, generates a structured complaint, checks for duplicate reports, calculates priority, assigns the complaint to the appropriate department and officer, and tracks it until resolution.

The system also provides **authority acknowledgement and automatic escalation** when deadlines are missed.

---

## ✨ Features

### 👤 Citizen

- Report civic issues with image, description, and location
- AI-assisted issue and severity analysis
- AI-generated professional complaint
- Review and edit generated complaint
- Duplicate complaint detection
- Transparent priority score
- Complaint status and timeline tracking
- Authority acknowledgement visibility
- In-app notifications

### 🤖 AI & NLP

- AI-based civic issue analysis
- Generative AI complaint creation
- TF-IDF text vectorization
- Cosine Similarity for duplicate detection
- GPS-based geographic validation
- Context-aware weighted priority scoring

### 🏢 Authority Workflow

- Automatic department assignment
- Officer assignment
- Mandatory complaint acknowledgement
- Deadline tracking
- Automatic escalation
- Resolution tracking
- Resolution evidence
- Citizen notification

### 🔐 Administration

- JWT authentication
- Role-Based Access Control
- User and department management
- Complaint monitoring
- Analytics dashboards
- Audit logs
- Configurable priority and deadline settings

---

## 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Leaflet
- OpenStreetMap
- Recharts

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Role-Based Access Control

### Database

- SQLite for local/demo execution
- PostgreSQL supported

### AI / Machine Learning

- Gemini AI
- Demo AI Mode
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Haversine Distance
- Weighted Priority Scoring

### Other

- APScheduler
- REST APIs
- Local / Supabase object storage

---

## 🔄 Project Workflow

```text
Citizen
   │
   ▼
Image + Description + Location
   │
   ▼
AI Issue Detection
   │
   ▼
Severity & Safety Analysis
   │
   ▼
AI Complaint Generation
   │
   ▼
Citizen Review / Edit
   │
   ▼
Duplicate Detection
(TF-IDF + Cosine Similarity + GPS)
   │
   ▼
Priority Scoring
   │
   ▼
Department & Officer Assignment
   │
   ▼
Officer Acknowledgement
   │
   ├── Acknowledged
   │       │
   │       ▼
   │   Work in Progress
   │       │
   │       ▼
   │     Resolved
   │       │
   │       ▼
   │   Citizen Notification
   │
   └── Deadline Missed
           │
           ▼
      Automatic Escalation
           │
           ▼
     Department Head

##🧠 AI Components
1. AI Issue Analysis

The system analyzes the submitted image and description to identify the possible civic issue, severity, and safety risk.

Example categories include:

Pothole
Road Damage
Garbage Accumulation
Broken Streetlight
Water Leakage
Drainage Issue
Fallen Tree
2. Generative AI Complaint Generation

The citizen's description is converted into a structured and professional complaint.

The generated complaint can be reviewed and edited before submission.

CivicAI supports two AI modes:

Demo AI Mode

Works offline
Requires no API key
Uses deterministic rule-based analysis

Live AI Mode

Uses Google Gemini
Requires a Gemini API key
Automatically falls back to Demo AI if the API request fails
3. Duplicate Detection

Potential duplicate complaints are identified using:

Complaint Description
        │
        ▼
   TF-IDF
        │
        ▼
Cosine Similarity
        │
        ▼
Text Similarity
        │
        +
GPS Distance
        │
        +
Issue Category
        │
        ▼
Duplicate Validation
4. Priority Scoring

CivicAI uses a transparent weighted scoring approach rather than a black-box priority prediction model.

The priority score considers factors such as:

Issue severity
Safety risk
Location importance
Recurrence
Related reports
Category urgency

The final score is converted into:

LOW
MEDIUM
HIGH
CRITICAL

No XGBoost, SHAP, or local GPU training is used.

The lightweight design keeps the project practical and reproducible on a normal student laptop.

🏗️ System Architecture
             ┌─────────────────────┐
             │       Citizen       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │   React Frontend    │
             │ TypeScript + Vite   │
             │    + Tailwind       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │   FastAPI Backend   │
             │   Modular Monolith  │
             └──────────┬──────────┘
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
   AI Services      NLP Services    Priority Engine
       │                │                │
       │          TF-IDF + Cosine       │
       │          + GPS Distance        │
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │    SQLite /         │
             │    PostgreSQL       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Authority Workflow  │
             │ Assignment          │
             │ Acknowledgement     │
             │ Resolution          │
             │ Escalation          │
             └─────────────────────┘

The project uses a modular monolithic architecture with a single frontend and backend, keeping deployment simple for a student project.

## 👥 User Roles
Citizen
Submit complaints
Upload images
Provide location
Review AI-generated complaints
Track status and timeline
View acknowledgement and resolution
Officer
View assigned complaints
Acknowledge complaints
Update complaint status
Work on assigned issues
Submit resolution details
Department Head
Monitor department complaints
Handle escalated complaints
Reassign complaints
Monitor department activity
Admin
Manage users and departments
Configure system settings
Monitor complaints
View analytics
Review audit logs
## 📂 Project Structure
CivicAI/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── workers/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── seed.py
│   ├── requirements.txt
│   └── .env.example
│
├── tests/
├── uploads/
├── docker-compose.yml
├── .gitignore
└── README.md
⚙️ Installation
Prerequisites
Python 3.11+
Node.js 18+
PostgreSQL — optional
Docker Desktop — optional
Backend
cd civicai\backend

python -m venv venv

.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env

python seed.py

uvicorn app.main:app --reload --port 8000

Backend:

http://localhost:8000

Swagger API Documentation:

http://localhost:8000/docs
Frontend

Open a second terminal:

cd civicai\frontend

npm install

Copy-Item .env.example .env

npm run dev

Frontend:

http://localhost:5173

SQLite is used by default, so the project can be run locally without setting up PostgreSQL.

##🚀 Usage
1. Login as Citizen

Use a citizen account to access the complaint dashboard.

2. Submit an Issue

Upload an image, enter a description, and provide the issue location.

3. AI Analysis

The system analyzes the issue and determines its category, severity, and safety risk.

4. Review Complaint

A professional complaint is generated and can be reviewed or edited.

5. Duplicate & Priority Analysis

The system checks for possible duplicate complaints and calculates a transparent priority score.

6. Department Assignment

The complaint is automatically assigned to the appropriate department and officer.

7. Acknowledgement

The officer acknowledges receipt of the complaint.

The citizen can see:

✓ Received & Acknowledged by Officer
Date & Time
8. Resolution

The officer updates the complaint and submits the resolution.

9. Escalation

If acknowledgement or resolution deadlines are missed, the complaint is automatically escalated.

## 🧪 Testing

The project includes automated backend tests covering:

Authentication
Protected routes
AI Demo Mode
Complaint creation
Duplicate detection
TF-IDF
Cosine Similarity
Geographic distance
Priority scoring
Department assignment
Role-based authorization

Run the tests with:

cd civicai

pytest -v

## 🔑 Demo Credentials

All seeded demo accounts use:

Password: Demo@123
Role	Email
Citizen	citizen@civicai.demo
Officer	roads.officer@civicai.demo
Department Head	roads.head@civicai.demo
Admin	admin@civicai.demo

## 📊 Project Status

Working Full-Stack Prototype

CivicAI currently supports:

Citizen complaint reporting
AI-assisted issue analysis
AI complaint generation
Duplicate detection
Priority scoring
Department assignment
Officer acknowledgement
Deadline monitoring
Automatic escalation
Resolution tracking
Notifications
Analytics dashboards
Audit logging

## ⚠️ Limitations
The current prototype does not connect directly to real municipal government systems or APIs.
Authority accounts are simulated internally using role-based accounts.
AI capabilities use pre-trained/cloud services rather than a custom-trained model.
Duplicate detection uses TF-IDF, Cosine Similarity, and GPS-based validation.
Notifications are currently in-app; SMS and email are future enhancements.

## 🔮 Future Scope
Integration with official municipal APIs
SMS and email notifications
Advanced computer vision models
Multilingual complaint support
Mobile application
Advanced geospatial analytics and heatmaps
Automated resolution verification
Predictive workload analysis
IoT integration for smart-city systems

