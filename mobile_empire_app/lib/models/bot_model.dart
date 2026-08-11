// -*- coding: utf-8 -*-
/// ==============================================================================
/// AymnGuard Sovereign Enterprise : Sovereign Bot Data Model v34.4
/// ==============================================================================

import 'package:flutter/material.dart';
import 'package:mobile_empire_app/app_config.dart';

class SovereignBotModel {
  final String id;
  final String name;
  final String description;
  final IconData icon;
  bool isInstalled;
  final bool isCustom;

  const SovereignBotModel({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    this.isInstalled = false,
    this.isCustom = false,
  });

  factory SovereignBotModel.fromJson(Map<String, dynamic> json) {
    return SovereignBotModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      icon: Icons.extension, // الأيقونة الافتراضية السيادية
      isInstalled: json['is_installed'] ?? false,
      isCustom: json['is_custom'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'is_installed': isInstalled,
      'is_custom': is_custom,
    };
  }
}
