// -*- coding: utf-8 -*-
/// ==============================================================================
/// AymnGuard Sovereign Enterprise : Sovereign API Engine v34.8
/// ==============================================================================

import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;

/// 👑 السنترال الشامل: محرك الاتصال بالبوابة المؤسسية السيادية
class SovereignApiEngine {
  static const String _baseUrl = 'http://135.181.86.199:8000/api/v1';
  static const String _licenseKey = 'AYMN-PREMIUM-LICENSE-2026';
  static const Duration _defaultTimeout = Duration(seconds: 15);

  // ===========================================================================
  // 1. محرك إدارة الجلسات (Sessions Engine)
  // ===========================================================================
  static Future<Map<String, dynamic>> registerSession({
    required String phoneNumber,
    required String sessionName,
    required int apiId,
    required String apiHash,
  }) async {
    return _postRequest('/sessions/register', {
      "license_key": _licenseKey,
      "session_name": sessionName,
      "api_id": apiId,
      "api_hash": apiHash,
      "phone_number": phoneNumber,
    });
  }

  // ===========================================================================
  // 2. محرك نقل الأعضاء (Transfer Engine)
  // ===========================================================================
  static Future<Map<String, dynamic>> executeMemberTransfer({
    required String sessionName,
    required String sourceChat,
    required String targetChat,
    int batchSize = 50,
  }) async {
    return _postRequest('/telegram/transfer', {
      "license_key": _licenseKey,
      "session_name": sessionName,
      "source_chat": sourceChat,
      "target_chat": targetChat,
      "batch_size": batchSize,
      "filter_active_users": true,
    });
  }

  // ===========================================================================
  // 3. درع الحماية السيادي (Protection Engine)
  // ===========================================================================
  static Future<Map<String, dynamic>> activateProtection(String channelId) async {
    return _postRequest('/protection/activate', {
      "license_key": _licenseKey,
      "channel_id": channelId,
    });
  }

  // ===========================================================================
  // 4. مؤشرات التداول (Trading Engine)
  // ===========================================================================
  static Future<Map<String, dynamic>> getTradingIndicators({
    required String sessionName,
    required String symbol,
    required String timeframe,
  }) async {
    return _postRequest('/trading/indicators', {
      "license_key": _licenseKey,
      "session_name": sessionName,
      "symbol": symbol,
      "timeframe": timeframe,
      "indicators": ["RSI", "EMA", "ParabolicSAR", "MACD"],
    });
  }

  // ===========================================================================
  // 5. استوديو الإبداع والذكاء الاصطناعي (Creative Engine)
  // ===========================================================================
  static Future<Map<String, dynamic>> generateCreativeAsset({
    required String prompt,
    String assetType = "logo",
  }) async {
    return _postRequest('/creative/generate', {
      "license_key": _licenseKey,
      "prompt": prompt,
      "asset_type": assetType,
      "aspect_ratio": "1:1",
    });
  }

  // ===========================================================================
  // الدالة المركزية لإرسال الطلبات المحصنة (Private Helper)
  // ===========================================================================
  static Future<Map<String, dynamic>> _postRequest(String endpoint, Map<String, dynamic> body) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl$endpoint'),
        headers: {
          'Content-Type': 'application/json',
          'X-Sovereign-License': _licenseKey,
        },
        body: jsonEncode(body),
      ).timeout(_defaultTimeout);

      if (response.statusCode == 200 || response.statusCode == 201) {
        final decoded = jsonDecode(response.body);
        if (decoded is Map<String, dynamic>) {
          return decoded;
        }
        return {"error": true, "message": "تنسيق الاستجابة غير متطابق"};
      } else {
        return {
          "error": true,
          "message": "فشل الاتصال بالخادم: ${response.statusCode}",
          "details": response.body
        };
      }
    } on TimeoutException {
      return {
        "error": true,
        "message": "انتهت مهلة الاتصال بالخادم الإمبراطوري"
      };
    } catch (e) {
      return {
        "error": true,
        "message": "عطل في الشبكة أو الخادم مغلق",
        "details": e.toString()
      };
    }
  }
}
