import 'package:flutter/material.dart';
import 'app_config.dart';

// مسارات الشاشات والقوائم المستخدمة في الواجهة الرئيسية
import 'package:mobile_empire_app/telegram_core_chats_screen.dart';
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
import 'package:mobile_empire_app/settings_screens.dart';
import 'package:mobile_empire_app/app_drawers.dart';

void main() {
  runApp(const AymnGuardPlusApp());
}

// ==============================================================================
// النواة الأساسية (App Root)
// ==============================================================================
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
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: AppColors.surface,
          selectedItemColor: AppColors.primary,
          unselectedItemColor: Colors.grey,
        ),
        fontFamily: 'Roboto',
      ),
      home: const MainSovereignScreen(),
    );
  }
}

class AppConfig {
  static const String serverUrl = "http://135.181.86.199:10050";
  static const String appVersion = "21.0.0 Enterprise";
  static const bool isOwnerStatus = true;
}

class AppColors {
  static const Color background = Color(0xFF151E27);
  static const Color surface = Color(0xFF1E293B);
  static const Color primary = Color(0xFF0EA5E9);
  static const Color accentGold = Color(0xFFFFD700);
  static const Color chatBackground = Color(0xFF0F172A);
}

// ==============================================================================
// جهاز التحكم المركزي (Master Navigation Controller)
// ==============================================================================
class MainSovereignScreen extends StatefulWidget {
  const MainSovereignScreen({super.key});
  
  @override
  State<MainSovereignScreen> createState() => _MainSovereignScreenState();
}

class _MainSovereignScreenState extends State<MainSovereignScreen> {
  // بدء التطبيق على شاشة المحادثات (رقم 3 في المصفوفة)
  int _currentIndex = 3; 

  final List<Widget> _screens = [
    const AccountSettingsScreen(), 
    const EmpirePremiumStore(),    
    const ContactsScreen(),        
    const TelegramCoreChats(),     
    // التحقق من صلاحيات المالك لعرض لوحة القيادة السيادية
    if (AppConfig.isOwnerStatus) const UltimateOwnerDashboard(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const MultiAccountDrawer(),
      endDrawer: const AdvancedToolsDrawer(),
      // استخدام IndexedStack للحفاظ على حالة الشاشات عند التنقل بينها
      body: IndexedStack(index: _currentIndex, children: _screens), 
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        items: [
          const BottomNavigationBarItem(icon: Icon(Icons.settings), label: "الإعدادات"),
          const BottomNavigationBarItem(icon: Icon(Icons.storefront, color: AppColors.accentGold), label: "المتجر"),
          const BottomNavigationBarItem(icon: Icon(Icons.perm_contact_calendar), label: "جهات الاتصال"),
          const BottomNavigationBarItem(icon: Badge(label: Text('w'), child: Icon(Icons.chat_bubble)), label: "محادثات"),
          if (AppConfig.isOwnerStatus)
            const BottomNavigationBarItem(icon: Icon(Icons.admin_panel_settings, color: Colors.redAccent), label: 'الإدارة'),
        ],
      ),
    );
  }
}
