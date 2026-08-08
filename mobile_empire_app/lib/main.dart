// ==============================================================================
// AymnGuard Enterprise : Sovereign Super App - Modular Engine Hub (v18.5.0)
// ==============================================================================
// يدمج هذا الإصدار واجهات المراسلة مع "مركز تثبيت البوتات والخدمات" 
// مما يسمح للمالك بإضافة محركات (حماية، نقل، تصميم، بحث) مستقبلاً بضغطة زر.

import 'package:flutter/material.dart';
const String kServerUrl = "http://135.181.86.199:10050";

void main() {
  runApp(const SovereignSuperApp());
}

class SovereignSuperApp extends StatelessWidget {
  const SovereignSuperApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AymnGuard Super App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF1c242f), 
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF242f3d),
          elevation: 0,
        ),
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: Color(0xFF242f3d),
          selectedItemColor: Color(0xFF38bdf8),
          unselectedItemColor: Colors.grey,
        ),
        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: Color(0xFF38bdf8),
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
  int _currentIndex = 4; // نبدأ من لوحة السيادة لاستعراض قوة الإدارة

  final List<Widget> _screens = [
    const ProfileScreenPreview(),   
    const SettingsScreenPreview(),  
    const Center(child: Text("جهات الاتصال")), 
    const ChatListScreen(),         
    const SovereignOwnerDashboard(),// لوحة السيادة ومركز التثبيت 👑
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('الإمبراطورية متصلة...', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text('الخادم السحابي المستقل نشط', style: TextStyle(fontSize: 12, color: Colors.greenAccent)),
          ],
        ),
        actions: [
          IconButton(icon: const Icon(Icons.search), onPressed: () {}),
          Builder(
            builder: (context) => IconButton(
              icon: const Icon(Icons.more_vert),
              onPressed: () => Scaffold.of(context).openEndDrawer(), 
            ),
          ),
        ],
      ),
      
      drawer: const AccountManagerDrawer(),
      endDrawer: const AdvancedToolsDrawer(),
      body: _screens[_currentIndex],

      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'الملف'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'الإعدادات'),
          BottomNavigationBarItem(icon: Icon(Icons.perm_contact_calendar), label: 'الجهات'),
          BottomNavigationBarItem(
            icon: Badge(label: Text('١٣'), child: Icon(Icons.chat_bubble)), 
            label: 'المحادثات'
          ),
          BottomNavigationBarItem(icon: Icon(Icons.admin_panel_settings, color: Colors.amber), label: 'السيادة'),
        ],
      ),
    );
  }
}

// ==============================================================================
// 2. لوحة القيادة السيادية للمالك + زر إضافة البوتات المستقبلي
// ==============================================================================
class SovereignOwnerDashboard extends StatelessWidget {
  const SovereignOwnerDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("👑 مركز السيطرة الإمبراطورية", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.amber)),
                  SizedBox(height: 5),
                  Text("إدارة الميكروسيرفسات والبوتات النشطة", style: TextStyle(color: Colors.grey, fontSize: 12)),
                ],
              ),
              // الزر الاستراتيجي لفتح "متجر التثبيت"
              IconButton(
                icon: const Icon(Icons.add_box, color: Color(0xFF38bdf8), size: 30),
                onPressed: () {
                  showModalBottomSheet(
                    context: context,
                    isScrollControlled: true,
                    backgroundColor: Colors.transparent,
                    builder: (context) => const BotInstallerSheet(),
                  );
                },
              )
            ],
          ),
          const SizedBox(height: 20),
          
          Expanded(
            child: GridView.count(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              children: [
                _buildDashboardCard("بوت الحماية الشامل", "نشط | يحمي 45 مجموعة", Icons.security, Colors.green),
                _buildDashboardCard("النقل الذكي", "وكلاء AI يعملون بالخلفية", Icons.group_add, Colors.blue),
                _buildDashboardCard("مولد التصميمات", "جاهز لإصدار الإيصالات", Icons.brush, Colors.pink),
                _buildDashboardCard("محركات البحث", "فهرسة استخباراتية نشطة", Icons.manage_search, Colors.teal),
                _buildDashboardCard("تداول Web3", "تدقيق العقود الذكية", Icons.candlestick_chart, Colors.orange),
                _buildDashboardCard("إدارة التراخيص", "18 ترخيص مفعل", Icons.vpn_key, Colors.purple),
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget _buildDashboardCard(String title, String status, IconData icon, Color color) {
    return Card(
      color: const Color(0xFF242f3d),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      elevation: 5,
      child: InkWell(
        onTap: () {}, 
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 38, color: color),
              const SizedBox(height: 10),
              Text(title, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
              const SizedBox(height: 5),
              Text(status, textAlign: TextAlign.center, style: TextStyle(color: Colors.grey.shade400, fontSize: 10)),
            ],
          ),
        ),
      ),
    );
  }
}

// ==============================================================================
// 3. واجهة تثبيت البوتات والخدمات (Future-Proof Bot Manager)
// ==============================================================================
class BotInstallerSheet extends StatelessWidget {
  const BotInstallerSheet({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.75,
      decoration: const BoxDecoration(
        color: Color(0xFF1c242f),
        borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20)),
      ),
      child: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(15.0),
            child: Center(
              child: Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.grey, borderRadius: BorderRadius.all(Radius.circular(10)))),
            ),
          ),
          const Text("➕ متجر البوتات والخدمات السيادية", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
          const Text("تثبيت محركات جديدة دون تحديث التطبيق", style: TextStyle(color: Colors.grey, fontSize: 12)),
          const Divider(color: Colors.white24, height: 30),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              children: [
                _buildInstallableBot("بوت النقل العكسي الذكي", "أداة متقدمة لنقل الأعضاء باستخدام العمال الخلفيين.", Icons.swap_calls, isInstalled: true),
                _buildInstallableBot("محرك التدقيق الجنائي", "فحص الثغرات الأمنية في الروابط والعقود.", Icons.policy, isInstalled: false),
                _buildInstallableBot("بوت الترجمة المالية الآلي", "ترجمة فورية للمصطلحات والتقارير المالية.", Icons.translate, isInstalled: false),
                _buildInstallableBot("خدمة API خارجية جديدة", "أضف رابط الـ Webhook لبوت مخصص.", Icons.add_link, isInstalled: false, isCustom: true),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInstallableBot(String name, String desc, IconData icon, {required bool isInstalled, bool isCustom = false}) {
    return Card(
      color: const Color(0xFF242f3d),
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: isCustom ? Colors.grey.shade800 : const Color(0xFF38bdf8).withOpacity(0.2), child: Icon(icon, color: isCustom ? Colors.white : const Color(0xFF38bdf8))),
        title: Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        subtitle: Text(desc, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        trailing: isInstalled 
            ? const Icon(Icons.check_circle, color: Colors.green)
            : ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF38bdf8), foregroundColor: Colors.black, minimumSize: const Size(60, 30)),
                onPressed: () {},
                child: const Text("تثبيت", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
              ),
      ),
    );
  }
}

// ==============================================================================
// 4. القائمة الجانبية اليمنى (الأدوات السريعة للمستخدمين)
// ==============================================================================
class AdvancedToolsDrawer extends StatelessWidget {
  const AdvancedToolsDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF242f3d),
      child: SafeArea(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF1c242f)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Icon(Icons.rocket_launch, color: Colors.blueAccent, size: 40),
                  SizedBox(height: 10),
                  Text("محركات الـ Super App", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            const ListTile(leading: Icon(Icons.manage_search, color: Colors.teal), title: Text("محرك البحث المتقدم")),
            const ListTile(leading: Icon(Icons.group_add, color: Colors.blue), title: Text("أداة النقل الذكي")),
            const ListTile(leading: Icon(Icons.design_services, color: Colors.pink), title: Text("استوديو التصميم وتوليد الإيصالات")),
            const ListTile(leading: Icon(Icons.psychology, color: Colors.purple), title: Text("مساعد الذكاء الاصطناعي (AGI)")),
            const Divider(color: Colors.grey),
            const ListTile(leading: Icon(Icons.light_mode), title: Text("النمط النهاري/الليلي")),
          ],
        ),
      ),
    );
  }
}

// ==============================================================================
// 5. القائمة الجانبية اليسرى (إدارة الحسابات) و واجهات المراسلة
// ==============================================================================
class AccountManagerDrawer extends StatelessWidget {
  const AccountManagerDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF1c242f),
      child: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('إدارة الحسابات', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  IconButton(icon: const Icon(Icons.info_outline), onPressed: () {}),
                ],
              ),
            ),
            const Divider(color: Colors.grey),
            Expanded(
              child: ListView(
                children: [
                  _buildAccountTile("انا انا", "ان", true, badge: null),
                  _buildAccountTile("AymnGuard Hub", "AG", false, badge: "VIP", isImage: true),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: FloatingActionButton(backgroundColor: const Color(0xFF38bdf8), onPressed: () {}, child: const Icon(Icons.add, color: Colors.black)),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildAccountTile(String name, String initials, bool isFrozen, {String? badge, bool isImage = false}) {
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: Colors.blueGrey,
        child: isImage ? const Icon(Icons.security, size: 20) : Text(initials, style: const TextStyle(color: Colors.white)),
      ),
      title: Text(name),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (badge != null)
            Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4), decoration: BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(12)), child: Text(badge, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold))),
          if (isFrozen) const Padding(padding: EdgeInsets.only(left: 8.0), child: Icon(Icons.ac_unit, color: Colors.lightBlueAccent, size: 20)),
          const SizedBox(width: 10),
          const Icon(Icons.settings, color: Colors.grey, size: 20),
        ],
      ),
      onTap: () {},
    );
  }
}

class ChatListScreen extends StatelessWidget {
  const ChatListScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        const ListTile(
          leading: CircleAvatar(backgroundColor: Colors.blue, child: Icon(Icons.security)),
          title: Text("درع الأمان | AymnGuard"), 
          subtitle: Text("💎 تم تشغيل درع الحماية بنجاح."),
        ),
      ],
    );
  }
}
class SettingsScreenPreview extends StatelessWidget { const SettingsScreenPreview({super.key}); @override Widget build(BuildContext context) { return const Center(child: Text("شاشة الإعدادات", style: TextStyle(color: Colors.grey))); } }
class ProfileScreenPreview extends StatelessWidget { const ProfileScreenPreview({super.key}); @override Widget build(BuildContext context) { return const Center(child: Text("شاشة الملف الشخصي", style: TextStyle(color: Colors.grey))); } }
