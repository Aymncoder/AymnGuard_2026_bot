# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Telegram WebApp Cryptographic Authentication Engine
محرك المصادقة والتحقق الرياضي المشفر لبيانات تيليجرام المصغرة (InitData Validation)
=============================================================================
"""

import hmac
import hashlib
import urllib.parse
import os
import json
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import jwt

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token_here")
SECRET_KEY = os.getenv("API_SECRET_KEY", "AymnGuard_Enterprise_2026_Secure_Key")
ALGORITHM = "HS256"

class TelegramAuthPayload(BaseModel):
    user_id: int | None = None
    username: str | None = None
    first_name: str | None = None

def verify_telegram_init_data(init_data: str, bot_token: str) -> tuple[bool, dict]:
    """
    التحقق الرياضي المشفر من توقيع Telegram WebApp InitData وفقاً للبروتوكول الرسمي.
    """
    try:
        parsed_url = urllib.parse.parse_qsl(init_data, keep_blank_values=True)
        data_dict = dict(parsed_url)
        
        if "hash" not in data_dict:
            return False, {}
            
        received_hash = data_dict.pop("hash")
        
        # ترتيب المفاتيح أبجدياً لإنشاء سلسلة التحقق (Data Check String)
        sorted_keys = sorted(data_dict.keys())
        data_check_string = "\n".join([f"{key}={data_dict[key]}" for key in sorted_keys])
        
        # حساب المفتاح السري باستخدام HMAC-SHA256 مع بادئة "WebAppData"
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        
        # حساب التوقيع المقارن
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        # مقارنة التوقيعين بأمان تام لمنع هجمات توقيت التنفيذ (Timing Attacks)
        if hmac.compare_digest(calculated_hash, received_hash):
            return True, data_dict
        return False, {}
    except Exception:
        return False, {}

@router.post("/telegram/verify")
async def telegram_auth_endpoint(payload: TelegramAuthPayload, authorization: str = Header(...)):
    """
    نقطة النهاية السيادية لاستلام بيانات Telegram Mini App والتحقق منها ثم إصدار JWT Token.
    """
    try:
        if not authorization.startswith("tma "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="صيغة ترخيص الوصول غير صالحة."
            )
            
        init_data_raw = authorization.split(" ")[1]
        
        # تنفيذ التحقق الكريبتوغرافي الرياضي واستخراج البيانات الموثوقة
        is_valid, secure_data = verify_telegram_init_data(init_data_raw, BOT_TOKEN)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="فشل التحقق الرياضي المشفر لتوقيع تيليجرام. البيانات غير موثوقة!"
            )
        
        # [إضافة أمنية حرجة]: التحقق من وقت الإصدار لمنع هجمات إعادة التشغيل (Replay Attacks)
        auth_date_str = secure_data.get("auth_date")
        if not auth_date_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="حقل تاريخ المصادقة (auth_date) مفقود من البيانات."
            )
            
        try:
            auth_date = int(auth_date_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="قيمة تاريخ المصادقة غير صالحة."
            )
            
        current_timestamp = int(datetime.now(timezone.utc).timestamp())
        max_age_seconds = 86400  # السماح بصلاحية البيانات لمدة 24 ساعة كحد أقصى (يمكن تقليلها)
        
        if current_timestamp - auth_date > max_age_seconds:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="انتهت صلاحية بيانات المصادقة (Auth data expired). يرجى إعادة تشغيل التطبيق."
            )

        # استخراج بيانات المستخدم من التوقيع المشفر وليس من جسم الطلب
        user_data_str = secure_data.get("user", "{}")
        secure_user = json.loads(user_data_str)
        
        secure_user_id = secure_user.get("id")
        secure_username = secure_user.get("username", payload.username) 
        
        if not secure_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="لم يتم العثور على معرف المستخدم داخل البيانات المشفرة."
            )

        # إصدار رمز الدخول السيادي (JWT Token) للمستخدم الموثق
        token_expires = timedelta(hours=12)
        expire = datetime.now(timezone.utc) + token_expires
        
        jwt_payload = {
            "sub": str(secure_user_id),
            "username": secure_username,
            "exp": expire
        }
        
        access_token = jwt.encode(jwt_payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "status": "success",
            "message": "تم التحقق الأمني الكريبتوغرافي وإصدار الترخيص بنجاح.",
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ داخلي في معالجة المصادقة: {str(e)}"
        )
