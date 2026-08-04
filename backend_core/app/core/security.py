import time
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

# مفتاح السيادة الموثوق (يمكن ربطه بمتغير بيئة لاحقاً)
SOVEREIGN_MASTER_KEY = "aymnguard-sovereign-master-key-2026"

def verify_sovereign_key(key: str) -> bool:
    """التحقق من صحة المفتاح السيادي للمالك"""
    return key == SOVEREIGN_MASTER_KEY

async def rate_limiter_middleware(request: Request, call_next):
    """وسيط مؤسسي للتحكم بمعدل الطلبات وحماية الخادم من الهجمات العشوائية"""
    # يمكن إضافة منطق التتبع والحد من الطلبات هنا مستقبلاً
    start_time = time.time()
    response = await call_next(request)
    return response
