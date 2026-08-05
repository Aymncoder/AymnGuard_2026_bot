# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Unit Testing Core
وحدة الفحص والاختبار الدقيق لمسارات الهوية والمستخدمين
=============================================================================
"""

from fastapi.testclient import TestClient
# لاحظ هنا: سنفترض أننا وحدنا المسار تحت backend_core
from backend_core.main import app 

# تجهيز محرك الاختبار اللحظي
client = TestClient(app)

def test_sovereign_guard_active():
    """
    فحص مبدئي للتأكد من أن بوابات النظام الأساسية تعمل ولا تعيد أخطاء 500
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "AymnGuard Enterprise AI Core is Active"}

def test_unauthorized_access_rejected():
    """
    اختبار درع الأمان: التأكد من أن محاولة الدخول بدون JWT يتم صدها فوراً
    """
    response = client.get("/api/v1/users/me")
    # يجب أن يصد النظام الطلب ويعيد رمز 401 (Unauthorized)
    assert response.status_code == 401 
