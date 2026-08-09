import 'package:flutter/material.dart';
import 'app_config.dart';
import 'app_config.dart';
import 'chat_widgets.dart';

// ==============================================================================
// 6. شاشة المحادثة الفعلية (Chat Room UI)
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
    this.avatarColor = AppColors.primary,
    this.avatarIcon = Icons.person,
  });

  @override
  State<ChatRoomScreen> createState() => _ChatRoomScreenState();
}

class _ChatRoomScreenState extends State<ChatRoomScreen> {
  final TextEditingController _messageController = TextEditingController();

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.chatBackground,
      appBar: AppBar(
        titleSpacing: 0,
        leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () => Navigator.pop(context)),
        title: Row(
          children: [
            CircleAvatar(
                radius: 18,
                backgroundColor: widget.avatarColor,
                child: Icon(widget.avatarIcon, color: Colors.white, size: 20)),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(widget.chatName,
                      style: const TextStyle(
                          fontSize: 16, fontWeight: FontWeight.bold)),
                  Text(widget.status,
                      style: const TextStyle(
                          fontSize: 12, color: AppColors.primary))
                ],
              ),
            )
          ],
        ),
        actions: [
          IconButton(icon: const Icon(Icons.call), onPressed: () {}),
          IconButton(icon: const Icon(Icons.more_vert), onPressed: () {})
        ],
      ),
      body: Column(
        children: [
          Expanded(
              child: ListView(
            padding: const EdgeInsets.all(16),
            children: const [
              DateBadgeWidget(date: "اليوم"),
              MessageBubbleWidget(
                  message: "أهلاً بك في AymnGuard Plus! كيف يمكنني مساعدتك اليوم؟",
                  time: "10:00 ص",
                  isMe: false),
              MessageBubbleWidget(
                  message: "مرحباً، تم تفعيل درع الأمان السحابي بنجاح.",
                  time: "10:05 ص",
                  isMe: true,
                  isRead: true),
            ],
          )),
          _buildMessageInputArea(),
        ],
      ),
    );
  }

  Widget _buildMessageInputArea() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      color: AppColors.surface,
      child: SafeArea(
        child: Row(
          children: [
            IconButton(
                icon: const Icon(Icons.attach_file, color: Colors.grey),
                onPressed: () {}),
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 15),
                decoration: BoxDecoration(
                    color: AppColors.chatBackground,
                    borderRadius: BorderRadius.circular(25)),
                child: TextField(
                  controller: _messageController,
                  style: const TextStyle(color: Colors.white),
                  decoration: const InputDecoration(
                      hintText: "مراسلة...",
                      hintStyle: TextStyle(color: Colors.grey),
                      border: InputBorder.none,
                      icon: Icon(Icons.emoji_emotions_outlined,
                          color: Colors.grey)),
                ),
              ),
            ),
            const SizedBox(width: 8),
            CircleAvatar(
                backgroundColor: AppColors.primary,
                radius: 22,
                child: IconButton(
                    icon: const Icon(Icons.mic, color: Colors.white),
                    onPressed: () {}))
          ],
        ),
      ),
    );
  }
}
