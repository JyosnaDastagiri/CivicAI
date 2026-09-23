"""
Assignment + authority acknowledgement endpoints (Requirement #16 - mandatory module)
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintStatus
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.schemas.assignment import AssignmentOut, AcknowledgeRequest, ReassignRequest
from app.schemas.common import ApiResponse
from app.services.assignment_service import assign_complaint
from app.services.audit_service import log_event
from app.services.notification_service import notify
from app.services.settings_service import get_setting_float

router = APIRouter(prefix="/api/complaints", tags=["assignments"])

RESOLUTION_HOURS_BY_PRIORITY = {
    "CRITICAL": "CRITICAL_RESOLUTION_HOURS", "HIGH": "HIGH_RESOLUTION_HOURS",
    "MEDIUM": "MEDIUM_RESOLUTION_HOURS", "LOW": "LOW_RESOLUTION_HOURS",
}


def _latest_assignment(db: Session, complaint_id: int) -> ComplaintAssignment:
    a = db.query(ComplaintAssignment).filter(ComplaintAssignment.complaint_id == complaint_id).order_by(ComplaintAssignment.id.desc()).first()
    if not a:
        raise HTTPException(status_code=404, detail="No assignment found for this complaint")
    return a


@router.post("/{complaint_id}/assign", response_model=ApiResponse[AssignmentOut])
def manual_assign(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD))):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    assignment = assign_complaint(db, complaint)
    if not assignment:
        raise HTTPException(status_code=400, detail="No available officer to assign")
    complaint.status = ComplaintStatus.ASSIGNED
    db.commit()
    log_event(db, complaint.id, "DEPARTMENT_ASSIGNED", "Manually (re)assigned by authority.", user_id=current_user.id, add_status_history=True)
    notify(db, assignment.assigned_to, "ASSIGNMENT", "Complaint assigned to you", f"Complaint #{complaint.id} assigned to you.", complaint_id=complaint.id)
    return ApiResponse(data=AssignmentOut.model_validate(assignment), message="Complaint assigned")


@router.get("/{complaint_id}/assignment", response_model=ApiResponse[AssignmentOut])
def get_assignment(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignment = _latest_assignment(db, complaint_id)
    return ApiResponse(data=AssignmentOut.model_validate(assignment))


@router.post("/{complaint_id}/acknowledge", response_model=ApiResponse[AssignmentOut])
def acknowledge(complaint_id: int, payload: AcknowledgeRequest, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.OFFICER, UserRole.ADMIN))):
    """
    THE core authority-accountability action: an officer explicitly confirms
    they received the complaint. Timestamp + officer id are persisted, the
    citizen is notified, and an audit trail entry is created.
    """
    assignment = _latest_assignment(db, complaint_id)
    if assignment.assigned_to != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only the assigned officer can acknowledge this complaint")
    if assignment.acknowledged_at is not None:
        raise HTTPException(status_code=400, detail="Complaint already acknowledged")

    now = datetime.utcnow()
    assignment.acknowledged_at = now
    assignment.acknowledged_by = current_user.id
    assignment.assignment_status = AssignmentStatus.ACKNOWLEDGED

    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    complaint.status = ComplaintStatus.ACKNOWLEDGED
    resolution_key = RESOLUTION_HOURS_BY_PRIORITY.get(complaint.priority.value if complaint.priority else "MEDIUM", "MEDIUM_RESOLUTION_HOURS")
    assignment.resolution_deadline = now + timedelta(hours=get_setting_float(db, resolution_key))
    db.commit()
    db.refresh(assignment)

    log_event(
        db, complaint.id, "COMPLAINT_ACKNOWLEDGED",
        f"Received & Acknowledged by Officer (user #{current_user.id}) at {now.isoformat()}.",
        user_id=current_user.id, add_status_history=True,
    )
    notify(db, complaint.citizen_id, "ACKNOWLEDGEMENT", "Complaint acknowledged", "Your complaint has been received and acknowledged by the assigned officer.", complaint_id=complaint.id)
    return ApiResponse(data=AssignmentOut.model_validate(assignment), message="Complaint acknowledged")


@router.get("/{complaint_id}/acknowledgement")
def get_acknowledgement(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignment = _latest_assignment(db, complaint_id)
    return ApiResponse(data={
        "acknowledged": assignment.acknowledged_at is not None,
        "acknowledgedAt": assignment.acknowledged_at,
        "acknowledgedBy": assignment.acknowledged_by,
        "acknowledgementDeadline": assignment.acknowledgement_deadline,
    })


@router.post("/{complaint_id}/reassign", response_model=ApiResponse[AssignmentOut])
def reassign(complaint_id: int, payload: ReassignRequest, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.DEPARTMENT_HEAD, UserRole.ADMIN))):
    assignment = _latest_assignment(db, complaint_id)
    old_officer = assignment.assigned_to
    assignment.assigned_to = payload.new_officer_id
    assignment.assignment_status = AssignmentStatus.ASSIGNED
    assignment.acknowledged_at = None
    assignment.acknowledged_by = None
    assignment.acknowledgement_deadline = datetime.utcnow() + timedelta(hours=get_setting_float(db, "ACKNOWLEDGEMENT_DEADLINE_HOURS"))
    db.commit()
    db.refresh(assignment)
    log_event(db, complaint_id, "COMPLAINT_REASSIGNED", payload.reason or f"Reassigned from officer #{old_officer} to #{payload.new_officer_id}.", user_id=current_user.id, add_status_history=True)
    notify(db, payload.new_officer_id, "ASSIGNMENT", "Complaint reassigned to you", f"Complaint #{complaint_id} has been reassigned to you.", complaint_id=complaint_id)
    return ApiResponse(data=AssignmentOut.model_validate(assignment), message="Complaint reassigned")
