
import 'package:flutter/material.dart';

import 'package:mobile_empire_app/app_config.dart';
import 'package:mobile_empire_app/models/bot_model.dart'; // مسار صحيح داخل مجلد models
import 'package:mobile_empire_app/api_service.dart';
import 'package:mobile_empire_app/widgets/smart_contract_audit_widget.dart'; // مسار صحيح داخل مجلد widgets
import 'package:mobile_empire_app/telegram_core_chats_screen.dart';
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
import 'package:mobile_empire_app/settings_screens.dart';
import 'package:mobile_empire_app/app_drawers.dart';


// ==============================================================================
// نموذج بيانات البوتات السيادية (Sovereign Bot Data Model)
// ==============================================================================

class SovereignBotModel {
  final String id;
  final String name;
  final String description;
  final IconData icon;
  bool isInstalled;
  final bool isCustom;

  SovereignBotModel({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    this.isInstalled = false,
    this.isCustom = false,
  });

  /// تحويل البيانات القادمة من السيرفر (JSON) إلى كائن (Object)
  factory SovereignBotModel.fromJson(Map<String, dynamic> json) {
    return SovereignBotModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      // ملاحظة: الأيقونة هنا ثابتة حالياً، يمكن ربطها لاحقاً ببيانات السيرفر إذا لزم الأمر.
      icon: Icons.extension, 
      isInstalled: json['is_installed'] ?? false,
      isCustom: json['is_custom'] ?? false,
    );
  }
}
