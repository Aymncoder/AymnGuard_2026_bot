import 'package:flutter/material.dart';
import 'app_config.dart';

import 'package:mobile_empire_app/telegram_core_chats_screen.dart';
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
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
        type: BottomNavigationBarType.fixed,
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

// ==============================================================================
// شاشة الإعدادات المدمجة لضمان عدم ضياع أي ملف
// ==============================================================================
class AccountSettingsScreen extends StatelessWidget {
  const AccountSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("الإعدادات", style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: ListView(
        children: [
          Container(
            color: AppColors.surface,
            padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
            child: const Row(
              children: [
                CircleAvatar(
                  radius: 35,
                  backgroundColor: AppColors.primary,
                  child: Icon(Icons.person, size: 40, color: Colors.white),
                ),
                SizedBox(width: 15),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("ابو يمان", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                    SizedBox(height: 5),
                    Text("+91 9265035200", style: TextStyle(fontSize: 14, color: Colors.grey)),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
            child: Text("جهات الاتصال الإمبراطورية", style: TextStyle(color: Colors.grey))));
  }
}
