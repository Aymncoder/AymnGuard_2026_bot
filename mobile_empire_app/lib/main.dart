import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
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
      home: const AccountLoginGatewayScreen(),
    );
  }
}

class AccountLoginGatewayScreen extends StatefulWidget {
  const AccountLoginGatewayScreen({super.key});

  @override
  State<AccountLoginGatewayScreen> createState() => _AccountLoginGatewayScreenState();
}

class _AccountLoginGatewayScreenState extends State<AccountLoginGatewayScreen> {
  final TextEditingController _accountController = TextEditingController();

  // دالة الاتصال بالباكن إند سيادياً
  Future<void> _loginAndConnect() async {
    String phoneInput = _accountController.text.trim();
    if (phoneInput.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("يرجى إدخال رقم الهاتف لبدء الجلسة")),
      );
      return;
    }

    // إظهار التحميل
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(
        child: CircularProgressIndicator(color: AppColors.accentGold),
      ),
    );

    try {
      // إرسال الطلب إلى بوابة المؤسسة (API Gateway) الخاصة بك
      final response = await http.post(
        Uri.parse('http://135.181.86.199:8000/api/v1/sessions/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "license_key": "AYMN-PREMIUM-LICENSE-2026",
          "session_name": "Sovereign_Mobile_Session",
          "api_id": 2040,
          "api_hash": "b18441a1ff607e10a989891a5462e627",
          "phone_number": phoneInput
        }),
      );

      // إخفاء التحميل
      if (mounted) Navigator.pop(context);

      if (response.statusCode == 200) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text("تم ربط الجلسة بالنواة بنجاح 🚀", style: TextStyle(color: Colors.greenAccent))),
          );
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => MainSovereignScreen(userAccount: phoneInput),
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("رفض النواة: ${response.statusCode}")),
          );
          // انتقال مؤقت لضمان عمل الواجهة حتى لو كان سيرفر البايثون مغلقاً
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => MainSovereignScreen(userAccount: phoneInput),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        Navigator.pop(context); // إخفاء التحميل
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("تعذر الاتصال بالسيرفر، تأكد من تشغيل النواة")),
        );
        // انتقال مؤقت لضمان عمل الواجهة
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => MainSovereignScreen(userAccount: phoneInput),
          ),
        );
      }
    }
  }

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
              const SizedBox(height: 30),
              Directionality(
                textDirection: TextDirection.ltr,
                child: TextField(
                  controller: _accountController,
                  textAlign: TextAlign.right,
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: AppColors.surface,
                    hintText: "أدخل رقم الهاتف (+967...)",
                    hintStyle: const TextStyle(color: Colors.grey),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  style: const TextStyle(color: Colors.white),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  minimumSize: const Size(double.infinity, 50),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: const Icon(Icons.power_settings_new, color: Colors.white),
                label: const Text("إطلاق الشرارة وبدء الجلسة 🚀", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                onPressed: _loginAndConnect,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class MainSovereignScreen extends StatefulWidget {
  final String userAccount;
  const MainSovereignScreen({super.key, required this.userAccount});
  
  @override
  State<MainSovereignScreen> createState() => _MainSovereignScreenState();
}

class _MainSovereignScreenState extends State<MainSovereignScreen> {
  int _currentIndex = 3; 

  late final List<Widget> _screens = [
    AccountSettingsScreen(userAccount: widget.userAccount), 
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
      appBar: AppBar(title: const Text("إدارة مجتمعاتي وأدواتي 👑", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
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

class AccountSettingsScreen extends StatelessWidget {
  final String userAccount;
  const AccountSettingsScreen({super.key, required this.userAccount});

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
                const CircleAvatar(radius: 30, backgroundColor: AppColors.primary, child: Icon(Icons.person, size: 35, color: Colors.white)),
                const SizedBox(width: 15),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("الحساب المؤسسي", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                    const SizedBox(height: 5),
                    Directionality(
                      textDirection: TextDirection.ltr,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text(userAccount, style: const TextStyle(color: Colors.greenAccent, fontSize: 14, fontWeight: FontWeight.w500)),
                      ),
                    ),
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
      body: Center(child: Text("جهات الاتصال الإمبراطورية", style: TextStyle(color: Colors.grey))),
    );
  }
}
