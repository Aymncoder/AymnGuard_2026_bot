import 'dart:async';
import 'package:flutter/material.dart';
import 'package:mobile_empire_app/app_config.dart';
import 'package:mobile_empire_app/api_service.dart';

class SmartContractAuditWidget extends StatefulWidget {
  const SmartContractAuditWidget({super.key});

  @override
  State<SmartContractAuditWidget> createState() => _SmartContractAuditWidgetState();
}

class _SmartContractAuditWidgetState extends State<SmartContractAuditWidget> {
  final TextEditingController _contractController = TextEditingController();
  
  bool _isAuditing = false; 
  String? _taskId; 
  String _auditStatusMessage = ""; 
  Map<String, dynamic>? _auditResult; 
  Timer? _statusTimer; 

  @override
  void dispose() {
    _contractController.dispose();
    _statusTimer?.cancel(); 
    super.dispose();
  }

  Future<void> _startAudit() async {
    final contractAddress = _contractController.text.trim();
    if (contractAddress.isEmpty) return;

    setState(() {
      _isAuditing = true;
      _auditResult = null;
      _auditStatusMessage = "جاري تحويل العقد لوكلاء الذكاء الاصطناعي...";
    });

    final taskId = await SovereignApiService.startSmartContractAudit(contractAddress);

    if (taskId != null) {
      setState(() {
        _taskId = taskId;
        _auditStatusMessage = "المهمة قيد التنفيذ (Task ID: ${_taskId!.substring(0, 8)}...)";
      });

      _statusTimer = Timer.periodic(const Duration(seconds: 3), (timer) async {
        final statusData = await SovereignApiService.checkTaskStatus(_taskId!);
        
        if (statusData != null) {
          if (statusData['status'] == 'completed') {
            timer.cancel(); 
            setState(() {
              _isAuditing = false;
              _auditStatusMessage = "تم الانتهاء من الفحص!";
              _auditResult = statusData['result']; 
            });
          } else {
            setState(() {
              _auditStatusMessage = statusData['message'] ?? "الوكيل يقوم بعمله...";
            });
          }
        }
      });
    } else {
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
              enabled: !_isAuditing, 
            ),
            const SizedBox(height: 15),
            
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

            if (_auditResult != null)
              Container(
                margin: const EdgeInsets.only(top: 15),
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
