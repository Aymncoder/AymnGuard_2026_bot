import 'package:flutter/material.dart';
import 'app_config.dart';

import 'package:mobile_empire_app/telegram_core_chats_screen.dart';
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
import 'package:mobile_empire_app/settings_screens.dart';
import 'package:mobile_empire_app/app_drawers.dart';

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
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: AppColors.surface,
          selectedItemColor: AppColors.primary,
          unselectedItemColor: Colors.grey,
        ),
      ),
      home: const MainSovereignScreen(),
    );
  }
}

class MainSovereignScreen extends StatefulWidget {
  const MainSovereignScreen({super.key});
  
  @override
  State<MainSovereignScreen> createState() => _MainSovereignScreenState();
}

class _MainSovereignScreenState extends State<MainSovereignScreen> {
  int _currentIndex = 3; 

  final List<Widget> _screens = [
    const AccountSettingsScreen(), 
    const EmpirePremiumStore(),    
    const ContactsScreen(),        
    const TelegramCoreChats(),     
    if (AppConfig.isOwnerStatus) const UltimateOwnerDashboard(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const MultiAccountDrawer(),
      endDrawer: const AdvancedToolsDrawer(),
      body: IndexedStack(index: _currentIndex, children: _screens), 
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: "الإعدادات"),
          BottomNavigationBarItem(icon: Icon(Icons.storefront, color: AppColors.accentGold), label: "المتجر"),
          BottomNavigationBarItem(icon: Icon(Icons.perm_contact_calendar), label: "جهات الاتصال"),
          BottomNavigationBarItem(icon: Icon(Icons.chat_bubble), label: "محادثات"),
        ],
      ),
    );
  }
}
