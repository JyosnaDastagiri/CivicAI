"""
Seed script for CivicAI demo data (Requirement #37, #38).

Creates:
  - 7 departments
  - 1 admin, 3 department heads, 5 officers, 5 citizens
  - ~25 realistic complaints covering every demo scenario required
    (normal, duplicate, high priority, critical safety, acknowledged,
    unacknowledged, escalated, resolved, resolution-overdue).

Run with:  python seed.py
"""
import random
from datetime import datetime, timedelta

from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.department import Department
from app.models.complaint import Complaint, ComplaintStatus, Severity
from app.models.complaint_location import ComplaintLocation
from app.models.complaint_analysis import ComplaintAnalysis
from app.models.priority_analysis import PriorityAnalysis
from app.models.complaint_assignment import ComplaintAssignment, AssignmentStatus
from app.models.complaint_duplicate import ComplaintDuplicate
from app.models.escalation import Escalation, EscalationStatus
from app.models.resolution import Resolution
from app.models.status_history import StatusHistory
from app.models.notification import Notification
from app.services.settings_service import ensure_default_settings
from app.services.priority_service import calculate_priority
from app.services.assignment_service import CATEGORY_TO_DEPARTMENT, DEFAULT_DEPARTMENT

DEMO_PASSWORD = "Demo@123"

DEPARTMENTS = [
    "Roads & Infrastructure", "Sanitation", "Electrical", "Water Supply",
    "Drainage", "Parks & Emergency Services", "General Civic Services",
]

# Hyderabad-area coordinates, spread out for realistic map demo
BASE_LAT, BASE_LON = 17.3850, 78.4867

SAMPLE_COMPLAINTS = [
    dict(title="Large pothole near college entrance", description="There is a very big pothole near the college entrance and bikes are almost falling into it.", category="Pothole", severity=Severity.HIGH, safety_risk=True),
    dict(title="Pothole on main road (duplicate demo)", description="Big pothole close to the college gate causing two-wheelers to swerve.", category="Pothole", severity=Severity.HIGH, safety_risk=True),
    dict(title="Garbage pile near market", description="Garbage has been accumulating near the vegetable market for a week.", category="Garbage", severity=Severity.MEDIUM, safety_risk=False),
    dict(title="Broken streetlight on 2nd cross", description="Streetlight has not worked for 10 days, area is dark at night.", category="Broken Streetlight", severity=Severity.MEDIUM, safety_risk=False),
    dict(title="Water pipeline leaking heavily", description="Major water leakage flooding the street outside house no. 12.", category="Water Leakage", severity=Severity.HIGH, safety_risk=True),
    dict(title="Drainage overflow near bus stop", description="Drainage is overflowing and causing bad smell and mosquito breeding.", category="Drainage", severity=Severity.MEDIUM, safety_risk=False),
    dict(title="Fallen tree blocking road", description="A large tree fell after the storm and is blocking half the road.", category="Fallen Tree", severity=Severity.CRITICAL, safety_risk=True),
    dict(title="Damaged road sign at junction", description="The stop sign at the junction is bent and hard to see.", category="Damaged Road Sign", severity=Severity.LOW, safety_risk=False),
    dict(title="Deep pothole causing accidents", description="Very deep pothole on the highway service road, two accidents already happened.", category="Pothole", severity=Severity.CRITICAL, safety_risk=True),
    dict(title="Overflowing garbage bin", description="Public garbage bin has been overflowing for days near the park entrance.", category="Garbage", severity=Severity.LOW, safety_risk=False),
    dict(title="Exposed electrical wire on pole", description="A live wire is hanging low from the electric pole, very dangerous.", category="Broken Streetlight", severity=Severity.CRITICAL, safety_risk=True),
    dict(title="Cracked road surface near school", description="Road surface has multiple cracks near the school zone.", category="Road Damage", severity=Severity.HIGH, safety_risk=True),
    dict(title="Clogged stormwater drain", description="Stormwater drain is clogged with debris causing waterlogging after rain.", category="Drainage", severity=Severity.HIGH, safety_risk=False),
    dict(title="Leaking water tank overflow", description="Community water tank has been overflowing and wasting water for two days.", category="Water Leakage", severity=Severity.MEDIUM, safety_risk=False),
    dict(title="Small pothole developing on lane", description="Small pothole forming on the residential lane, will worsen with rain.", category="Pothole", severity=Severity.LOW, safety_risk=False),
    dict(title="Uncollected garbage for a week", description="Garbage collection has been missed for over a week in this street.", category="Garbage", severity=Severity.MEDIUM, safety_risk=False),
    dict(title="Multiple streetlights not working", description="Three consecutive streetlights are non-functional on the main avenue.", category="Broken Streetlight", severity=Severity.MEDIUM, safety_risk=True),
    dict(title="Broken footpath tiles", description="Footpath tiles are broken and loose, elderly people are tripping.", category="Road Damage", severity=Severity.MEDIUM, safety_risk=True),
    dict(title="Leaning tree threatens houses", description="A large tree is leaning dangerously towards nearby houses.", category="Fallen Tree", severity=Severity.HIGH, safety_risk=True),
    dict(title="Sewage overflow onto street", description="Sewage line has burst and is overflowing onto the main street.", category="Drainage", severity=Severity.CRITICAL, safety_risk=True),
    dict(title="Missing manhole cover", description="Manhole cover missing near the crossing, very risky for pedestrians at night.", category="Drainage", severity=Severity.CRITICAL, safety_risk=True),
    dict(title="Faded pedestrian crossing sign", description="Pedestrian crossing sign has faded and is barely visible.", category="Damaged Road Sign", severity=Severity.LOW, safety_risk=False),
    dict(title="General civic issue - unclear category", description="There seems to be an unspecified civic maintenance issue near the park.", category="General Civic Issue", severity=Severity.LOW, safety_risk=False),
    dict(title="Water leakage under road", description="Water is seeping up through cracks in the road, suspected underground pipe leak.", category="Water Leakage", severity=Severity.HIGH, safety_risk=True),
    dict(title="Streetlight flickering constantly", description="Streetlight near the park keeps flickering all night.", category="Broken Streetlight", severity=Severity.LOW, safety_risk=False),
]


def jittered_location(i: int):
    return BASE_LAT + random.uniform(-0.03, 0.03), BASE_LON + random.uniform(-0.03, 0.03)


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_default_settings(db)

        if db.query(Department).count() == 0:
            for name in DEPARTMENTS:
                db.add(Department(name=name, description=f"{name} department handling related civic complaints."))
            db.commit()
        depts = {d.name: d for d in db.query(Department).all()}

        if db.query(User).filter(User.role == UserRole.ADMIN).count() == 0:
            admin = User(name="System Admin", email="admin@civicai.demo", password_hash=hash_password(DEMO_PASSWORD), role=UserRole.ADMIN, is_active=True)
            db.add(admin)

            head_defs = [
                ("Roads Head", "roads.head@civicai.demo", "Roads & Infrastructure"),
                ("Sanitation Head", "sanitation.head@civicai.demo", "Sanitation"),
                ("Electrical Head", "electrical.head@civicai.demo", "Electrical"),
            ]
            for name, email, dept_name in head_defs:
                db.add(User(name=name, email=email, password_hash=hash_password(DEMO_PASSWORD), role=UserRole.DEPARTMENT_HEAD, department_id=depts[dept_name].id, is_active=True))

            officer_defs = [
                ("Roads Officer", "roads.officer@civicai.demo", "Roads & Infrastructure"),
                ("Sanitation Officer", "sanitation.officer@civicai.demo", "Sanitation"),
                ("Electrical Officer", "electrical.officer@civicai.demo", "Electrical"),
                ("Water Officer", "water.officer@civicai.demo", "Water Supply"),
                ("Drainage Officer", "drainage.officer@civicai.demo", "Drainage"),
            ]
            for name, email, dept_name in officer_defs:
                db.add(User(name=name, email=email, password_hash=hash_password(DEMO_PASSWORD), role=UserRole.OFFICER, department_id=depts[dept_name].id, is_active=True))

            citizen_defs = [
                ("Demo Citizen", "citizen@civicai.demo"),
                ("Asha Rao", "asha.rao@civicai.demo"),
                ("Vikram Singh", "vikram.singh@civicai.demo"),
                ("Priya Nair", "priya.nair@civicai.demo"),
                ("Rahul Verma", "rahul.verma@civicai.demo"),
            ]
            for name, email in citizen_defs:
                db.add(User(name=name, email=email, password_hash=hash_password(DEMO_PASSWORD), role=UserRole.CITIZEN, is_active=True))

            db.commit()

        citizens = db.query(User).filter(User.role == UserRole.CITIZEN).all()
        officers = db.query(User).filter(User.role == UserRole.OFFICER).all()
        heads = db.query(User).filter(User.role == UserRole.DEPARTMENT_HEAD).all()

        if db.query(Complaint).count() > 0:
            print("Complaints already seeded. Skipping complaint seeding.")
            return

        now = datetime.utcnow()

        for idx, sample in enumerate(SAMPLE_COMPLAINTS):
            citizen = random.choice(citizens)
            created_at = now - timedelta(days=random.randint(0, 20), hours=random.randint(0, 23))

            complaint = Complaint(
                citizen_id=citizen.id, title=sample["title"], description=sample["description"],
                category=sample["category"], severity=sample["severity"], safety_risk=sample["safety_risk"],
                status=ComplaintStatus.AI_ANALYZED, created_at=created_at, updated_at=created_at,
            )
            db.add(complaint)
            db.commit()
            db.refresh(complaint)

            lat, lon = jittered_location(idx)
            db.add(ComplaintLocation(complaint_id=complaint.id, latitude=lat, longitude=lon, address=f"Sector {idx + 1}, Demo City"))
            db.add(ComplaintAnalysis(complaint_id=complaint.id, category=sample["category"], severity=sample["severity"].value, safety_risk=sample["safety_risk"], confidence=0.85, ai_provider="demo", raw_result=None))
            db.add(StatusHistory(complaint_id=complaint.id, status="COMPLAINT_CREATED", description="Citizen submitted a new complaint.", created_at=created_at))
            db.commit()

            priority_result = calculate_priority(db, complaint)
            db.add(PriorityAnalysis(
                complaint_id=complaint.id, severity_score=priority_result["severityScore"], safety_score=priority_result["safetyScore"],
                location_score=priority_result["locationScore"], recurrence_score=priority_result["recurrenceScore"],
                urgency_score=priority_result["urgencyScore"], final_score=priority_result["finalScore"],
                priority=priority_result["priority"], explanation=priority_result["explanation"],
            ))
            complaint.priority = priority_result["priority"]
            complaint.priority_score = priority_result["finalScore"]
            db.commit()

            dept_name = CATEGORY_TO_DEPARTMENT.get(sample["category"], DEFAULT_DEPARTMENT)
            department = depts.get(dept_name, depts[DEFAULT_DEPARTMENT])
            complaint.department_id = department.id
            complaint.status = ComplaintStatus.ASSIGNED

            dept_officers = [o for o in officers if o.department_id == department.id] or officers
            officer = random.choice(dept_officers)
            ack_deadline = created_at + timedelta(hours=6)

            scenario = idx % 6  # cycle through demo scenarios
            assignment = ComplaintAssignment(
                complaint_id=complaint.id, assigned_to=officer.id, assigned_at=created_at,
                assignment_status=AssignmentStatus.ASSIGNED, acknowledgement_deadline=ack_deadline,
            )

            if scenario in (0, 1):  # acknowledged, in progress
                assignment.acknowledged_at = created_at + timedelta(hours=1)
                assignment.acknowledged_by = officer.id
                assignment.assignment_status = AssignmentStatus.IN_PROGRESS
                assignment.resolution_deadline = created_at + timedelta(hours=24)
                complaint.status = ComplaintStatus.IN_PROGRESS
            elif scenario == 2:  # resolved
                assignment.acknowledged_at = created_at + timedelta(hours=1)
                assignment.acknowledged_by = officer.id
                assignment.assignment_status = AssignmentStatus.RESOLVED
                assignment.resolution_deadline = created_at + timedelta(hours=24)
                complaint.status = ComplaintStatus.RESOLVED
                complaint.resolved_at = created_at + timedelta(hours=20)
                db.add(Resolution(complaint_id=complaint.id, resolved_by=officer.id, description="Issue inspected and repaired by the field team.", evidence_url=None, created_at=complaint.resolved_at))
            elif scenario == 3:  # unacknowledged, overdue -> will be escalated by live scheduler
                assignment.acknowledgement_deadline = now - timedelta(hours=2)  # already overdue for demo
            elif scenario == 4:  # already escalated (acknowledgement)
                assignment.assignment_status = AssignmentStatus.ESCALATED
                complaint.status = ComplaintStatus.ESCALATED
                head = next((h for h in heads if h.department_id == department.id), None)
                db.add(Escalation(
                    complaint_id=complaint.id, from_user_id=officer.id, to_user_id=head.id if head else None,
                    reason="Officer failed to acknowledge complaint within configured deadline.",
                    escalated_at=created_at + timedelta(hours=7), previous_deadline=ack_deadline,
                    new_deadline=created_at + timedelta(hours=13), status=EscalationStatus.OPEN,
                ))
            else:  # resolution-overdue (acknowledged, in progress, deadline passed)
                assignment.acknowledged_at = created_at + timedelta(hours=1)
                assignment.acknowledged_by = officer.id
                assignment.assignment_status = AssignmentStatus.IN_PROGRESS
                assignment.resolution_deadline = now - timedelta(hours=5)  # overdue for demo
                complaint.status = ComplaintStatus.IN_PROGRESS

            db.add(assignment)
            db.commit()

            db.add(Notification(user_id=citizen.id, complaint_id=complaint.id, type="STATUS", title="Complaint submitted", message=f"Your complaint '{complaint.title}' was submitted.", created_at=created_at))
            db.commit()

        # Run duplicate detection across the seeded data so the "duplicate" demo pair is linked
        from app.services.duplicate_service import find_duplicates
        for complaint in db.query(Complaint).all():
            find_duplicates(db, complaint, lookback_days=60)

        print("Seed data created successfully.")
        print(f"Departments: {db.query(Department).count()}")
        print(f"Users: {db.query(User).count()}")
        print(f"Complaints: {db.query(Complaint).count()}")
        print("\nDemo password for all accounts:", DEMO_PASSWORD)

    finally:
        db.close()


if __name__ == "__main__":
    run()
