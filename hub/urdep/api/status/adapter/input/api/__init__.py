from fastapi import APIRouter
from pydantic import BaseModel

class HealthStatus(BaseModel):
    ok: bool = True

router = APIRouter(prefix="/api/status")

@router.get("/health", response_model=HealthStatus)
async def get_health():
    return {"ok": True}

__all__ = ["router"]
