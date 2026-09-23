"""Central helper for writing AuditLog + citizen-facing StatusHistory entries."""
from __future__ import annotations
import json
from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.status_history import StatusHistory


def log_event(
    db: Session,
    complaint_id: Optional[int],
    event_type: str,
    description: str,
    user_id: Optional[int] = None,
    metadata: Optional[dict] = None,
    add_status_history: bool = False,
) -> AuditLog:
    entry = AuditLog(
        complaint_id=complaint_id,
        user_id=user_id,
        event_type=event_type,
        description=description,
        event_metadata=json.dumps(metadata) if metadata else None,
    )
    db.add(entry)
    if add_status_history and complaint_id:
        db.add(
            StatusHistory(
                complaint_id=complaint_id,
                status=event_type,
                changed_by=user_id,
                description=description,
            )
        )
    db.commit()
    return entry
