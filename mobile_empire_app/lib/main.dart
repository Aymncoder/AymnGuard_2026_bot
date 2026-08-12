// -*- coding: utf-8 -*-
/// ==============================================================================
/// AymnGuard Sovereign Enterprise : Main Application Entry Point v35.1 (Hardened Core)
/// ==============================================================================

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'app_config.dart';
import 'core/backend_ecosystem.dart';
import 'sovereign_card.dart';
import 'package:mobile_empire_app/premium_dashboard_screens.dart';
import 'package:mobile_empire_app/app_drawers.dart';
import 'package:mobile_empire_app/models/bot_model.dart';
import 'package:mobile_empire_app/neural_core_screen.dart';

void main() {
  // صندوق حماية عالمي لالتقاط أي استثناء قاتل ومنع الانهيار الفوري
  runZonedGuarded(() async {
    // 1. ربط فلاتر بنظام أندرويد قبل إطلاق أي واجهة أو خدمة
    WidgetsFlutterBinding.ensureInitialized();

    runApp(const AymnGuardPlusApp());
  }, (error, stackTrace) {
    debugPrint('🚨 [Sovereign Fatal Catch]: $error');
  });
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

// ==============================================================================
// 1. بوابة الدخول السيادية (Account Login Gateway)
// ==============================================================================
class AccountLoginGatewayScreen extends StatefulWidget {
  const AccountLoginGatewayScreen({super.key});

  @override
  State<AccountLoginGatewayScreen> createState() => _AccountLoginGatewayScreenState();
}

class _AccountLoginGatewayScreenState extends State<AccountLoginGatewayScreen> {
  final TextEditingController _phoneController = TextEditingController();
  String _selectedCountryName = "اليمن";
  String _selectedCountryCode = "+967";

  final List<Map<String, String>> _countriesList = [
    {'name': 'اليمن', 'code': '+967', 'flag': '🇾🇪'},
    {'name': 'المملكة العربية السعودية', 'code': '+966', 'flag': '🇸🇦'},
    {'name': 'مصر', 'code': '+20', 'flag': '🇪🇬'},
    {'name': 'الإمارات العربية المتحدة', 'code': '+971', 'flag': '🇦🇪'},
    {'name': 'الكويت', 'code': '+965', 'flag': '🇰🇼'},
    {'name': 'قطر', 'code': '+974', 'flag': '🇶🇦'},
    {'name': 'سلطنة عمان', 'code': '+968', 'flag': '🇴🇲'},
    {'name': 'البحرين', 'code': '+973', 'flag': '🇧🇭'},
    {'name': 'الأردن', 'code': '+962', 'flag': '🇯🇴'},
    {'name': 'فلسطين', 'code': '+970', 'flag': '🇵🇸'},
    {'name': 'العراق', 'code': '+964', 'flag': '🇮🇶'},
    {'name': 'سوريا', 'code': '+963', 'flag': '🇸🇾'},
    {'name': 'لبنان', 'code': '+961', 'flag': '🇱🇧'},
    {'name': 'السودان', 'code': '+249', 'flag': '🇸🇩'},
    {'name': 'ليبيا', 'code': '+218', 'flag': '🇱🇾'},
    {'name': 'تونس', 'code': '+216', 'flag': '🇹🇳'},
    {'name': 'الجزائر', 'code': '+213', 'flag': '🇩🇿'},
    {'name': 'المغرب', 'code': '+212', 'flag': '🇲🇦'},
    {'name': 'موريتانيا', 'code': '+222', 'flag': '🇲🇷'},
    {'name': 'الصومال', 'code': '+252', 'flag': '🇸🇴'},
    {'name': 'جيبوتي', 'code': '+253', 'flag': '🇩🇯'},
    {'name': 'جزر القمر', 'code': '+269', 'flag': '🇰🇲'},
  ];

  void _openCountryPicker() {
    List<Map<String, String>> filteredList = List.from(_countriesList);

    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.background,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return Container(
              height: MediaQuery.of(context).size.height * 0.75,
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  TextField(
                    style: const TextStyle(color: Colors.white),
                    onChanged: (query) {
                      setModalState(() {
                        if (query.isEmpty) {
                          filteredList = List.from(_countriesList);
                        } else {
                          filteredList = _countriesList.where((c) => c['name']!.contains(query) || c['code']!.contains(query)).toList();
                        }
                      });
                    },
                    decoration: InputDecoration(
                      hintText: "ابحث عن الدولة أو المفتاح الدولي...",
                      hintStyle: const TextStyle(color: Colors.grey),
                      prefixIcon: const Icon(Icons.search, color: AppColors.accentGold),
                      filled: true,
                      fillColor: AppColors.surface,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Expanded(
                    child: ListView.builder(
                      itemCount: filteredList.length,
                      itemBuilder: (context, index) {
                        var country = filteredList[index];
                        return ListTile(
                          leading: Text(country['flag']!, style: const TextStyle(fontSize: 24)),
                          title: Text(country['name']!, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          trailing: Text(country['code']!, style: const TextStyle(color: AppColors.accentGold, fontWeight: FontWeight.bold)),
                          onTap: () {
                            setState(() {
                              _selectedCountryName = country['name']!;
                              _selectedCountryCode = country['code']!;
                            });
                            Navigator.pop(context);
                          },
                        );
                      },
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  Future<void> _loginAndConnect() async {
    String rawPhone = _phoneController.text.trim();
    if (rawPhone.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("يرجى إدخال رقم الهاتف لبدء الجلسة")));
      return;
    }

    if (rawPhone.startsWith('0')) rawPhone = rawPhone.substring(1);
    String fullPhoneNumber = "$_selectedCountryCode$rawPhone";

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(child: CircularProgressIndicator(color: AppColors.accentGold)),
    );

    try {
      var response = await BackendCoreEcosystem.requestTelegramOtp("AymnGuard_Session", fullPhoneNumber, 2040, "b18441a1ff607e10a989891a5462e627");

      if (mounted) Navigator.pop(context);

      if (response['error'] == true) {
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("تعذر الاتصال: ${response['message']}")));
      } else {
        if (mounted) {
          Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => MainSovereignScreen(userAccount: fullPhoneNumber)));
        }
      }
    } catch (e) {
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("خطأ في الاتصال: $e")));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [IconButton(icon: const Icon(Icons.security, color: AppColors.accentGold), onPressed: () {})],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("رقم هاتفك", style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 8),
            const Text("يرجى تأكيد مفتاح بلدك وإدخال رقم هاتفك للاتصال بالمنصة السيادية.", style: TextStyle(color: Colors.grey, fontSize: 13)),
            const SizedBox(height: 30),
            GestureDetector(
              onTap: _openCountryPicker,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(12), border: Border.all(color: AppColors.accentGold.withOpacity(0.3))),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text("الدولة: $_selectedCountryName ($_selectedCountryCode)", style: const TextStyle(color: Colors.white, fontSize: 16)),
                    const Icon(Icons.arrow_forward_ios, size: 16, color: AppColors.accentGold),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Directionality(
              textDirection: TextDirection.ltr,
              child: TextField(
                controller: _phoneController,
                keyboardType: TextInputType.phone,
                textAlign: TextAlign.right,
                style: const TextStyle(color: Colors.white, fontSize: 18),
                decoration: InputDecoration(
                  labelText: "رقم الهاتف",
                  labelStyle: const TextStyle(color: Colors.grey),
                  filled: true,
                  fillColor: AppColors.surface,
                  prefixText: "$_selectedCountryCode ",
                  prefixStyle: const TextStyle(color: AppColors.accentGold, fontSize: 18, fontWeight: FontWeight.bold),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
            const Spacer(),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary, minimumSize: const Size(double.infinity, 50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              onPressed: _loginAndConnect,
              child: const Text("إطلاق الجلسة وبدء الاتصال 🚀", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}

// ==============================================================================
// 2. المحرك الرئيسي (Main Screen)
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
    return Scaffold(
      extendBody: true,
      backgroundColor: Colors.transparent, 
      appBar: AppBar(
        backgroundColor: Colors.transparent, elevation: 0,
        leading: Builder(builder: (c) => IconButton(icon: const Icon(Icons.manage_accounts_rounded, color: AppColors.accentGold, size: 28), onPressed: () => Scaffold.of(c).openDrawer())),
        actions: [Builder(builder: (c) => IconButton(icon: const Icon(Icons.handyman_rounded, color: AppColors.accentGold, size: 26), onPressed: () => Scaffold.of(c).openEndDrawer()))],
      ),
      drawer: const MultiAccountDrawer(),     
      endDrawer: const AdvancedToolsDrawer(), 
      body: CyberEnterpriseBackground(
        child: IndexedStack(
          index: _currentIndex,
          children: [
            AccountSettingsScreen(userAccount: widget.userAccount), 
            const EmpirePremiumStore(),                             
            const ContactsScreen(),                                 
            const SovereignDashboardTab(),                          
            if (AppConfig.isOwnerStatus) const UltimateOwnerDashboard(), 
          ],
        ),
      ), 
      bottomNavigationBar: SafeArea(child: Padding(padding: const EdgeInsets.only(left: 16, right: 16, bottom: 16), child: FloatingGlassyNavBar(currentIndex: _currentIndex, onTap: (i) => setState(() => _currentIndex = i)))),
    );
  }
}

// ==============================================================================
// 3. الواجهة السيادية المدمجة
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
          const Text('THE COMMAND HUB', style: TextStyle(color: Color(0xFFD4AF37), fontSize: 13, fontWeight: FontWeight.bold, letterSpacing: 1.5)),
          const SizedBox(height: 12),
          GridView.count(
            shrinkWrap: true, physics: const NeverScrollableScrollPhysics(), crossAxisCount: 2, crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.3,
            children: [
              _buildButton(context, 'نقل الأعضاء', Icons.move_up_rounded, const Color(0xFFE83845), () => Scaffold.of(context).openDrawer()),
              _buildButton(context, 'بوت الحماية', Icons.shield_rounded, const Color(0xFF8A2BE2), () => launchUrl(Uri.parse('https://t.me/AymnGuard_2026_bot'), mode: LaunchMode.externalApplication)),
              _buildButton(context, 'المحادثات', Icons.telegram, const Color(0xFF2FA4E7), () => Navigator.push(context, MaterialPageRoute(builder: (context) => const TelegramCoreChatsScreen()))),
              _buildButton(context, 'تصميم الإيصالات', Icons.receipt_long_rounded, const Color(0xFFD4AF37), () => Scaffold.of(context).openEndDrawer()),
              _buildButton(context, 'قناة التحديثات', Icons.campaign_rounded, const Color(0xFFE2A12B), () => launchUrl(Uri.parse('https://t.me/AymnGuardChat'), mode: LaunchMode.externalApplication)),
              _buildButton(context, 'مجموعة الدعم', Icons.group, const Color(0xFF3FB950), () => launchUrl(Uri.parse('https://t.me/AymnGuard'), mode: LaunchMode.externalApplication)),
            ],
          ),
          const SizedBox(height: 100),
        ],
      ),
    );
  }

  Widget _buildButton(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(onTap: onTap, child: Container(decoration: BoxDecoration(color: const Color(0xFF161B22).withOpacity(0.7), borderRadius: BorderRadius.circular(14), border: Border.all(color: Colors.white.withOpacity(0.08))), padding: const EdgeInsets.all(16), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(icon, color: color, size: 30), const SizedBox(height: 10), Text(title, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold))])));
  }
}

// ==============================================================================
// 4. المحرك البصري (تشغيل صورتك الخاصة كخلفية)
// ==============================================================================
class CyberEnterpriseBackground extends StatelessWidget {
  final Widget child;
  const CyberEnterpriseBackground({Key? key, required this.child}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      height: double.infinity,
      decoration: const BoxDecoration(
        // سحب الصورة التي قمت برفعها مسبقاً
        image: DecorationImage(
          image: AssetImage('assets/images/bg.jpg'),
          fit: BoxFit.cover, // لتتمدد الصورة وتغطي الشاشة بالكامل
          // تعتيم خفيف جداً فوق الصورة لكي تظل النصوص واضحة ومقروءة
          colorFilter: ColorFilter.mode(Colors.black54, BlendMode.darken),
        ),
      ),
      child: SafeArea(child: child),
    );
  }
}

// ==============================================================================
// 5. العناصر الجمالية المتبقية
// ==============================================================================
class SovereignBrandingHeader extends StatelessWidget {
  const SovereignBrandingHeader({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 24.0, horizontal: 16.0),
      decoration: BoxDecoration(color: const Color(0xFF0D1117), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFD4AF37).withOpacity(0.3), width: 1)),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(shape: BoxShape.circle, gradient: LinearGradient(colors: [const Color(0xFFD4AF37).withOpacity(0.4), const Color(0xFF1A1F2C)], begin: Alignment.topLeft, end: Alignment.bottomRight), boxShadow: [BoxShadow(color: const Color(0xFFD4AF37).withOpacity(0.3), blurRadius: 15, spreadRadius: 2)], border: Border.all(color: const Color(0xFFD4AF37), width: 2)),
            child: const Icon(Icons.security_rounded, size: 40, color: Color(0xFFF3C68F)),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text('AymnGuard', style: TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold, letterSpacing: 2.0, shadows: [Shadow(color: Colors.white.withOpacity(0.4), blurRadius: 8)])),
              const SizedBox(width: 8),
              Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4), decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFFBF953F), Color(0xFFFCF6BA), Color(0xFFB38728)]), borderRadius: BorderRadius.circular(6), boxShadow: [BoxShadow(color: const Color(0xFFD4AF37).withOpacity(0.5), blurRadius: 6)]), child: const Text('PLUS', style: TextStyle(color: Color(0xFF1A1A1A), fontSize: 12, fontWeight: FontWeight.w900, letterSpacing: 1.0))),
            ],
          ),
          const SizedBox(height: 8),
          Text('Sovereign Enterprise Security & Core Architecture', textAlign: TextAlign.center, style: TextStyle(color: Colors.grey[400], fontSize: 11, fontWeight: FontWeight.w300, letterSpacing: 1.2)),
        ],
      ),
    );
  }
}

class SovereignStatusBanner extends StatelessWidget {
  const SovereignStatusBanner({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(color: const Color(0xFF161B22), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF238636).withOpacity(0.5), width: 1), boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.4), blurRadius: 8, offset: const Offset(0, 4))]),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(children: [Container(width: 12, height: 12, decoration: const BoxDecoration(color: Color(0xFF238636), shape: BoxShape.circle, boxShadow: [BoxShadow(color: Color(0xFF238636), blurRadius: 8, spreadRadius: 2)])), const SizedBox(width: 12), const Text('CORE SYSTEM STATUS', style: TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.w600, letterSpacing: 1.0))]),
          const Text('SECURE & OPERATIONAL 100%', style: TextStyle(color: Color(0xFF3FB950), fontSize: 11, fontWeight: FontWeight.bold, letterSpacing: 0.5)),
        ],
      ),
    );
  }
}

class FloatingGlassyNavBar extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;
  const FloatingGlassyNavBar({Key? key, required this.currentIndex, required this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70, padding: const EdgeInsets.symmetric(horizontal: 12),
      decoration: BoxDecoration(color: const Color(0xFF161B22).withOpacity(0.85), borderRadius: BorderRadius.circular(25), border: Border.all(color: const Color(0xFFD4AF37).withOpacity(0.3), width: 1.5), boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 15, spreadRadius: 2, offset: const Offset(0, 5))]),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _navItem(0, Icons.settings_rounded, 'الإعدادات'),
          _navItem(1, Icons.store_rounded, 'متجر البوتات'),
          _navItem(2, Icons.contacts_rounded, 'جهات الاتصال'),
          _navItem(3, Icons.dashboard_rounded, 'الرئيسية'),
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
        decoration: BoxDecoration(color: isSelected ? const Color(0xFFD4AF37).withOpacity(0.2) : Colors.transparent, borderRadius: BorderRadius.circular(16)),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: isSelected ? const Color(0xFFF3C68F) : Colors.grey[500], size: 24),
            if (isSelected) Padding(padding: const EdgeInsets.only(right: 6), child: Text(label, style: const TextStyle(color: Color(0xFFF3C68F), fontSize: 12, fontWeight: FontWeight.bold))),
          ],
        ),
      ),
    );
  }
}

class TelegramCoreChatsScreen extends StatelessWidget {
  const TelegramCoreChatsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('محادثات وبوتات تليجرام السيادية 🛡️', style: TextStyle(fontSize: 18))),
      body: ListView(padding: const EdgeInsets.all(16), children: const [ListTile(leading: CircleAvatar(backgroundColor: Colors.purple, child: Icon(Icons.smart_toy, color: Colors.white)), title: Text('AymnGuard 2026 Bot', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)), subtitle: Text('إدارة العمليات والأمان السيادي', style: TextStyle(color: Colors.grey)))]),
    );
  }
}

class AccountSettingsScreen extends StatelessWidget {
  final String userAccount;
  const AccountSettingsScreen({super.key, required this.userAccount});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: ListView(
        padding: const EdgeInsets.only(top: 24, left: 16, right: 16, bottom: 100),
        children: [
          const SovereignEnterpriseBanner(),
          const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.all(16), decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(12)),
            child: Row(children: [const CircleAvatar(radius: 30, backgroundColor: AppColors.primary, child: Icon(Icons.person, size: 35, color: Colors.white)), const SizedBox(width: 15), Column(crossAxisAlignment: CrossAxisAlignment.start, children: [const Text("الحساب المؤسسي", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)), const SizedBox(height: 5), Directionality(textDirection: TextDirection.ltr, child: Container(alignment: Alignment.centerLeft, child: Text(userAccount, style: const TextStyle(color: Colors.greenAccent, fontSize: 14, fontWeight: FontWeight.w500))))])]),
          ),
        ],
      ),
    );
  }
}

class SovereignEnterpriseBanner extends StatelessWidget {
  const SovereignEnterpriseBanner({super.key});
  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity, padding: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFF0A192F), Color(0xFF050505)], begin: Alignment.topLeft, end: Alignment.bottomRight), borderRadius: BorderRadius.circular(20), border: Border.all(color: const Color(0xFFD4AF37).withOpacity(0.5), width: 1.5), boxShadow: [BoxShadow(color: const Color(0xFF0A192F).withOpacity(0.8), blurRadius: 15, spreadRadius: 2, offset: const Offset(0, 8))]),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(padding: const EdgeInsets.all(16), decoration: BoxDecoration(shape: BoxShape.circle, color: const Color(0xFFD4AF37).withOpacity(0.1), border: Border.all(color: const Color(0xFFD4AF37), width: 2)), child: const Icon(Icons.shield_rounded, size: 50, color: Color(0xFFD4AF37))),
          const SizedBox(height: 16), const Text("AymnGuard Plus", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 1.2)), const SizedBox(height: 6), const Text("Sovereign Enterprise Security & Core Architecture", textAlign: TextAlign.center, style: TextStyle(fontSize: 12, color: Colors.grey, letterSpacing: 0.8)), const SizedBox(height: 20),
          Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6), decoration: BoxDecoration(color: Colors.greenAccent.withOpacity(0.1), borderRadius: BorderRadius.circular(30), border: Border.all(color: Colors.greenAccent.withOpacity(0.3))), child: const Row(mainAxisSize: MainAxisSize.min, children: [Icon(Icons.verified, size: 14, color: Colors.greenAccent), SizedBox(width: 6), Text("SECURE & OPERATIONAL 100%", style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.greenAccent))])),
        ],
      ),
    );
  }
}

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return const Scaffold(backgroundColor: Colors.transparent, body: Center(child: Text("جهات الاتصال الإمبراطورية", style: TextStyle(color: Colors.grey))));
  }
}
