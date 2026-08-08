import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'app_config.dart';
import 'bot_model.dart';

// ==============================================================================
// طبقة الاتصال والخدمات الخلفية (Enterprise Service Layer)
// ==============================================================================

class SovereignApiService {
  // ------------------------------------------------------------------
  // 1. دوال جلب وتثبيت البوتات من السيرفر
  // ------------------------------------------------------------------
  static Future<List<SovereignBotModel>> fetchBots() async {
    try {
      final response = await http
          .get(Uri.parse('${AppConfig.serverUrl}/api/bots'))
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        Iterable data = json.decode(response.body);
        return data.map((json) => SovereignBotModel.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint("API Error: $e");
    }

    // بيانات افتراضية (Fallback Data) في حال فشل الاتصال
    return [
      SovereignBotModel(
          id: 'bot_1',
          name: 'بوت النقل العكسي الذكي',
          description: 'نقل الأعضاء باستخدام وكلاء AI.',
          icon: Icons.swap_calls,
          isInstalled: true),
      SovereignBotModel(
          id: 'bot_2',
          name: 'محرك التدقيق الجنائي',
          description: 'فحص الثغرات الأمنية في العقود.',
          icon: Icons.policy,
          isInstalled: false),
      SovereignBotModel(
          id: 'bot_3',
          name: 'الترجمة المالية الآلية',
          description: 'ترجمة فورية للتقارير المالية.',
          icon: Icons.translate,
          isInstalled: false),
      SovereignBotModel(
          id: 'bot_4',
          name: 'خدمة Webhook خارجية',
          description: 'أضف رابط لبوت مخصص.',
          icon: Icons.add_link,
          isInstalled: false,
          isCustom: true),
    ];
  }

  static Future<bool> installBotOnServer(String botId) async {
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.serverUrl}/api/bots/install'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          "bot_id": botId,
          "timestamp": DateTime.now().toIso8601String()
        }),
      ).timeout(const Duration(seconds: 10));
      return response.statusCode == 200;
    } catch (e) {
      // محاكاة لنجاح التثبيت في حال عدم وجود سيرفر حقيقي حالياً
      await Future.delayed(const Duration(milliseconds: 800));
      return true; 
    }
  }

  // ------------------------------------------------------------------
  // 2. دوال الاتصال بالعمال الخلفيين ووكلاء الذكاء الاصطناعي (FastAPI & Celery)
  // ------------------------------------------------------------------

  /// إرسال عقد ذكي للتدقيق والحصول على رقم تتبع المهمة (Task ID)
  static Future<String?> startSmartContractAudit(String contractAddress) async {
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.serverUrl}/api/services/audit'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({"contract_address": contractAddress}),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        debugPrint("تم إرسال المهمة بنجاح. رقم التتبع: ${data['task_id']}");
        return data['task_id']; // إعادة رقم التتبع للتطبيق
      }
    } catch (e) {
      debugPrint("خطأ في إرسال طلب التدقيق: $e");
    }
    return null;
  }

  /// الاستعلام عن حالة المهمة باستخدام رقم التتبع
  static Future<Map<String, dynamic>?> checkTaskStatus(String taskId) async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.serverUrl}/api/services/status/$taskId'),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      debugPrint("خطأ في جلب حالة المهمة: $e");
    }
    return null;
  }
}
