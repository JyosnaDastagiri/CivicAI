from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    description: str | None = None


class DepartmentOut(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool

    class Config:
        from_attributes = True
