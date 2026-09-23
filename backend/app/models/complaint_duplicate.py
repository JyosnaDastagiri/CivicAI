from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ComplaintDuplicate(Base):
    __tablename__ = "complaint_duplicates"

    id: Mapped[int] = mapped_column(primary_key=True)
    complaint_id: Mapped[int] = mapped_column(ForeignKey("complaints.id"), nullable=False)
    similar_complaint_id: Mapped[int] = mapped_column(ForeignKey("complaints.id"), nullable=False)
    text_similarity: Mapped[float] = mapped_column(Float, nullable=False)
    distance_meters: Mapped[float] = mapped_column(Float, nullable=False)
    category_match: Mapped[bool] = mapped_column(Boolean, default=False)
    duplicate_score: Mapped[float] = mapped_column(Float, nullable=False)
    is_potential_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
