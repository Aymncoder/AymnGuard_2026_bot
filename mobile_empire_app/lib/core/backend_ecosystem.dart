import 'dart:convert';
import 'package:http/http.dart' as http;

/// 👑 نظام الربط الشامل والنهائي (The Universal Integration Engine)
/// يربط كل ملفات ومجلدات إمبراطورية AymnGuard بالتطبيق دون أي نقصان.
class BackendCoreEcosystem {
  static const String _baseUrl = 'http://135.181.86.199:8000';
  static const String _license = 'AYMN-PREMIUM-LICENSE-2026';

  // ===========================================================================
  // 1. الربط مع ملفات API/V1 العامة (البوابات والمسارات)
  // ===========================================================================
  static Future<Map<String, dynamic>> sendToGateway(String path, Map<String, dynamic> data) async {
    return _post('/api/v1/$path', data);
  }

  // ===========================================================================
  // 2. الربط مع الخدمات الأساسية (Services & Meta Engine)
  // ===========================================================================
  static Future<Map<String, dynamic>> triggerService(String serviceName, Map<String, dynamic> config) async {
    return _post('/api/v1/services/$serviceName/deploy', config);
  }

  // ===========================================================================
  // 3. الربط مع عمال المهام الخلفية (Workers & Task Broker)
  // ===========================================================================
  static Future<Map<String, dynamic>> dispatchWorkerTask(String taskName, Map<String, dynamic> payload) async {
    return _post('/api/v1/tasks/dispatch', {"task": taskName, "payload": payload});
  }

  // ===========================================================================
  // 4. الربط مع إدارة تيليجرام (Telegram Bots & Clients)
  // ===========================================================================
  static Future<Map<String, dynamic>> controlTelegramEngine(String action, Map<String, dynamic> params) async {
    return _post('/api/v1/telegram/engine/$action', params);
  }

  // ===========================================================================
  // 5. الربط مع محرك الذكاء الاصطناعي والبيانات (Neural & CRUD)
  // ===========================================================================
  static Future<Map<String, dynamic>> syncNeuralData(String action, Map<String, dynamic> data) async {
    return _post('/api/v1/neural/$action', data);
  }

  // ===========================================================================
  // 6. قوات الروبوتات المستقلة (Bots Ecosystem: Creative, Protection, Search)
  // ===========================================================================
  static Future<Map<String, dynamic>> runCreativeBot(String prompt, String type) async {
    return _post('/api/v1/bots/creative/generate', {
      "prompt": prompt, 
      "type": type
    });
  }

  static Future<Map<String, dynamic>> toggleProtectionBot(String chatId, bool isActive) async {
    return _post('/api/v1/bots/protection/toggle', {
      "chat_id": chatId, 
      "status": isActive
    });
  }

  static Future<Map<String, dynamic>> executeEnterpriseSearch(String query) async {
    return _post('/api/v1/bots/search/query', {
      "search_query": query
    });
  }

  static Future<Map<String, dynamic>> sendTelegramBotCommand(String command, Map<String, dynamic> args) async {
    return _post('/api/v1/bots/telegram/execute', {
      "command": command, 
      "args": args
    });
  }

  // ===========================================================================
  // 12. السيطرة على العمال والمهام المجدولة (workers/ & scripts/)
  // ===========================================================================
  static Future<Map<String, dynamic>> executeSystemScript(String scriptName) async {
    return _post('/api/v1/system/scripts/run', {
      "script_name": scriptName
    });
  }

  static Future<Map<String, dynamic>> checkWorkersHealth() async {
    return _get('/api/v1/system/workers/health');
  }

  // ===========================================================================
  // 13. نظام الأمان والتدقيق الشامل (security/ & middlewares/)
  // ===========================================================================
  static Future<Map<String, dynamic>> fetchSecurityAuditLogs(String level) async {
    return _post('/api/v1/system/security/logs', {
      "log_level": level
    });
  }

  static Future<Map<String, dynamic>> toggleSystemLockdown(bool enable) async {
    return _post('/api/v1/system/security/lockdown', {
      "enable_lockdown": enable
    });
  }

  // ===========================================================================
  // 14. فحص نبض البوابات الإمبراطورية (api_gateway.py & enterprise_gateway.py)
  // ===========================================================================
  static Future<Map<String, dynamic>> checkGatewayPulse() async {
    return _get('/health');
  }

  // ===========================================================================
  // 15. أنظمة التدقيق المعرفي والذكاء الاصطناعي (scripts/)
  // ===========================================================================
  static Future<Map<String, dynamic>> runCognitiveReview(String contentToReview) async {
    return _post('/api/v1/scripts/cognitive/review', {
      "content": contentToReview
    });
  }

  static Future<Map<String, dynamic>> runEnterpriseAudit(Map<String, dynamic> auditData) async {
    return _post('/api/v1/scripts/cognitive/audit', {
      "audit_data": auditData
    });
  }

  // ===========================================================================
  // 16. المحرك السيادي الأعلى (python scripts/sovereign_master_engine.py)
  // ===========================================================================
  static Future<Map<String, dynamic>> executeMasterEngineCommand(String commandAction) async {
    return _post('/api/v1/master/execute', {
      "command": commandAction
    });
  }

  // ===========================================================================
  // 17. التطبيقات المصغرة وبوابة الميديا (frontend_core/mini_app)
  // ===========================================================================
  static Future<Map<String, dynamic>> fetchMiniAppConfig() async {
    return _get('/api/v1/frontend/mini_app/config');
  }

  // ===========================================================================
  // 18. درع الحماية الأمني المطلق (security/)
  // ===========================================================================
  static Future<Map<String, dynamic>> verifySecurityToken(String token) async {
    return _post('/api/v1/security/verify', {
      "security_token": token
    });
  }

  static Future<Map<String, dynamic>> checkSystemShieldStatus() async {
    return _get('/api/v1/security/shield/status');
  }

  // ===========================================================================
  // 19. مملكة الخدمات المصغرة ومحركات التشغيل (services/)
  // ===========================================================================
  static Future<Map<String, dynamic>> executeEnterpriseTransfer({
    required String sessionId,
    required String sourceChat,
    required String targetChat,
  }) async {
    return _post('/api/v1/services/transfer/execute', {
      "session_id": sessionId,
      "source_chat": sourceChat,
      "target_chat": targetChat,
    });
  }

  static Future<Map<String, dynamic>> getMarketIntelligenceData(String symbol) async {
    return _post('/api/v1/services/market/intelligence', {
      "symbol": symbol
    });
  }

  static Future<Map<String, dynamic>> processEnterprisePayment(String planType, double amount) async {
    return _post('/api/v1/services/payment/process', {
      "plan": planType,
      "amount": amount
    });
  }

  static Future<Map<String, dynamic>> controlWorkerQueue(String command) async {
    return _post('/api/v1/services/worker/control', {
      "command": command
    });
  }

  static Future<Map<String, dynamic>> bridgeTelegramAction(String action, Map<String, dynamic> data) async {
    return _post('/api/v1/services/telegram/bridge', {
      "action": action,
      "payload": data
    });
  }

  // ===========================================================================
  // 20. محرك ومكونات الواجهة الأمامية (src/)
  // ===========================================================================
  static Future<Map<String, dynamic>> processFrontendAiTask(String prompt) async {
    return _post('/api/v1/frontend/ai/process', {
      "prompt": prompt
    });
  }

  static Future<Map<String, dynamic>> fetchFeatureForgeData() async {
    return _get('/api/v1/frontend/feature_forge/config');
  }

  // ===========================================================================
  // 21. فحص النظام واختبارات الجودة (tests/ & .env)
  // ===========================================================================
  static Future<Map<String, dynamic>> runSystemUnitTests() async {
    return _get('/api/v1/system/tests/run');
  }

  static Future<Map<String, dynamic>> verifyEnvironmentStatus() async {
    return _get('/api/v1/system/environment/status');
  }

  // ===========================================================================
  // 22. محطة التشغيل والتحكم بالحاويات والسيرفر الرئيسي (run.py & main.py)
  // ===========================================================================
  static Future<Map<String, dynamic>> checkMegaCorePulse() async {
    return _get('/');
  }

  static Future<Map<String, dynamic>> executeMegaCoreTrade({
    required String symbol,
    required String side,
    required double amount,
    required int leverage,
    required String apiKey,
    required String apiSecret,
  }) async {
    return _post('/api/v1/trade/execute', {
      "symbol": symbol,
      "side": side,
      "amount": amount,
      "leverage": leverage,
      "market": "SPOT",
      "api_key": apiKey,
      "api_secret": apiSecret,
    });
  }

  // ===========================================================================
  // ⚙️ معالجات الاتصال الأساسية (POST & GET Middlewares)
  // ===========================================================================
  static Future<Map<String, dynamic>> _post(String endpoint, Map<String, dynamic> body) async {
    body['license_key'] = _license;
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

  static Future<Map<String, dynamic>> _get(String endpoint) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl$endpoint'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 429) {
        return {"error": true, "message": "نظام الحماية نشط - يرجى التمهل"};
      }
      return jsonDecode(response.body);
    } catch (e) {
      return {"error": true, "message": "السيرفر لا يستجيب أو مغلق."};
    }
  }
}
