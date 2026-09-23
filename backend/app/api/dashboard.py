from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintStatus
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.models.escalation import Escalation
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/citizen")
def citizen_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.CITIZEN))):
    q = db.query(Complaint).filter(Complaint.citizen_id == current_user.id)
    total = q.count()
    active = q.filter(Complaint.status.notin_([ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED, ComplaintStatus.REJECTED])).count()
    resolved = q.filter(Complaint.status.in_([ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED])).count()
    escalated = q.filter(Complaint.status == ComplaintStatus.ESCALATED).count()
    recent = q.order_by(Complaint.created_at.desc()).limit(5).all()
    status_counts = dict(db.query(Complaint.status, func.count(Complaint.id)).filter(Complaint.citizen_id == current_user.id).group_by(Complaint.status).all())
    return ApiResponse(data={
        "totalComplaints": total, "activeComplaints": active, "resolvedComplaints": resolved,
        "escalatedComplaints": escalated,
        "recentComplaints": [{"id": c.id, "title": c.title, "status": c.status.value, "priority": c.priority.value if c.priority else None, "createdAt": c.created_at} for c in recent],
        "statusOverview": {k.value if hasattr(k, "value") else k: v for k, v in status_counts.items()},
    })


@router.get("/officer")
def officer_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.OFFICER))):
    q = db.query(ComplaintAssignment).filter(ComplaintAssignment.assigned_to == current_user.id)
    now = datetime.utcnow()
    assigned = q.count()
    awaiting_ack = q.filter(ComplaintAssignment.assignment_status == AssignmentStatus.ASSIGNED, ComplaintAssignment.acknowledged_at.is_(None)).count()
    acknowledged = q.filter(ComplaintAssignment.assignment_status == AssignmentStatus.ACKNOWLEDGED).count()
    in_progress = q.filter(ComplaintAssignment.assignment_status == AssignmentStatus.IN_PROGRESS).count()
    overdue = q.filter(ComplaintAssignment.acknowledgement_deadline < now, ComplaintAssignment.acknowledged_at.is_(None)).count()
    resolved = q.filter(ComplaintAssignment.assignment_status == AssignmentStatus.RESOLVED).count()
    escalated = q.filter(ComplaintAssignment.assignment_status == AssignmentStatus.ESCALATED).count()
    return ApiResponse(data={
        "assigned": assigned, "awaitingAcknowledgement": awaiting_ack, "acknowledged": acknowledged,
        "inProgress": in_progress, "overdue": overdue, "resolved": resolved, "escalated": escalated,
    })


@router.get("/department")
def department_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.DEPARTMENT_HEAD))):
    q = db.query(Complaint).filter(Complaint.department_id == current_user.department_id)
    total = q.count()
    pending_ack = db.query(ComplaintAssignment).join(Complaint, Complaint.id == ComplaintAssignment.complaint_id).filter(
        Complaint.department_id == current_user.department_id, ComplaintAssignment.acknowledged_at.is_(None)
    ).count()
    overdue = db.query(ComplaintAssignment).join(Complaint, Complaint.id == ComplaintAssignment.complaint_id).filter(
        Complaint.department_id == current_user.department_id,
        ComplaintAssignment.acknowledgement_deadline < datetime.utcnow(), ComplaintAssignment.acknowledged_at.is_(None),
    ).count()
    escalated = q.filter(Complaint.status == ComplaintStatus.ESCALATED).count()
    resolved = q.filter(Complaint.status.in_([ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED])).count()
    priority_dist = dict(db.query(Complaint.priority, func.count(Complaint.id)).filter(Complaint.department_id == current_user.department_id).group_by(Complaint.priority).all())
    return ApiResponse(data={
        "departmentComplaintCount": total, "pendingAcknowledgement": pending_ack, "overdue": overdue,
        "escalated": escalated, "resolved": resolved,
        "priorityDistribution": {k.value if hasattr(k, "value") else k: v for k, v in priority_dist.items() if k},
    })


@router.get("/admin")
def admin_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    total = db.query(Complaint).count()
    open_count = db.query(Complaint).filter(Complaint.status.notin_([ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED])).count()
    resolved = db.query(Complaint).filter(Complaint.status.in_([ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED])).count()
    critical = db.query(Complaint).filter(Complaint.priority == "CRITICAL").count()
    escalated = db.query(Escalation).count()
    from app.models.complaint_duplicate import ComplaintDuplicate
    duplicates = db.query(ComplaintDuplicate).filter(ComplaintDuplicate.is_potential_duplicate.is_(True)).count()
    return ApiResponse(data={
        "totalComplaints": total, "openComplaints": open_count, "resolvedComplaints": resolved,
        "criticalComplaints": critical, "escalatedComplaints": escalated, "duplicateComplaints": duplicates,
    })
