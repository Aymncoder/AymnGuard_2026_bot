import 'package:flutter/material.dart';
import 'app_config.dart'; // لاستيراد AppColors المعرفة مسبقاً

class SovereignCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsetsGeometry? padding;

  const SovereignCard({
    super.key,
    required this.child,
    this.onTap,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
        padding: padding ?? const EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          // 1. الخلفية الداكنة العميقة مع الشفافية الزجاجية (Glassmorphism)
          color: AppColors.surface.withOpacity(0.75),
          borderRadius: BorderRadius.circular(16),
          
          // 2. الحدود الذهبية المطفأة الرفيعة لإعطاء الطابع الفاخر
          border: Border.all(
            color: AppColors.accentGold.withOpacity(0.35),
            width: 1.3,
          ),
          
          // 3. تأثير الظل والعمق ثلاثي الأبعاد
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.7),
              blurRadius: 14,
              offset: const Offset(0, 6),
            ),
          ],
        ),
        child: child,
      ),
    );
  }
}
