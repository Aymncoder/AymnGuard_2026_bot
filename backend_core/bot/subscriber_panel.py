# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Subscriber Control Panel Engine
محرك واجهة تحكم المشتركين والخدمات السيادية المتاحة للمستخدمين
=============================================================================
"""

import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

MINI_APP_URL = os.getenv("MINI_APP_URL", "https://mattress-before-exec-artwork.trycloudflare.com/app/index.html")

def get_subscriber_main_keyboard() -> ReplyKeyboardMarkup:
    """
    إنشاء لوحة المفاتيح السيادية المنظمة للمشتركين لضمان تجربة مستخدم عالمية وسلسة.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📱 فتح تطبيق تيليجرام السيادي (Mini App)", web_app=WebAppInfo(url=MINI_APP_URL))
            ],
            [
                KeyboardButton(text="💎 شراء اشتراك VIP الشامل ($70.0)"),
                KeyboardButton(text="🤖 شراء اشتراك البوت فقط ($35.0)")
            ],
            [
                KeyboardButton(text="🚀 شراء أداة نقل الأعضاء فقط ($45.0)"),
                KeyboardButton(text="⚡ أداة نقل الأعضاء الذكية (جلسات، فحص، نقل)")
            ],
            [
                KeyboardButton(text="🎨 استوديو التصميم والشعارات (4K)"),
                KeyboardButton(text="🌐 محرك البحث والوسائط الشامل")
            ],
            [
                KeyboardButton(text="💼 إدارة تليجرام الأعمال"),
                KeyboardButton(text="📥 البريد الوارد والتحديثات")
            ],
            [
                KeyboardButton(text="🎟️ تفعيل كوبون خصم"),
                KeyboardButton(text="🎫 خدمة العملاء والدعم")
            ],
            [
                KeyboardButton(text="🔄 تحديث الخدمات")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="🛡️ منصة AymnGuard السيادية - اختر الخدمة المطلوبة"
    )
    return keyboard
