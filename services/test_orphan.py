from fastapi import APIRouter

router = APIRouter()

@router.get("/test-status")
async def test_status():
    return {"status": "success", "message": "This is an orphan test file."}
