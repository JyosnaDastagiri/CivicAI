"""In-app notification helper. No SMS/email dependency required (Requirement #31)."""
from __future__ import annotations
from typing import Optional

from sqlalchemy.orm import Session

from app.models.notification import Notification


def notify(
    db: Session,
    user_id: int,
    type_: str,
    title: str,
    message: str,
    complaint_id: Optional[int] = None,
) -> Notification:
    note = Notification(
        user_id=user_id,
        complaint_id=complaint_id,
        type=type_,
        title=title,
        message=message,
    )
    db.add(note)
    db.commit()
    return note
