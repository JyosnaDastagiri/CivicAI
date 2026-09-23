from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = ""


class ApiError(BaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None
