from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["ops"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": settings.gemini_model}
