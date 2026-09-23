"""
CivicAI backend entrypoint.

Modular monolith - no microservices. Run with:
    uvicorn app.main:app --reload --port 8000
"""
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.database import Base, engine, SessionLocal
from app.utils.error_handlers import register_error_handlers
from app.workers.scheduler import start_scheduler, stop_scheduler
from app.services.settings_service import ensure_default_settings

# Routers
from app.api import auth, ai, uploads, complaints, assignments, resolutions, escalations, notifications, dashboard, analytics, settings as settings_router, audit, admin

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("civicai")

settings = get_settings()

app = FastAPI(
    title="CivicAI API",
    description="AI-Based Civic Issue Detection, Prioritization and Resolution System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

# Ensure tables exist (for SQLite/demo use; use Alembic migrations for PostgreSQL production)
Base.metadata.create_all(bind=engine)

# Serve locally-stored uploaded images
uploads_dir = Path(__file__).resolve().parents[2] / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(uploads.router)
app.include_router(complaints.router)
app.include_router(assignments.router)
app.include_router(resolutions.router)
app.include_router(escalations.router)
app.include_router(notifications.router)
app.include_router(dashboard.router)
app.include_router(analytics.router)
app.include_router(settings_router.router)
app.include_router(audit.router)
app.include_router(admin.router)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        ensure_default_settings(db)
    finally:
        db.close()
    start_scheduler(settings.SCHEDULER_INTERVAL_MINUTES)
    logger.info("CivicAI backend started. AI_MODE=%s, STORAGE_PROVIDER=%s", settings.AI_MODE, settings.STORAGE_PROVIDER)


@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()


@app.get("/")
def root():
    return {
        "success": True,
        "message": "CivicAI API is running",
        "aiMode": settings.AI_MODE,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"success": True, "status": "healthy"}
