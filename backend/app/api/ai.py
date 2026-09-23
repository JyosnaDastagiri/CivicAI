from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.config import get_settings
from app.models.user import User
from app.schemas.complaint import AnalyzeImageRequest, GenerateComplaintRequest
from app.schemas.common import ApiResponse
from app.services.ai_service import get_ai_service

router = APIRouter(prefix="/api/ai", tags=["ai"])
settings = get_settings()


@router.post("/analyze-image")
def analyze_image(payload: AnalyzeImageRequest, current_user: User = Depends(get_current_user)):
    ai = get_ai_service()
    result = ai.analyze_image(payload.image_url, payload.description)
    result["aiMode"] = settings.AI_MODE if settings.GEMINI_API_KEY else "demo"
    return ApiResponse(data=result, message="Image analyzed")


@router.post("/generate-complaint")
def generate_complaint(payload: GenerateComplaintRequest, current_user: User = Depends(get_current_user)):
    ai = get_ai_service()
    result = ai.generate_complaint(
        payload.citizen_description, payload.category, payload.severity, payload.safety_risk, payload.address
    )
    result["aiMode"] = settings.AI_MODE if settings.GEMINI_API_KEY else "demo"
    return ApiResponse(data=result, message="Complaint generated")
