from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintStatus
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.models.resolution import Resolution
from app.schemas.resolution import ResolveComplaintRequest, ResolutionOut
from app.schemas.common import ApiResponse
from app.services.audit_service import log_event
from app.services.notification_service import notify

router = APIRouter(prefix="/api/complaints", tags=["resolutions"])


@router.post("/{complaint_id}/resolve", response_model=ApiResponse[ResolutionOut])
def resolve_complaint(complaint_id: int, payload: ResolveComplaintRequest, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.OFFICER, UserRole.ADMIN))):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    resolution = Resolution(complaint_id=complaint_id, resolved_by=current_user.id, description=payload.description, evidence_url=payload.evidence_url)
    db.add(resolution)

    complaint.status = ComplaintStatus.RESOLVED
    complaint.resolved_at = datetime.utcnow()

    assignment = db.query(ComplaintAssignment).filter(ComplaintAssignment.complaint_id == complaint_id).order_by(ComplaintAssignment.id.desc()).first()
    if assignment:
        assignment.assignment_status = AssignmentStatus.RESOLVED
    db.commit()
    db.refresh(resolution)

    log_event(db, complaint_id, "RESOLUTION_SUBMITTED", "Resolution evidence submitted by officer.", user_id=current_user.id, add_status_history=True)
    log_event(db, complaint_id, "COMPLAINT_RESOLVED", "Complaint marked resolved.", user_id=current_user.id, add_status_history=True)
    notify(db, complaint.citizen_id, "RESOLUTION", "Complaint resolved", "Your complaint has been resolved. Please review the resolution evidence.", complaint_id=complaint_id)
    return ApiResponse(data=ResolutionOut.model_validate(resolution), message="Complaint resolved")


@router.get("/{complaint_id}/resolution", response_model=ApiResponse[ResolutionOut])
def get_resolution(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resolution = db.query(Resolution).filter(Resolution.complaint_id == complaint_id).first()
    if not resolution:
        raise HTTPException(status_code=404, detail="No resolution recorded yet")
    return ApiResponse(data=ResolutionOut.model_validate(resolution))


@router.post("/{complaint_id}/close")
def close_complaint(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.CITIZEN, UserRole.ADMIN))):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if current_user.role == UserRole.CITIZEN and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    complaint.status = ComplaintStatus.CLOSED
    db.commit()
    log_event(db, complaint_id, "COMPLAINT_CLOSED", "Citizen confirmed resolution and closed the complaint.", user_id=current_user.id, add_status_history=True)
    return ApiResponse(message="Complaint closed")
