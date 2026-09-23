from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ComplaintAnalysis(Base):
    __tablename__ = "complaint_analysis"

    id: Mapped[int] = mapped_column(primary_key=True)
    complaint_id: Mapped[int] = mapped_column(ForeignKey("complaints.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    safety_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    ai_provider: Mapped[str] = mapped_column(String(40), nullable=False)
    raw_result: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    complaint: Mapped["Complaint"] = relationship("Complaint", back_populates="analysis")
