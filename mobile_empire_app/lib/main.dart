// -*- coding: utf-8 -*-
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'app_config.dart';
import 'core/backend_ecosystem.dart';
import 'sovereign_card.dart';
// هذه المكتبات تحتوي على أدواتك الحقيقية التي لن نلمسها
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
import 'package:mobile_empire_app/app_drawers.dart';
import 'package:mobile_empire_app/models/bot_model.dart';
import 'package:mobile_empire_app/neural_core_screen.dart';

void main() {
  runApp(const AymnGuardPlusApp());
}

class AymnGuardPlusApp extends StatelessWidget {
  const AymnGuardPlusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AymnGuard Plus Ultimate',
      debugShowCheckedModeBanner: false,
      builder: (context, child) => Directionality(textDirection: TextDirection.rtl, child: child!),
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: AppColors.background,
        primaryColor: AppColors.primary,
        appBarTheme: const AppBarTheme(backgroundColor: AppColors.surface, elevation: 0),
      ),
      home: const AccountLoginGatewayScreen(),
    );
  }
}

// ==============================================================================
// 🌟 المركز الرئيسي (تم ربط كل شيء بالدوال الحقيقية) 🌟
// ==============================================================================

class MainSovereignScreen extends StatefulWidget {
  final String userAccount;
  const MainSovereignScreen({super.key, required this.userAccount});
  
  @override
  State<MainSovereignScreen> createState() => _MainSovereignScreenState();
}

class _MainSovereignScreenState extends State<MainSovereignScreen> {
  int _currentIndex = 3; 

  @override
  Widget build(BuildContext context) {
    // هذه المصفوفة تستدعي ملفاتك الأصلية التي تحتوي على أدواتك الحقيقية
    final List<Widget> screens = [
      AccountSettingsScreen(userAccount: widget.userAccount), 
      const EmpirePremiumStore(),                             
      const ContactsScreen(),                                 
      const SovereignDashboardTab(), // هذه هي واجهتنا الإمبراطورية الجديدة المربوطة
      if (AppConfig.isOwnerStatus) const UltimateOwnerDashboard(),
    ];

    return Scaffold(
      extendBody: true,
      backgroundColor: AppColors.background,
      
      // الأزرار العلوية تفتح الأدوات الحقيقية (Drawers) التي برمجتها أنت
      appBar: AppBar(
        backgroundColor: Colors.transparent, elevation: 0,
        leading: Builder(builder: (context) => IconButton(icon: const Icon(Icons.manage_accounts_rounded, color: AppColors.accentGold), onPressed: () => Scaffold.of(context).openDrawer())),
        actions: [Builder(builder: (context) => IconButton(icon: const Icon(Icons.handyman_rounded, color: AppColors.accentGold), onPressed: () => Scaffold.of(context).openEndDrawer()))],
      ),

      drawer: const MultiAccountDrawer(),     // أدواتك الحقيقية لإدارة الحسابات
      endDrawer: const AdvancedToolsDrawer(), // أدواتك الحقيقية لتصميم الإيصالات
      
      body: CyberEnterpriseBackground(child: IndexedStack(index: _currentIndex, children: screens)), 
      
      bottomNavigationBar: SafeArea(child: Padding(padding: const EdgeInsets.all(16), child: FloatingGlassyNavBar(currentIndex: _currentIndex, onTap: (i) => setState(() => _currentIndex = i)))),
    );
  }
}

// ==============================================================================
// 🌟 الواجهة الإمبراطورية (Command Hub) - تم ربط الأزرار بالأدوات الحقيقية 🌟
// ==============================================================================

class SovereignDashboardTab extends StatelessWidget {
  const SovereignDashboardTab({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          const SovereignBrandingHeader(),
          const SizedBox(height: 20),
          const SovereignStatusBanner(),
          const SizedBox(height: 20),
          // شبكة التحكم المربوطة بالأدوات الحقيقية
          CommandHubGrid(), 
          const SizedBox(height: 100),
        ],
      ),
    );
  }
}

class CommandHubGrid extends StatelessWidget {
  const CommandHubGrid({super.key});
  
  @override
  Widget build(BuildContext context) {
    return GridView.count(
      shrinkWrap: true, physics: const NeverScrollableScrollPhysics(), crossAxisCount: 2, crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.3,
      children: [
        _buildButton(context, 'نقل الأعضاء', Icons.move_up_rounded, const Color(0xFFE83845), () => Scaffold.of(context).openDrawer()),
        _buildButton(context, 'بوت الحماية', Icons.shield_rounded, const Color(0xFF8A2BE2), () => launchUrl(Uri.parse('https://t.me/AymnGuard_2026_bot'))),
        _buildButton(context, 'المحادثات', Icons.telegram, const Color(0xFF2FA4E7), () => Navigator.push(context, MaterialPageRoute(builder: (context) => const TelegramCoreChatsScreen()))),
        _buildButton(context, 'تصميم الإيصالات', Icons.receipt_long_rounded, const Color(0xFFD4AF37), () => Scaffold.of(context).openEndDrawer()),
        _buildButton(context, 'قناة التحديثات', Icons.campaign_rounded, const Color(0xFFE2A12B), () => launchUrl(Uri.parse('https://t.me/AymnGuardChat'))),
        _buildButton(context, 'مجموعة الدعم', Icons.group, const Color(0xFF3FB950), () => launchUrl(Uri.parse('https://t.me/AymnGuard'))),
      ],
    );
  }

  Widget _buildButton(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(onTap: onTap, child: Container(decoration: BoxDecoration(color: const Color(0xFF161B22), borderRadius: BorderRadius.circular(12)), padding: const EdgeInsets.all(16), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(icon, color: color, size: 30), const SizedBox(height: 10), Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))])));
  }
}

// الخلفية السيبرانية المدمجة
class CyberEnterpriseBackground extends StatelessWidget {
  final Widget child;
  const CyberEnterpriseBackground({super.key, required this.child});
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(gradient: LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [Color(0xFF060D1A), Color(0xFF020409)])),
      child: child,
    );
  }
}

// (أعد إدراج كلاساتك الأصلية: SovereignBrandingHeader, SovereignStatusBanner, AccountLoginGatewayScreen, إلخ)
