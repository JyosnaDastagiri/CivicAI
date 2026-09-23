"""
Transparent, context-aware weighted priority scoring (Requirement #14).

NO XGBoost. NO SHAP. NO black-box ML. Just a documented weighted-sum
algorithm whose factors and final score are stored and explainable.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.complaint import Complaint, Severity
from app.models.complaint_duplicate import ComplaintDuplicate
from app.services.settings_service import get_setting_float

SEVERITY_POINTS = {
    Severity.LOW: 0.25,
    Severity.MEDIUM: 0.55,
    Severity.HIGH: 0.8,
    Severity.CRITICAL: 1.0,
}

# High-traffic / high-importance categories get a bigger location weight share.
HIGH_IMPORTANCE_CATEGORIES = {"Pothole", "Road Damage", "Drainage", "Water Leakage"}

CATEGORY_URGENCY = {
    "Pothole": 0.9,
    "Road Damage": 0.85,
    "Water Leakage": 0.8,
    "Drainage": 0.75,
    "Broken Streetlight": 0.6,
    "Fallen Tree": 0.85,
    "Garbage": 0.5,
    "Damaged Road Sign": 0.45,
    "General Civic Issue": 0.4,
}


def calculate_priority(db: Session, complaint: Complaint) -> dict:
    w_severity = get_setting_float(db, "WEIGHT_SEVERITY")
    w_safety = get_setting_float(db, "WEIGHT_SAFETY")
    w_location = get_setting_float(db, "WEIGHT_LOCATION")
    w_recurrence = get_setting_float(db, "WEIGHT_RECURRENCE")
    w_urgency = get_setting_float(db, "WEIGHT_URGENCY")

    severity_score = round(SEVERITY_POINTS.get(complaint.severity, 0.5) * w_severity, 2)
    safety_score = round((1.0 if complaint.safety_risk else 0.2) * w_safety, 2)
    location_score = round((0.8 if complaint.category in HIGH_IMPORTANCE_CATEGORIES else 0.4) * w_location, 2)

    related_count = (
        db.query(ComplaintDuplicate)
        .filter(ComplaintDuplicate.complaint_id == complaint.id, ComplaintDuplicate.is_potential_duplicate.is_(True))
        .count()
    )
    recurrence_factor = min(1.0, 0.3 + related_count * 0.25)
    recurrence_score = round(recurrence_factor * w_recurrence, 2)

    urgency_score = round(CATEGORY_URGENCY.get(complaint.category, 0.4) * w_urgency, 2)

    final_score = round(severity_score + safety_score + location_score + recurrence_score + urgency_score, 2)
    final_score = min(final_score, 100.0)

    if final_score <= 30:
        priority = "LOW"
    elif final_score <= 60:
        priority = "MEDIUM"
    elif final_score <= 80:
        priority = "HIGH"
    else:
        priority = "CRITICAL"

    reasons = []
    if complaint.severity in (Severity.HIGH, Severity.CRITICAL):
        reasons.append("the issue has high severity")
    if complaint.safety_risk:
        reasons.append("it presents a safety risk")
    if complaint.category in HIGH_IMPORTANCE_CATEGORIES:
        reasons.append("it is located in a high-importance category area")
    if related_count > 0:
        reasons.append(f"{related_count} related report(s) were found nearby")
    if not reasons:
        reasons.append("the combined weighted factors were moderate")

    explanation = f"{priority.title()} priority because " + ", ".join(reasons) + "."

    return {
        "severityScore": severity_score,
        "safetyScore": safety_score,
        "locationScore": location_score,
        "recurrenceScore": recurrence_score,
        "urgencyScore": urgency_score,
        "finalScore": final_score,
        "priority": priority,
        "explanation": explanation,
    }
