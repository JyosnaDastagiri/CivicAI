# CivicAI – AI-Based Civic Issue Detection, Prioritization and Resolution System

A complete, working, full-stack final-year project: an AI-assisted civic complaint
management platform where citizens report issues (potholes, garbage, broken
streetlights, water leakage, drainage, fallen trees, etc.), AI analyzes and drafts
the complaint, lightweight algorithms detect duplicates and calculate priority,
the system routes it to the right department, and a background scheduler
enforces authority accountability through acknowledgement deadlines and
automatic escalation.

---

## 1. Problem Statement

Civic issue reporting today is manual, unstructured, and unaccountable: citizens
don't know if their complaint was ever actually seen, complaints are duplicated,
and there is no transparent way to prioritize what needs urgent attention.

## 2. Objectives

- Let citizens report issues with an image, description, and location.
- Use AI to understand the issue and draft a professional complaint.
- Detect duplicate reports of the same issue nearby.
- Calculate a transparent, explainable priority score.
- Automatically route the complaint to the right department and officer.
- **Prove** the responsible authority actually received it (acknowledgement).
- Automatically escalate to a higher authority if deadlines are missed.
- Give citizens full visibility through a timeline and notifications.

## 3. Features

- Role-based portals for Citizen, Officer, Department Head, and Admin.
- 9-step guided complaint submission wizard (image → description → location →
  AI analysis → generated complaint → review/edit → submit).
- AI Demo Mode: works fully offline with **zero API keys**, with a clearly
  labeled "Demo AI Mode" indicator in the UI.
- TF-IDF + Cosine Similarity + GPS duplicate detection.
- Transparent weighted priority scoring (no black-box ML).
- Rule-based department routing and least-loaded officer assignment.
- Mandatory officer acknowledgement workflow with deadline tracking.
- Automatic background escalation scheduler (APScheduler).
- Full audit trail and citizen-facing timeline.
- In-app notifications (no SMS/email dependency required).
- Admin-configurable deadlines, thresholds, and priority weights.
- Recharts-based analytics dashboards; Leaflet + OpenStreetMap maps.
- 18 automated backend tests covering auth, AI, duplicates, priority,
  assignment, and authorization boundaries.

## 4. Architecture

```
React Frontend (Vite + TS + Tailwind)
        |
        v
FastAPI Backend (modular monolith)
        |
        +-- PostgreSQL / SQLite
        +-- Object Storage (local dir or Supabase Storage)
        +-- AI Vision / Gemini (or Demo AI Service)
        +-- In-app Notification System
        +-- APScheduler Escalation Job (runs every N minutes)
```

No microservices, no Kafka, no Kubernetes — a single deployable backend and a
single deployable frontend, as appropriate for a lightweight student project.

## 5. Complete Workflow

```
Citizen submits image + description + location
   -> AI-based issue detection (category, severity, safety risk)
   -> Generative AI drafts a professional complaint
   -> Citizen reviews/edits
   -> Duplicate check (TF-IDF + cosine similarity + Haversine GPS distance)
   -> Priority scoring (weighted, transparent, 0-100 -> LOW/MEDIUM/HIGH/CRITICAL)
   -> Department assignment (rule-based) + officer selection
   -> Officer notified, acknowledgement deadline starts
   -> Officer acknowledges?
        YES -> "Received & Acknowledged" + resolution deadline starts
        NO (deadline exceeded) -> automatic escalation to Department Head
   -> Officer marks IN_PROGRESS -> submits resolution evidence -> RESOLVED
        (if resolution deadline exceeded -> automatic escalation again)
   -> Citizen sees full timeline and can close the complaint
```

## 6. AI Components

`AIService` is an abstraction (`backend/app/services/ai_service.py`) with two
implementations:

- **DemoAIService** — deterministic, keyword-based, fully offline. Used when
  `AI_MODE=demo` or when no `GEMINI_API_KEY` is set. The app **never crashes**
  due to a missing AI key.
- **GeminiAIService** — calls Google Gemini's `generateContent` endpoint when
  `AI_MODE=live` and a key is configured. Falls back to Demo automatically on
  any API failure.

Both implement `analyze_image()` and `generate_complaint()`, so the provider
can be swapped without touching any other code.

## 7. Algorithms (documented, no black-box ML)

| Algorithm | Where | Purpose |
|---|---|---|
| TF-IDF vectorization | `duplicate_service.py` | Represent complaint text numerically |
| Cosine similarity | `duplicate_service.py` | Compare two complaints' text similarity |
| Haversine formula | `duplicate_service.py` | GPS distance between two complaints |
| Weighted priority scoring | `priority_service.py` | Transparent 0–100 priority score |
| Rule-based department routing | `assignment_service.py` | Category → department mapping |
| Rule-based escalation | `workers/scheduler.py` | Deadline-based automatic escalation |

**No XGBoost. No SHAP. No local GPU training.** These were deliberately
excluded per the project's lightweight, transparent, and reproducible design
goals.

## 8. Database Design

15 tables: `User`, `Department`, `Complaint`, `ComplaintImage`,
`ComplaintAnalysis`, `ComplaintLocation`, `ComplaintDuplicate`,
`PriorityAnalysis`, `ComplaintAssignment`, `StatusHistory`, `Escalation`,
`Notification`, `Resolution`, `SystemSetting`, `AuditLog`.

See `backend/app/models/` for full SQLAlchemy definitions with foreign keys
and relationships.

## 9. User Roles

- **CITIZEN** — submit/track complaints, view AI analysis, timeline, resolution.
- **OFFICER** — acknowledge, work on, and resolve assigned complaints.
- **DEPARTMENT_HEAD** — monitor department complaints, handle escalations, reassign.
- **ADMIN** — manage users/departments, configure settings, view all analytics/audit logs.

## 10. Authority Acknowledgement Mechanism

Every assignment stores `assigned_at`, `acknowledgement_deadline`,
`acknowledged_at`, `acknowledged_by`, and `resolution_deadline`. The officer
dashboard shows a prominent **"Acknowledge Complaint"** button. On click, the
timestamp and officer ID are recorded, an audit log entry is created, and the
citizen is notified and sees "✓ Received & Acknowledged by Officer" with the
exact date/time on their timeline. This is the strongest evidence of
authority receipt in the system.

## 11. Escalation Mechanism

A lightweight APScheduler background job (no Celery/Kafka) runs every
`SCHEDULER_INTERVAL_MINUTES` and:

1. Finds assignments past `acknowledgement_deadline` with no acknowledgement
   → escalates to the Department Head, notifies them, logs the audit trail,
   and updates the citizen's timeline.
2. Finds `IN_PROGRESS` assignments past `resolution_deadline` → escalates
   again with a new deadline.

Duplicate escalation is prevented by checking for an existing OPEN escalation
with the same reason before creating a new one.

---

## 12. Installation

### Prerequisites
- Python 3.11+ (3.12 recommended)
- Node.js 18+
- (Optional) PostgreSQL 14+ — SQLite is used automatically if you skip this
- (Optional) Docker Desktop — the project also runs natively without Docker

### Option A — Run natively without Docker (Windows PowerShell)

```powershell
# 1. Clone / unzip the project, then:
cd civicai\backend

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (SQLite works out of the box — no edits needed)
Copy-Item .env.example .env

# 5. Seed demo data (creates SQLite DB + departments + users + complaints)
python seed.py

# 6. Start the backend
uvicorn app.main:app --reload --port 8000
```

In a **second** PowerShell window:

```powershell
cd civicai\frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open **http://localhost:5173** and sign in with a demo account below.

### Option B — Run with PostgreSQL locally

1. Create a database: `createdb civicai` (or via pgAdmin).
2. In `backend/.env`, set:
   ```
   USE_SQLITE=false
   DATABASE_URL=postgresql+psycopg2://<user>:<password>@localhost:5432/civicai
   ```
3. Continue with steps 3–6 above.

### Option C — Run with Docker (optional)

```powershell
docker compose up --build
```

This starts PostgreSQL, the backend on port 8000, and the frontend on port 5173.
Run `docker compose exec backend python seed.py` once to seed demo data.

---

## 13. Environment Variables

See `backend/.env.example` and `frontend/.env.example`. Key variables:

| Variable | Purpose |
|---|---|
| `AI_MODE` | `demo` (offline, default) or `live` (Gemini) |
| `GEMINI_API_KEY` | Only needed for `AI_MODE=live` |
| `USE_SQLITE` | `true` for zero-setup demo, `false` for PostgreSQL |
| `ACKNOWLEDGEMENT_DEADLINE_HOURS` | Default 6, admin-configurable at runtime |
| `TEXT_SIMILARITY_THRESHOLD` / `DUPLICATE_RADIUS_METERS` | Duplicate detection tuning |
| `SCHEDULER_INTERVAL_MINUTES` | Escalation check frequency |

**No secrets are hard-coded anywhere in the codebase.**

## 14. Demo Credentials

All demo accounts use the password: **`Demo@123`**

| Role | Email |
|---|---|
| Admin | admin@civicai.demo |
| Department Head (Roads) | roads.head@civicai.demo |
| Officer (Roads) | roads.officer@civicai.demo |
| Citizen | citizen@civicai.demo |

(4 more officers and 2 more heads across Sanitation/Electrical/Water/Drainage
are also seeded — see `backend/seed.py`.)

## 15. API Overview

Interactive API docs are auto-generated at **http://localhost:8000/docs**
(Swagger UI) once the backend is running. Key endpoint groups:
`/api/auth`, `/api/complaints`, `/api/ai`, `/api/complaints/{id}/duplicate-check`,
`/api/complaints/{id}/priority`, `/api/complaints/{id}/assign`,
`/api/complaints/{id}/acknowledge`, `/api/complaints/{id}/resolve`,
`/api/escalations`, `/api/notifications`, `/api/dashboard/*`,
`/api/analytics/*`, `/api/settings`, `/api/audit-logs`, `/api/admin/*`.

## 16. Testing

```powershell
cd civicai
pip install -r backend\requirements.txt
cd tests\backend
pytest -v
```

18 tests cover: registration/login/protected routes, AI demo mode, the full
complaint creation pipeline, TF-IDF/cosine/Haversine algorithms, department
routing, and role-based authorization boundaries (citizens cannot access
admin endpoints, etc.).

## 17. Demonstrating the Project (Evaluation Script)

1. **Login as Citizen** → Report Issue → upload a pothole photo → describe
   *"Large pothole near college entrance"* → see AI detect **Pothole / HIGH /
   Safety Risk: Yes** (labeled "Demo AI Mode") → see the generated complaint →
   edit if desired → submit. Note the duplicate check and **HIGH priority**
   with its plain-English explanation, and that it's auto-assigned to
   **Roads & Infrastructure**.
2. **Login as the assigned Officer** → do **not** acknowledge it yet.
3. Wait for the scheduler interval (or lower `ACKNOWLEDGEMENT_DEADLINE_HOURS`
   to a few minutes and `SCHEDULER_INTERVAL_MINUTES=1` in Admin Settings for
   a live demo) → the complaint automatically escalates → **login as
   Department Head** and see the escalation notification.
4. **Submit a second complaint**, this time **acknowledge it promptly** as
   the officer → citizen sees "✓ Received & Acknowledged by Officer" with
   timestamp → officer moves it **IN_PROGRESS → RESOLVED** with evidence →
   citizen sees the full timeline and closes the complaint.
5. **Login as Admin** to show analytics, audit logs, and system settings.

This entire scenario works with **zero external API keys** using AI Demo Mode.

## 18. Screenshots

*(Add screenshots of the citizen wizard, officer dashboard, department head
escalations view, and admin analytics here before submission.)*

## 19. Limitations

- The project does **not** connect to real municipal government systems or
  APIs. Authority accounts (Department Heads, Officers, Admin) are **simulated
  internally** using role-based accounts seeded for demonstration purposes.
- AI vision/generation uses pre-trained/cloud capabilities (Gemini) rather
  than a custom-trained model, by design, to remain lightweight and
  reproducible on a normal student laptop.
- Duplicate detection uses TF-IDF/cosine/GPS heuristics rather than deep
  semantic embeddings — sufficient for demonstration, not production-grade
  at city scale.
- Notifications are in-app only; SMS/email integration is future scope.

## 20. Future Scope

- Real municipal API integration (once official access is granted).
- SMS/email notification channels.
- Advanced computer vision (custom-trained detection models).
- Native mobile application.
- Multilingual complaint support.
- Advanced geospatial analytics / heatmaps.
- Image-based automatic resolution verification.
- Predictive officer workload forecasting.
- IoT sensor integration (e.g., smart streetlights, water sensors).

---

## Project Structure

```
civicai/
├── frontend/           React + TypeScript + Vite + Tailwind
│   └── src/{components,pages,layouts,hooks,services,context,types,utils}
├── backend/             FastAPI modular monolith
│   └── app/{api,core,models,schemas,services,workers,utils}
├── tests/backend/       pytest suite (18 tests)
├── uploads/             Local file storage fallback
├── docker-compose.yml   Optional containerized setup
└── README.md
```

## Academic Positioning

CivicAI integrates image understanding, Generative AI, lightweight text
similarity, geospatial validation, transparent priority scoring, rule-based
department assignment, authority acknowledgement, and automatic escalation
into a single end-to-end platform. The contribution is the **integrated,
lightweight, practical combination** of these techniques into one
accountable civic workflow — not any single novel algorithm.
