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
- [Demo Credentials](#-demo-credentials)
- [Project Status](#-project-status)
- [Limitations](#️-limitations)
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
```

---

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

CivicAI provides two AI modes.

#### Demo AI Mode

- Works offline
- Requires no API key
- Uses deterministic rule-based analysis
- Useful for local development and demonstration

#### Live AI Mode

- Uses Google Gemini
- Supports AI-assisted analysis of the submitted issue
- Requires a Gemini API key
- Automatically falls back to Demo AI if the API request fails

---

### 2. Generative AI Complaint Generation

The citizen's description is converted into a structured and professional complaint.

The generated complaint can be reviewed and edited by the citizen before submission.

The generated complaint can include:

- Issue category
- Issue description
- Severity
- Safety concern
- Location
- Recommended action

This reduces the need for citizens to manually prepare formal complaint text.

---

### 3. Duplicate Detection

Potential duplicate complaints are identified using text similarity, geographic proximity, and issue category.

The basic process is:

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
        ├──────────────┐
        ▼              ▼
 GPS Distance    Issue Category
        │              │
        └───────┬──────┘
                ▼
       Duplicate Validation
```

#### TF-IDF

TF-IDF converts complaint descriptions into numerical vectors based on the importance of words within the complaint collection.

#### Cosine Similarity

Cosine Similarity measures how similar two complaint descriptions are.

A higher similarity indicates that two complaints may describe the same issue.

#### GPS Validation

Geographic distance is considered along with text similarity.

This helps distinguish between:

- Two similar complaints about the same location
- Two similar complaints occurring at different locations

#### Category Validation

The detected issue category is also considered before treating two complaints as potential duplicates.

---

### 4. Context-Aware Priority Scoring

CivicAI uses a transparent weighted scoring approach instead of a black-box priority prediction model.

The priority score considers factors such as:

- Severity
- Safety risk
- Location importance
- Recurrence
- Related reports
- Issue category urgency

Example:

```text
Severity
   +
Safety Risk
   +
Location Importance
   +
Recurrence
   +
Related Reports
   +
Category Urgency
   │
   ▼
Weighted Priority Score
   │
   ▼
Low / Medium / High / Critical
```

The weighted approach makes the priority decision easier to understand and explain.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      CITIZEN         │
                    │  Web Application     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React + TypeScript │
                    │   Vite + Tailwind    │
                    └──────────┬───────────┘
                               │
                         REST API / JWT
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ AI Service  │   │ Duplicate   │   │  Priority   │
      │ Gemini /    │   │ Detection   │   │  Scoring    │
      │ Demo Mode   │   │ TF-IDF +    │   │  Weighted   │
      └─────────────┘   │ Cosine + GPS│   └─────────────┘
                        └─────────────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Department Routing │
                    │   & Officer Assign.  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Authority Workflow   │
                    │ Acknowledgement      │
                    │ Deadlines            │
                    │ Escalation           │
                    │ Resolution           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ SQLite / PostgreSQL  │
                    │ Audit Logs           │
                    │ Notifications        │
                    └──────────────────────┘
```

---

## 👥 User Roles

CivicAI implements role-based access control.

### 👤 Citizen

Citizens can:

- Register and login
- Submit civic complaints
- Upload issue images
- Provide descriptions
- Provide location
- Review AI-generated complaints
- View duplicate warnings
- Track priority
- Track complaint status
- View acknowledgement
- Receive notifications
- Track resolution

### 👨‍💼 Officer

Officers can:

- View assigned complaints
- Review complaint details
- Acknowledge complaints
- Update complaint status
- Add resolution information
- Upload resolution evidence
- Complete assigned work

### 👨‍💼 Department Head

Department Heads can:

- Monitor department complaints
- View escalated complaints
- Handle acknowledgement deadline escalations
- Handle resolution deadline escalations
- Monitor department performance
- Review analytics

### 🛡️ Administrator

Administrators can:

- Manage users
- Manage departments
- Monitor complaints
- Configure system settings
- View analytics
- View audit logs
- Monitor escalations
- Manage priority and deadline configurations

---

## 📂 Project Structure

```text
CivicAI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── tests/
│   ├── seed.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── ...
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Prerequisites

Install the following before running the project:

- Python 3.13
- Node.js
- npm
- Git
- VS Code

---

### 1. Clone the Repository

```powershell
git clone https://github.com/JyosnaDastagiri/CivicAI.git
cd CivicAI
```

---

### 2. Backend Setup

Open a terminal in the project directory.

```powershell
cd backend
```

Create a Python virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create the environment file:

```powershell
Copy-Item .env.example .env
```

The application can run in Demo AI Mode without a Gemini API key.

For Live AI Mode, configure the Gemini API key in `.env`.

Example:

```env
AI_MODE=demo
GEMINI_API_KEY=
```

For Gemini-based AI analysis:

```env
AI_MODE=live
GEMINI_API_KEY=your_api_key_here
```

Do not commit `.env` or API keys to GitHub.

---

### 4. Seed the Database

Run:

```powershell
python seed.py
```

The seed script creates demo data including:

- Users
- Departments
- Officers
- Department Heads
- Sample complaints
- Roles
- Initial system data

---

### 5. Start the Backend

Run:

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend will run at:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

### 6. Frontend Setup

Open a second terminal.

Navigate to the frontend:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## 🚀 Usage

### Step 1 – Citizen Login

Login using the demo citizen account.

### Step 2 – Create Complaint

The citizen provides:

- Issue image
- Issue description
- Location

### Step 3 – AI Analysis

The system analyzes the complaint and identifies:

- Issue category
- Severity
- Safety risk

### Step 4 – Complaint Generation

Generative AI creates a structured complaint.

The citizen can review and edit the generated complaint.

### Step 5 – Duplicate Detection

The system compares the complaint with existing reports using:

- TF-IDF
- Cosine Similarity
- GPS distance
- Issue category

### Step 6 – Priority Calculation

A weighted priority score is calculated using contextual factors.

### Step 7 – Department Assignment

The complaint is automatically routed to the appropriate department and officer.

### Step 8 – Acknowledgement

The assigned officer must acknowledge the complaint.

The citizen can see the acknowledgement status.

### Step 9 – Resolution

The officer works on the complaint and updates its status.

Resolution evidence can also be added.

### Step 10 – Escalation

If the complaint is not acknowledged or resolved within the configured deadline, the system automatically escalates it to the next authority level.

### Step 11 – Citizen Notification

The citizen receives status updates and can track the complete complaint timeline.

---

## 🔔 Acknowledgement Mechanism

CivicAI provides an explicit acknowledgement mechanism between the citizen and authority.

After a complaint is assigned:

```text
Complaint Created
       │
       ▼
Department Assigned
       │
       ▼
Officer Assigned
       │
       ▼
Acknowledgement Deadline
       │
       ├── Officer Acknowledges
       │          │
       │          ▼
       │     Work in Progress
       │
       └── Deadline Missed
                  │
                  ▼
          Automatic Escalation
                  │
                  ▼
           Department Head
```

The system records:

- Assigned officer
- Assignment time
- Acknowledgement deadline
- Acknowledgement time
- Officer who acknowledged
- Resolution deadline

This allows the citizen to verify that the complaint has actually been received by the responsible authority.

---

## ⏱️ Automatic Escalation

CivicAI monitors complaint deadlines using a background scheduler.

### Acknowledgement Escalation

If an officer does not acknowledge a complaint within the configured acknowledgement deadline:

```text
Officer
   │
   │ No acknowledgement
   ▼
Deadline Exceeded
   │
   ▼
Automatic Escalation
   │
   ▼
Department Head
```

### Resolution Escalation

If a complaint is acknowledged but not resolved within the configured resolution deadline:

```text
Officer
   │
   │ Resolution deadline exceeded
   ▼
Automatic Escalation
   │
   ▼
Higher Authority
```

The escalation is recorded in the audit trail and notifications are generated for the relevant users.

---

## 🗺️ Location and Maps

CivicAI uses location information for:

- Complaint mapping
- Geographic duplicate validation
- Distance calculation
- Issue visualization
- Authority monitoring

The frontend uses:

- Leaflet
- OpenStreetMap

Geographic distance is calculated using the Haversine approach.

The location information is stored with the complaint so that authorities can understand where the civic issue occurred.

---

## 🧾 Audit Trail

Important complaint actions are recorded in the system.

Examples include:

- Complaint creation
- AI analysis
- Complaint generation
- Duplicate analysis
- Priority calculation
- Department assignment
- Officer assignment
- Acknowledgement
- Status changes
- Escalation
- Resolution
- Notifications

This provides a traceable history of the complaint lifecycle.

---

## 🧪 Testing

The backend includes automated tests covering important system functionality.

Run the tests using:

```powershell
pytest
```

The project was designed with automated testing for:

- Authentication
- Complaint creation
- AI analysis
- Duplicate detection
- Priority scoring
- Department routing
- Acknowledgement workflow
- Escalation
- Resolution workflow
- API behavior

The current project test suite contains **18 tests**.

---

## 🔑 Demo Credentials

### Citizen

```text
Email: citizen@civicai.demo
Password: Demo@123
```

Other demo users are created through the database seed script.

The seeded environment includes users representing:

- Citizens
- Officers
- Department Heads
- Administrators

---

## 📊 Project Status

### Implemented

- ✅ Citizen registration and login
- ✅ JWT authentication
- ✅ Role-Based Access Control
- ✅ Civic issue reporting
- ✅ Image and description submission
- ✅ AI-assisted issue analysis
- ✅ Demo AI Mode
- ✅ Gemini Live AI Mode
- ✅ AI complaint generation
- ✅ Complaint review and editing
- ✅ TF-IDF duplicate detection
- ✅ Cosine Similarity
- ✅ GPS-based duplicate validation
- ✅ Context-aware priority scoring
- ✅ Automatic department assignment
- ✅ Officer assignment
- ✅ Complaint acknowledgement
- ✅ Deadline monitoring
- ✅ Automatic escalation
- ✅ Resolution tracking
- ✅ Resolution evidence
- ✅ Citizen notifications
- ✅ Complaint timeline
- ✅ Audit trail
- ✅ Analytics dashboards
- ✅ Map-based visualization
- ✅ Configurable system settings
- ✅ Automated backend tests
- ✅ React frontend
- ✅ FastAPI backend
- ✅ SQLite local/demo database
- ✅ PostgreSQL support

---

## ⚠️ Limitations

- The Demo AI mode uses deterministic rule-based analysis and is intended for offline development and demonstration.
- Live AI analysis requires a Gemini API key.
- The project does not directly connect to real municipal or government systems.
- Department and authority workflows are modeled internally using role-based accounts.
- Real-world government integration would require access to official APIs and authentication mechanisms.
- AI-generated results should be reviewed before being treated as authoritative.
- Location accuracy depends on the location information supplied through the application.
- The system is intended as an academic/prototype implementation rather than a production municipal deployment.

---

## 🔮 Future Scope

Possible future enhancements include:

- Integration with official municipal APIs
- Real-time government department integration
- More advanced geospatial analytics
- Larger civic issue datasets
- Improved computer vision models
- Multilingual complaint generation
- Voice-based complaint submission
- Mobile application
- SMS and email notifications
- Predictive civic issue analysis
- Heatmap-based civic issue monitoring
- Historical trend analysis
- Integration with smart-city infrastructure

---

## 🧠 Academic Positioning

CivicAI focuses on the **integration of multiple practical AI and software engineering techniques into one complete civic issue management workflow**.

The project combines:

```text
AI Issue Analysis
        +
Generative AI
        +
TF-IDF
        +
Cosine Similarity
        +
Geospatial Validation
        +
Weighted Priority Scoring
        +
Automatic Routing
        +
Acknowledgement Tracking
        +
Deadline Monitoring
        +
Escalation
        +
Resolution Management
```

The primary contribution is the implementation of a lightweight, practical, and traceable end-to-end civic complaint management system rather than the proposal of a new standalone machine-learning algorithm.

---



