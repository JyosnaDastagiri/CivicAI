"""
Core complaint lifecycle endpoints: create (full AI + duplicate + priority +
assignment pipeline), list, get, update, delete, status change.
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintStatus
from app.models.complaint_location import ComplaintLocation as Location
from app.models.complaint_analysis import ComplaintAnalysis
from app.models.priority_analysis import PriorityAnalysis
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.models.complaint_duplicate import ComplaintDuplicate
from app.models.resolution import Resolution
from app.models.escalation import Escalation
from app.models.status_history import StatusHistory
from app.models.audit_log import AuditLog
from app.models.department import Department
from app.schemas.complaint import ComplaintCreate, ComplaintOut, ComplaintUpdate, StatusUpdateRequest
from app.schemas.common import ApiResponse
from app.services.duplicate_service import find_duplicates
from app.services.priority_service import calculate_priority
from app.services.assignment_service import assign_complaint
from app.services.audit_service import log_event
from app.services.notification_service import notify
from app.services.settings_service import get_setting_float, ensure_default_settings

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

RESOLUTION_HOURS_BY_PRIORITY = {
    "CRITICAL": "CRITICAL_RESOLUTION_HOURS",
    "HIGH": "HIGH_RESOLUTION_HOURS",
    "MEDIUM": "MEDIUM_RESOLUTION_HOURS",
    "LOW": "LOW_RESOLUTION_HOURS",
}


def _complaint_or_404(db: Session, complaint_id: int) -> Complaint:
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


def _authorize_view(complaint: Complaint, user: User):
    if user.role == UserRole.CITIZEN and complaint.citizen_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this complaint")
    if user.role == UserRole.OFFICER:
        assigned = any(a.assigned_to == user.id for a in complaint.assignments)
        if not assigned:
            raise HTTPException(status_code=403, detail="Not authorized to view this complaint")
    if user.role == UserRole.DEPARTMENT_HEAD and complaint.department_id != user.department_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this complaint")


@router.post("", response_model=ApiResponse[ComplaintOut])
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.CITIZEN, UserRole.ADMIN)),
):
    ensure_default_settings(db)

    complaint = Complaint(
        citizen_id=current_user.id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        severity=payload.severity,
        safety_risk=payload.safety_risk,
        status=ComplaintStatus.SUBMITTED,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    log_event(db, complaint.id, "COMPLAINT_CREATED", "Citizen submitted a new complaint.", user_id=current_user.id, add_status_history=True)

    loc = Location(complaint_id=complaint.id, latitude=payload.location.latitude, longitude=payload.location.longitude, address=payload.location.address)
    db.add(loc)

    if payload.image_url:
        from app.models.complaint_image import ComplaintImage
        db.add(ComplaintImage(complaint_id=complaint.id, storage_url=payload.image_url, file_name="upload", mime_type="image/jpeg"))
        log_event(db, complaint.id, "IMAGE_UPLOADED", "Citizen uploaded an image for the complaint.", user_id=current_user.id)

    db.add(ComplaintAnalysis(
        complaint_id=complaint.id, category=payload.category, severity=payload.severity.value,
        safety_risk=payload.safety_risk, confidence=0.9, ai_provider="client-provided", raw_result=None,
    ))
    complaint.status = ComplaintStatus.AI_ANALYZED
    db.commit()
    log_event(db, complaint.id, "AI_ANALYSIS_COMPLETED", "AI analysis result stored with the complaint.", add_status_history=True)

    # Duplicate detection
    find_duplicates(db, complaint)
    log_event(db, complaint.id, "DUPLICATE_CHECK_COMPLETED", "TF-IDF + GPS duplicate check completed.", add_status_history=True)

    # Priority scoring
    priority_result = calculate_priority(db, complaint)
    db.add(PriorityAnalysis(
        complaint_id=complaint.id,
        severity_score=priority_result["severityScore"], safety_score=priority_result["safetyScore"],
        location_score=priority_result["locationScore"], recurrence_score=priority_result["recurrenceScore"],
        urgency_score=priority_result["urgencyScore"], final_score=priority_result["finalScore"],
        priority=priority_result["priority"], explanation=priority_result["explanation"],
    ))
    complaint.priority = priority_result["priority"]
    complaint.priority_score = priority_result["finalScore"]
    db.commit()
    log_event(db, complaint.id, "PRIORITY_CALCULATED", f"Priority calculated as {priority_result['priority']}.", add_status_history=True)

    # Department assignment
    assignment = assign_complaint(db, complaint)
    if assignment:
        complaint.status = ComplaintStatus.ASSIGNED
        resolution_hours_key = RESOLUTION_HOURS_BY_PRIORITY.get(complaint.priority, "MEDIUM_RESOLUTION_HOURS")
        assignment.resolution_deadline = assignment.assigned_at + timedelta(hours=get_setting_float(db, resolution_hours_key))
        db.commit()
        dept = db.query(Department).filter(Department.id == complaint.department_id).first()
        log_event(db, complaint.id, "DEPARTMENT_ASSIGNED", f"Assigned to {dept.name if dept else 'a department'}.", add_status_history=True)
        notify(db, assignment.assigned_to, "ASSIGNMENT", "New complaint assigned to you", f"Complaint #{complaint.id} ({complaint.title}) has been assigned to you.", complaint_id=complaint.id)
        log_event(db, complaint.id, "OFFICER_NOTIFIED", "Assigned officer notified.")
    else:
        log_event(db, complaint.id, "DEPARTMENT_ASSIGNED", "No available officer found; complaint pending manual assignment.")

    notify(db, current_user.id, "STATUS", "Complaint submitted", f"Your complaint #{complaint.id} was submitted and analyzed.", complaint_id=complaint.id)

    db.refresh(complaint)
    return ApiResponse(data=ComplaintOut.model_validate(complaint), message="Complaint created successfully")


@router.get("", response_model=ApiResponse[list[ComplaintOut]])
def list_complaints(
    status_filter: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Complaint)
    if current_user.role == UserRole.CITIZEN:
        query = query.filter(Complaint.citizen_id == current_user.id)
    elif current_user.role == UserRole.OFFICER:
        assigned_ids = [a.complaint_id for a in db.query(ComplaintAssignment).filter(ComplaintAssignment.assigned_to == current_user.id).all()]
        query = query.filter(Complaint.id.in_(assigned_ids or [-1]))
    elif current_user.role == UserRole.DEPARTMENT_HEAD:
        query = query.filter(Complaint.department_id == current_user.department_id)
    # ADMIN sees all

    if status_filter:
        query = query.filter(Complaint.status == status_filter)

    items = query.order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()
    return ApiResponse(data=[ComplaintOut.model_validate(c) for c in items])


@router.get("/{complaint_id}")
def get_complaint(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    complaint = _complaint_or_404(db, complaint_id)
    _authorize_view(complaint, current_user)

    location = db.query(Location).filter(Location.complaint_id == complaint_id).first()
    analysis = db.query(ComplaintAnalysis).filter(ComplaintAnalysis.complaint_id == complaint_id).all()
    priority_analysis = db.query(PriorityAnalysis).filter(PriorityAnalysis.complaint_id == complaint_id).first()
    assignment = db.query(ComplaintAssignment).filter(ComplaintAssignment.complaint_id == complaint_id).order_by(ComplaintAssignment.id.desc()).first()
    duplicates = db.query(ComplaintDuplicate).filter(ComplaintDuplicate.complaint_id == complaint_id, ComplaintDuplicate.is_potential_duplicate.is_(True)).all()
    escalations = db.query(Escalation).filter(Escalation.complaint_id == complaint_id).all()
    resolution = db.query(Resolution).filter(Resolution.complaint_id == complaint_id).first()
    timeline = db.query(StatusHistory).filter(StatusHistory.complaint_id == complaint_id).order_by(StatusHistory.created_at.asc()).all()
    images = complaint.images

    def serialize(obj):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns} if obj else None

    return ApiResponse(data={
        "complaint": ComplaintOut.model_validate(complaint).model_dump(mode="json"),
        "location": serialize(location),
        "images": [serialize(i) for i in images],
        "analysis": [serialize(a) for a in analysis],
        "priorityAnalysis": serialize(priority_analysis),
        "assignment": serialize(assignment),
        "duplicates": [serialize(d) for d in duplicates],
        "escalations": [serialize(e) for e in escalations],
        "resolution": serialize(resolution),
        "timeline": [serialize(t) for t in timeline],
    })


@router.put("/{complaint_id}", response_model=ApiResponse[ComplaintOut])
def update_complaint(complaint_id: int, payload: ComplaintUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    complaint = _complaint_or_404(db, complaint_id)
    if current_user.role == UserRole.CITIZEN and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(complaint, field, value)
    db.commit()
    db.refresh(complaint)
    log_event(db, complaint.id, "COMPLAINT_EDITED", "Complaint details edited.", user_id=current_user.id)
    return ApiResponse(data=ComplaintOut.model_validate(complaint), message="Complaint updated")


@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.CITIZEN))):
    complaint = _complaint_or_404(db, complaint_id)
    if current_user.role == UserRole.CITIZEN and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(complaint)
    db.commit()
    return ApiResponse(message="Complaint deleted")


@router.post("/{complaint_id}/status")
def change_status(complaint_id: int, payload: StatusUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.OFFICER, UserRole.DEPARTMENT_HEAD, UserRole.ADMIN))):
    complaint = _complaint_or_404(db, complaint_id)
    _authorize_view(complaint, current_user)

    complaint.status = payload.status
    if payload.status == ComplaintStatus.IN_PROGRESS:
        assignment = db.query(ComplaintAssignment).filter(ComplaintAssignment.complaint_id == complaint_id).order_by(ComplaintAssignment.id.desc()).first()
        if assignment:
            assignment.assignment_status = AssignmentStatus.IN_PROGRESS
    db.commit()

    log_event(db, complaint.id, f"STATUS_CHANGED_{payload.status.value}", payload.description or f"Status changed to {payload.status.value}.", user_id=current_user.id, add_status_history=True)
    notify(db, complaint.citizen_id, "STATUS", "Complaint status updated", f"Your complaint #{complaint.id} status changed to {payload.status.value}.", complaint_id=complaint.id)
    db.refresh(complaint)
    return ApiResponse(data=ComplaintOut.model_validate(complaint), message="Status updated")


@router.get("/{complaint_id}/duplicates")
def get_duplicates(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    complaint = _complaint_or_404(db, complaint_id)
    _authorize_view(complaint, current_user)
    dups = db.query(ComplaintDuplicate).filter(ComplaintDuplicate.complaint_id == complaint_id).all()
    return ApiResponse(data=[{c.name: getattr(d, c.name) for c in d.__table__.columns} for d in dups])


@router.post("/{complaint_id}/duplicate-check")
def rerun_duplicate_check(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    complaint = _complaint_or_404(db, complaint_id)
    _authorize_view(complaint, current_user)
    results = find_duplicates(db, complaint)
    return ApiResponse(data={"potentialDuplicates": sum(1 for r in results if r.is_potential_duplicate)}, message="Duplicate check completed")


@router.get("/{complaint_id}/priority")
def get_priority(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    complaint = _complaint_or_404(db, complaint_id)
    _authorize_view(complaint, current_user)
    pa = db.query(PriorityAnalysis).filter(PriorityAnalysis.complaint_id == complaint_id).first()
    if not pa:
        raise HTTPException(status_code=404, detail="Priority analysis not found")
    return ApiResponse(data={c.name: getattr(pa, c.name) for c in pa.__table__.columns})


@router.post("/{complaint_id}/priority")
def recalculate_priority(complaint_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD))):
    complaint = _complaint_or_404(db, complaint_id)
    result = calculate_priority(db, complaint)
    pa = db.query(PriorityAnalysis).filter(PriorityAnalysis.complaint_id == complaint_id).first()
    if pa:
        pa.severity_score = result["severityScore"]; pa.safety_score = result["safetyScore"]
        pa.location_score = result["locationScore"]; pa.recurrence_score = result["recurrenceScore"]
        pa.urgency_score = result["urgencyScore"]; pa.final_score = result["finalScore"]
        pa.priority = result["priority"]; pa.explanation = result["explanation"]
    complaint.priority = result["priority"]
    complaint.priority_score = result["finalScore"]
    db.commit()
    return ApiResponse(data=result, message="Priority recalculated")
