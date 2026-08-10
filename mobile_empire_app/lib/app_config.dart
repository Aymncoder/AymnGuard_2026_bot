import 'package:flutter/material.dart';

class AppConfig {
  // إعدادات الخادم والاتصال النواتي السيادي
  static const String serverUrl = "http://135.181.86.199:10050";
  static const String baseUrl = "https://api.aymnguard.sovereign";
  static const String apiKey = "Sovereign_Enterprise_Key_2026";
  static const String appVersion = "21.0.0 Enterprise";
  
  // صلاحيات النواة الإمبراطورية والمالك
  static const bool isOwnerStatus = true;
}

class AppColors {
  // الخلفية الداكنة العميقة الإمبراطورية
  static const Color background = Color(0xFF050505);
  
  // السطوح والبطاقات ذات الطابع الزجاجي الملكي
  static const Color surface = Color(0xFF0A192F);
  
  // اللون الأساسي للسيادة والهيمنة
  static const Color primary = Color(0xFF1E3A8A);
  
  // اللون الذهبي الفاخر المعتمد في الهوية
  static const Color accentGold = Color(0xFFD4AF37);
  
  // اللون الأخضر السيبراني للعمليات والنشاط
  static const Color cyberGreen = Color(0xFF00FF66);
  
  // لون خلفية المحادثات والدردشة السيادية
  static const Color chatBackground = Color(0xFF0F172A);
}
