from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.services.storage_service import save_file, UnsupportedFileError

router = APIRouter(prefix="/api/uploads", tags=["uploads"])


@router.post("/image")
async def upload_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        url = save_file(content, file.filename, file.content_type)
    except UnsupportedFileError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(data={"url": url, "fileName": file.filename, "mimeType": file.content_type}, message="File uploaded")
