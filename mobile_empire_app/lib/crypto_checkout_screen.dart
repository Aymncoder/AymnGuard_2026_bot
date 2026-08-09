import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'crypto_checkout_screen.dart'; // تأكد من مسار الملف إذا وضعته في مجلد widgets

import 'app_config.dart';

class CryptoCheckoutScreen extends StatefulWidget {
  final String invoiceId;
  final double amount;
  final String walletAddress;

  const CryptoCheckoutScreen({
    super.key,
    required this.invoiceId,
    required this.amount,
    required this.walletAddress,
  });

  @override
  State<CryptoCheckoutScreen> createState() => _CryptoCheckoutScreenState();
}

class _CryptoCheckoutScreenState extends State<CryptoCheckoutScreen> {
  // عداد 15 دقيقة (900 ثانية)
  int _remainingSeconds = 900; 
  Timer? _timer;
  bool _isPaid = false;

  @override
  void initState() {
    super.initState();
    _startTimer();
    _simulatePaymentChecking(); // محاكاة لعملية تتبع البلوكتشين
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_remainingSeconds > 0 && !_isPaid) {
        setState(() {
          _remainingSeconds--;
        });
      } else {
        timer.cancel();
      }
    });
  }

  // هذه الدالة ستقوم لاحقاً بالاتصال بالسيرفر كل 10 ثوانٍ لسؤاله: "هل تم الدفع؟"
  void _simulatePaymentChecking() {
    Future.delayed(const Duration(seconds: 15), () {
      if (mounted) {
        setState(() {
          _isPaid = true;
          _timer?.cancel();
        });
        
        // إظهار رسالة النجاح والعودة بعد ثانيتين
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: Colors.green,
            content: Text("✅ تم تأكيد الدفع بنجاح على شبكة BSC! مرحباً بك."),
          )
        );
        Future.delayed(const Duration(seconds: 2), () {
          Navigator.pop(context); // العودة للشاشة السابقة
        });
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  String _formatTime(int seconds) {
    int minutes = seconds ~/ 60;
    int remainingSeconds = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${remainingSeconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("الدفع الآمن - Web3"),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              "أرسل المبلغ المطلوب لإتمام الاشتراك",
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),
            const SizedBox(height: 20),
            
            // مربع تفاصيل المبلغ والشبكة
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: AppColors.accentGold, width: 1),
              ),
              child: Column(
                children: [
                  Text(
                    "${widget.amount} USDT",
                    style: const TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.white),
                  ),
                  const SizedBox(height: 5),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: Colors.orangeAccent.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      "الشبكة: BSC (BEP20)",
                      style: TextStyle(color: Colors.orangeAccent, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  // الباركود (QR Code)
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: QrImageView(
                      data: widget.walletAddress,
                      version: QrVersions.auto,
                      size: 200.0,
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  const Text(
                    "عنوان المحفظة:",
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                  const SizedBox(height: 5),
                  
                  // حقل نسخ عنوان المحفظة
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12),
                    decoration: BoxDecoration(
                      color: AppColors.background,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: Text(
                            widget.walletAddress,
                            style: const TextStyle(color: Colors.white, fontSize: 13),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        InkWell(
                          onTap: () {
                            Clipboard.setData(ClipboardData(text: widget.walletAddress));
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text("تم نسخ عنوان المحفظة!"))
                            );
                          },
                          child: const Icon(Icons.copy, color: AppColors.accentGold, size: 20),
                        )
                      ],
                    ),
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 30),
            
            // حالة الدفع والعداد التنازلي
            if (_isPaid)
              const Column(
                children: [
                  Icon(Icons.check_circle, color: Colors.green, size: 60),
                  SizedBox(height: 10),
                  Text("تم تأكيد الدفع بنجاح!", style: TextStyle(color: Colors.green, fontSize: 18, fontWeight: FontWeight.bold)),
                ],
              )
            else if (_remainingSeconds > 0)
              Column(
                children: [
                  const CircularProgressIndicator(color: AppColors.primary),
                  const SizedBox(height: 15),
                  const Text("في انتظار تأكيد البلوكتشين...", style: TextStyle(color: Colors.white)),
                  const SizedBox(height: 10),
                  Text(
                    "تنتهي صلاحية الفاتورة خلال: ${_formatTime(_remainingSeconds)}",
                    style: const TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold),
                  ),
                ],
              )
            else
              const Text(
                "انتهت صلاحية الفاتورة. يرجى المحاولة مرة أخرى.",
                style: TextStyle(color: Colors.redAccent, fontSize: 16),
              ),

            const SizedBox(height: 30),
            const Text(
              "⚠️ تحذير: أرسل عملة USDT فقط عبر شبكة BEP20 (BSC). إرسال أي عملة أخرى أو عبر شبكة مختلفة سيؤدي إلى فقدان أموالك ولن يتم تفعيل الاشتراك.",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey, fontSize: 11),
            )
          ],
        ),
      ),
    );
  }
}
