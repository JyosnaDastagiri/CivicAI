from datetime import datetime
from pydantic import BaseModel


class SettingOut(BaseModel):
    key: str
    value: str
    description: str | None
    updated_at: datetime

    class Config:
        from_attributes = True


class SettingUpdate(BaseModel):
    value: str
