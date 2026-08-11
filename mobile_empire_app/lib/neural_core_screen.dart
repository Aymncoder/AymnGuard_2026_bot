// -*- coding: utf-8 -*-
/// ==============================================================================
/// AymnGuard Sovereign Enterprise : Autonomous Neural Core Screen v1.1
/// ==============================================================================

import 'package:flutter/material.dart';
import 'core/app_config.dart';
import 'core/backend_ecosystem.dart';

class NeuralCoreScreen extends StatefulWidget {
  const NeuralCoreScreen({super.key});

  @override
  State<NeuralCoreScreen> createState() => _NeuralCoreScreenState();
}

class _NeuralCoreScreenState extends State<NeuralCoreScreen> {
  final TextEditingController _promptController = TextEditingController();
  bool _isProcessing = false;
  String _responseResult = "قم بإدخال أمرك أو سؤالك الذكي لتفعيل العقل السيادي المستقل...";

  Future<void> _executeNeuralTask() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _isProcessing = true;
      _responseResult = "جاري المعالجة عبر العقل السيادي المستقل...";
    });

    try {
      final result = await BackendCoreEcosystem.processFrontendAiTask(prompt);
      setState(() {
        if (result['error'] == true) {
          _responseResult = "⚠️ تنبيه سيادي: ${result['message']}";
        } else {
          _responseResult = result['response'] ?? result.toString();
        }
      });
    } catch (e) {
      setState(() {
        _responseResult = "❌ حدث خطأ في الاتصال بالمحرك العصبي: $e";
      });
    } finally {
      setState(() {
        _isProcessing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('المحرك العصبي المستقل 🧠', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        backgroundColor: AppColors.surface,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "منصة الذكاء الاصطناعي السيادي",
              style: TextStyle(color: AppColors.accentGold, fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              "تفاعل مع العقل المدبر لتنفيذ المهام البرمجية والتحليلية المتقدمة.",
              style: TextStyle(color: Colors.grey, fontSize: 13),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _promptController,
              maxLines: 4,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "اكتب أمرك الذكي هنا (مثال: تحليل هيكل البيانات أو توليد كود معالج)...",
                hintStyle: const TextStyle(color: Colors.grey),
                filled: true,
                fillColor: AppColors.surface,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: _isProcessing ? null : _executeNeuralTask,
                child: _isProcessing
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text("تنفيذ الأمر العصبي 🚀", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              "نتيجة التحليل السيادي:",
              style: TextStyle(color: Colors.white70, fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 8),
            Expanded(
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.accentGold.withOpacity(0.3)),
                ),
                child: SingleChildScrollView(
                  child: Text(
                    _responseResult,
                    style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.5),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
