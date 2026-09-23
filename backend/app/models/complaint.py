import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ComplaintStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    AI_ANALYZED = "AI_ANALYZED"
    ASSIGNED = "ASSIGNED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    ESCALATED = "ESCALATED"
    REJECTED = "REJECTED"


class Severity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Priority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    citizen_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[Severity] = mapped_column(SAEnum(Severity), default=Severity.MEDIUM)
    safety_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[Priority | None] = mapped_column(SAEnum(Priority), nullable=True)
    priority_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[ComplaintStatus] = mapped_column(SAEnum(ComplaintStatus), default=ComplaintStatus.SUBMITTED)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    citizen: Mapped["User"] = relationship("User", foreign_keys=[citizen_id])
    department: Mapped["Department"] = relationship("Department", foreign_keys=[department_id])
    images: Mapped[list["ComplaintImage"]] = relationship("ComplaintImage", back_populates="complaint", cascade="all, delete-orphan")
    analysis: Mapped[list["ComplaintAnalysis"]] = relationship("ComplaintAnalysis", back_populates="complaint", cascade="all, delete-orphan")
    location: Mapped["ComplaintLocation"] = relationship("ComplaintLocation", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    priority_analysis: Mapped["PriorityAnalysis"] = relationship("PriorityAnalysis", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    assignments: Mapped[list["ComplaintAssignment"]] = relationship("ComplaintAssignment", back_populates="complaint", cascade="all, delete-orphan")
    status_history: Mapped[list["StatusHistory"]] = relationship("StatusHistory", back_populates="complaint", cascade="all, delete-orphan")
    escalations: Mapped[list["Escalation"]] = relationship("Escalation", back_populates="complaint", cascade="all, delete-orphan")
    resolution: Mapped["Resolution"] = relationship("Resolution", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="complaint", cascade="all, delete-orphan")
