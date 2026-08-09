import 'package:mobile_empire_app/app_config.dart';
import 'dart:async';
import 'package:flutter/material.dart';

import 'package:mobile_empire_app/models/bot_model.dart'; // مسار صحيح داخل مجلد models
import 'package:mobile_empire_app/api_service.dart';
import 'package:mobile_empire_app/widgets/smart_contract_audit_widget.dart'; // مسار صحيح داخل مجلد widgets
import 'package:mobile_empire_app/telegram_core_chats_screen.dart';
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
import 'package:mobile_empire_app/settings_screens.dart';
import 'package:mobile_empire_app/app_drawers.dart';

// ==============================================================================
// 10. واجهة التدقيق الجنائي الذكي (Smart Contract Audit Widget)
// ==============================================================================

class SmartContractAuditWidget extends StatefulWidget {
  const SmartContractAuditWidget({super.key});

  @override
  State<SmartContractAuditWidget> createState() => _SmartContractAuditWidgetState();
}

class _SmartContractAuditWidgetState extends State<SmartContractAuditWidget> {
  final TextEditingController _contractController = TextEditingController();
  
  bool _isAuditing = false; // هل التدقيق جاري حالياً؟
  String? _taskId; // رقم التتبع الخاص بالمهمة
  String _auditStatusMessage = ""; // الرسالة التي تظهر للمستخدم
  Map<String, dynamic>? _auditResult; // نتيجة الفحص النهائية
  Timer? _statusTimer; // المؤقت الذي يسأل السيرفر

  @override
  void dispose() {
    _contractController.dispose();
    _statusTimer?.cancel(); // إيقاف المؤقت عند الخروج من الشاشة لمنع تسرب الذاكرة
    super.dispose();
  }

  // الدالة التي تبدأ عملية التدقيق
  Future<void> _startAudit() async {
    final contractAddress = _contractController.text.trim();
    if (contractAddress.isEmpty) return;

    setState(() {
      _isAuditing = true;
      _auditResult = null;
      _auditStatusMessage = "جاري تحويل العقد لوكلاء الذكاء الاصطناعي...";
    });

    // 1. إرسال الطلب للسيرفر واستلام رقم التتبع
    final taskId = await SovereignApiService.startSmartContractAudit(contractAddress);

    if (taskId != null) {
      setState(() {
        _taskId = taskId;
        _auditStatusMessage = "المهمة قيد التنفيذ (Task ID: ${_taskId!.substring(0, 8)}...)";
      });

      // 2. تشغيل المؤقت لسؤال السيرفر كل 3 ثوانٍ
      _statusTimer = Timer.periodic(const Duration(seconds: 3), (timer) async {
        final statusData = await SovereignApiService.checkTaskStatus(_taskId!);
        
        if (statusData != null) {
          if (statusData['status'] == 'completed') {
            // التدقيق انتهى!
            timer.cancel(); // نوقف السؤال
            setState(() {
              _isAuditing = false;
              _auditStatusMessage = "تم الانتهاء من الفحص!";
              _auditResult = statusData['result']; // حفظ النتيجة
            });
          } else {
            // التدقيق ما زال جارياً
            setState(() {
              _auditStatusMessage = statusData['message'] ?? "الوكيل يقوم بعمله...";
            });
          }
        }
      });
    } else {
      // في حال فشل الاتصال بالسيرفر في البداية
      setState(() {
        _isAuditing = false;
        _auditStatusMessage = "فشل في إرسال المهمة للسيرفر. تأكد من الاتصال.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
        side: const BorderSide(color: Colors.orange, width: 0.5),
      ),
      margin: const EdgeInsets.symmetric(vertical: 15),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.policy, color: Colors.orange, size: 28),
                SizedBox(width: 10),
                Text("محرك التدقيق الجنائي",
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
              ],
            ),
            const SizedBox(height: 10),
            const Text("أدخل عنوان العقد الذكي لفحصه من ثغرات السحب (Rug Pull).",
                style: TextStyle(color: Colors.grey, fontSize: 12)),
            const SizedBox(height: 15),
            
            // حقل إدخال عنوان العقد
            TextField(
              controller: _contractController,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "مثال: 0x123...DEF",
                hintStyle: const TextStyle(color: Colors.white30),
                filled: true,
                fillColor: AppColors.background,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide.none),
                contentPadding: const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
              ),
              enabled: !_isAuditing, // تعطيل الإدخال أثناء الفحص
            ),
            const SizedBox(height: 15),
            
            // زر البدء أو مؤشر التحميل
            if (_isAuditing)
              Column(
                children: [
                  const Center(child: CircularProgressIndicator(color: Colors.orange)),
                  const SizedBox(height: 10),
                  Text(_auditStatusMessage, style: const TextStyle(color: Colors.orangeAccent, fontSize: 12), textAlign: TextAlign.center),
                ],
              )
            else
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                  onPressed: _startAudit,
                  child: const Text("بدء الفحص الجنائي", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                ),
              ),

            // عرض نتيجة الفحص (إذا اكتملت)
            if (_auditResult != null)
              Container(
                margin: const EdgeInsets.top(15),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Colors.green.withOpacity(0.1), borderRadius: BorderRadius.circular(10), border: Border.all(color: Colors.green)),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("✅ تقرير الفحص الأمني:", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 5),
                    Text("الرسالة: ${_auditResult!['message']}", style: const TextStyle(color: Colors.white, fontSize: 12)),
                    Text("عدد الثغرات: ${_auditResult!['vulnerabilities_found']}", style: const TextStyle(color: Colors.white, fontSize: 12)),
                  ],
                ),
              ),
              
            // رسالة الخطأ (إذا فشل الإرسال ولم يكن هناك فحص جاري)
            if (!_isAuditing && _auditResult == null && _auditStatusMessage.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 10),
                child: Text(_auditStatusMessage, style: const TextStyle(color: Colors.redAccent, fontSize: 12)),
              ),
          ],
        ),
      ),
    );
  }
}
