from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.system_setting import SystemSetting
from app.schemas.settings import SettingOut, SettingUpdate
from app.schemas.common import ApiResponse
from app.services.settings_service import ensure_default_settings, set_setting
from app.services.audit_service import log_event

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=ApiResponse[list[SettingOut]])
def list_settings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ensure_default_settings(db)
    rows = db.query(SystemSetting).order_by(SystemSetting.key).all()
    return ApiResponse(data=[SettingOut.model_validate(r) for r in rows])


@router.put("/{key}", response_model=ApiResponse[SettingOut])
def update_setting(key: str, payload: SettingUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    row = set_setting(db, key, payload.value)
    log_event(db, None, "SETTING_UPDATED", f"Setting {key} updated to {payload.value}.", user_id=current_user.id)
    return ApiResponse(data=SettingOut.model_validate(row), message="Setting updated")
