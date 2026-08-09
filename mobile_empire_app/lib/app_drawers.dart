import 'package:flutter/material.dart';
export 'app_config.dart';

// ==============================================================================
// 10. القوائم الجانبية (Drawers)
// ==============================================================================

/// القائمة الجانبية لحسابات المستخدم (النسخة الشاملة)
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
              accountName: Text("يارب",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              accountEmail: Text("+967 775 786 363"),
              currentAccountPicture: CircleAvatar(
                  backgroundColor: Colors.white,
                  child: Icon(Icons.person, size: 40, color: Colors.grey)),
              otherAccountsPictures: [
                CircleAvatar(backgroundColor: Colors.blue, child: Text("AN"))
              ],
            ),
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  const ListTile(
                      leading: Icon(Icons.add), title: Text("إضافة حساب")),
                  const Divider(color: Colors.white24),
                  const ListTile(
                      leading: Icon(Icons.perm_contact_calendar),
                      title: Text("جهات الاتصال")),
                  const ListTile(
                      leading: Icon(Icons.call), title: Text("المكالمات")),
                  const ListTile(
                      leading: Icon(Icons.bookmark),
                      title: Text("الرسائل المحفوظة")),
                  const ListTile(
                      leading: Icon(Icons.settings), title: Text("الإعدادات")),
                  const Divider(color: Colors.white24),
                  const ListTile(
                      leading: Icon(Icons.person_add),
                      title: Text("دعوة الأصدقاء")),
                  const ListTile(
                      leading: Icon(Icons.help_outline), title: Text("مساعدة")),
                  ListTile(
                    leading: const Icon(Icons.nightlight_round),
                    title: const Text("الوضع الليلي"),
                    trailing: Switch(
                        value: true,
                        activeColor: AppColors.primary,
                        onChanged: (v) {}),
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

/// القائمة الجانبية للأدوات المتقدمة (Super App Tools)
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
                  Icon(Icons.rocket_launch,
                      color: AppColors.primary, size: 40),
                  SizedBox(height: 10),
                  Text("محركات الـ Super App",
                      style: TextStyle(
                          fontSize: 18,
                          color: Colors.white,
                          fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            ListTile(
                leading: Icon(Icons.manage_search, color: Colors.tealAccent),
                title: Text("محرك البحث المتقدم")),
            ListTile(
                leading: Icon(Icons.group_add, color: Colors.blue),
                title: Text("أداة النقل الذكي")),
            ListTile(
                leading: Icon(Icons.design_services, color: Colors.pinkAccent),
                title: Text("استوديو التصميم وتوليد الإيصالات")),
            ListTile(
                leading: Icon(Icons.psychology, color: Colors.purpleAccent),
                title: Text("مساعد الذكاء الاصطناعي (AGI)")),
            Divider(color: Colors.grey),
            ListTile(
                leading: Icon(Icons.light_mode),
                title: Text("النمط النهاري/الليلي")),
          ],
        ),
      ),
    );
  }
}
