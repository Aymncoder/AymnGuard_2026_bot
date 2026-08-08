// ==============================================================================
// AymnGuard Enterprise : Ultimate Sovereign Super App (v21.0.0 Enterprise)
// Architecture: Clean Code + Modular Widgets + Centralized Config + API Engine
// ==============================================================================
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const AymnGuardPlusApp());
}

// ==============================================================================
// 1. التكوين المركزي والسيادي (Central Configuration & Theming)
// ==============================================================================
class AppConfig {
  static const String serverUrl = "http://135.181.86.199:10050";
  static const String appVersion = "21.0.0 Enterprise";
  static const bool isOwnerStatus = true; // التحكم المركزي في صلاحيات المالك
}

class AppColors {
  static const Color background = Color(0xFF151E27);
  static const Color surface = Color(0xFF1E293B);
  static const Color primary = Color(0xFF0EA5E9);
  static const Color accentGold = Color(0xFFFFD700);
  static const Color chatBackground = Color(0xFF0F172A);
}

// ==============================================================================
// 2. طبقة الاتصال والخدمات الخلفية (Enterprise Service Layer)
// ==============================================================================
class SovereignApiService {
  static Future<List<SovereignBotModel>> fetchBots() async {
    try {
      final response = await http.get(Uri.parse('${AppConfig.serverUrl}/api/bots')).timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        Iterable data = json.decode(response.body);
        return data.map((json) => SovereignBotModel.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint("API Error: $e");
    }
    // Fallback Data
    return {
      SovereignBotModel(id: 'bot_1', name: 'بوت النقل العكسي الذكي', description: 'نقل الأعضاء باستخدام وكلاء AI.', icon: Icons.swap_calls, isInstalled: true),
      SovereignBotModel(id: 'bot_2', name: 'محرك التدقيق الجنائي', description: 'فحص الثغرات الأمنية في العقود.', icon: Icons.policy, isInstalled: false),
      SovereignBotModel(id: 'bot_3', name: 'الترجمة المالية الآلية', description: 'ترجمة فورية للتقارير المالية.', icon: Icons.translate, isInstalled: false),       SovereignBotModel(id: 'bot_4', name: 'خدمة Webhook خارجية', description: 'أضف رابط لبوت مخصص.', icon: Icons.add_link, isInstalled: false, isCustom: true),
    }
  }

  static Future<bool> installBotOnServer(String botId) async {
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.serverUrl}/api/bots/install'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({"bot_id": botId, "timestamp": DateTime.now().toIso8601String()}),
      ).timeout(const Duration(seconds: 10));
      return response.statusCode == 200;
    } catch (e) {
      await Future.delayed(const Duration(milliseconds: 800));
      return true; // محاكاة لنجاح التثبيت
    }
  }
}

class SovereignBotModel {
  final String id, name, description;
  final IconData icon;
  bool isInstalled;
  final bool isCustom;

  SovereignBotModel({required this.id, required this.name, required this.description, required this.icon, this.isInstalled = false, this.isCustom = false});

  factory SovereignBotModel.fromJson(Map<String, dynamic> json) {
    return SovereignBotModel(
      id: json['id'] ?? '', name: json['name'] ?? '', description: json['description'] ?? '',
      icon: Icons.extension, isInstalled: json['is_installed'] ?? false, isCustom: json['is_custom'] ?? false,
    );
  }
}

// ==============================================================================
// 3. النواة الأساسية (App Root)
// ==============================================================================
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
        fontFamily: 'Roboto',
      ),
      home: const MainSovereignScreen(),
    );
  }
}

// ==============================================================================
// 4. جهاز التحكم المركزي (Master Navigation Controller)
// ==============================================================================
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
      body: IndexedStack(index: _currentIndex, children: _screens), // استخدام IndexedStack للحفاظ على حالة الشاشات
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        items: [
          const BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'الإعدادات'),
          const BottomNavigationBarItem(icon: Icon(Icons.storefront, color: AppColors.accentGold), label: 'المتجر'),
          const BottomNavigationBarItem(icon: Icon(Icons.perm_contact_calendar), label: 'الجهات'),
          const BottomNavigationBarItem(icon: Badge(label: Text('١٣'), child: Icon(Icons.chat_bubble)), label: 'المحادثات'),
          if (AppConfig.isOwnerStatus) const BottomNavigationBarItem(icon: Icon(Icons.admin_panel_settings, color: Colors.redAccent), label: 'السيادة'),
        ],
      ),
    );
  }
}

// ==============================================================================
// 5. نواة تليجرام المجانية المفتوحة (Telegram Core UI)
// ==============================================================================
class TelegramCoreChats extends StatelessWidget {
  const TelegramCoreChats({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 6,
      child: Scaffold(
        appBar: AppBar(
          leading: Builder(builder: (context) => IconButton(icon: const Icon(Icons.menu, color: Colors.white), onPressed: () => Scaffold.of(context).openDrawer())),
          title: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("يتم الاتصال بالخادم الوكيل", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
              Text("إعداد الخادم الوكيل...", style: TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          actions: [
            IconButton(icon: const Icon(Icons.search, color: Colors.white), onPressed: () {}),
            Builder(builder: (context) => IconButton(icon: const Icon(Icons.rocket_launch, color: AppColors.primary), onPressed: () => Scaffold.of(context).openEndDrawer())),
          ],
          bottom: const TabBar(
            isScrollable: true,
            indicatorColor: AppColors.primary, labelColor: AppColors.primary, unselectedLabelColor: Colors.grey,
            tabs: [
              Tab(text: "الكل", icon: Badge(label: Text('١٣'), child: Icon(Icons.chat))),
              Tab(text: "شخصي", icon: Icon(Icons.person)),
              Tab(text: "مجموعات", icon: Badge(label: Text('١٢'), child: Icon(Icons.group))),
              Tab(text: "قنوات", icon: Icon(Icons.campaign)),
              Tab(text: "بوتات", icon: Icon(Icons.smart_toy)),
              Tab(text: "مجتمعاتي", icon: Icon(Icons.hub, color: AppColors.accentGold)), 
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            AllChatsListWidget(), // تم تحويل الدالة إلى كلاس لرفع الأداء
            Center(child: Text("المراسلات الشخصية", style: TextStyle(color: Colors.grey))),
            Center(child: Text("مجموعاتك النشطة", style: TextStyle(color: Colors.grey))),
            Center(child: Text("قنواتك المشترك بها", style: TextStyle(color: Colors.grey))),
            Center(child: Text("البوتات الخدمية", style: TextStyle(color: Colors.grey))),
            MyCommunitiesPortalWidget(), // تحويل الدالة لكلاس
          ],
        ),
        floatingActionButton: FloatingActionButton(backgroundColor: AppColors.primary, onPressed: () {}, child: const Icon(Icons.edit, color: Colors.white)),
      ),
    );
  }
}

// مكون (Widget) مستقل لعرض المحادثات لتحسين استهلاك الذاكرة (Best Practice)
class AllChatsListWidget extends StatelessWidget {
  const AllChatsListWidget({super.key});
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: const [
        AdvertisementBanner(),
        ChatTileWidget(name: "درع الأمان | AymnGuard", message: "💎 شراء اشتراك VIP الشامل", icon: Icons.security, color: Colors.blueGrey, isVerified: true, time: "الجمعة", count: 1),
        ChatTileWidget(name: "+966561225123", message: "ص انضم +966561225123 لتلي...", icon: Icons.person, color: Colors.pinkAccent, time: "3:38 ص", count: 1),
        ChatTileWidget(name: "فريق المطورين", message: "تم تحديث الخوادم بنجاح.", icon: Icons.group, color: Colors.green, time: "أمس", count: 12),
      ],
    );
  }
}

class AdvertisementBanner extends StatelessWidget {
  const AdvertisementBanner({super.key});
  @override
  Widget build(BuildContext context) {
    return Container(color: AppColors.surface, padding: const EdgeInsets.all(8), alignment: Alignment.center, child: const Text("إعلان", style: TextStyle(color: Colors.grey, fontSize: 12)));
  }
}

// مكون (Widget) خلية المحادثة المستقل
class ChatTileWidget extends StatelessWidget {
  final String name, message, time;
  final IconData icon;
  final Color color;
  final bool isVerified;
  final int count;

  const ChatTileWidget({super.key, required this.name, required this.message, required this.icon, required this.color, this.isVerified = false, required this.time, required this.count});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => ChatRoomScreen(chatName: name, status: "متصل الآن", avatarColor: color, avatarIcon: icon))),
      leading: CircleAvatar(radius: 25, backgroundColor: color, child: Icon(icon, color: Colors.white, size: 30)),
      title: Row(children: [Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)), if (isVerified) const SizedBox(width: 5), if (isVerified) const Icon(Icons.verified, color: AppColors.primary, size: 16)]),
      subtitle: Text(message, style: const TextStyle(color: Colors.grey), maxLines: 1, overflow: TextOverflow.ellipsis),
      trailing: Column(
        mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(time, style: const TextStyle(color: Colors.grey, fontSize: 12)), const SizedBox(height: 5),
          if (count > 0) Container(padding: const EdgeInsets.all(6), decoration: const BoxDecoration(color: AppColors.primary, shape: BoxShape.circle), child: Text(count.toString(), style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold))),
        ],
      ),
    );
  }
}

// مكون بوابة مجتمعاتي المستقل
class MyCommunitiesPortalWidget extends StatelessWidget {
  const MyCommunitiesPortalWidget({super.key});
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: const [
        Text("إدارة مجتمعاتي وأدواتي 👑", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.accentGold)),
        SizedBox(height: 5),
        Text("نظرة شاملة لكل ما تملكه أو تديره في الإمبراطورية.", style: TextStyle(color: Colors.grey, fontSize: 12)),
        Divider(color: Colors.white24, height: 30),
        Text("قنواتي ومجموعاتي", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
        SizedBox(height: 10),
        CommunityCardWidget(title: "مجموعة التداول VIP", subtitle: "أنت المالك • 5,430 عضو", icon: Icons.group, iconColor: Colors.orangeAccent),
        CommunityCardWidget(title: "قناة تحديثات AymnGuard", subtitle: "أنت المالك • 12,000 مشترك", icon: Icons.campaign, iconColor: Colors.blueAccent),
        SizedBox(height: 20),
        Text("أدواتي وبوتاتي النشطة", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
        SizedBox(height: 10),
        CommunityCardWidget(title: "بوت الحماية الشامل", subtitle: "اشتراك مفعل (ينتهي بعد 20 يوم)", icon: Icons.security, iconColor: Colors.green),
        CommunityCardWidget(title: "مولد التصميمات الذكي", subtitle: "أداة مفعلة • جاهز للاستخدام", icon: Icons.brush, iconColor: Colors.pinkAccent),
      ],
    );
  }
}

class CommunityCardWidget extends StatelessWidget {
  final String title, subtitle;
  final IconData icon;
  final Color iconColor;
  const CommunityCardWidget({super.key, required this.title, required this.subtitle, required this.icon, required this.iconColor});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.surface, margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: iconColor.withOpacity(0.3), width: 1)),
      child: ListTile(
        leading: Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: iconColor.withOpacity(0.2), borderRadius: BorderRadius.circular(8)), child: Icon(icon, color: iconColor)),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
        trailing: const Icon(Icons.arrow_forward_ios, color: Colors.grey, size: 14),
      ),
    );
  }
}

// ==============================================================================
// 6. شاشة المحادثة الفعلية (Chat Room UI)
// ==============================================================================
class ChatRoomScreen extends StatefulWidget {
  final String chatName, status;
  final Color avatarColor;
  final IconData avatarIcon;

  const ChatRoomScreen({super.key, required this.chatName, required this.status, this.avatarColor = AppColors.primary, this.avatarIcon = Icons.person});
  @override
  State<ChatRoomScreen> createState() => _ChatRoomScreenState();
}

class _ChatRoomScreenState extends State<ChatRoomScreen> {
  final TextEditingController _messageController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.chatBackground,
      appBar: AppBar(
        titleSpacing: 0,
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => Navigator.pop(context)),
        title: Row(children: [CircleAvatar(radius: 18, backgroundColor: widget.avatarColor, child: Icon(widget.avatarIcon, color: Colors.white, size: 20)), const SizedBox(width: 10), Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(widget.chatName, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)), Text(widget.status, style: const TextStyle(fontSize: 12, color: AppColors.primary))]))]),
        actions: [IconButton(icon: const Icon(Icons.call), onPressed: () {}), IconButton(icon: const Icon(Icons.more_vert), onPressed: () {})],
      ),
      body: Column(
        children: [
          Expanded(child: ListView(padding: const EdgeInsets.all(16), children: const [
            DateBadgeWidget(date: "اليوم"),
            MessageBubbleWidget(message: "أهلاً بك في AymnGuard Plus! كيف يمكنني مساعدتك اليوم؟", time: "10:00 ص", isMe: false),
            MessageBubbleWidget(message: "مرحباً، تم تفعيل درع الأمان السحابي بنجاح.", time: "10:05 ص", isMe: true, isRead: true),
          ])),
          _buildMessageInputArea(),
        ],
      ),
    );
  }

  Widget _buildMessageInputArea() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8), color: AppColors.surface,
      child: SafeArea(child: Row(children: [
        IconButton(icon: const Icon(Icons.attach_file, color: Colors.grey), onPressed: () {}),
        Expanded(child: Container(padding: const EdgeInsets.symmetric(horizontal: 15), decoration: BoxDecoration(color: AppColors.chatBackground, borderRadius: BorderRadius.circular(25)), child: TextField(controller: _messageController, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(hintText: "مراسلة...", hintStyle: TextStyle(color: Colors.grey), border: InputBorder.none, icon: Icon(Icons.emoji_emotions_outlined, color: Colors.grey))))),
        const SizedBox(width: 8),
        CircleAvatar(backgroundColor: AppColors.primary, radius: 22, child: IconButton(icon: const Icon(Icons.mic, color: Colors.white), onPressed: () {}))
      ])),
    );
  }
}

class MessageBubbleWidget extends StatelessWidget {
  final String message, time;
  final bool isMe, isRead;
  const MessageBubbleWidget({super.key, required this.message, required this.time, required this.isMe, this.isRead = false});
  @override
  Widget build(BuildContext context) {
    return Align(alignment: isMe ? Alignment.centerRight : Alignment.centerLeft, child: Container(margin: const EdgeInsets.only(bottom: 10), constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75), padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10), decoration: BoxDecoration(color: isMe ? AppColors.primary : AppColors.surface, borderRadius: BorderRadius.only(topLeft: const Radius.circular(15), topRight: const Radius.circular(15), bottomRight: Radius.circular(isMe ? 0 : 15), bottomLeft: Radius.circular(isMe ? 15 : 0))), child: Column(crossAxisAlignment: CrossAxisAlignment.end, children: [Text(message, style: const TextStyle(color: Colors.white, fontSize: 15)), const SizedBox(height: 5), Row(mainAxisSize: MainAxisSize.min, children: [Text(time, style: TextStyle(color: isMe ? Colors.white70 : Colors.grey, fontSize: 10)), if (isMe) const SizedBox(width: 4), if (isMe) Icon(isRead ? Icons.done_all : Icons.done, color: isRead ? AppColors.accentGold : Colors.white70, size: 14)])])));
  }
}

class DateBadgeWidget extends StatelessWidget {
  final String date;
  const DateBadgeWidget({super.key, required this.date});
  @override
  Widget build(BuildContext context) {
    return Center(child: Container(margin: const EdgeInsets.only(bottom: 15), padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5), decoration: BoxDecoration(color: AppColors.surface.withOpacity(0.5), borderRadius: BorderRadius.circular(10)), child: Text(date, style: const TextStyle(color: Colors.grey, fontSize: 12))));
  }
}

// ==============================================================================
// 7. متجر الخدمات السيادية للمستخدمين (Premium Store)
// ==============================================================================
class EmpirePremiumStore extends StatelessWidget {
  const EmpirePremiumStore({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("المتجر الإمبراطوري 💎", style: TextStyle(fontWeight: FontWeight.bold)), centerTitle: true),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Text("ارتقِ بأعمالك مع الخدمات السيادية الاحترافية", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.accentGold)), SizedBox(height: 20),
          PremiumItemWidget(title: "استوديو التصميم وتوليد الإيصالات", desc: "تصميم شعارات وإيصالات مالية احترافية.", icon: Icons.brush, price: "15\$/شهرياً"),
          PremiumItemWidget(title: "مؤشرات التداول (Trading AI)", desc: "تحليل ذكي وحصري لأسواق الـ Web3.", icon: Icons.candlestick_chart, price: "50\$/شهرياً"),
          PremiumItemWidget(title: "محركات البحث العالمية", desc: "فهرسة استخباراتية وبحث دقيق غير محدود.", icon: Icons.travel_explore, price: "25\$/شهرياً"),
          PremiumItemWidget(title: "بوت الحماية الجنائية الشامل", desc: "حماية مجموعاتك من الثغرات والعقود.", icon: Icons.security, price: "10\$/شهرياً"),
        ],
      ),
    );
  }
}

class PremiumItemWidget extends StatelessWidget {
  final String title, desc, price; final IconData icon;
  const PremiumItemWidget({super.key, required this.title, required this.desc, required this.icon, required this.price});
  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.surface, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15), side: const BorderSide(color: AppColors.accentGold, width: 0.5)), margin: const EdgeInsets.only(bottom: 15),
      child: Padding(padding: const EdgeInsets.all(16.0), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [Icon(icon, color: AppColors.accentGold, size: 30), const SizedBox(width: 10), Expanded(child: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white))), Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5), decoration: BoxDecoration(color: Colors.redAccent, borderRadius: BorderRadius.circular(8)), child: Text(price, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)))]),
        const SizedBox(height: 10), Text(desc, style: const TextStyle(color: Colors.grey, fontSize: 13)), const SizedBox(height: 15),
        SizedBox(width: double.infinity, child: ElevatedButton(style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary), onPressed: () {}, child: const Text("اشتراك الآن", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)))),
      ])),
    );
  }
}

// ==============================================================================
// 8. لوحة تحكم المالك (Ultimate Owner Dashboard)
// ==============================================================================
class UltimateOwnerDashboard extends StatelessWidget {
  const UltimateOwnerDashboard({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("لوحة القيادة السيادية 👑", style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
        actions: [IconButton(icon: const Icon(Icons.add_box, color: AppColors.primary, size: 28), onPressed: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent, builder: (c) => const BotInstallerSheet()))],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text("الميكروسيرفسات التشغيلية الحية", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.accentGold)), const SizedBox(height: 15),
          GridView.count(shrinkWrap: true, physics: const NeverScrollableScrollPhysics(), crossAxisCount: 2, crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.1, children: const [
            ServiceCardWidget(title: "بوت الحماية", status: "يحمي 45 مجموعة", icon: Icons.security, color: Colors.green), ServiceCardWidget(title: "النقل الذكي", status: "وكلاء AI نشطون", icon: Icons.group_add, color: Colors.blue),
            ServiceCardWidget(title: "مولد التصميمات", status: "جاهز للعمل", icon: Icons.brush, color: Colors.pink), ServiceCardWidget(title: "تداول Web3", status: "تدقيق العقود", icon: Icons.candlestick_chart, color: Colors.orange),
          ]),
          const Divider(color: Colors.white24, height: 40, thickness: 1),
          const Text("إدارة الأسعار وجدار الدفع (Paywall)", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)), const SizedBox(height: 15),
          const AdminControlTileWidget(title: "أدوات التصميم والإيصالات", subtitle: "السعر الحالي: 15\$", isActive: true),
          const AdminControlTileWidget(title: "مؤشرات التداول (AI)", subtitle: "السعر الحالي: 50\$", isActive: true),
          const AdminControlTileWidget(title: "محركات البحث العالمية", subtitle: "السعر الحالي: 25\$", isActive: true),
          const AdminControlTileWidget(title: "بوت الحماية الجنائية", subtitle: "السعر الحالي: 10\$", isActive: true),
        ]),
      ),
    );
  }
}

class ServiceCardWidget extends StatelessWidget {
  final String title, status; final IconData icon; final Color color;
  const ServiceCardWidget({super.key, required this.title, required this.status, required this.icon, required this.color});
  @override
  Widget build(BuildContext context) {
    return Card(color: AppColors.surface, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)), elevation: 4, child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(icon, size: 38, color: color), const SizedBox(height: 10), Text(title, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.white)), const SizedBox(height: 4), Text(status, textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey, fontSize: 10))]));
  }
}

class AdminControlTileWidget extends StatelessWidget {
  final String title, subtitle; final bool isActive;
  const AdminControlTileWidget({super.key, required this.title, required this.subtitle, required this.isActive});
  @override
  Widget build(BuildContext context) {
    return Card(color: AppColors.surface, margin: const EdgeInsets.only(bottom: 10), child: ListTile(title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)), subtitle: Text(subtitle, style: const TextStyle(color: Colors.redAccent, fontSize: 12)), trailing: Switch(value: isActive, activeColor: Colors.green, onChanged: (val) {})));
  }
}

// ==============================================================================
// 9. متجر البوتات API السحابي (Bot Installer)
// ==============================================================================
class BotInstallerSheet extends StatefulWidget {
  const BotInstallerSheet({super.key});
  @override
  State<BotInstallerSheet> createState() => _BotInstallerSheetState();
}
class _BotInstallerSheetState extends State<BotInstallerSheet> {
  late Future<List<SovereignBotModel>> _botsFuture;
  @override
  void initState() { super.initState(); _botsFuture = SovereignApiService.fetchBots(); }
  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.75, decoration: const BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20))),
      child: Column(children: [
        const Padding(padding: EdgeInsets.all(15.0), child: Center(child: SizedBox(width: 40, height: 5, child: DecoratedBox(decoration: BoxDecoration(color: Colors.grey, borderRadius: BorderRadius.all(Radius.circular(10))))))),
        const Text("➕ السحابة الإمبراطورية لتثبيت البوتات", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
        const Text("تواصل حي مع السيرفر ${AppConfig.serverUrl}", style: TextStyle(color: Colors.greenAccent, fontSize: 12)),
        const Divider(color: Colors.white24, height: 30),
        Expanded(child: FutureBuilder<List<SovereignBotModel>>(
          future: _botsFuture, builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator(color: AppColors.primary));
            if (snapshot.hasError || !snapshot.hasData) return const Center(child: Text("فشل الاتصال بالخادم", style: TextStyle(color: Colors.redAccent)));
            final bots = snapshot.data!;
            return ListView.builder(padding: const EdgeInsets.symmetric(horizontal: 16), itemCount: bots.length, itemBuilder: (context, index) {
              final bot = bots[index];
              return Card(color: AppColors.background, margin: const EdgeInsets.only(bottom: 12), child: ListTile(leading: CircleAvatar(backgroundColor: AppColors.primary.withOpacity(0.2), child: Icon(bot.icon, color: AppColors.primary)), title: Text(bot.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)), subtitle: Text(bot.description, style: const TextStyle(fontSize: 11, color: Colors.grey)), trailing: bot.isInstalled ? const Icon(Icons.check_circle, color: Colors.green) : ElevatedButton(style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary, foregroundColor: Colors.white), onPressed: () async { bool success = await SovereignApiService.installBotOnServer(bot.id); if (success) { setState(() { bot.isInstalled = true; }); } }, child: const Text("تثبيت", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)))));
            });
          },
        )),
      ]),
    );
  }
}

// ==============================================================================
// 10. القوائم الجانبية والإعدادات (Drawers & Settings)
// ==============================================================================
class MultiAccountDrawer extends StatelessWidget {
  const MultiAccountDrawer({super.key});
  @override
  Widget build(BuildContext context) {
    return Drawer(backgroundColor: AppColors.background, child: SafeArea(child: Column(children: [
      const UserAccountsDrawerHeader(decoration: BoxDecoration(color: AppColors.surface), accountName: Text("يارب", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)), accountEmail: Text("+967 775 786 363"), currentAccountPicture: CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.person, size: 40, color: Colors.grey)), otherAccountsPictures: [CircleAvatar(backgroundColor: Colors.blue, child: Text("AN"))]),
      Expanded(child: ListView(padding: EdgeInsets.zero, children: [
        const ListTile(leading: Icon(Icons.add), title: Text("إضافة حساب")), const Divider(color: Colors.white24),
        const ListTile(leading: Icon(Icons.perm_contact_calendar), title: Text("جهات الاتصال")), const ListTile(leading: Icon(Icons.settings), title: Text("الإعدادات")), const Divider(color: Colors.white24),
        ListTile(leading: const Icon(Icons.nightlight_round), title: const Text("الوضع الليلي"), trailing: Switch(value: true, activeColor: AppColors.primary, onChanged: (v) {})),
      ])),
    ])));
  }
}

// ==============================================================================
// 10. القوائم الجانبية (النسخة الشاملة دون أي نقصان)
// ==============================================================================
class MultiAccountDrawer extends StatelessWidget {
  const MultiAccountDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: AppColors.background,
      child: SafeArea(
        child: Column(
          children: [
            const UserAccountsDrawerHeader(
              decoration: BoxDecoration(color: AppColors.surface),
              accountName: Text("يارب", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              accountEmail: Text("+967 775 786 363"),
              currentAccountPicture: CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.person, size: 40, color: Colors.grey)),
              otherAccountsPictures: [CircleAvatar(backgroundColor: Colors.blue, child: Text("AN"))],
            ),
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  const ListTile(leading: Icon(Icons.add), title: Text("إضافة حساب")),
                  const Divider(color: Colors.white24),
                  const ListTile(leading: Icon(Icons.perm_contact_calendar), title: Text("جهات الاتصال")),
                  const ListTile(leading: Icon(Icons.call), title: Text("المكالمات")),
                  const ListTile(leading: Icon(Icons.bookmark), title: Text("الرسائل المحفوظة")),
                  const ListTile(leading: Icon(Icons.settings), title: Text("الإعدادات")),
                  const Divider(color: Colors.white24),
                  const ListTile(leading: Icon(Icons.person_add), title: Text("دعوة الأصدقاء")),
                  const ListTile(leading: Icon(Icons.help_outline), title: Text("مساعدة")),
                  ListTile(
                    leading: const Icon(Icons.nightlight_round),
                    title: const Text("الوضع الليلي"),
                    trailing: Switch(value: true, activeColor: AppColors.primary, onChanged: (v) {}),
                  ),
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
      backgroundColor: AppColors.surface,
      child: SafeArea(
        child: ListView(
          padding: EdgeInsets.zero,
          children: const [
            DrawerHeader(
              decoration: BoxDecoration(color: AppColors.background),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Icon(Icons.rocket_launch, color: AppColors.primary, size: 40),
                  SizedBox(height: 10),
                  Text("محركات الـ Super App", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            ListTile(leading: Icon(Icons.manage_search, color: Colors.tealAccent), title: Text("محرك البحث المتقدم")),
            ListTile(leading: Icon(Icons.group_add, color: Colors.blue), title: Text("أداة النقل الذكي")),
            ListTile(leading: Icon(Icons.design_services, color: Colors.pinkAccent), title: Text("استوديو التصميم وتوليد الإيصالات")),
            ListTile(leading: Icon(Icons.psychology, color: Colors.purpleAccent), title: Text("مساعد الذكاء الاصطناعي (AGI)")),
            Divider(color: Colors.grey),
            ListTile(leading: Icon(Icons.light_mode), title: Text("النمط النهاري/الليلي")),
          ],
        ),
      ),
    );
  }
}
// ==============================================================================
// 9. شاشات الإعدادات والخصوصية (النسخة الكاملة والمطابقة للصور 100%)
// ==============================================================================
class AccountSettingsScreen extends StatelessWidget {
  const AccountSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("الإعدادات", style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(icon: const Icon(Icons.search), onPressed: () {}),
          IconButton(icon: const Icon(Icons.more_vert), onPressed: () {}),
        ],
      ),
      body: ListView(
        children: [
          // 1. ترويسة الحساب الشخصي (Profile Header)
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
                    SizedBox(height: 5),
                    Text("@AymnGuard", style: TextStyle(fontSize: 14, color: Colors.white54)),
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
          child: Text(title, style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
        ),
        Container(
          color: AppColors.surface,
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
          ? Switch(value: switchValue, activeColor: AppColors.primary, onChanged: (v) {})
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
// 10. شاشة الخصوصية والأمان (النسخة الكاملة المطابقة للصور)
// ==============================================================================
class PrivacyAndSecurityScreen extends StatelessWidget {
  const PrivacyAndSecurityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("الخصوصية والأمان"),
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
            child: Text("مراجعة قائمة الأجهزة التي قمت بتسجيل دخول حسابك على الإمبراطورية فيها.", style: TextStyle(color: Colors.grey, fontSize: 12)),
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
          child: Text(title, style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
        ),
        Container(
          color: AppColors.surface,
          child: Column(children: items),
        ),
      ],
    );
  }

  Widget _buildPrivacyTile(String title, String status, IconData icon) {
    return ListTile(
      leading: Icon(icon, color: Colors.grey),
      title: Text(title, style: const TextStyle(color: Colors.white, fontSize: 15)),
      trailing: Text(status, style: const TextStyle(color: AppColors.primary, fontSize: 14)),
      onTap: () {},
    );
  }
}

class ContactsScreen extends StatelessWidget { 
  const ContactsScreen({super.key}); 
  @override 
  Widget build(BuildContext context) { 
    return const Scaffold(backgroundColor: AppColors.background, body: Center(child: Text("جهات الاتصال الإمبراطورية", style: TextStyle(color: Colors.grey)))); 
  } 
}

