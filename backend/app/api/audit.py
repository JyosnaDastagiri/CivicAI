from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.models.user import User, UserRole
from app.models.audit_log import AuditLog
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/audit-logs", tags=["audit"])


@router.get("")
def list_audit_logs(complaint_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD, UserRole.OFFICER))):
    query = db.query(AuditLog)
    if complaint_id:
        query = query.filter(AuditLog.complaint_id == complaint_id)
    items = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    return ApiResponse(data=[{c.name: getattr(i, c.name) for c in i.__table__.columns} for i in items])
