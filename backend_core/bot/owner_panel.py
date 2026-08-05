# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Owner Control Panel Engine
محرك لوحة تحكم المالك المركزية والتحقق السيادي من الصلاحيات
=============================================================================
"""

import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

OWNER_ID = int(os.getenv("OWNER_ID", "5193790077"))
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://mattress-before-exec-artwork.trycloudflare.com/app/index.html")

def get_owner_main_keyboard() -> ReplyKeyboardMarkup:
    """
    إنشاء لوحة المفاتيح السيادية الشاملة للمالك بدقة تنظيمية عالية لمنع تداخل الأوامر.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📱 فتح تطبيق تيليجرام السيادي (Mini App)", web_app=WebAppInfo(url=MINI_APP_URL))
            ],
            [
                KeyboardButton(text="🏛️ غرفة العمليات السيادية (War Room)"),
                KeyboardButton(text="📢 صانع ونشر المنشورات السيادية")
            ],
            [
                KeyboardButton(text="🔄 تحديث الخدمات والصيانة"),
                KeyboardButton(text="📥 البريد الوارد والتدقيقات")
            ],
            [
                KeyboardButton(text="👥 عرض وإدارة الفريق والمشرفين"),
                KeyboardButton(text="➕ إضافة عضو جديد للفريق / الإداري")
            ],
            [
                KeyboardButton(text="💰 إضافة محفظة جديدة"),
                KeyboardButton(text="🗑️ حذف محفظة مسجلة")
            ],
            [
                KeyboardButton(text="📋 عرض المحافظ المعتمدة"),
                KeyboardButton(text="🎟️ إنشاء وإدارة الكوبونات")
            ],
            [
                KeyboardButton(text="🎛️ تعديل سعر ترخيص البوت / الأسعار"),
                KeyboardButton(text="📢 إعلان تخفيض وبيع آلي")
            ],
            [
                KeyboardButton(text="🔗 تعديل روابط القناة والمجموعة"),
                KeyboardButton(text="✍️ تعديل رسالة الشرح الترحيبية")
            ],
            [
                KeyboardButton(text="👥 عرض المشتركين والمستخدمين"),
                KeyboardButton(text="📢 إذاعة عامة للجميع")
            ],
            [
                KeyboardButton(text="🎟️ إدارة التذاكر والشكاوى"),
                KeyboardButton(text="🧹 تنظيف وطرد الحسابات الوهمية")
            ],
            [
                KeyboardButton(text="🔄 إعادة تشغيل عمليات البوت"),
                KeyboardButton(text="➕ إضافة خدمة أو ميزة مستقبلية جديدة")
            ],
            [
                KeyboardButton(text="🔄 مزامنة وتحديث الأداة والبوت من GitHub")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="🛡️ لوحة التحكم السيادية للمالك - AymnGuard v5.0"
    )
    return keyboard
