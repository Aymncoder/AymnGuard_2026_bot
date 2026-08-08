// ==============================================================================
// AymnGuard Enterprise : Ultimate Sovereign Super App (v20.0.0)
// Integration: Telegram Core + Premium Store + Live API Engine + Admin Panel
// ==============================================================================
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// الثابت السيادي للخادم السحابي المستقل
const String kServerUrl = "http://135.181.86.199:10050";

void main() {
  runApp(const AymnGuardPlusApp());
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
      // العودة للبيانات التشغيلية الافتراضية المؤمنة
    }
    return [
      SovereignBotModel(id: 'bot_1', name: 'بوت النقل العكسي الذكي', description: 'نقل الأعضاء باستخدام وكلاء AI.', icon: Icons.swap_calls, isInstalled: true),
      SovereignBotModel(id: 'bot_2', name: 'محرك التدقيق الجنائي', description: 'فحص الثغرات الأمنية في العقود.', icon: Icons.policy, isInstalled: false),
      SovereignBotModel(id: 'bot_3', name: 'الترجمة المالية الآلية', description: 'ترجمة فورية للتقارير المالية.', icon: Icons.translate, isInstalled: false),
      SovereignBotModel(id: 'bot_4', name: 'خدمة Webhook خارجية', description: 'أضف رابط لبوت مخصص.', icon: Icons.add_link, isInstalled: false, isCustom: true),
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
      return true; // محاكاة لنجاح التثبيت للتجربة
    }
  }
}

class SovereignBotModel {
  final String id;
  final String name;
  final String description;
  final IconData icon;
  bool isInstalled;
  final bool isCustom;

  SovereignBotModel({
    required this.id, required this.name, required this.description, 
    required this.icon, this.isInstalled = false, this.isCustom = false,
  });

  factory SovereignBotModel.fromJson(Map<String, dynamic> json) {
    return SovereignBotModel(
      id: json['id'] ?? '', name: json['name'] ?? '', description: json['description'] ?? '',
      icon: Icons.extension, isInstalled: json['is_installed'] ?? false, isCustom: json['is_custom'] ?? false,
    );
  }
}

// ==============================================================================
// 2. النواة الأساسية وثيم الإمبراطورية (App Root)
// ==============================================================================
class AymnGuardPlusApp extends StatelessWidget {
  const AymnGuardPlusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AymnGuard Plus Ultimate',
      debugShowCheckedModeBanner: false,
      builder: (context, child) {
        return Directionality(textDirection: TextDirection.rtl, child: child!);
      },
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF151E27),
        primaryColor: const Color(0xFF0EA5E9),
        appBarTheme: const AppBarTheme(backgroundColor: Color(0xFF1E293B), elevation: 0),
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: Color(0xFF1E293B),
          selectedItemColor: Color(0xFF0EA5E9),
          unselectedItemColor: Colors.grey,
        ),
        fontFamily: 'Roboto',
      ),
      home: const MainSovereignScreen(),
    );
  }
}

// ==============================================================================
// 3. مركز الملاحة الرئيسي (Master Controller)
// ==============================================================================
class MainSovereignScreen extends StatefulWidget {
  const MainSovereignScreen({super.key});

  @override
  State<MainSovereignScreen> createState() => _MainSovereignScreenState();
}

class _MainSovereignScreenState extends State<MainSovereignScreen> {
  int _currentIndex = 3; 
  final bool isOwner = true; // حالة المالك

  late List<Widget> _screens;

  @override
  void initState() {
    super.initState();
    _screens = [
      const AccountSettingsScreen(), 
      const EmpirePremiumStore(),    
      const ContactsScreen(),        
      const TelegramCoreChats(),     
      if (isOwner) const UltimateOwnerDashboard(), // لوحة المالك المدمجة الخارقة
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const MultiAccountDrawer(), // الدرج الأساسي للحسابات
      endDrawer: const AdvancedToolsDrawer(), // درج المطورين/الأدوات المتقدمة
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        items: [
          const BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'الإعدادات'),
          const BottomNavigationBarItem(icon: Icon(Icons.storefront, color: Color(0xFFFFD700)), label: 'المتجر'),
          const BottomNavigationBarItem(icon: Icon(Icons.perm_contact_calendar), label: 'الجهات'),
          const BottomNavigationBarItem(icon: Badge(label: Text('١٣'), child: Icon(Icons.chat_bubble)), label: 'المحادثات'),
          if (isOwner) const BottomNavigationBarItem(icon: Icon(Icons.admin_panel_settings, color: Colors.redAccent), label: 'السيادة'),
        ],
      ),
    );
  }
}

// ==============================================================================
// 4. نواة تليجرام المجانية المفتوحة (Free Telegram Core)
// ==============================================================================
class TelegramCoreChats extends StatelessWidget {
  const TelegramCoreChats({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 5, 
      child: Scaffold(
        appBar: AppBar(
          leading: Builder(
            builder: (context) => IconButton(
              icon: const Icon(Icons.menu, color: Colors.white),
              onPressed: () => Scaffold.of(context).openDrawer(),
            ),
          ),
          title: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("يتم الاتصال بالخادم الوكيل", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
              Text("إعداد الخادم الوكيل...", style: TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          actions: [
            IconButton(icon: const Icon(Icons.search, color: Colors.white), onPressed: () {}),
            Builder(
              builder: (context) => IconButton(
                icon: const Icon(Icons.rocket_launch, color: Color(0xFF0EA5E9)),
                onPressed: () => Scaffold.of(context).openEndDrawer(), // فتح أدوات المطور
              ),
            ),
          ],
          bottom: const TabBar(
            isScrollable: true,
            indicatorColor: Color(0xFF0EA5E9), labelColor: Color(0xFF0EA5E9), unselectedLabelColor: Colors.grey,
            tabs: [
              Tab(icon: Badge(label: Text('١٣'), child: Icon(Icons.chat))),
              Tab(icon: Badge(label: Text('١٣'), child: Icon(Icons.person))),
              Tab(icon: Badge(label: Text('١٢'), child: Icon(Icons.group))),
              Tab(icon: Icon(Icons.campaign)),
              Tab(icon: Icon(Icons.smart_toy)),
            ],
          ),
        ),
        body: ListView(
          children: [
            Container(color: const Color(0xFF1E293B), padding: const EdgeInsets.all(8), alignment: Alignment.center, child: const Text("إعلان", style: TextStyle(color: Colors.grey, fontSize: 12))),
            _buildChatTile("درع الأمان | AymnGuard", "💎 شراء اشتراك VIP الشامل", Icons.security, Colors.blueGrey, isVerified: true, time: "الجمعة", count: 1),
            _buildChatTile("+966561225123", "ص انضم +966561225123 لتلي...", Icons.person, Colors.pinkAccent, time: "3:38 ص", count: 1),
          ],
        ),
        floatingActionButton: FloatingActionButton(backgroundColor: const Color(0xFF0EA5E9), onPressed: () {}, child: const Icon(Icons.edit, color: Colors.white)),
      ),
    );
  }

          // ويدجت مساعدة لبناء خلايا المحادثات (محدثة لفتح الشاشة الجديدة)
  Widget _buildChatTile(String name, String message, IconData icon, Color color, {bool isVerified = false, required String time, required int count}) {
    return ListTile(
      // هذا هو السطر الجديد الذي يربط الخلية بشاشة المحادثة
      onTap: () {
        // يتم استخدام Builder هنا لضمان وجود سياق (Context) صحيح للـ Navigator
        Builder(builder: (context) {
          Navigator.push(context, MaterialPageRoute(
            builder: (context) => ChatRoomScreen(chatName: name, status: "متصل الآن", avatarColor: color, avatarIcon: icon)
          ));
          return const SizedBox.shrink();
        });
      },
      leading: CircleAvatar(radius: 25, backgroundColor: color, child: Icon(icon, color: Colors.white, size: 30)),
      title: Row(children: [Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)), if (isVerified) const SizedBox(width: 5), if (isVerified) const Icon(Icons.verified, color: Color(0xFF0EA5E9), size: 16)]),
      subtitle: Text(message, style: const TextStyle(color: Colors.grey), maxLines: 1, overflow: TextOverflow.ellipsis),
      trailing: Column(
        mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(time, style: const TextStyle(color: Colors.grey, fontSize: 12)), const SizedBox(height: 5),
          if (count > 0) Container(padding: const EdgeInsets.all(6), decoration: const BoxDecoration(color: Color(0xFF0EA5E9), shape: BoxShape.circle), child: Text(count.toString(), style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold))),
        ],
      ),
    );
}
// ==============================================================================
// 11. شاشة المحادثة الفعلية من الداخل (Chat Room UI)
// ==============================================================================
class ChatRoomScreen extends StatefulWidget {
  final String chatName;
  final String status;
  final Color avatarColor;
  final IconData avatarIcon;

  const ChatRoomScreen({
    super.key,
    required this.chatName,
    required this.status,
    this.avatarColor = const Color(0xFF0EA5E9),
    this.avatarIcon = Icons.person,
  });

  @override
  State<ChatRoomScreen> createState() => _ChatRoomScreenState();
}

class _ChatRoomScreenState extends State<ChatRoomScreen> {
  final TextEditingController _messageController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A), // لون خلفية المحادثة (أغمق قليلاً للتركيز)
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        titleSpacing: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
        title: Row(
          children: [
            CircleAvatar(
              radius: 18,
              backgroundColor: widget.avatarColor,
              child: Icon(widget.avatarIcon, color: Colors.white, size: 20),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(widget.chatName, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  Text(widget.status, style: const TextStyle(fontSize: 12, color: Color(0xFF0EA5E9))), // حالة الاتصال
                ],
              ),
            ),
          ],
        ),
        actions: [
          IconButton(icon: const Icon(Icons.call), onPressed: () {}),
          IconButton(icon: const Icon(Icons.more_vert), onPressed: () {}),
        ],
      ),
      body: Column(
        children: [
          // 1. منطقة عرض الرسائل (Chat History)
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildDateBadge("اليوم"),
                _buildMessageBubble("أهلاً بك في AymnGuard Plus! كيف يمكنني مساعدتك اليوم؟", "10:00 ص", isMe: false),
                _buildMessageBubble("مرحباً، تم تفعيل درع الأمان السحابي بنجاح.", "10:05 ص", isMe: true, isRead: true),
                _buildMessageBubble("ممتاز. الخوادم تعمل الآن بكفاءة 100%.", "10:06 ص", isMe: false),
              ],
            ),
          ),
          
          // 2. منطقة الكتابة والمرفقات (Message Input Field)
          _buildMessageInputArea(),
        ],
      ),
    );
  }

  // ويدجت فقاعة الرسالة
  Widget _buildMessageBubble(String message, String time, {required bool isMe, bool isRead = false}) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: isMe ? const Color(0xFF0EA5E9) : const Color(0xFF1E293B),
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(15),
            topRight: const Radius.circular(15),
            bottomRight: Radius.circular(isMe ? 0 : 15),
            bottomLeft: Radius.circular(isMe ? 15 : 0),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(message, style: const TextStyle(color: Colors.white, fontSize: 15)),
            const SizedBox(height: 5),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(time, style: TextStyle(color: isMe ? Colors.white70 : Colors.grey, fontSize: 10)),
                if (isMe) const SizedBox(width: 4),
                if (isMe) Icon(isRead ? Icons.done_all : Icons.done, color: isRead ? Colors.amberAccent : Colors.white70, size: 14),
              ],
            )
          ],
        ),
      ),
    );
  }

  // ويدجت تاريخ اليوم
  Widget _buildDateBadge(String date) {
    return Center(
      child: Container(
        margin: const EdgeInsets.only(bottom: 15),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
        decoration: BoxDecoration(color: const Color(0xFF1E293B).withOpacity(0.5), borderRadius: BorderRadius.circular(10)),
        child: Text(date, style: const TextStyle(color: Colors.grey, fontSize: 12)),
      ),
    );
  }

  // ويدجت مربع الإدخال
  Widget _buildMessageInputArea() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      color: const Color(0xFF1E293B),
      child: SafeArea(
        child: Row(
          children: [
            IconButton(icon: const Icon(Icons.attach_file, color: Colors.grey), onPressed: () {}),
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 15),
                decoration: BoxDecoration(color: const Color(0xFF0F172A), borderRadius: BorderRadius.circular(25)),
                child: TextField(
                  controller: _messageController,
                  style: const TextStyle(color: Colors.white),
                  decoration: const InputDecoration(
                    hintText: "مراسلة...",
                    hintStyle: TextStyle(color: Colors.grey),
                    border: InputBorder.none,
                    icon: Icon(Icons.emoji_emotions_outlined, color: Colors.grey),
                  ),
                ),
              ),
            ),
            const SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: const Color(0xFF0EA5E9),
              radius: 22,
              child: IconButton(icon: const Icon(Icons.mic, color: Colors.white), onPressed: () {}),
            ),
          ],
        ),
      ),
    );
  }
}
    return ListTile(
      // --- أضف هذا السطر هنا لربط الشاشة الجديدة ---
      onTap: () {
        Navigator.push(context, MaterialPageRoute(
          builder: (context) => ChatRoomScreen(chatName: name, status: "متصل الآن", avatarColor: color, avatarIcon: icon)
        ));
      },
      // ---------------------------------------------
      leading: CircleAvatar(radius: 25, backgroundColor: color, child: Icon(icon, color: Colors.white, size: 30)),
      // ... (باقي الكود كما هو)

// ==============================================================================
// 5. متجر الخدمات السيادية للمستخدمين (Premium Empire Store)
// ==============================================================================
class EmpirePremiumStore extends StatelessWidget {
  const EmpirePremiumStore({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("المتجر الإمبراطوري 💎", style: TextStyle(fontWeight: FontWeight.bold)), centerTitle: true),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text("ارتقِ بأعمالك مع الخدمات السيادية الاحترافية", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
          const SizedBox(height: 20),
          _buildPremiumItem("استوديو التصميم وتوليد الإيصالات", "تصميم شعارات وإيصالات مالية احترافية.", Icons.brush, "15\$/شهرياً"),
          _buildPremiumItem("مؤشرات التداول (Trading AI)", "تحليل ذكي وحصري لأسواق الـ Web3.", Icons.candlestick_chart, "50\$/شهرياً"),
          _buildPremiumItem("محركات البحث العالمية", "فهرسة استخباراتية وبحث دقيق غير محدود.", Icons.travel_explore, "25\$/شهرياً"),
          _buildPremiumItem("بوت الحماية الجنائية الشامل", "حماية مجموعاتك من الثغرات والعقود.", Icons.security, "10\$/شهرياً"),
        ],
      ),
    );
  }

  Widget _buildPremiumItem(String title, String desc, IconData icon, String price) {
    return Card(
      color: const Color(0xFF1E293B),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15), side: const BorderSide(color: Color(0xFFFFD700), width: 0.5)),
      margin: const EdgeInsets.only(bottom: 15),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: const Color(0xFFFFD700), size: 30), const SizedBox(width: 10),
                Expanded(child: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white))),
                Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5), decoration: BoxDecoration(color: Colors.redAccent, borderRadius: BorderRadius.circular(8)), child: Text(price, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)))
              ],
            ),
            const SizedBox(height: 10),
            Text(desc, style: const TextStyle(color: Colors.grey, fontSize: 13)),
            const SizedBox(height: 15),
            SizedBox(width: double.infinity, child: ElevatedButton(style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0EA5E9)), onPressed: () {}, child: const Text("اشتراك الآن", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)))),
          ],
        ),
      ),
    );
  }
}

// ==============================================================================
// 6. لوحة تحكم المالك الخارقة (Ultimate Owner Dashboard) - دمج الكودين
// ==============================================================================
class UltimateOwnerDashboard extends StatelessWidget {
  const UltimateOwnerDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("لوحة القيادة السيادية 👑", style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF151E27),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_box, color: Color(0xFF0EA5E9), size: 28),
            onPressed: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent, builder: (c) => const BotInstallerSheet()),
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // القسم الأول: الميكروسيرفسات الحية (من الكود 1)
            const Text("الميكروسيرفسات التشغيلية الحية", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
            const SizedBox(height: 15),
            GridView.count(
              shrinkWrap: true, // ضروري داخل الـ ScrollView
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2, crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.1,
              children: [
                _buildServiceCard("بوت الحماية", "يحمي 45 مجموعة", Icons.security, Colors.green),
                _buildServiceCard("النقل الذكي", "وكلاء AI نشطون", Icons.group_add, Colors.blue),
                _buildServiceCard("مولد التصميمات", "جاهز للعمل", Icons.brush, Colors.pink),
                _buildServiceCard("تداول Web3", "تدقيق العقود", Icons.candlestick_chart, Colors.orange),
              ],
            ),
            const Divider(color: Colors.white24, height: 40, thickness: 1),
            // القسم الثاني: التحكم المالي والأسعار (من الكود 2)
            const Text("إدارة الأسعار وجدار الدفع (Paywall)", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 15),
            _buildAdminControlTile("أدوات التصميم والإيصالات", "السعر الحالي: 15\$", true),
            _buildAdminControlTile("مؤشرات التداول (AI)", "السعر الحالي: 50\$", true),
            _buildAdminControlTile("محركات البحث العالمية", "السعر الحالي: 25\$", true),
            _buildAdminControlTile("بوت الحماية الجنائية", "السعر الحالي: 10\$", true),
          ],
        ),
      ),
    );
  }

  Widget _buildServiceCard(String title, String status, IconData icon, Color color) {
    return Card(
      color: const Color(0xFF1E293B),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      elevation: 4,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 38, color: color), const SizedBox(height: 10),
          Text(title, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.white)),
          const SizedBox(height: 4),
          Text(status, textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey, fontSize: 10)),
        ],
      ),
    );
  }

  Widget _buildAdminControlTile(String title, String subtitle, bool isActive) {
    return Card(
      color: const Color(0xFF1E293B),
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.redAccent, fontSize: 12)),
        trailing: Switch(value: isActive, activeColor: Colors.green, onChanged: (val) {}),
      ),
    );
  }
}

// ==============================================================================
// 7. متجر البوتات API السحابي (Bot Installer Sheet)
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
      decoration: const BoxDecoration(color: Color(0xFF1E293B), borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20))),
      child: Column(
        children: [
          const Padding(padding: EdgeInsets.all(15.0), child: Center(child: SizedBox(width: 40, height: 5, child: DecoratedBox(decoration: BoxDecoration(color: Colors.grey, borderRadius: BorderRadius.all(Radius.circular(10))))))),
          const Text("➕ السحابة الإمبراطورية لتثبيت البوتات", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
          const Text("تواصل حي مع السيرفر 135.181.86.199", style: TextStyle(color: Colors.greenAccent, fontSize: 12)),
          const Divider(color: Colors.white24, height: 30),
          Expanded(
            child: FutureBuilder<List<SovereignBotModel>>(
              future: _botsFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator(color: Color(0xFF0EA5E9)));
                if (snapshot.hasError || !snapshot.hasData) return const Center(child: Text("فشل الاتصال بالخادم", style: TextStyle(color: Colors.redAccent)));
                final bots = snapshot.data!;
                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: bots.length,
                  itemBuilder: (context, index) {
                    final bot = bots[index];
                    return Card(
                      color: const Color(0xFF151E27), margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        leading: CircleAvatar(backgroundColor: const Color(0xFF0EA5E9).withOpacity(0.2), child: Icon(bot.icon, color: const Color(0xFF0EA5E9))),
                        title: Text(bot.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        subtitle: Text(bot.description, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                        trailing: bot.isInstalled ? const Icon(Icons.check_circle, color: Colors.green) : ElevatedButton(
                          style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0EA5E9), foregroundColor: Colors.white),
                          onPressed: () async {
                            bool success = await SovereignApiService.installBotOnServer(bot.id);
                            if (success) { setState(() { bot.isInstalled = true; }); }
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
// 8. القوائم الجانبية (Drawers) 
// ==============================================================================
class MultiAccountDrawer extends StatelessWidget {
  const MultiAccountDrawer({super.key});
  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF151E27),
      child: SafeArea(
        child: Column(
          children: [
            UserAccountsDrawerHeader(
              decoration: const BoxDecoration(color: Color(0xFF1E293B)),
              accountName: const Text("يارب", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              accountEmail: const Text("+967 775 786 363"),
              currentAccountPicture: const CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.person, size: 40, color: Colors.grey)),
              otherAccountsPictures: const [CircleAvatar(backgroundColor: Colors.blue, child: Text("AN"))],
            ),
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  const ListTile(leading: Icon(Icons.add), title: Text("إضافة حساب")),
                  const Divider(color: Colors.white24),
                  const ListTile(leading: Icon(Icons.perm_contact_calendar), title: Text("جهات الاتصال")),
                  const ListTile(leading: Icon(Icons.settings), title: Text("الإعدادات")),
                  const Divider(color: Colors.white24),
                  ListTile(leading: const Icon(Icons.nightlight_round), title: const Text("الوضع الليلي"), trailing: Switch(value: true, activeColor: const Color(0xFF0EA5E9), onChanged: (v) {})),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class AdvancedToolsDrawer extends StatelessWidget {
  const AdvancedToolsDrawer({super.key});
  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF1E293B),
      child: SafeArea(
        child: ListView(
          padding: EdgeInsets.zero,
          children: const [
            DrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF151E27)),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.end, children: [
                Icon(Icons.rocket_launch, color: Color(0xFF0EA5E9), size: 40), SizedBox(height: 10),
                Text("محركات الـ Super App", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
              ]),
            ),
            ListTile(leading: Icon(Icons.manage_search, color: Colors.tealAccent), title: Text("محرك البحث المتقدم")),
            ListTile(leading: Icon(Icons.psychology, color: Colors.purpleAccent), title: Text("مساعد الذكاء الاصطناعي")),
          ],
        ),
      ),
    );
  }
}

// ==============================================================================
// 9. شاشات الإعدادات والخصوصية المتقدمة (Settings & Privacy UI)
// ==============================================================================
class AccountSettingsScreen extends StatelessWidget {
  const AccountSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF151E27),
      appBar: AppBar(
        title: const Text("الإعدادات", style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E293B),
        actions: [
          IconButton(icon: const Icon(Icons.search), onPressed: () {}),
          IconButton(icon: const Icon(Icons.more_vert), onPressed: () {}),
        ],
      ),
      body: ListView(
        children: [
          // 1. ترويسة الحساب الشخصي (Profile Header)
          Container(
            color: const Color(0xFF1E293B),
            padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
            child: Row(
              children: [
                const CircleAvatar(
                  radius: 35,
                  backgroundColor: Color(0xFF0EA5E9),
                  child: Icon(Icons.person, size: 40, color: Colors.white),
                ),
                const SizedBox(width: 15),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("ابو يمان", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                    const SizedBox(height: 5),
                    const Text("+91 9265035200", style: TextStyle(fontSize: 14, color: Colors.grey)),
                    const SizedBox(height: 5),
                    Text("@AymnGuard", style: TextStyle(fontSize: 14, color: Colors.grey.shade400)),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),

          // 2. إعدادات AymnGuard المتقدمة (تحاكي إعدادات Graph/تليجراف)
          _buildSettingsSection(
            title: "إعدادات الإمبراطورية",
            items: [
              _buildSettingsTile(context, "إعدادات AymnGuard Plus", Icons.settings_suggest, Colors.green),
              _buildSettingsTile(context, "الأقسام المخفية", Icons.visibility_off, Colors.blueGrey),
              _buildSettingsTile(context, "مانع الإعلانات", Icons.block, Colors.redAccent, hasSwitch: true, switchValue: true),
            ],
          ),

          // 3. الإعدادات العامة (General Settings)
          _buildSettingsSection(
            title: "الإعدادات العامة",
            items: [
              _buildSettingsTile(context, "إعدادات المحادثات", Icons.chat, Colors.greenAccent),
              _buildSettingsTile(context, "الخصوصية والأمان", Icons.lock, Colors.lightBlueAccent, destination: const PrivacyAndSecurityScreen()),
              _buildSettingsTile(context, "الإشعارات والأصوات", Icons.notifications, Colors.redAccent),
              _buildSettingsTile(context, "البيانات والتخزين", Icons.pie_chart, Colors.blue),
              _buildSettingsTile(context, "توفير الطاقة", Icons.battery_charging_full, Colors.orange),
              _buildSettingsTile(context, "اللغة", Icons.language, Colors.purpleAccent, subtitle: "العربية"),
            ],
          ),

          // 4. الخدمات المميزة (Premium Features)
          _buildSettingsSection(
            title: "المميزات",
            items: [
              _buildSettingsTile(context, "AymnGuard المُميَّز", Icons.star, Colors.purple),
              _buildSettingsTile(context, "الأعمال (Business)", Icons.store, Colors.pinkAccent),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSettingsSection({required String title, required List<Widget> items}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(right: 16, top: 15, bottom: 5),
          child: Text(title, style: const TextStyle(color: Color(0xFF0EA5E9), fontWeight: FontWeight.bold)),
        ),
        Container(
          color: const Color(0xFF1E293B),
          child: Column(children: items),
        ),
        const SizedBox(height: 10),
      ],
    );
  }

  Widget _buildSettingsTile(BuildContext context, String title, IconData icon, Color iconColor, {String? subtitle, bool hasSwitch = false, bool switchValue = false, Widget? destination}) {
    return ListTile(
      leading: CircleAvatar(
        radius: 18,
        backgroundColor: iconColor.withOpacity(0.2),
        child: Icon(icon, size: 20, color: iconColor),
      ),
      title: Text(title, style: const TextStyle(color: Colors.white, fontSize: 15)),
      subtitle: subtitle != null ? Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)) : null,
      trailing: hasSwitch
          ? Switch(value: switchValue, activeColor: const Color(0xFF0EA5E9), onChanged: (v) {})
          : const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
      onTap: () {
        if (destination != null) {
          Navigator.push(context, MaterialPageRoute(builder: (context) => destination));
        }
      },
    );
  }
}

// ==============================================================================
// 10. شاشة الخصوصية والأمان (Privacy & Security) مطابقة للصور
// ==============================================================================
class PrivacyAndSecurityScreen extends StatelessWidget {
  const PrivacyAndSecurityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF151E27),
      appBar: AppBar(
        title: const Text("الخصوصية والأمان"),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: ListView(
        children: [
          _buildPrivacySection(
            title: "الأمان",
            items: [
              _buildPrivacyTile("التحقق بخطوتين", "مفعّل", Icons.verified_user),
              _buildPrivacyTile("الحذف التلقائي للرسائل", "معطّلة", Icons.auto_delete),
              _buildPrivacyTile("رمز القفل أو النقش", "معطّلة", Icons.lock),
              _buildPrivacyTile("المستخدمون المحظورون", "لا أحد", Icons.block),
              _buildPrivacyTile("الأجهزة", "3", Icons.devices),
            ],
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Text("مراجعة قائمة الأجهزة التي قمت بتسجيل دخول حسابك على تليجرام فيها.", style: TextStyle(color: Colors.grey, fontSize: 12)),
          ),
          _buildPrivacySection(
            title: "الخصوصية",
            items: [
              _buildPrivacyTile("رقم الهاتف", "لا أحد", Icons.phone),
              _buildPrivacyTile("آخر ظهور و«متصل»", "الجميع", Icons.access_time),
              _buildPrivacyTile("صور الملف الشخصي", "الجميع", Icons.photo_camera),
              _buildPrivacyTile("الرسائل المحوّلة", "الجميع", Icons.forward),
              _buildPrivacyTile("المكالمات", "الجميع", Icons.call),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPrivacySection({required String title, required List<Widget> items}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(right: 16, top: 15, bottom: 5),
          child: Text(title, style: const TextStyle(color: Color(0xFF0EA5E9), fontWeight: FontWeight.bold)),
        ),
        Container(
          color: const Color(0xFF1E293B),
          child: Column(children: items),
        ),
      ],
    );
  }

  Widget _buildPrivacyTile(String title, String status, IconData icon) {
    return ListTile(
      leading: Icon(icon, color: Colors.grey),
      title: Text(title, style: const TextStyle(color: Colors.white, fontSize: 15)),
      trailing: Text(status, style: const TextStyle(color: Color(0xFF0EA5E9), fontSize: 14)),
      onTap: () {},
    );
  }
}

// شاشة جهات الاتصال (مؤقتة لحين بنائها)
class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Color(0xFF151E27),
      body: Center(child: Text("جهات الاتصال الإمبراطورية\n(سيتم بناؤها لاحقاً)", textAlign: TextAlign.center, style: TextStyle(color: Colors.grey))),
    );
  }
}
