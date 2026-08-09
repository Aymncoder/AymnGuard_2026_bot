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
      // تبدأ التطبيق بشاشة تسجيل وإضافة الحساب السيادية الأولى
      home: const AccountLoginGatewayScreen(),
    );
  }
}

// ==============================================================================
// 1. شاشة إضافة الحساب وتسجيل الدخول عند البداية
// ==============================================================================
class AccountLoginGatewayScreen extends StatelessWidget {
  const AccountLoginGatewayScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.shield_rounded, size: 80, color: AppColors.primary),
              const SizedBox(height: 20),
              const Text("بوابة AymnGuard السيادية", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 10),
              const Text("أضف حسابك الإمبراطوري لبدء الجلسة السحابية", style: TextStyle(color: Colors.grey, fontSize: 14)),
              const SizedBox(height: 30),
              TextField(
                decoration: InputDecoration(
                  filled: true,
                  fillColor: AppColors.surface,
                  labelText: "رقم الهاتف أو المعرف (@username)",
                  labelStyle: const TextStyle(color: Colors.grey),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                style: const TextStyle(color: Colors.white),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  minimumSize: const Size(double.infinity, 50),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: const Icon(Icons.add_moderator, color: Colors.white),
                label: const Text("إضافة الحساب وبدء الجلسة", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const MainSovereignScreen()),
                  );
                },
              ),
            ],
          ),
        ),
      ),
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
    const CommunitiesScreenTab(), 
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

class CommunitiesScreenTab extends StatelessWidget {
  const CommunitiesScreenTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("إدارة مجتمعاتي وأدواتي 👑", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          const Text("قنواتي ومجموعاتي السيادية", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 15)),
          const SizedBox(height: 8),
          _buildCard(context, "مجموعة التداول VIP", "أنت المالِك • 5,430 عضو", Icons.group, Colors.amber),
          _buildCard(context, "قناة تحديثات AymnGuard", "أنت المالِك • 12,000 مشترِك", Icons.campaign, Colors.blueAccent),
        ],
      ),
    );
  }

  Widget _buildCard(BuildContext context, String title, String subtitle, IconData icon, Color color) {
    return Card(
      color: AppColors.surface,
      margin: const EdgeInsets.symmetric(vertical: 6),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.2), child: Icon(icon, color: color)),
        title: Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
        trailing: const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
        onTap: () {},
      ),
    );
  }
}

// ==============================================================================
// 2. شاشة الإعدادات مع زر "إضافة حساب جديد" داخل التطبيق بعد الجلسة
// ==============================================================================
class AccountSettingsScreen extends StatelessWidget {
  const AccountSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text("الإعدادات")),
      body: ListView(
        children: [
          Container(
            color: AppColors.surface,
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                const CircleAvatar(radius: 30, backgroundColor: AppColors.primary, child: Icon(Icons.person, size: 35)),
                const SizedBox(width: 15),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("ابو يمان", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                    const SizedBox(height: 5),
                    Directionality(
                      textDirection: TextDirection.ltr,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: const Text("+91 9265035200", style: TextStyle(color: Colors.grey)),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 15),
          // زر إضافة حساب داخل التطبيق بعد تسجيل الجلسة
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.surface,
                padding: const EdgeInsets.symmetric(vertical: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10), side: const BorderSide(color: AppColors.primary)),
              ),
              icon: const Icon(Icons.person_add, color: AppColors.primary),
              label: const Text("إضافة حساب إمبراطوري جديد", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              onPressed: () {
                // فتح نافذة إضافة حساب إضافي
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    backgroundColor: AppColors.surface,
                    title: const Text("إضافة حساب جديد", style: TextStyle(color: Colors.white)),
                    content: const Text("أدخل بيانات الحساب الجديد المراد ربطه بالتطبيق.", style: TextStyle(color: Colors.grey)),
                    actions: [
                      TextButton(onPressed: () => Navigator.pop(context), child: const Text("إلغاء")),
                      ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("ربط الحساب")),
                    ],
                  ),
                );
              },
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
      body: Center(child: Text("جهات الاتصال الإمبراطورية", style: TextStyle(color: Colors.grey))),
    );
  }
}
