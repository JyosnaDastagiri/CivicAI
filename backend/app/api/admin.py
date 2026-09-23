"""Admin-only user & department management."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.department import Department
from app.schemas.user import UserCreateByAdmin, UserUpdate
from app.schemas.department import DepartmentCreate, DepartmentOut
from app.schemas.auth import UserOut
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=ApiResponse[list[UserOut]])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return ApiResponse(data=[UserOut.model_validate(u) for u in users])


@router.post("/users", response_model=ApiResponse[UserOut])
def create_user(payload: UserCreateByAdmin, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(name=payload.name, email=payload.email, password_hash=hash_password(payload.password), role=payload.role, department_id=payload.department_id, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return ApiResponse(data=UserOut.model_validate(user), message="User created")


@router.put("/users/{user_id}", response_model=ApiResponse[UserOut])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return ApiResponse(data=UserOut.model_validate(user), message="User updated")


@router.get("/departments", response_model=ApiResponse[list[DepartmentOut]])
def list_departments(db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.DEPARTMENT_HEAD, UserRole.OFFICER, UserRole.CITIZEN))):
    depts = db.query(Department).order_by(Department.name).all()
    return ApiResponse(data=[DepartmentOut.model_validate(d) for d in depts])


@router.post("/departments", response_model=ApiResponse[DepartmentOut])
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles(UserRole.ADMIN))):
    if db.query(Department).filter(Department.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Department already exists")
    dept = Department(name=payload.name, description=payload.description)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return ApiResponse(data=DepartmentOut.model_validate(dept), message="Department created")
