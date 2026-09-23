"""
Rule-based department assignment + officer selection (Requirement #15).
No ML model is used for routing.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.user import User, UserRole
from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.services.settings_service import get_setting_float

CATEGORY_TO_DEPARTMENT = {
    "Pothole": "Roads & Infrastructure",
    "Road Damage": "Roads & Infrastructure",
    "Garbage": "Sanitation",
    "Broken Streetlight": "Electrical",
    "Water Leakage": "Water Supply",
    "Drainage": "Drainage",
    "Fallen Tree": "Parks & Emergency Services",
    "Damaged Road Sign": "Roads & Infrastructure",
}

DEFAULT_DEPARTMENT = "General Civic Services"


def resolve_department(db: Session, category: str) -> Department:
    dept_name = CATEGORY_TO_DEPARTMENT.get(category, DEFAULT_DEPARTMENT)
    dept = db.query(Department).filter(Department.name == dept_name).first()
    if not dept:
        dept = db.query(Department).filter(Department.name == DEFAULT_DEPARTMENT).first()
    return dept


def _pick_officer(db: Session, department_id: int) -> User | None:
    """Simple least-loaded round robin: officer in dept with fewest open assignments."""
    officers = (
        db.query(User)
        .filter(User.role == UserRole.OFFICER, User.department_id == department_id, User.is_active.is_(True))
        .all()
    )
    if not officers:
        return None

    def open_load(officer: User) -> int:
        return (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.assigned_to == officer.id,
                ComplaintAssignment.assignment_status.in_(
                    [AssignmentStatus.ASSIGNED, AssignmentStatus.ACKNOWLEDGED, AssignmentStatus.IN_PROGRESS]
                ),
            )
            .count()
        )

    return min(officers, key=open_load)


def assign_complaint(db: Session, complaint: Complaint) -> ComplaintAssignment | None:
    department = resolve_department(db, complaint.category)
    if not department:
        return None
    complaint.department_id = department.id

    officer = _pick_officer(db, department.id)
    if not officer:
        db.commit()
        return None

    ack_hours = get_setting_float(db, "ACKNOWLEDGEMENT_DEADLINE_HOURS")
    assignment = ComplaintAssignment(
        complaint_id=complaint.id,
        assigned_to=officer.id,
        assigned_at=datetime.utcnow(),
        assignment_status=AssignmentStatus.ASSIGNED,
        acknowledgement_deadline=datetime.utcnow() + timedelta(hours=ack_hours),
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
