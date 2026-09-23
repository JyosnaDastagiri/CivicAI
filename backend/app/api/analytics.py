from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintStatus
from app.models.department import Department
from app.models.escalation import Escalation
from app.models.complaint_assignment import ComplaintAssignment
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def _scope(db: Session, current_user: User):
    q = db.query(Complaint)
    if current_user.role == UserRole.DEPARTMENT_HEAD:
        q = q.filter(Complaint.department_id == current_user.department_id)
    return q


@router.get("/complaints")
def complaints_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD))):
    q = _scope(db, current_user)
    by_category = dict(q.with_entities(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all())
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly = (
        db.query(func.strftime("%Y-%m", Complaint.created_at), func.count(Complaint.id))
        .filter(Complaint.created_at >= six_months_ago)
        .group_by(func.strftime("%Y-%m", Complaint.created_at))
        .all()
    )
    return ApiResponse(data={"byCategory": by_category, "monthlyTrend": dict(monthly)})


@router.get("/departments")
def department_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    rows = (
        db.query(Department.name, func.count(Complaint.id))
        .outerjoin(Complaint, Complaint.department_id == Department.id)
        .group_by(Department.name)
        .all()
    )
    return ApiResponse(data={"complaintsByDepartment": dict(rows)})


@router.get("/status")
def status_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD))):
    q = _scope(db, current_user)
    rows = q.with_entities(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    return ApiResponse(data={"byStatus": {k.value: v for k, v in rows}})


@router.get("/priority")
def priority_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD))):
    q = _scope(db, current_user)
    rows = q.with_entities(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority).all()
    return ApiResponse(data={"byPriority": {(k.value if k else "UNSET"): v for k, v in rows}})


@router.get("/escalations")
def escalation_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD))):
    query = db.query(Escalation)
    if current_user.role == UserRole.DEPARTMENT_HEAD:
        query = query.filter(Escalation.to_user_id == current_user.id)
    total = query.count()
    open_count = query.filter(Escalation.status == "OPEN").count()
    return ApiResponse(data={"totalEscalations": total, "openEscalations": open_count})
