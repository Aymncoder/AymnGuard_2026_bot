import 'package:flutter/material.dart';
import 'app_config.dart';
import 'core/backend_ecosystem.dart';

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
      // 🚀 الاتصال الفعلي بـ auth_manager.py عبر النظام البيئي الموحد
      var response = await BackendCoreEcosystem.requestTelegramOtp(
        "Sovereign_Mobile_Session",
        phoneInput,
        2040,
        "b18441a1ff607e10a989891a5462e627"
      );

      // إخفاء التحميل
      if (mounted) Navigator.pop(context);

      if (response['error'] == true) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("تعذر الاتصال أو رفض النواة: ${response['message']}")),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("تم إرسال كود التحقق عبر: ${response['delivery_method']} 🚀", style: const TextStyle(color: Colors.greenAccent))),
          );
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
          SnackBar(content: Text("عطل في الشبكة أو السيرفر مغلق: $e")),
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

// تأكد من استيراد ملفات الألوان (AppColors) الخاصة بك هنا

class CommunitiesScreenTab extends StatelessWidget {
  const CommunitiesScreenTab({super.key});

  @override
  Widget build(BuildContext context) {
    // تم إصلاح وتثبيت قائمة الكيانات السيادية
    final List<Map<String, dynamic>> sovereignGroups = [
      {
        'title': 'قنواتي ومجموعاتي السيادية',
        'subtitle': 'أنت المالك • 5,430 عضو • مجموعة VIP',
        'icon': Icons.group,
        'color': Colors.amber,
      },
      {
        'title': 'حملات AymnGuard',
        'subtitle': 'أنت المالك • 12,000 مشترك • قناة ترويجية',
        'icon': Icons.campaign,
        'color': Colors.blueAccent,
      },
    ];

    // قائمة فئات واجهات المراسلة وإدارة المنصة
    final List<Map<String, dynamic>> communicationCategories = [
      {
        'title': 'الرسائل الخاصة',
        'subtitle': 'تصل هنا كافة الرسائل المباشرة والمشفرة',
        'icon': Icons.chat,
        'color': Colors.green,
      },
      {
        'title': 'واجهة البوتات (Bots)',
        'subtitle': 'إدارة وتوجيه الروبوتات والذكاء الاصطناعي',
        'icon': Icons.smart_toy,
        'color': Colors.purple,
      },
      {
        'title': 'واجهة المجموعات',
        'subtitle': 'إدارة النقاشات والمجتمعات التفاعلية',
        'icon': Icons.forum,
        'color': Colors.orange,
      },
      {
        'title': 'واجهة القنوات',
        'subtitle': 'منصات البث المباشر والإعلانات السيادية',
        'icon': Icons.cell_tower,
        'color': Colors.redAccent,
      },
      {
        'title': 'الرسائل المحفوظة (الملف الشخصي)',
        'subtitle': 'مساحتك الخاصة لحفظ الرسائل والملفات المهمة',
        'icon': Icons.bookmark,
        'color': Colors.teal,
      },
      {
        'title': 'المحادثات المؤرشفة',
        'subtitle': 'سجل المحادثات والمجموعات المخفية مؤقتاً',
        'icon': Icons.archive,
        'color': Colors.grey,
      },
    ];

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('إدارة مجتمعاتي وأدواتي 👑', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          // القسم الأول: المجموعات والقنوات الإدارية السيادية (تم تثبيتها)
          const Text("القنوات والمجموعات النشطة", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          ...sovereignGroups.map((group) => _buildCard(
                context,
                group['title'] ?? '',
                group['subtitle'] ?? '',
                group['icon'] ?? Icons.circle,
                group['color'] ?? Colors.grey,
              )),
              
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16.0),
            child: Divider(color: Colors.white24, thickness: 1),
          ),

          // القسم الثاني: واجهات المراسلة المتكاملة والتصنيفات الجديدة
          const Text("بوابات الاتصال والمراسلة", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          ...communicationCategories.map((category) => _buildCard(
                context,
                category['title'] ?? '',
                category['subtitle'] ?? '',
                category['icon'] ?? Icons.chat,
                category['color'] ?? Colors.grey,
              )),
        ],
      ),
    );
  }

  Widget _buildCard(BuildContext context, String title, String subtitle, IconData icon, Color color) {
    return Card(
      color: AppColors.surface, // تأكد من تعريف AppColors.surface
      margin: const EdgeInsets.symmetric(vertical: 6),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.2), child: Icon(icon, color: color)),
        title: Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)), // لون النص أبيض ليتناسب مع الوضع الداكن
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
        trailing: const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
        onTap: () {
          // هنا يتم توجيه المستخدم إلى الشاشة المخصصة عند الضغط
          // مثال: Navigator.push(context, MaterialPageRoute(builder: (context) => PrivateMessagesScreen()));
        },
      ),
    );
  }
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
        padding: const EdgeInsets.all(16),
        children: [
          // 👈 اللافتة المؤسسية الفاخرة في أعلى شاشة الإعدادات
          const SovereignEnterpriseBanner(),
          const SizedBox(height: 20),
          Container(
            color: AppColors.surface,
            padding: const EdgeInsets.all(16),
            child: Row(
              children: 
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
/// 🏛️ مكون اللافتة المؤسسية السيادية
class SovereignEnterpriseBanner extends StatelessWidget {
  const SovereignEnterpriseBanner({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF0A192F), Color(0xFF050505)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFD4AF37).withOpacity(0.5), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF0A192F).withOpacity(0.8),
            blurRadius: 15,
            spreadRadius: 2,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: const Color(0xFFD4AF37).withOpacity(0.1),
              border: Border.all(color: const Color(0xFFD4AF37), width: 2),
            ),
            child: const Icon(
              Icons.shield_rounded,
              size: 50,
              color: Color(0xFFD4AF37),
            ),
          ),
          const SizedBox(height: 16),
          const Text(
            "AymnGuard Plus",
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
              letterSpacing: 1.2,
            ),
          ),
          const SizedBox(height: 6),
          const Text(
            "Sovereign Enterprise Security & Core Architecture",
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey,
              letterSpacing: 0.8,
            ),
          ),
          const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.greenAccent.withOpacity(0.1),
              borderRadius: BorderRadius.circular(30),
              border: Border.all(color: Colors.greenAccent.withOpacity(0.3)),
            ),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: 
                Icon(Icons.verified, size: 14, color: Colors.greenAccent),
                SizedBox(width: 6),
                Text(
                  "SECURE & OPERATIONAL 100%",
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    color: Colors.greenAccent,
                  ),
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
