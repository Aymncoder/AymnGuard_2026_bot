import 'dart:convert';
import 'package:http/http.dart' as http;

/// 👑 نظام الربط الشامل (The Universal Integration Engine)
/// يربط كل ملفات backend_core (API, CRUD, Services, Workers, Telegram) بالتطبيق.
class BackendCoreEcosystem {
  static const String _baseUrl = 'http://135.181.86.199:8000';
  static const String _license = 'AYMN-PREMIUM-LICENSE-2026';
   // ===========================================================================
  // 12. السيطرة على العمال والمهام المجدولة (workers/ & scripts/)
  // ===========================================================================
  /// تشغيل سكربتات الصيانة والتحديث الآلي من الموبايل
  static Future<Map<String, dynamic>> executeSystemScript(String scriptName) async {
    return _post('/api/v1/system/scripts/run', {
      "script_name": scriptName
    });
  }

  /// مراقبة صحة العمال (Workers) والمهام الخلفية
  static Future<Map<String, dynamic>> checkWorkersHealth() async {
    return _get('/api/v1/system/workers/health');
  }

  // ===========================================================================
  // 13. نظام الأمان والتدقيق الشامل (security/ & middlewares/)
  // ===========================================================================
  /// سحب سجلات الأمان (Security Logs) لمعرفة أي محاولة اختراق
  static Future<Map<String, dynamic>> fetchSecurityAuditLogs(String level) async {
    return _post('/api/v1/system/security/logs', {
      "log_level": level // مثال: 'CRITICAL' أو 'WARNING'
    });
  }
  // ===========================================================================
  // 15. أنظمة التدقيق المعرفي والذكاء الاصطناعي (scripts/)
  // ===========================================================================
  /// تشغيل ai_cognitive_reviewer.py لمراجعة نص أو كود معين
  static Future<Map<String, dynamic>> runCognitiveReview(String contentToReview) async {
    return _post('/api/v1/scripts/cognitive/review', {
      "content": contentToReview
    });
  }

  /// تشغيل enterprise_cognitive_auditor.py للتدقيق المؤسسي
  static Future<Map<String, dynamic>> runEnterpriseAudit(Map<String, dynamic> auditData) async {
    return _post('/api/v1/scripts/cognitive/audit', {
      "audit_data": auditData
    });
  }
  // ===========================================================================
  // 20. محرك ومكونات الواجهة الأمامية (src/)
  // ===========================================================================
  
  /// استدعاء معالجة محرك الذكاء الاصطناعي للواجهة (src/ai_engine.py)
  static Future<Map<String, dynamic>> processFrontendAiTask(String prompt) async {
    return _post('/api/v1/frontend/ai/process', {
      "prompt": prompt
    });
  }

  /// جلب بيانات مكونات الويب وتوليد الميزات (FeatureForge)
  static Future<Map<String, dynamic>> fetchFeatureForgeData() async {
    return _get('/api/v1/frontend/feature_forge/config');
  }

  // ===========================================================================
  // 16. المحرك السيادي الأعلى (python scripts/sovereign_master_engine.py)
  // ===========================================================================
  /// إرسال أوامر تحكم عليا مباشرة للمحرك الماستر
  static Future<Map<String, dynamic>> executeMasterEngineCommand(String commandAction) async {
    return _post('/api/v1/master/execute', {
      "command": commandAction
    });
  }
  // ===========================================================================
  // 18. درع الحماية الأمني المطلق (security/)
  // ===========================================================================
  /// التحقق من سلامة التوقيع الرقمي للطلب عبر hmac_security_guard.py
  static Future<Map<String, dynamic>> verifySecurityToken(String token) async {
    return _post('/api/v1/security/verify', {
      "security_token": token
    });
  }

  /// تفعيل أو فحص حالة الدرع الأمني (shield.py & protection_bot.py)
  static Future<Map<String, dynamic>> checkSystemShieldStatus() async {
    return _get('/api/v1/security/shield/status');
  }

  // ===========================================================================
  // 17. التطبيقات المصغرة وبوابة الميديا (frontend_core/mini_app)
  // ===========================================================================
  /// جلب إعدادات وبحث التطبيقات المصغرة (Mini App Controller)
  static Future<Map<String, dynamic>> fetchMiniAppConfig() async {
    return _get('/api/v1/frontend/mini_app/config');
  }

  /// تفعيل أو تعطيل وضع الحماية القصوى (Lockdown Mode)
  static Future<Map<String, dynamic>> toggleSystemLockdown(bool enable) async {
    return _post('/api/v1/system/security/lockdown', {
      "enable_lockdown": enable
    });
  }

  // ===========================================================================
  // 14. فحص نبض البوابات الإمبراطورية (api_gateway.py & enterprise_gateway.py)
  // ===========================================================================
  /// دالة تفحص ما إذا كان الباكن إند بأكمله يعمل ويستجيب
  static Future<Map<String, dynamic>> checkGatewayPulse() async {
    return _get('/health');
  }
  // ===========================================================================
  // 21. فحص النظام واختبارات الجودة (tests/ & .env)
  // ===========================================================================
  
  /// فحص حالة الاختبارات والمايسترو عبر (tests/test_orchestrator.py)
  static Future<Map<String, dynamic>> runSystemUnitTests() async {
    return _get('/api/v1/system/tests/run');
  }

  /// التحقق من توافق إعدادات البيئة والاتصال العام
  static Future<Map<String, dynamic>> verifyEnvironmentStatus() async {
    return _get('/api/v1/system/environment/status');
  }

  // ===========================================================================
  // 🛡️ دعم دالة GET المركزية (لجلب البيانات بدون إرسال Body)
  // ===========================================================================
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
  // ===========================================================================
  // 19. مملكة الخدمات المصغرة ومحركات التشغيل (services/)
  // ===========================================================================
  
  /// تشغيل محرك النقل المؤسسي الذكي (enterprise_transfer_engine.py)
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

  /// استدعاء استخبارات السوق والتحليل المتقدم (market_intelligence.py)
  static Future<Map<String, dynamic>> getMarketIntelligenceData(String symbol) async {
    return _post('/api/v1/services/market/intelligence', {
      "symbol": symbol
    });
  }

  /// معالجة المدفوعات والاشتراكات عبر (payment_engine.py)
  static Future<Map<String, dynamic>> processEnterprisePayment(String planType, double amount) async {
    return _post('/api/v1/services/payment/process', {
      "plan": planType,
      "amount": amount
    });
  }

  /// التحكم بالعمال الخلفيين ومدير الطوابير (worker.py & queue_manager.py)
  static Future<Map<String, dynamic>> controlWorkerQueue(String command) async {
    return _post('/api/v1/services/worker/control', {
      "command": command
    });
  }

  /// مخاطبة جسر تيليجرام المركزي (telegram_bridge.py)
  static Future<Map<String, dynamic>> bridgeTelegramAction(String action, Map<String, dynamic> data) async {
    return _post('/api/v1/services/telegram/bridge', {
      "action": action,
      "payload": data
    });
  }

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
