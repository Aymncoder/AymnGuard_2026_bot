import time
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from telebot.types import Update
import telebot

from config import settings
from database.db import redis_client, mongo_db
from middlewares.throttling import rate_limiter_middleware
from services.queue_manager import MessageQueueManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | %(message)s"
)
logger = logging.getLogger("AymnGuardEnterprise")

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, threaded=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 جاري إطلاق خادم AymnGuard Enterprise...")
    try:
        bot.remove_webhook()
        await asyncio.sleep(1)
        bot.set_webhook(url=settings.WEBHOOK_URL, secret_token=settings.TELEGRAM_SECRET_TOKEN)
        logger.info(f"✅ تم ربط الـ Webhook بنجاح: {settings.WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ خطأ في إعداد الـ Webhook: {e}")
    yield
    logger.warning("🛑 يتم إيقاف تشغيل النظام...")
    bot.remove_webhook()

app = FastAPI(title="AymnGuard Ultimate Enterprise Server", version="2026.5.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limiter_middleware)

@app.get("/", response_class=PlainTextResponse)
async def root():
    return "AymnGuard Enterprise Ecosystem is Active & Secure!"

@app.api_route("/webhook", methods=["GET", "POST"])
async def telegram_webhook(request: Request):
    """استقبال الـ Webhook بأمان ودفع التحديث لطابور Redis للمعالجة الفورية العالية"""
    if request.method == "GET":
        return PlainTextResponse("Webhook Active!")
    
    try:
        # التحقق الأمني من الـ Secret Token الخاص بتيليجرام
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != settings.TELEGRAM_SECRET_TOKEN:
            return Response(status_code=403, content="Forbidden")
        
        # استلام التحديث ودفع مباشرة إلى طابور Redis لضمان السرعة القصوى وعدم الضغط
        data = await request.json()
        success = MessageQueueManager.push_to_queue("telegram_updates_queue", data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Queue insertion failed")
            
        return JSONResponse(content={"status": "queued"}, status_code=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return Response(status_code=500, content="Internal Error")

app.mount("/app", StaticFiles(directory="www", html=True), name="static_www")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=settings.PORT, reload=False)
