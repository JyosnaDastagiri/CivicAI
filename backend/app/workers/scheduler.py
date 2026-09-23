"""
Lightweight background escalation scheduler (Requirement #18, #36).

Uses APScheduler's BackgroundScheduler (no Celery/Kafka/microservices).
Periodically (SCHEDULER_INTERVAL_MINUTES) checks:
  1. Assignments past their acknowledgement_deadline that are still ASSIGNED
     -> auto-escalate to the Department Head.
  2. Assignments past their resolution_deadline that are not RESOLVED
     -> auto-escalate to the Department Head with a new deadline.

Duplicate escalation is prevented by checking for an existing OPEN
escalation of the same reason before creating a new one.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.complaint import Complaint, ComplaintStatus, Priority
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.models.escalation import Escalation, EscalationStatus
from app.models.user import User, UserRole
from app.services.audit_service import log_event
from app.services.notification_service import notify
from app.services.settings_service import get_setting_float, ensure_default_settings

logger = logging.getLogger("civicai.scheduler")

RESOLUTION_HOURS_BY_PRIORITY = {
    "CRITICAL": "CRITICAL_RESOLUTION_HOURS",
    "HIGH": "HIGH_RESOLUTION_HOURS",
    "MEDIUM": "MEDIUM_RESOLUTION_HOURS",
    "LOW": "LOW_RESOLUTION_HOURS",
}


def _department_head(db: Session, department_id: int) -> User | None:
    return (
        db.query(User)
        .filter(User.role == UserRole.DEPARTMENT_HEAD, User.department_id == department_id, User.is_active.is_(True))
        .first()
    )


def _has_open_escalation(db: Session, complaint_id: int, reason_snippet: str) -> bool:
    return (
        db.query(Escalation)
        .filter(
            Escalation.complaint_id == complaint_id,
            Escalation.status == EscalationStatus.OPEN,
            Escalation.reason.like(f"%{reason_snippet}%"),
        )
        .first()
        is not None
    )


def check_acknowledgement_deadlines(db: Session) -> int:
    now = datetime.utcnow()
    overdue = (
        db.query(ComplaintAssignment)
        .filter(
            ComplaintAssignment.assignment_status == AssignmentStatus.ASSIGNED,
            ComplaintAssignment.acknowledged_at.is_(None),
            ComplaintAssignment.acknowledgement_deadline < now,
        )
        .all()
    )
    count = 0
    for assignment in overdue:
        reason = "Officer failed to acknowledge complaint within configured deadline."
        if _has_open_escalation(db, assignment.complaint_id, "acknowledge"):
            continue

        complaint = db.query(Complaint).filter(Complaint.id == assignment.complaint_id).first()
        if not complaint:
            continue

        head = _department_head(db, complaint.department_id) if complaint.department_id else None
        new_deadline = now + timedelta(hours=get_setting_float(db, "ACKNOWLEDGEMENT_DEADLINE_HOURS"))

        escalation = Escalation(
            complaint_id=complaint.id,
            from_user_id=assignment.assigned_to,
            to_user_id=head.id if head else None,
            reason=reason,
            escalated_at=now,
            previous_deadline=assignment.acknowledgement_deadline,
            new_deadline=new_deadline,
            status=EscalationStatus.OPEN,
        )
        db.add(escalation)

        assignment.assignment_status = AssignmentStatus.ESCALATED
        complaint.status = ComplaintStatus.ESCALATED
        db.commit()

        log_event(
            db, complaint.id, "ACKNOWLEDGEMENT_DEADLINE_EXCEEDED", reason,
            user_id=None, add_status_history=True,
        )
        log_event(
            db, complaint.id, "COMPLAINT_ESCALATED",
            "Automatically escalated to Department Head.",
            add_status_history=True,
        )

        if head:
            notify(
                db, head.id, "ESCALATION",
                "Complaint escalated to you",
                f"Complaint #{complaint.id} ({complaint.title}) was not acknowledged in time and has been escalated to you.",
                complaint_id=complaint.id,
            )
            log_event(db, complaint.id, "HIGHER_AUTHORITY_NOTIFIED", f"Department Head (user #{head.id}) notified.")

        notify(
            db, complaint.citizen_id, "ESCALATION",
            "Your complaint was escalated",
            "Complaint escalated because the acknowledgement deadline was exceeded. It has been forwarded to the Department Head.",
            complaint_id=complaint.id,
        )
        count += 1
    return count


def check_resolution_deadlines(db: Session) -> int:
    now = datetime.utcnow()
    overdue = (
        db.query(ComplaintAssignment)
        .filter(
            ComplaintAssignment.assignment_status == AssignmentStatus.IN_PROGRESS,
            ComplaintAssignment.resolution_deadline.isnot(None),
            ComplaintAssignment.resolution_deadline < now,
        )
        .all()
    )
    count = 0
    for assignment in overdue:
        if _has_open_escalation(db, assignment.complaint_id, "resolution deadline"):
            continue
        complaint = db.query(Complaint).filter(Complaint.id == assignment.complaint_id).first()
        if not complaint or complaint.status in (ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED):
            continue

        head = _department_head(db, complaint.department_id) if complaint.department_id else None
        setting_key = RESOLUTION_HOURS_BY_PRIORITY.get(complaint.priority.value if complaint.priority else "MEDIUM", "MEDIUM_RESOLUTION_HOURS")
        new_deadline = now + timedelta(hours=get_setting_float(db, setting_key))

        reason = "Officer failed to resolve complaint within the configured resolution deadline."
        escalation = Escalation(
            complaint_id=complaint.id,
            from_user_id=assignment.assigned_to,
            to_user_id=head.id if head else None,
            reason=reason,
            escalated_at=now,
            previous_deadline=assignment.resolution_deadline,
            new_deadline=new_deadline,
            status=EscalationStatus.OPEN,
        )
        db.add(escalation)
        assignment.assignment_status = AssignmentStatus.ESCALATED
        assignment.resolution_deadline = new_deadline
        complaint.status = ComplaintStatus.ESCALATED
        db.commit()

        log_event(db, complaint.id, "RESOLUTION_DEADLINE_EXCEEDED", reason, add_status_history=True)
        log_event(db, complaint.id, "COMPLAINT_ESCALATED", "Automatically escalated for delayed resolution.", add_status_history=True)

        if head:
            notify(
                db, head.id, "ESCALATION",
                "Resolution overdue - escalated to you",
                f"Complaint #{complaint.id} ({complaint.title}) missed its resolution deadline and has been escalated to you.",
                complaint_id=complaint.id,
            )
            log_event(db, complaint.id, "HIGHER_AUTHORITY_NOTIFIED", f"Department Head (user #{head.id}) notified of resolution delay.")

        notify(
            db, complaint.citizen_id, "ESCALATION",
            "Resolution delayed - complaint escalated",
            "Your complaint's resolution deadline was exceeded and it has been escalated to the Department Head for prioritized action.",
            complaint_id=complaint.id,
        )
        count += 1
    return count


def run_escalation_check() -> None:
    db = SessionLocal()
    try:
        ensure_default_settings(db)
        ack_count = check_acknowledgement_deadlines(db)
        res_count = check_resolution_deadlines(db)
        if ack_count or res_count:
            logger.info(f"[scheduler] Escalated {ack_count} unacknowledged, {res_count} unresolved complaints.")
    finally:
        db.close()


_scheduler: BackgroundScheduler | None = None


def start_scheduler(interval_minutes: float) -> BackgroundScheduler:
    global _scheduler
    if _scheduler and _scheduler.running:
        return _scheduler
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(run_escalation_check, "interval", minutes=interval_minutes, id="escalation_check", replace_existing=True)
    _scheduler.start()
    logger.info(f"[scheduler] Started escalation scheduler, interval={interval_minutes} minute(s).")
    return _scheduler


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
