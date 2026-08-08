import 'package:flutter/material.dart';

import 'app_config.dart';
// ملاحظة: قمنا بتضمين chat_room_screen.dart هنا لأن ChatTileWidget تحتاج للانتقال إليه.
// سيظهر لك خطأ مؤقت في المستودع بخصوص هذا الملف حتى نقوم بإنشائه في الخطوة القادمة.
import 'chat_room_screen.dart';

// ==============================================================================
// مكونات واجهة المحادثات (Chat Widgets)
// ==============================================================================

/// مكون (Widget) مستقل لعرض قائمة المحادثات
class AllChatsListWidget extends StatelessWidget {
  const AllChatsListWidget({super.key});
  
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: const [
        AdvertisementBanner(),
        ChatTileWidget(
            name: "درع الأمان | AymnGuard",
            message: "💎 شراء اشتراك VIP الشامل",
            icon: Icons.security,
            color: Colors.blueGrey,
            isVerified: true,
            time: "الجمعة",
            count: 1),
        ChatTileWidget(
            name: "+966561225123",
            message: "ص انضم +966561225123 لتلي...",
            icon: Icons.person,
            color: Colors.pinkAccent,
            time: "3:38 ص",
            count: 1),
        ChatTileWidget(
            name: "فريق المطورين",
            message: "تم تحديث الخوادم بنجاح.",
            icon: Icons.group,
            color: Colors.green,
            time: "أمس",
            count: 12),
      ],
    );
  }
}

/// بانر الإعلانات
class AdvertisementBanner extends StatelessWidget {
  const AdvertisementBanner({super.key});
  @override
  Widget build(BuildContext context) {
    return Container(
        color: AppColors.surface,
        padding: const EdgeInsets.all(8),
        alignment: Alignment.center,
        child: const Text("إعلان", style: TextStyle(color: Colors.grey, fontSize: 12)));
  }
}

/// خلية المحادثة (Chat Tile)
class ChatTileWidget extends StatelessWidget {
  final String name, message, time;
  final IconData icon;
  final Color color;
  final bool isVerified;
  final int count;

  const ChatTileWidget({
    super.key,
    required this.name,
    required this.message,
    required this.icon,
    required this.color,
    this.isVerified = false,
    required this.time,
    required this.count,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => ChatRoomScreen(
                  chatName: name,
                  status: "متصل الآن",
                  avatarColor: color,
                  avatarIcon: icon))),
      leading: CircleAvatar(
          radius: 25, backgroundColor: color, child: Icon(icon, color: Colors.white, size: 30)),
      title: Row(children: [
        Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        if (isVerified) const SizedBox(width: 5),
        if (isVerified) const Icon(Icons.verified, color: AppColors.primary, size: 16)
      ]),
      subtitle: Text(message,
          style: const TextStyle(color: Colors.grey),
          maxLines: 1,
          overflow: TextOverflow.ellipsis),
      trailing: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(time, style: const TextStyle(color: Colors.grey, fontSize: 12)),
          const SizedBox(height: 5),
          if (count > 0)
            Container(
                padding: const EdgeInsets.all(6),
                decoration: const BoxDecoration(
                    color: AppColors.primary, shape: BoxShape.circle),
                child: Text(count.toString(),
                    style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.bold))),
        ],
      ),
    );
  }
}

/// فقاعة الرسالة داخل غرفة المحادثة
class MessageBubbleWidget extends StatelessWidget {
  final String message, time;
  final bool isMe, isRead;
  const MessageBubbleWidget({
    super.key,
    required this.message,
    required this.time,
    required this.isMe,
    this.isRead = false,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
        alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
        child: Container(
            margin: const EdgeInsets.only(bottom: 10),
            constraints:
                BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
                color: isMe ? AppColors.primary : AppColors.surface,
                borderRadius: BorderRadius.only(
                    topLeft: const Radius.circular(15),
                    topRight: const Radius.circular(15),
                    bottomRight: Radius.circular(isMe ? 0 : 15),
                    bottomLeft: Radius.circular(isMe ? 15 : 0))),
            child: Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(message, style: const TextStyle(color: Colors.white, fontSize: 15)),
                  const SizedBox(height: 5),
                  Row(mainAxisSize: MainAxisSize.min, children: [
                    Text(time,
                        style: TextStyle(
                            color: isMe ? Colors.white70 : Colors.grey,
                            fontSize: 10)),
                    if (isMe) const SizedBox(width: 4),
                    if (isMe)
                      Icon(isRead ? Icons.done_all : Icons.done,
                          color: isRead ? AppColors.accentGold : Colors.white70,
                          size: 14)
                  ])
                ])));
  }
}

/// شارة التاريخ (مثل: اليوم، الأمس)
class DateBadgeWidget extends StatelessWidget {
  final String date;
  const DateBadgeWidget({super.key, required this.date});
  
  @override
  Widget build(BuildContext context) {
    return Center(
        child: Container(
            margin: const EdgeInsets.only(bottom: 15),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
            decoration: BoxDecoration(
                color: AppColors.surface.withOpacity(0.5),
                borderRadius: BorderRadius.circular(10)),
            child: Text(date,
                style: const TextStyle(color: Colors.grey, fontSize: 12))));
  }
}
