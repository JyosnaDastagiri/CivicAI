
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

## 🧠 AI Components

### 1. AI Issue Analysis

The system analyzes the submitted image and description to identify the possible civic issue, severity, and safety risk.

Example categories include:

- Pothole
- Road Damage
- Garbage Accumulation
- Broken Streetlight
- Water Leakage
- Drainage Issue
- Fallen Tree

### 2. Generative AI Complaint Generation

The citizen's description is converted into a structured and professional complaint.

The generated complaint can be reviewed and edited before submission.

CivicAI supports two AI modes:

**Demo AI Mode**
- Works offline
- Requires no API key
- Uses deterministic rule-based analysis

**Live AI Mode**
- Uses Google Gemini
- Requires a Gemini API key
- Automatically falls back to Demo AI if the API request fails

### 3. Duplicate Detection

Potential duplicate complaints are identified using:

```text
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
