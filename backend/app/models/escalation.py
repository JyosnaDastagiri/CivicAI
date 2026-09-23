import enum
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EscalationStatus(str, enum.Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


class Escalation(Base):
    __tablename__ = "escalations"

    id: Mapped[int] = mapped_column(primary_key=True)
    complaint_id: Mapped[int] = mapped_column(ForeignKey("complaints.id"), nullable=False)
    from_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    to_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    escalated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    previous_deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    new_deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[EscalationStatus] = mapped_column(SAEnum(EscalationStatus), default=EscalationStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    complaint: Mapped["Complaint"] = relationship("Complaint", back_populates="escalations")
