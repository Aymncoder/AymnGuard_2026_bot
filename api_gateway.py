# gateway/api_gateway.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# استيراد النواة والمحركات المستقلة للإمبراطورية
from core.license_manager import SovereignLicenseManager
from bots.protection.bot_engine import SovereignProtectionEngine
from bots.creative.creative_engine import SovereignCreativeStudio
from bots.search.search_engine import SovereignSearchEngine

app = FastAPI(
    title="AymnGuard Imperial Gateway",
    version="5.0.0",
    description="بوابة العمليات والخدمات السيادية الموحدة - النظام المؤسسي العالمي"
)

# --- نماذج بيانات الطلبات (Pydantic Schemas) ---
class LicenseLinkRequest(BaseModel):
    license_key: str
    chat_id: str

class ProtectionSlotRequest(BaseModel):
    license_key: str
    channel_id: str

class CreativeAssetRequest(BaseModel):
    license_key: str
    prompt: str
    asset_type: Optional[str] = "logo"
    aspect_ratio: Optional[str] = "1:1"

class EnterpriseSearchRequest(BaseModel):
    license_key: str
    query: str
    scope: Optional[str] = "all"


# --- مسارات البوابة المركزية (Endpoints) ---

@app.post("/api/v1/license/link", summary="ربط أو استعادة المفتاح السيادي بالحساب الجديد")
async def api_link_license(data: LicenseLinkRequest):
    """إدارة استعادة الهوية وربط المفتاح الموحد بحساب تليجرام جديد"""
    result = await SovereignLicenseManager.verify_and_link_user(data.license_key, data.chat_id)
    return result


@app.post("/api/v1/protection/activate", summary="تفعيل درع الحماية ونظام الخانات الديناميكي")
async def api_activate_protection(data: ProtectionSlotRequest):
    """التحقق من الصيانة وخانات المجموعات الـ 5 وتفعيل الحماية"""
    result = await SovereignProtectionEngine.activate_protection(data.license_key, data.channel_id)
    return result


@app.post("/api/v1/creative/generate", summary="طلب أصل بصري من استوديو الإبداع الذكي")
async def api_generate_asset(data: CreativeAssetRequest):
    """توليد الشعارات والتصاميم عبر الذكاء الاصطناعي للمفتاح المصرح له"""
    result = await SovereignCreativeStudio.generate_asset_request(
        data.license_key, data.prompt, data.asset_type, data.aspect_ratio
    )
    return result


@app.post("/api/v1/search/intelligence", summary="تنفيذ بحث استخباراتي شامل وشبكي")
async def api_enterprise_search(data: EnterpriseSearchRequest):
    """استعلام دقيق يربط بين الويب وشبكات التواصل الاجتماعي لخدمة أعمال المستخدم"""
    result = await SovereignSearchEngine.execute_enterprise_search(
        data.license_key, data.query, data.scope
    )
    return result


@app.get("/health", summary="فحص نبض النظام السيادي")
async def health_check():
    return {"status": "online", "system": "AymnGuard Imperial Core", "version": "5.0.0"}
