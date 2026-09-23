from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationOut
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("", response_model=ApiResponse[list[NotificationOut]])
def list_notifications(unread_only: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    if unread_only:
        query = query.filter(Notification.is_read.is_(False))
    items = query.order_by(Notification.created_at.desc()).limit(100).all()
    return ApiResponse(data=[NotificationOut.model_validate(n) for n in items])


@router.post("/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Notification not found")
    note.is_read = True
    db.commit()
    return ApiResponse(message="Marked as read")
