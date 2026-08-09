import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_empire_app/main.dart';

void main() {
  testWidgets('AymnGuard Plus Smoke Test', (WidgetTester tester) async {
    // بناء وتشغيل التطبيق الرئيسي
    await tester.pumpWidget(const AymnGuardPlusApp());

    // التحقق من أن التطبيق يعمل بنجاح ويعرض واجهة الماتريال
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
