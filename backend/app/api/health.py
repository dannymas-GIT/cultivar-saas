"""Health check endpoint."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """Return 200 when the service is healthy."""
    return {"status": "ok", "service": "cultivar-saas"}
