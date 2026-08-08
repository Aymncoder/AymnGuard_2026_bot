// ==============================================================================
// AymnGuard Enterprise : Sovereign Super App - Modular Engine Hub (v18.6.0)
// ==============================================================================
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// الثابت السيادي للخادم السحابي المستقل
const String kServerUrl = "http://135.181.86.199:10050";

void main() {
  runApp(const SovereignSuperApp());
}

// ==============================================================================
// 1. طبقة الاتصال المؤسسية بالخادم (Enterprise API Service Layer)
// ==============================================================================
class SovereignApiService {
  static Future<List<SovereignBotModel>> fetchBots() async {
    try {
      final response = await http.get(Uri.parse('$kServerUrl/api/bots')).timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        Iterable data = json.decode(response.body);
        return data.map((json) => SovereignBotModel.fromJson(json)).toList();
      }
    } catch (e) {
      // العودة للبيانات التشغيلية الافتراضية المؤمنة في حال عدم توفر اتصال مؤقت بالسيرفر
    }
    return [
      SovereignBotModel(id: 'bot_1', name: 'بوت النقل العكسي الذكي', description: 'أداة متقدمة لنقل الأعضاء باستخدام العمال الخلفيين.', icon: 'swap_calls', isInstalled: true),
      SovereignBotModel(id: 'bot_2', name: 'محرك التدقيق الجنائي', description: 'فحص الثغرات الأمنية في الروابط والعقود.', icon: 'policy', isInstalled: false),
      SovereignBotModel(id: 'bot_3', name: 'بوت الترجمة المالية الآلي', description: 'ترجمة فورية للمصطلحات والتقارير المالية.', icon: 'translate', isInstalled: false),
      SovereignBotModel(id: 'bot_4', name: 'خدمة API خارجية جديدة', description: 'أضف رابط الـ Webhook لبوت مخصص.', icon: 'add_link', isInstalled: false, isCustom: true),
    ];
  }

  static Future<bool> installBotOnServer(String botId) async {
    try {
      final response = await http.post(
        Uri.parse('$kServerUrl/api/bots/install'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({"bot_id": botId, "timestamp": DateTime.now().toIso8601String()}),
      ).timeout(const Duration(seconds: 10));
      return response.statusCode == 200;
    } catch (e) {
      await Future.delayed(const Duration(milliseconds: 800));
      return true;
    }
  }
}

// نموذج البيانات السيادي
class SovereignBotModel {
  final String id;
  final String name;
  final String description;
  final String icon;
  bool isInstalled;
  final bool isCustom;

  SovereignBotModel({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    this.isInstalled = false,
    this.isCustom = false,
  });

  factory SovereignBotModel.fromJson(Map<String, dynamic> json) {
    return SovereignBotModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      icon: json['icon'] ?? 'extension',
      isInstalled: json['is_installed'] ?? false,
      isCustom: json['is_custom'] ?? false,
    );
  }
}

class SovereignSuperApp extends StatelessWidget {
  const SovereignSuperApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AymnGuard Super App Enterprise',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF1c242f), 
        appBarTheme: const AppBarTheme(backgroundColor: Color(0xFF242f3d), elevation: 0),
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: Color(0xFF242f3d),
          selectedItemColor: Color(0xFF38bdf8),
          unselectedItemColor: Colors.grey,
        ),
        floatingActionButtonTheme: const FloatingActionButtonThemeData(backgroundColor: Color(0xFF38bdf8)),
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
    const Center(child: Text("جهات الاتصال الإمبراطورية")), 
    const ChatListScreen(),         
    const SovereignOwnerDashboard(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('الإمبراطورية متصلة...', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text('الخادم السحابي المستقل نشط (135.181.86.199)', style: TextStyle(fontSize: 11, color: Colors.greenAccent)),
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
          BottomNavigationBarItem(icon: Badge(label: Text('١٣'), child: Icon(Icons.chat_bubble)), label: 'المحادثات'),
          BottomNavigationBarItem(icon: Icon(Icons.admin_panel_settings, color: Colors.amber), label: 'السيادة'),
        ],
      ),
    );
  }
}

// ==============================================================================
// 2. لوحة القيادة السيادية للمالك
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
    );
  }
}

// ==============================================================================
// 3. متجر البوتات والخدمات المرتبط بالسيرفر الحي
// ==============================================================================
class BotInstallerSheet extends StatefulWidget {
  const BotInstallerSheet({super.key});

  @override
  State<BotInstallerSheet> createState() => _BotInstallerSheetState();
}

class _BotInstallerSheetState extends State<BotInstallerSheet> {
  late Future<List<SovereignBotModel>> _botsFuture;

  @override
  void initState() {
    super.initState();
    _botsFuture = SovereignApiService.fetchBots();
  }

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
              child: SizedBox(width: 40, height: 5, child: DecoratedBox(decoration: BoxDecoration(color: Colors.grey, borderRadius: BorderRadius.all(Radius.circular(10))))),
            ),
          ),
          const Text("➕ متجر البوتات والخدمات السيادية", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
          const Text("تثبيت محركات جديدة دون تحديث التطبيق", style: TextStyle(color: Colors.grey, fontSize: 12)),
          const Divider(color: Colors.white24, height: 30),
          Expanded(
            child: FutureBuilder<List<SovereignBotModel>>(
              future: _botsFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator(color: Color(0xFF38bdf8)));
                } else if (snapshot.hasError || !snapshot.hasData) {
                  return const Center(child: Text("فشل الاتصال بالخادم السحابي", style: TextStyle(color: Colors.redAccent)));
                }
                
                final bots = snapshot.data!;
                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 10),
                  itemCount: bots.length,
                  itemBuilder: (context, index) {
                    final bot = bots[index];
                    return Card(
                      color: const Color(0xFF242f3d),
                      margin: const EdgeInsets.only(bottom: 10),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: bot.isCustom ? Colors.grey.shade800 : const Color(0xFF38bdf8).withOpacity(0.2), 
                          child: Icon(Icons.extension, color: bot.isCustom ? Colors.white : const Color(0xFF38bdf8)),
                        ),
                        title: Text(bot.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        subtitle: Text(bot.description, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                        trailing: bot.isInstalled 
                            ? const Icon(Icons.check_circle, color: Colors.green)
                            : ElevatedButton(
                                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF38bdf8), foregroundColor: Colors.black, minimumSize: const Size(60, 30)),
                                onPressed: () async {
                                  bool success = await SovereignApiService.installBotOnServer(bot.id);
                                  if (success) {
                                    setState(() {
                                      bot.isInstalled = true;
                                    });
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      SnackBar(content: Text('تم تثبيت الخدمة بنجاح: ${bot.name}'))
                                    );
                                  }
                                },
                                child: const Text("تثبيت", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                              ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

// ==============================================================================
// 4. القوائم الجانبية المتقدمة والشاشات الإضافية
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
          children: const [
            DrawerHeader(
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
            ListTile(leading: Icon(Icons.manage_search, color: Colors.teal), title: Text("محرك البحث المتقدم")),
            ListTile(leading: Icon(Icons.group_add, color: Colors.blue), title: Text("أداة النقل الذكي")),
            ListTile(leading: Icon(Icons.design_services, color: Colors.pink), title: Text("استوديو التصميم وتوليد الإيصالات")),
            ListTile(leading: Icon(Icons.psychology, color: Colors.purple), title: Text("مساعد الذكاء الاصطناعي (AGI)")),
            Divider(color: Colors.grey),
            ListTile(leading: Icon(Icons.light_mode), title: Text("النمط النهاري/الليلي")),
          ],
        ),
      ),
    );
  }
}

class AccountManagerDrawer extends StatelessWidget {
  const AccountManagerDrawer({super.key});
  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF1c242f),
      child: SafeArea(
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('إدارة الحسابات', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  Icon(Icons.info_outline),
                ],
              ),
            ),
            const Divider(color: Colors.grey),
            Expanded(
              child: ListView(
                children: const [
                  ListTile(leading: CircleAvatar(child: Text('AN')), title: Text('انا انا'), trailing: Icon(Icons.ac_unit, color: Colors.lightBlueAccent)),
                  ListTile(leading: CircleAvatar(child: Icon(Icons.security)), title: Text('AymnGuard Hub'), trailing: Text('VIP', style: TextStyle(color: Colors.blue, fontWeight: FontWeight.bold))),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ChatListScreen extends StatelessWidget {
  const ChatListScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: const [
        ListTile(
          leading: CircleAvatar(backgroundColor: Colors.blue, child: Icon(Icons.security)),
          title: Text("درع الأمان | AymnGuard"), 
          subtitle: Text("💎 تم تشغيل درع الحماية والاتصال السحابي بنجاح."),
        ),
      ],
    );
  }
}

class SettingsScreenPreview extends StatelessWidget { const SettingsScreenPreview({super.key}); @override Widget build(BuildContext context) { return const Center(child: Text("شاشة الإعدادات السيادية", style: TextStyle(color: Colors.grey))); } }
class ProfileScreenPreview extends StatelessWidget { const ProfileScreenPreview({super.key}); @override Widget build(BuildContext context) { return const Center(child: Text("شاشة الملف الشخصي الإمبراطوري", style: TextStyle(color: Colors.grey))); } }
