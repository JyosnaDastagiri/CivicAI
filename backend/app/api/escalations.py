from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.escalation import Escalation, EscalationStatus
from app.schemas.common import ApiResponse
from app.services.audit_service import log_event

router = APIRouter(prefix="/api", tags=["escalations"])


def _serialize(e: Escalation) -> dict:
    return {c.name: getattr(e, c.name) for c in e.__table__.columns}


@router.get("/escalations")
def list_escalations(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.DEPARTMENT_HEAD, UserRole.ADMIN))):
    query = db.query(Escalation)
    if current_user.role == UserRole.DEPARTMENT_HEAD:
        query = query.filter(Escalation.to_user_id == current_user.id)
    items = query.order_by(Escalation.escalated_at.desc()).all()
    return ApiResponse(data=[_serialize(e) for e in items])


@router.get("/complaints/{complaint_id}/escalations")
def get_complaint_escalations(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(Escalation).filter(Escalation.complaint_id == complaint_id).order_by(Escalation.escalated_at.asc()).all()
    return ApiResponse(data=[_serialize(e) for e in items])


@router.post("/escalations/{escalation_id}/acknowledge")
def acknowledge_escalation(escalation_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.DEPARTMENT_HEAD, UserRole.ADMIN))):
    escalation = db.query(Escalation).filter(Escalation.id == escalation_id).first()
    if not escalation:
        raise HTTPException(status_code=404, detail="Escalation not found")
    escalation.status = EscalationStatus.ACKNOWLEDGED
    db.commit()
    log_event(db, escalation.complaint_id, "ESCALATION_ACKNOWLEDGED", "Department Head acknowledged the escalation.", user_id=current_user.id, add_status_history=True)
    return ApiResponse(message="Escalation acknowledged")
