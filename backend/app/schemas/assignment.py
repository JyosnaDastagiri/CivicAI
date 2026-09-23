from datetime import datetime
from pydantic import BaseModel
from app.models.complaint_assignment import AssignmentStatus


class AssignmentOut(BaseModel):
    id: int
    complaint_id: int
    assigned_to: int
    assigned_at: datetime
    assignment_status: AssignmentStatus
    acknowledgement_deadline: datetime
    acknowledged_at: datetime | None
    acknowledged_by: int | None
    resolution_deadline: datetime | None

    class Config:
        from_attributes = True


class AcknowledgeRequest(BaseModel):
    note: str | None = None


class ReassignRequest(BaseModel):
    new_officer_id: int
    reason: str | None = None
