import 'package:flutter/material.dart';
import 'package:mobile_empire_app/app_config.dart';

// ==============================================================================
// شاشات الإعدادات والخصوصية (Settings & Privacy Screens)
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
                    Text("ابو يمان",
                        style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.white)),
                    SizedBox(height: 5),
                    Text("+91 9265035200",
                        style: TextStyle(fontSize: 14, color: Colors.grey)),
                    SizedBox(height: 5),
                    Text("@AymnGuard",
                        style: TextStyle(fontSize: 14, color: Colors.white54)),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),

          // 2. إعدادات AymnGuard المتقدمة
          _buildSettingsSection(
            title: "إعدادات الإمبراطورية",
            items: [
              _buildSettingsTile(context, "إعدادات AymnGuard Plus",
                  Icons.settings_suggest, Colors.green),
              _buildSettingsTile(
                  context, "الأقسام المخفية", Icons.visibility_off, Colors.blueGrey),
              _buildSettingsTile(
                  context, "مانع الإعلانات", Icons.block, Colors.redAccent,
                  hasSwitch: true, switchValue: true),
            ],
          ),

          // 3. الإعدادات العامة
          _buildSettingsSection(
            title: "الإعدادات العامة",
            items: [
              _buildSettingsTile(
                  context, "إعدادات المحادثات", Icons.chat, Colors.greenAccent),
              _buildSettingsTile(context, "الخصوصية والأمان", Icons.lock,
                  Colors.lightBlueAccent,
                  destination: const PrivacyAndSecurityScreen()),
              _buildSettingsTile(context, "الإشعارات والأصوات", Icons.notifications,
                  Colors.redAccent),
              _buildSettingsTile(
                  context, "البيانات والتخزين", Icons.pie_chart, Colors.blue),
              _buildSettingsTile(context, "توفير الطاقة",
                  Icons.battery_charging_full, Colors.orange),
              _buildSettingsTile(
                  context, "اللغة", Icons.language, Colors.purpleAccent,
                  subtitle: "العربية"),
            ],
          ),

          // 4. الخدمات المميزة
          _buildSettingsSection(
            title: "المميزات",
            items: [
              _buildSettingsTile(
                  context, "AymnGuard المُميَّز", Icons.star, Colors.purple),
              _buildSettingsTile(
                  context, "الأعمال (Business)", Icons.store, Colors.pinkAccent),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSettingsSection(
      {required String title, required List<Widget> items}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(right: 16, top: 15, bottom: 5),
          child: Text(title,
              style: const TextStyle(
                  color: AppColors.primary, fontWeight: FontWeight.bold)),
        ),
        Container(
          color: AppColors.surface,
          child: Column(children: items),
        ),
        const SizedBox(height: 10),
      ],
    );
  }

  Widget _buildSettingsTile(
      BuildContext context, String title, IconData icon, Color iconColor,
      {String? subtitle,
      bool hasSwitch = false,
      bool switchValue = false,
      Widget? destination}) {
    return ListTile(
      leading: CircleAvatar(
        radius: 18,
        backgroundColor: iconColor.withOpacity(0.2),
        child: Icon(icon, size: 20, color: iconColor),
      ),
      title: Text(title, style: const TextStyle(color: Colors.white, fontSize: 15)),
      subtitle: subtitle != null
          ? Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12))
          : null,
      trailing: hasSwitch
          ? Switch(
              value: switchValue, activeColor: AppColors.primary, onChanged: (v) {})
          : const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
      onTap: () {
        if (destination != null) {
          Navigator.push(
              context, MaterialPageRoute(builder: (context) => destination));
        }
      },
    );
  }
}

// ==============================================================================
// شاشة الخصوصية والأمان
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
            child: Text(
                "مراجعة قائمة الأجهزة التي قمت بتسجيل دخول حسابك على الإمبراطورية فيها.",
                style: TextStyle(color: Colors.grey, fontSize: 12)),
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

  Widget _buildPrivacySection(
      {required String title, required List<Widget> items}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(right: 16, top: 15, bottom: 5),
          child: Text(title,
              style: const TextStyle(
                  color: AppColors.primary, fontWeight: FontWeight.bold)),
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
      trailing:
          Text(status, style: const TextStyle(color: AppColors.primary, fontSize: 14)),
      onTap: () {},
    );
  }
}

// ==============================================================================
// شاشة جهات الاتصال
// ==============================================================================

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
            child: Text("جهات الاتصال الإمبراطورية",
                style: TextStyle(color: Colors.grey))));
  }
}
