import 'package:flutter/material.dart';
import 'package:mobile_empire_app/app_config.dart';
import 'package:mobile_empire_app/chat_widgets.dart'; 
import 'package:mobile_empire_app/community_widgets.dart'; 

class TelegramCoreChats extends StatelessWidget {
  const TelegramCoreChats({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 6,
      child: Scaffold(
        appBar: AppBar(
          leading: Builder(
              builder: (context) => IconButton(
                  icon: const Icon(Icons.menu, color: Colors.white),
                  onPressed: () => Scaffold.of(context).openDrawer())),
          title: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("يتم الاتصال بالخادم الوكيل",
                  style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.white)),
              Text("إعداد الخادم الوكيل...",
                  style: TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          actions: [
            IconButton(
                icon: const Icon(Icons.search, color: Colors.white),
                onPressed: () {}),
            Builder(
                builder: (context) => IconButton(
                    icon: const Icon(Icons.rocket_launch,
                        color: AppColors.primary),
                    onPressed: () => Scaffold.of(context).openEndDrawer())),
          ],
          bottom: const TabBar(
            isScrollable: true,
            indicatorColor: AppColors.primary,
            labelColor: AppColors.primary,
            unselectedLabelColor: Colors.grey,
            tabs: [
              Tab(text: "الكل", icon: Badge(label: Text('١٣'), child: Icon(Icons.chat))),
              Tab(text: "شخصي", icon: Icon(Icons.person)),
              Tab(text: "مجموعات", icon: Badge(label: Text('١٢'), child: Icon(Icons.group))),
              Tab(text: "قنوات", icon: Icon(Icons.campaign)),
              Tab(text: "بوتات", icon: Icon(Icons.smart_toy)),
              Tab(
                  text: "مجتمعاتي",
                  icon: Icon(Icons.hub, color: AppColors.accentGold)),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            AllChatsListWidget(), 
            Center(
                child: Text("المراسلات الشخصية",
                    style: TextStyle(color: Colors.grey))),
            Center(
                child: Text("مجموعاتك النشطة",
                    style: TextStyle(color: Colors.grey))),
            Center(
                child: Text("قنواتك المشترك بها",
                    style: TextStyle(color: Colors.grey))),
            Center(
                child: Text("بوتاتك الخدمية",
                    style: TextStyle(color: Colors.grey))),
            MyCommunitiesPortalWidget(), 
          ],
        ),
        floatingActionButton: FloatingActionButton(
            backgroundColor: AppColors.primary,
            onPressed: () {},
            child: const Icon(Icons.edit, color: Colors.white)),
      ),
    );
  }
}
