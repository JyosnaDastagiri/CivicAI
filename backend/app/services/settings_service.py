"""
Reads/writes SystemSetting rows, falling back to environment defaults.
This is what makes deadlines, thresholds, and scheduler interval fully
configurable from the Admin UI without code changes.
"""
from sqlalchemy.orm import Session
from app.models.system_setting import SystemSetting
from app.core.config import get_settings

settings = get_settings()

DEFAULTS = {
    "ACKNOWLEDGEMENT_DEADLINE_HOURS": (str(settings.ACKNOWLEDGEMENT_DEADLINE_HOURS), "Hours allowed for an officer to acknowledge a new assignment."),
    "CRITICAL_RESOLUTION_HOURS": (str(settings.CRITICAL_RESOLUTION_HOURS), "Resolution deadline (hours) for CRITICAL priority complaints."),
    "HIGH_RESOLUTION_HOURS": (str(settings.HIGH_RESOLUTION_HOURS), "Resolution deadline (hours) for HIGH priority complaints."),
    "MEDIUM_RESOLUTION_HOURS": (str(settings.MEDIUM_RESOLUTION_HOURS), "Resolution deadline (hours) for MEDIUM priority complaints."),
    "LOW_RESOLUTION_HOURS": (str(settings.LOW_RESOLUTION_HOURS), "Resolution deadline (hours) for LOW priority complaints."),
    "TEXT_SIMILARITY_THRESHOLD": (str(settings.TEXT_SIMILARITY_THRESHOLD), "Minimum TF-IDF cosine similarity to flag a potential duplicate."),
    "DUPLICATE_RADIUS_METERS": (str(settings.DUPLICATE_RADIUS_METERS), "Maximum GPS distance (meters) to flag a potential duplicate."),
    "SCHEDULER_INTERVAL_MINUTES": (str(settings.SCHEDULER_INTERVAL_MINUTES), "How often (minutes) the escalation scheduler runs."),
    "AI_MODE": (settings.AI_MODE, "AI mode: demo or live."),
    "WEIGHT_SEVERITY": ("30", "Max points contributed by severity to the priority score."),
    "WEIGHT_SAFETY": ("25", "Max points contributed by safety risk to the priority score."),
    "WEIGHT_LOCATION": ("20", "Max points contributed by location importance to the priority score."),
    "WEIGHT_RECURRENCE": ("15", "Max points contributed by recurrence/related reports to the priority score."),
    "WEIGHT_URGENCY": ("10", "Max points contributed by category urgency to the priority score."),
}


def ensure_default_settings(db: Session) -> None:
    existing_keys = {row.key for row in db.query(SystemSetting.key).all()}
    for key, (value, description) in DEFAULTS.items():
        if key not in existing_keys:
            db.add(SystemSetting(key=key, value=value, description=description))
    db.commit()


def get_setting(db: Session, key: str) -> str:
    row = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if row:
        return row.value
    if key in DEFAULTS:
        return DEFAULTS[key][0]
    raise KeyError(f"Unknown setting: {key}")


def get_setting_float(db: Session, key: str) -> float:
    return float(get_setting(db, key))


def set_setting(db: Session, key: str, value: str) -> SystemSetting:
    row = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not row:
        row = SystemSetting(key=key, value=value, description=DEFAULTS.get(key, ("", ""))[1])
        db.add(row)
    else:
        row.value = value
    db.commit()
    db.refresh(row)
    return row
