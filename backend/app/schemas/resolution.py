from datetime import datetime
from pydantic import BaseModel


class ResolveComplaintRequest(BaseModel):
    description: str
    evidence_url: str | None = None


class ResolutionOut(BaseModel):
    id: int
    complaint_id: int
    resolved_by: int
    description: str
    evidence_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True
