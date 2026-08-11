import 'package:flutter/material.dart';

class SovereignDashboardScreen extends StatefulWidget {
  const SovereignDashboardScreen({Key? key}) : super(key: key);

  @override
  State<SovereignDashboardScreen> createState() => _SovereignDashboardScreenState();
}

class _SovereignDashboardScreenState extends State<SovereignDashboardScreen> {
  int _currentIndex = 3; // الافتراضي على محور المحادثات السيادية

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1117), // خلفية سيادية داكنة
      body: SafeArea(
        child: Stack(
          children: [
            SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // 1. بطاقة الحالة التشغيلية السيادية (Status Banner)
                  const SovereignStatusBanner(),
                  
                  const SizedBox(height: 20),

                  // 2. بوابات الاتصال والمراسلة (The Command Hub)
                  const Text(
                    'THE COMMAND HUB',
                    style: TextStyle(
                      color: Color(0xFFD4AF37),
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.5,
                    ),
                  ),
                  const SizedBox(height: 12),
                  const CommandHubGrid(),
                  
                  const SizedBox(height: 100), // مسافة إضافية لتجنب تداخل الشريط السفلي العائم
                ],
              ),
            ),

            // 3. شريط التنقل السفلي العائم (Floating & Glassy Bottom Navigation Bar)
            Positioned(
              left: 16,
              right: 16,
              bottom: 20,
              child: FloatingGlassyNavBar(
                currentIndex: _currentIndex,
                onTap: (index) {
                  setState(() {
                    _currentIndex = index;
                  });
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// -------------------------------------------------------------------------
// 1. بطاقة الحالة التشغيلية (Status Banner)
// -------------------------------------------------------------------------
class SovereignStatusBanner extends StatelessWidget {
  const SovereignStatusBanner({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF161B22),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFF238636).withOpacity(0.5), // إطار أخضر تقني خفيف
          width: 1,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.4),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              // مؤشر النبض الأخضر
              Container(
                width: 12,
                height: 12,
                decoration: const BoxDecoration(
                  color: Color(0xFF238636),
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: Color(0xFF238636),
                      blurRadius: 8,
                      spreadRadius: 2,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              const Text(
                'CORE SYSTEM STATUS',
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 1.0,
                ),
              ),
            ],
          ),
          const Text(
            'SECURE & OPERATIONAL 100%',
            style: TextStyle(
              color: Color(0xFF3FB950),
              fontSize: 11,
              fontWeight: FontWeight.bold,
              letterSpacing: 0.5,
            ),
          ),
        ],
      ),
    );
  }
}

// -------------------------------------------------------------------------
// 2. شبكة بوابات الاتصال (Command Hub Grid)
// -------------------------------------------------------------------------
class CommandHubGrid extends StatelessWidget {
  const CommandHubGrid({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> hubs = [
      {'title': 'محادثات تيليجرام', 'icon': Icons.telegram, 'color': const Color(0xFF2FA4E7)},
      {'title': 'قنوات الإدارة', 'icon': Icons.campaign_rounded, 'color': const Color(0xFFD4AF37)},
      {'title': 'التحكم بالروبوتات', 'icon': Icons.smart_toy_rounded, 'color': const Color(0xFF8A2BE2)},
      {'title': 'حماية المجموعات', 'icon': Icons.shield_rounded, 'color': const Color(0xFF3FB950)},
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: hubs.count,
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.4,
      ),
      itemBuilder: (context, index) {
        final item = hubs[index];
        return Container(
          decoration: BoxDecoration(
            color: const Color(0xFF161B22).withOpacity(0.7),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: Colors.white.withOpacity(0.08),
              width: 1,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.2),
                blurRadius: 6,
              ),
            ],
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: () {},
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: (item['color'] as Color).withOpacity(0.15),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Icon(
                        item['icon'] as IconData,
                        color: item['color'] as Color,
                        size: 26,
                      ),
                    ),
                    const Spacer(),
                    Text(
                      item['title'] as String,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}

// -------------------------------------------------------------------------
// 3. شريط التنقل السفلي العائم (Floating Glassy Bottom Navigation Bar)
// -------------------------------------------------------------------------
class FloatingGlassyNavBar extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;

  const FloatingGlassyNavBar({
    Key? key,
    required this.currentIndex,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF161B22).withOpacity(0.85),
        borderRadius: BorderRadius.circular(25),
        border: Border.all(
          color: const Color(0xFFD4AF37).withOpacity(0.3), // إطار ذهبي خפيف
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.5),
            blurRadius: 15,
            spreadRadius: 2,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _navItem(0, Icons.settings_rounded, 'الإعدادات'),
          _navItem(1, Icons.store_rounded, 'المتجر'),
          _navItem(2, Icons.contacts_rounded, 'جهات الاتصال'),
          _navItem(3, Icons.chat_bubble_rounded, 'المحادثات'),
        ],
      ),
    );
  }

  Widget _navItem(int index, IconData icon, String label) {
    final isSelected = currentIndex == index;
    return GestureDetector(
      onTap: () => onTap(index),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        padding: EdgeInsets.symmetric(horizontal: isSelected ? 14 : 8, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFFD4AF37).withOpacity(0.2) : Colors.transparent,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected ? const Color(0xFFF3C68F) : Colors.grey[500],
              size: 24,
            ),
            if (isSelected) ...[
              const SizedBox(width: 6),
              Text(
                label,
                style: const TextStyle(
                  color: Color(0xFFF3C68F),
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
