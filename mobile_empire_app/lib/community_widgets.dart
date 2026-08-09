import 'package:flutter/material.dart';
import 'package:mobile_empire_app/app_config.dart';


// ==============================================================================
// مكونات بوابة مجتمعاتي المستقلة (Community Portal Widgets)
// ==============================================================================

class MyCommunitiesPortalWidget extends StatelessWidget {
  const MyCommunitiesPortalWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: const [
        Text("إدارة مجتمعاتي وأدواتي 👑",
            style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: AppColors.accentGold)),
        SizedBox(height: 5),
        Text("نظرة شاملة لكل ما تملكه أو تديره في الإمبراطورية.",
            style: TextStyle(color: Colors.grey, fontSize: 12)),
        Divider(color: Colors.white24, height: 30),
        
        Text("قنواتي ومجموعاتي",
            style: TextStyle(
                color: AppColors.primary, fontWeight: FontWeight.bold)),
        SizedBox(height: 10),
        CommunityCardWidget(
            title: "مجموعة التداول VIP",
            subtitle: "أنت المالك • 5,430 عضو",
            icon: Icons.group,
            iconColor: Colors.orangeAccent),
        CommunityCardWidget(
            title: "قناة تحديثات AymnGuard",
            subtitle: "أنت المالك • 12,000 مشترك",
            icon: Icons.campaign,
            iconColor: Colors.blueAccent),
        
        SizedBox(height: 20),
        Text("أدواتي وبوتاتي النشطة",
            style: TextStyle(
                color: AppColors.primary, fontWeight: FontWeight.bold)),
        SizedBox(height: 10),
        CommunityCardWidget(
            title: "بوت الحماية الشامل",
            subtitle: "اشتراك مفعل (ينتهي بعد 20 يوم)",
            icon: Icons.security,
            iconColor: Colors.green),
        CommunityCardWidget(
            title: "مولد التصميمات الذكي",
            subtitle: "أداة مفعلة • جاهز للاستخدام",
            icon: Icons.brush,
            iconColor: Colors.pinkAccent),
      ],
    );
  }
}

class CommunityCardWidget extends StatelessWidget {
  final String title, subtitle;
  final IconData icon;
  final Color iconColor;

  const CommunityCardWidget({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.surface,
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(color: iconColor.withOpacity(0.3), width: 1)),
      child: ListTile(
        leading: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
                color: iconColor.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8)),
            child: Icon(icon, color: iconColor)),
        title: Text(title,
            style: const TextStyle(
                fontWeight: FontWeight.bold, color: Colors.white)),
        subtitle: Text(subtitle,
            style: const TextStyle(color: Colors.grey, fontSize: 12)),
        trailing: const Icon(Icons.arrow_forward_ios,
            color: Colors.grey, size: 14),
      ),
    );
  }
}
