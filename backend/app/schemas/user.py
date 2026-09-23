from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserCreateByAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    department_id: int | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    role: UserRole | None = None
    department_id: int | None = None
    is_active: bool | None = None
