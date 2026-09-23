from datetime import datetime
from pydantic import BaseModel, Field
from app.models.complaint import ComplaintStatus, Severity, Priority


class LocationIn(BaseModel):
    latitude: float
    longitude: float
    address: str | None = None


class ComplaintCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    category: str
    severity: Severity = Severity.MEDIUM
    safety_risk: bool = False
    location: LocationIn
    image_url: str | None = None


class ComplaintUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    severity: Severity | None = None
    safety_risk: bool | None = None


class ComplaintOut(BaseModel):
    id: int
    citizen_id: int
    title: str
    description: str
    category: str
    severity: Severity
    safety_risk: bool
    priority: Priority | None
    priority_score: float | None
    status: ComplaintStatus
    department_id: int | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True


class StatusUpdateRequest(BaseModel):
    status: ComplaintStatus
    description: str | None = None


class AnalyzeImageRequest(BaseModel):
    image_url: str
    description: str | None = None


class GenerateComplaintRequest(BaseModel):
    citizen_description: str
    category: str
    severity: str
    safety_risk: bool
    address: str | None = None
