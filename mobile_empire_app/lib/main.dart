// -*- coding: utf-8 -*-
/// ==============================================================================
/// AymnGuard Sovereign Enterprise : Main Application Entry Point v34.5
/// ==============================================================================

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
      home: const SovereignDashboardScreen(),
    );
  }
}

// ==============================================================================
// Sovereign Dashboard Screen & Empire Components
// ==============================================================================

class SovereignDashboardScreen extends StatefulWidget {
  const SovereignDashboardScreen({Key? key}) : super(key: key);

  @override
  State<SovereignDashboardScreen> createState() => _SovereignDashboardScreenState();
}

class _SovereignDashboardScreenState extends State<SovereignDashboardScreen> {
  int _currentIndex = 3;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Stack(
          children: [
            SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // 🌟 الشعار الإمبراطوري في قمة الشاشة
                  const SovereignBrandingHeader(),
                  
                  const SizedBox(height: 20),

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
                  
                  const SizedBox(height: 100),
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

class SovereignBrandingHeader extends StatelessWidget {
  const SovereignBrandingHeader({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 24.0, horizontal: 16.0),
      decoration: BoxDecoration(
        color: const Color(0xFF0D1117),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: const Color(0xFFD4AF37).withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
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
              color: Color(0xFFF3C68F),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
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
          color: const Color(0xFF238636).withOpacity(0.5),
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
      itemCount: hubs.length,
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
          color: const Color(0xFFD4AF37).withOpacity(0.3),
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

// ==============================================================================
// Original Application Screens & Gateways (Preserved Intact)
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
  bool _syncContacts = false;

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
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
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
                          filteredList = _countriesList.where((c) => 
                            c['name']!.toLowerCase().contains(query.toLowerCase()) || 
                            c['code']!.contains(query)
                          ).toList();
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
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("يرجى إدخال رقم الهاتف لبدء الجلسة")),
      );
      return;
    }

    if (rawPhone.startsWith('0')) rawPhone = rawPhone.substring(1);
    String fullPhoneNumber = "$_selectedCountryCode$rawPhone";

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(
        child: CircularProgressIndicator(color: AppColors.accentGold),
      ),
    );

    try {
      var response = await BackendCoreEcosystem.requestTelegramOtp(
        "AymnGuard_Sovereign_Proxy_Session",
        fullPhoneNumber,
        2040,
        "b18441a1ff607e10a989891a5462e627"
      );

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
            SnackBar(content: Text("تم إرسال كود التحقق بنجاح إلى: $fullPhoneNumber 🚀", style: const TextStyle(color: Colors.greenAccent))),
          );
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => MainSovereignScreen(userAccount: fullPhoneNumber),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("خطأ في الاتصال بالبروكسي أو السيرفر: $e")),
        );
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
        actions: [
          IconButton(
            icon: const Icon(Icons.security, color: AppColors.accentGold),
            onPressed: () {},
          ),
        ],
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
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.accentGold.withOpacity(0.3)),
                ),
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
            const SizedBox(height: 16),
            Row(
              children: [
                Checkbox(
                  value: _syncContacts,
                  activeColor: AppColors.primary,
                  onChanged: (val) {
                    setState(() {
                      _syncContacts = val ?? false;
                    });
                  },
                ),
                const Text("مزامنة جهات الاتصال", style: TextStyle(color: Colors.white70, fontSize: 14)),
              ],
            ),
            const Spacer(),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                minimumSize: const Size(double.infinity, 50),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              onPressed: _loginAndConnect,
              child: const Text("إطلاق الجلسة وبدء الاتصال 🚀", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
            ),
          ],
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

  Future<void> _launchSovereignUrl(String urlString) async {
    final Uri url = Uri.parse(urlString);
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      throw Exception('تعذر فتح الرابط: $urlString');
    }
  }

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> sovereignGroups = [
      {
        'title': 'قناة التحديثات الرسمية',
        'role': 'المالك • قناة البث السيادي',
        'members': 'AymnGuardChat',
        'type': 'قناة عامة',
        'icon': Icons.campaign,
        'color': Colors.amber,
        'link': 'https://t.me/AymnGuardChat',
      },
      {
        'title': 'مجموعة الدعم الفني',
        'role': 'المشرف العام • مجتمع النقاش',
        'members': 'AymnGuard',
        'type': 'مجموعة VIP',
        'icon': Icons.group,
        'color': Colors.blueAccent,
        'link': 'https://t.me/AymnGuard',
      },
    ];

    final List<Map<String, dynamic>> communicationCategories = [
      {
        'title': 'بوت الحماية والسيادة',
        'subtitle': '@AymnGuard_2026_bot • إدارة العمليات والأمان',
        'icon': Icons.smart_toy,
        'color': Colors.purple,
        'link': 'https://t.me/AymnGuard_2026_bot',
      },
      {
        'title': 'الرسائل الخاصة والمشفرة',
        'subtitle': 'تصل هنا كافة الرسائل المباشرة والمؤمنة',
        'icon': Icons.chat,
        'color': Colors.green,
        'link': '',
      },
      {
        'title': 'واجهة المجموعات',
        'subtitle': 'إدارة النقاشات والمجتمعات التفاعلية',
        'icon': Icons.forum,
        'color': Colors.orange,
        'link': '',
      },
      {
        'title': 'واجهة القنوات',
        'subtitle': 'منصات البث المباشر والإعلانات السيادية',
        'icon': Icons.cell_tower,
        'color': Colors.redAccent,
        'link': '',
      },
      {
        'title': 'الرسائل المحفوظة (الملف الشخصي)',
        'subtitle': 'مساحتك الخاصة لحفظ الرسائل والملفات المهمة',
        'icon': Icons.bookmark,
        'color': Colors.teal,
        'link': '',
      },
      {
        'title': 'المحادثات المؤرشفة',
        'subtitle': 'سجل المحادثات والمجموعات المخفية مؤقتاً',
        'icon': Icons.archive,
        'color': Colors.grey,
        'link': '',
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
          const Text("القنوات والمجموعات النشطة", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          ...sovereignGroups.map((group) => _buildCustomCard(
                context,
                group['title'],
                "${group['role']} • ${group['members']} • ${group['type']}",
                group['icon'],
                group['color'],
                () => _launchSovereignUrl(group['link']),
              )),
              
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16.0),
            child: Divider(color: Colors.white24, thickness: 1),
          ),

          const Text("بوابات الاتصال والمراسلة", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          ...communicationCategories.map((category) => _buildCustomCard(
                context,
                category['title'],
                category['subtitle'],
                category['icon'],
                category['color'],
                () {
                  if (category['link'].isNotEmpty) {
                    _launchSovereignUrl(category['link']);
                  } else {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const TelegramCoreChatsScreen(),
                      ),
                    );
                  }
                },
              )),
        ],
      ),
    );
  }

  Widget _buildCustomCard(BuildContext context, String title, String subtitle, IconData icon, Color color, VoidCallback onTapAction) {
    return SovereignCard(
      onTap: onTapAction,
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: color.withOpacity(0.2), 
            child: Icon(icon, color: color),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title, 
                  style: const TextStyle(
                    color: Colors.white, 
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 4),
                Directionality(
                  textDirection: TextDirection.rtl,
                  child: Text(
                    subtitle, 
                    style: const TextStyle(
                      color: Colors.grey, 
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const Icon(
            Icons.arrow_forward_ios, 
            size: 14, 
            color: AppColors.accentGold,
          ),
        ],
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
      appBar: AppBar(
        title: const Text('محادثات وبوتات تليجرام السيادية 🛡️', style: TextStyle(fontSize: 18)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          ListTile(
            leading: CircleAvatar(backgroundColor: Colors.purple, child: Icon(Icons.smart_toy, color: Colors.white)),
            title: Text('AymnGuard 2026 Bot', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            subtitle: Text('إدارة العمليات والأمان السيادي', style: TextStyle(color: Colors.grey)),
          ),
        ],
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
          const SovereignEnterpriseBanner(),
          const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(12),
            ),
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
              children: [
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
