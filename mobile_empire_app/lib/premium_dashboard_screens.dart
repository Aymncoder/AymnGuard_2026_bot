import 'package:flutter/material.dart';

import 'package:mobile_empire_app/app_config.dart';
import 'package:mobile_empire_app/models/bot_model.dart';
import 'package:mobile_empire_app/api_service.dart';
import 'package:mobile_empire_app/widgets/smart_contract_audit_widget.dart';
import 'crypto_checkout_screen.dart'; // استدعاء هام جداً لعملية الدفع

// ==============================================================================
// 7. متجر الخدمات السيادية للمستخدمين (Premium Store)
// ==============================================================================

class EmpirePremiumStore extends StatelessWidget {
  const EmpirePremiumStore({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: const Text("المتجر الإمبراطوري 💎",
              style: TextStyle(fontWeight: FontWeight.bold)),
          centerTitle: true),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Text("ارتقِ بأعمالك مع الخدمات السيادية الاحترافية",
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppColors.accentGold)),
          SizedBox(height: 20),
          PremiumItemWidget(
              title: "استوديو التصميم وتوليد الإيصالات",
              desc: "تصميم شعارات وإيصالات مالية احترافية.",
              icon: Icons.brush,
              price: "15\$/شهرياً"),
          PremiumItemWidget(
              title: "مؤشرات التداول (Trading AI)",
              desc: "تحليل ذكي وحصري لأسواق الـ Web3.",
              icon: Icons.candlestick_chart,
              price: "50\$/شهرياً"),
          PremiumItemWidget(
              title: "محركات البحث العالمية",
              desc: "فهرسة استخباراتية وبحث دقيق غير محدود.",
              icon: Icons.travel_explore,
              price: "25\$/شهرياً"),
          PremiumItemWidget(
              title: "بوت الحماية الجنائية الشامل",
              desc: "حماية مجموعاتك من الثغرات والعقود.",
              icon: Icons.security,
              price: "10\$/شهرياً"),
        ],
      ),
    );
  }
}

class PremiumItemWidget extends StatelessWidget {
  final String title, desc, price;
  final IconData icon;

  const PremiumItemWidget({
    super.key,
    required this.title,
    required this.desc,
    required this.icon,
    required this.price,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.surface,
      shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
          side: const BorderSide(color: AppColors.accentGold, width: 0.5)),
      margin: const EdgeInsets.only(bottom: 15),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(children: [
              Icon(icon, color: AppColors.accentGold, size: 30),
              const SizedBox(width: 10),
              Expanded(
                  child: Text(title,
                      style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.white))),
              Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                      color: Colors.redAccent,
                      borderRadius: BorderRadius.circular(8)),
                  child: Text(price,
                      style: const TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 12)))
            ]),
            const SizedBox(height: 10),
            Text(desc,
                style: const TextStyle(color: Colors.grey, fontSize: 13)),
            const SizedBox(height: 15),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary),
                onPressed: () {
                  // استخراج الرقم فقط من نص السعر
                  double planPrice = double.tryParse(price.replaceAll(RegExp(r'[^0-9.]'), '')) ?? 10.0;

                  // الانتقال إلى شاشة الدفع
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => CryptoCheckoutScreen(
                        invoiceId: "INV_${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}",
                        amount: planPrice,
                        // ضع عنوان محفظتك هنا
                        walletAddress: "0x55d398326f99059fF775485246999027B3197955", 
                      ),
                    ),
                  );
                },
                child: const Text("اشتراك الآن",
                    style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
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
        title: const Text("لوحة القيادة السيادية 👑",
            style: TextStyle(
                color: Colors.redAccent, fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
              icon: const Icon(Icons.add_box,
                  color: AppColors.primary, size: 28),
              onPressed: () => showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  backgroundColor: Colors.transparent,
                  builder: (c) => const BotInstallerSheet()))
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text("الميكروسيرفسات التشغيلية الحية",
                  style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppColors.accentGold)),
              const SizedBox(height: 15),
              GridView.count(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  crossAxisCount: 2,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 1.1,
                  children: const [
                    ServiceCardWidget(
                        title: "بوت الحماية",
                        status: "يحمي 45 مجموعة",
                        icon: Icons.security,
                        color: Colors.green),
                    ServiceCardWidget(
                        title: "النقل الذكي",
                        status: "وكلاء AI نشطون",
                        icon: Icons.group_add,
                        color: Colors.blue),
                    ServiceCardWidget(
                        title: "مولد التصميمات",
                        status: "جاهز للعمل",
                        icon: Icons.brush,
                        color: Colors.pink),
                    ServiceCardWidget(
                        title: "تداول Web3",
                        status: "تدقيق العقود",
                        icon: Icons.candlestick_chart,
                        color: Colors.orange),
                  ]),
              
              const SizedBox(height: 20), // مسافة بسيطة قبل البطاقة الجديدة

              // === إدراج بطاقة التدقيق الجنائي هنا ===
              const SmartContractAuditWidget(), 

              const Divider(color: Colors.white24, height: 40, thickness: 1),
              
              const Text("إدارة الأسعار وجدار الدفع (Paywall)",
                  style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white)),
              const SizedBox(height: 15),
              const AdminControlTileWidget(
                  title: "أدوات التصميم والإيصالات",
                  subtitle: "السعر الحالي: 15\$",
                  isActive: true),
              const AdminControlTileWidget(
                  title: "مؤشرات التداول (AI)",
                  subtitle: "السعر الحالي: 50\$",
                  isActive: true),
              const AdminControlTileWidget(
                  title: "محركات البحث العالمية",
                  subtitle: "السعر الحالي: 25\$",
                  isActive: true),
              const AdminControlTileWidget(
                  title: "بوت الحماية الجنائية",
                  subtitle: "السعر الحالي: 10\$",
                  isActive: true),
            ]),
      ),
    );
  }
}

class ServiceCardWidget extends StatelessWidget {
  final String title, status;
  final IconData icon;
  final Color color;

  const ServiceCardWidget({
    super.key,
    required this.title,
    required this.status,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
        color: AppColors.surface,
        shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15)),
        elevation: 4,
        child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 38, color: color),
              const SizedBox(height: 10),
              Text(title,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 13,
                      color: Colors.white)),
              const SizedBox(height: 4),
              Text(status,
                  textAlign: TextAlign.center,
                  style:
                      const TextStyle(color: Colors.grey, fontSize: 10))
            ]));
  }
}

class AdminControlTileWidget extends StatelessWidget {
  final String title, subtitle;
  final bool isActive;

  const AdminControlTileWidget({
    super.key,
    required this.title,
    required this.subtitle,
    required this.isActive,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
        color: AppColors.surface,
        margin: const EdgeInsets.only(bottom: 10),
        child: ListTile(
            title: Text(title,
                style: const TextStyle(
                    fontWeight: FontWeight.bold, fontSize: 14)),
            subtitle: Text(subtitle,
                style: const TextStyle(
                    color: Colors.redAccent, fontSize: 12)),
            trailing: Switch(
                value: isActive,
                activeColor: Colors.green,
                onChanged: (val) {})));
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
  void initState() {
    super.initState();
    _botsFuture = SovereignApiService.fetchBots();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.75,
      decoration: const BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.only(
              topLeft: Radius.circular(20), topRight: Radius.circular(20))),
      child: Column(children: [
        const Padding(
            padding: EdgeInsets.all(15.0),
            child: Center(
                child: SizedBox(
                    width: 40,
                    height: 5,
                    child: DecoratedBox(
                        decoration: BoxDecoration(
                            color: Colors.grey,
                            borderRadius:
                                BorderRadius.all(Radius.circular(10))))))),
        const Text("➕ السحابة الإمبراطورية لتثبيت البوتات",
            style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white)),
        const Text("تواصل حي مع السيرفر ${AppConfig.serverUrl}",
            style:
                TextStyle(color: Colors.greenAccent, fontSize: 12)),
        const Divider(color: Colors.white24, height: 30),
        Expanded(
            child: FutureBuilder<List<SovereignBotModel>>(
          future: _botsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(
                  child: CircularProgressIndicator(
                      color: AppColors.primary));
            }
            if (snapshot.hasError || !snapshot.hasData) {
              return const Center(
                  child: Text("فشل الاتصال بالخادم",
                      style: TextStyle(color: Colors.redAccent)));
            }
            final bots = snapshot.data!;
            return ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: bots.length,
                itemBuilder: (context, index) {
                  final bot = bots[index];
                  return Card(
                      color: AppColors.background,
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                          leading: CircleAvatar(
                              backgroundColor:
                                  AppColors.primary.withOpacity(0.2),
                              child: Icon(bot.icon,
                                  color: AppColors.primary)),
                          title: Text(bot.name,
                              style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 14)),
                          subtitle: Text(bot.description,
                              style: const TextStyle(
                                  fontSize: 11, color: Colors.grey)),
                          trailing: bot.isInstalled
                              ? const Icon(Icons.check_circle,
                                  color: Colors.green)
                              : ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                      backgroundColor: AppColors.primary,
                                      foregroundColor: Colors.white),
                                  onPressed: () async {
                                    bool success =
                                        await SovereignApiService
                                            .installBotOnServer(bot.id);
                                    if (success) {
                                      setState(() {
                                        bot.isInstalled = true;
                                      });
                                    }
                                  },
                                  child: const Text("تثبيت",
                                      style: TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.bold)))));
                });
          },
        )),
      ]),
    );
  }
}
