import 'package:flutter/material.dart';

class AccountSettingsScreen extends StatelessWidget {
  const AccountSettingsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF151E27),
      appBar: AppBar(title: const Text('إعدادات الحساب')),
      body: const Center(child: Text('إعدادات الحساب', style: TextStyle(color: Colors.white))),
    );
  }
}

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF151E27),
      appBar: AppBar(title: const Text('جهات الاتصال')),
      body: const Center(child: Text('جهات الاتصال', style: TextStyle(color: Colors.white))),
    );
  }
}
