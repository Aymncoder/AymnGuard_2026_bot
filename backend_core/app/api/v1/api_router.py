from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/health", summary="فحص سلامة النظام والروترات الفرعية")
async def health_check():
    return {
        "status": "healthy",
        "module": "AymnGuard API v1 Hub",
        "operational_mode": "Secure"
    }
