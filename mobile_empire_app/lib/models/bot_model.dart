import 'package:flutter/material.dart';
import 'package:mobile_empire_app/app_config.dart';

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
      // ملاحظة: الأيقونة هنا ثابتة حالياً، يمكن ربطها لاحقاً ببيانات السيرفر إذا لزم الأمر
      icon: Icons.extension,
      isInstalled: json['is_installed'] ?? false,
      isCustom: json['is_custom'] ?? false,
    );
  }
}
