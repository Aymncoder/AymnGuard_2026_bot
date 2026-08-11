// -*- coding: utf-8 -*-
/// ==============================================================================
/// AymnGuard Sovereign Enterprise : Enterprise Smoke Test Suite v1.0
/// ==============================================================================

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_empire_app/main.dart';

void main() {
  testWidgets('AymnGuard Plus Sovereign Smoke Test', (WidgetTester tester) async {
    // بدء تشغيل التطبيق الرئيسي للإمبراطورية
    await tester.pumpWidget(const AymnGuardPlusApp());

    // التحقق من أن التطبيق يعمل بنجاح ويعرض واجهة الماتريال السيادية
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
