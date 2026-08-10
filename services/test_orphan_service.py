# services/test_orphan_service.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def get_status():
    return {"status": "orphan_service_online", "message": "waiting_to_be_integrated"}
