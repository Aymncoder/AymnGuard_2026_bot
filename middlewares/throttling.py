cat << 'EOF' > middlewares/throttling.py
import time
from fastapi import Request, HTTPException, status
import logging

logger = logging.getLogger("AymnGuardEnterprise")

async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    path = request.url.path
    if "/api/" in path:
        logger.debug(f"Processing API request from {client_ip} to {path}")
    response = await call_next(request)
    return response
EOF

