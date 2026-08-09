import 'dart:convert';
import 'package:http/http.dart' as http;

/// 👑 نظام الربط الشامل (The Universal Integration Engine)
/// يربط كل ملفات backend_core (API, CRUD, Services, Workers, Telegram) بالتطبيق.
class BackendCoreEcosystem {
  static const String _baseUrl = 'http://135.181.86.199:8000';
  static const String _license = 'AYMN-PREMIUM-LICENSE-2026';
  // ===========================================================================
  // 6. قوات الروبوتات المستقلة (Bots Ecosystem: Creative, Protection, Search)
  // ===========================================================================
  
  /// تشغيل روبوت الإبداع والتصميم
  static Future<Map<String, dynamic>> runCreativeBot(String prompt, String type) async {
    return _post('/api/v1/bots/creative/generate', {
      "prompt": prompt, 
      "type": type
    });
  }

  /// تفعيل أو تعطيل روبوت الحماية لمجموعة معينة
  static Future<Map<String, dynamic>> toggleProtectionBot(String chatId, bool isActive) async {
    return _post('/api/v1/bots/protection/toggle', {
      "chat_id": chatId, 
      "status": isActive
    });
  }

  /// تنفيذ بحث مؤسسي عميق عبر روبوت البحث
  static Future<Map<String, dynamic>> executeEnterpriseSearch(String query) async {
    return _post('/api/v1/bots/search/query', {
      "search_query": query
    });
  }

  /// إرسال أوامر مباشرة للروبوت المركزي
  static Future<Map<String, dynamic>> sendTelegramBotCommand(String command, Map<String, dynamic> args) async {
    return _post('/api/v1/bots/telegram/execute', {
      "command": command, 
      "args": args
    });
  }

  // 1. الربط مع ملفات API/V1 (البوابات والمسارات)
  static Future<Map<String, dynamic>> sendToGateway(String path, Map<String, dynamic> data) async {
    return _post('/api/v1/$path', data);
  }

  // 2. الربط مع الخدمات الأساسية (Services & Meta Engine)
  static Future<Map<String, dynamic>> triggerService(String serviceName, Map<String, dynamic> config) async {
    return _post('/api/v1/services/$serviceName/deploy', config);
  }

  // 3. الربط مع عمال المهام الخلفية (Workers & Task Broker)
  static Future<Map<String, dynamic>> dispatchWorkerTask(String taskName, Map<String, dynamic> payload) async {
    return _post('/api/v1/tasks/dispatch', {"task": taskName, "payload": payload});
  }

  // 4. الربط مع إدارة تيليجرام (Telegram Bots & Clients)
  static Future<Map<String, dynamic>> controlTelegramEngine(String action, Map<String, dynamic> params) async {
    return _post('/api/v1/telegram/engine/$action', params);
  }

  // 5. الربط مع محرك الذكاء الاصطناعي والبيانات (Neural & CRUD)
  static Future<Map<String, dynamic>> syncNeuralData(String action, Map<String, dynamic> data) async {
    return _post('/api/v1/neural/$action', data);
  }

  // دالة الإرسال المركزية (تمثل معالج الطلبات لـ Throttling & Middlewares)
  static Future<Map<String, dynamic>> _post(String endpoint, Map<String, dynamic> body) async {
    body['license_key'] = _license; // إلحاق الترخيص تلقائياً
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );
      if (response.statusCode == 429) return {"error": true, "message": "نظام الحماية نشط - يرجى التمهل"};
      return jsonDecode(response.body);
    } catch (e) {
      return {"error": true, "message": "فشل الربط بالمسار: $endpoint"};
    }
  }
}
