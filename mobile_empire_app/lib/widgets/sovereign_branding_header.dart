file_content = """import 'package:flutter/material.dart';

class SovereignBrandingHeader extends StatelessWidget {
  const SovereignBrandingHeader({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 24.0, horizontal: 16.0),
      decoration: BoxDecoration(
        color: const Color(0xFF0D1117), // خلفية داكنة تحاكي طابع السيادة التقنية
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: const Color(0xFFD4AF37).withOpacity(0.3), // إطار ذهبي خفيف
          width: 1,
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // 1. أيقونة الدرع الإمبراطوري ثلاثي الأبعاد مع إطار ذهبي مضيء
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: LinearGradient(
                colors: [
                  const Color(0xFFD4AF37).withOpacity(0.4),
                  const Color(0xFF1A1F2C),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              boxShadow: [
                BoxShadow(
                  color: const Color(0xFFD4AF37).withOpacity(0.3),
                  blurRadius: 15,
                  spreadRadius: 2,
                ),
              ],
              border: Border.all(
                color: const Color(0xFFD4AF37),
                width: 2,
              ),
            ),
            child: const Icon(
              Icons.security_rounded,
              size: 40,
              color: Color(0xFFF3C68F), // لون ذهبي متوهج للأيقونة
            ),
          ),
          
          const SizedBox(height: 16),

          // 2. اسم التطبيق بخط إبداعي عالمي (AymnGuard Plus)
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // كلمة AymnGuard بيضاء ناصعة مع تباعد حروف أنيق
              Text(
                'AymnGuard',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2.0,
                  shadows: [
                    Shadow(
                      color: Colors.white.withOpacity(0.4),
                      blurRadius: 8,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              
              // شارة Plus الذهبية للإصدار السيادي المتقدم
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFBF953F), Color(0xFFFCF6BA), Color(0xFFB38728)],
                  ),
                  borderRadius: BorderRadius.circular(6),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFFD4AF37).withOpacity(0.5),
                      blurRadius: 6,
                    ),
                  ],
                ),
                child: const Text(
                  'PLUS',
                  style: TextStyle(
                    color: Color(0xFF1A1A1A),
                    fontSize: 12,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 1.0,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 8),

          // 3. الشعار الترويجي التحتي (Tagline) بخط رمادي رفيع ودقيق
          Text(
            'Sovereign Enterprise Security & Core Architecture',
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Colors.grey[400],
              fontSize: 11,
              fontWeight: FontWeight.w300,
              letterSpacing: 1.2,
            ),
          ),
        ],
      ),
    );
  }
}
"""

with open('sovereign_branding_header.dart', 'w', encoding='utf-8') as f:
    f.write(file_content)
