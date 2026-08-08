// ==============================================================================
// AymnGuard Enterprise : Sovereign Mobile App (Flutter Frontend - v18.0.0)
// ==============================================================================
// واجهة التحكم السيادية: تتصل بخادم Python على السيرفر السحابي (VPS) 
// وتمنح المالك تحكماً مطلقاً بجميع الميكروسيرفسات.

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() {
  runApp(const SovereignEmpireApp());
}

class SovereignEmpireApp extends StatelessWidget {
  const SovereignEmpireApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AymnGuard Sovereign Hub',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: const Color(0xFF38bdf8),
        scaffoldBackgroundColor: const Color(0xFF0f172a), // لون خلفية فخم
        cardColor: const Color(0xFF1e293b),
      ),
      home: const LoginScreen(),
    );
  }
}

// ==============================================================================
// 1. شاشة الدخول السيادية (تتطلب مفتاح المالك)
// ==============================================================================
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _keyController = TextEditingController();
  final String serverIP = "192.168.X.X"; // سيتم تغييره إلى IP السيرفر السحابي (VPS)

  void _authenticate() {
    // المفتاح السري الذي برمجناه في السيرفر
    if (_keyController.text == "AG-ABSOLUTE-OWNER-KEY-2026") {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => DashboardScreen(serverIP: serverIP, ownerKey: _keyController.text)),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('❌ مفتاح السيادة غير صالح! الوصول مرفوض.', style: TextStyle(color: Colors.red))),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(30.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.security, size: 100, color: Color(0xFF38bdf8)),
              const SizedBox(height: 20),
              const Text("AymnGuard Enterprise", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const Text("بوابة التحكم السيادية", style: TextStyle(color: Colors.grey)),
              const SizedBox(height: 40),
              TextField(
                controller: _keyController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: "أدخل مفتاح المالك (Owner Key)",
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.vpn_key),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF38bdf8),
                  foregroundColor: Colors.black,
                  minimumSize: const Size(double.infinity, 50),
                ),
                onPressed: _authenticate,
                child: const Text("تأكيد الدخول الإمبراطوري", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              )
            ],
          ),
        ),
      ),
    );
  }
}

// ==============================================================================
// 2. لوحة القيادة التفاعلية (Dashboard) والمراقبة الحية
// ==============================================================================
class DashboardScreen extends StatefulWidget {
  final String serverIP;
  final String ownerKey;
  
  const DashboardScreen({super.key, required this.serverIP, required this.ownerKey});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late WebSocketChannel channel;
  String _liveStatus = "بانتظار الاتصال...";

  @override
  void initState() {
    super.initState();
    // الاتصال الحي بالسيرفر عبر WebSocket
    channel = WebSocketChannel.connect(
      Uri.parse('ws://${widget.serverIP}:8000/api/v1/empire/ws/live_monitor'),
    );
  }

  @override
  void dispose() {
    channel.sink.close();
    super.dispose();
  }

  // دالة إرسال الأوامر للسيرفر السحابي
  Future<void> sendEmpireCommand(String engine, String action) async {
    final url = Uri.parse('http://${widget.serverIP}:8000/api/v1/empire/execute');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "owner_key": widget.ownerKey,
          "target_engine": engine,
          "action": action,
          "parameters": {}
        }),
      );
      if (response.statusCode == 200) {
        setState(() => _liveStatus = "✅ تم تنفيذ أمر [$action] على [$engine]");
      } else {
        setState(() => _liveStatus = "❌ فشل التنفيذ: ${response.body}");
      }
    } catch (e) {
      setState(() => _liveStatus = "❌ خطأ في الاتصال بالسيرفر: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('👑 مركز القيادة الإمبراطوري'),
        backgroundColor: const Color(0xFF090d16),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // شاشة المراقبة الحية (WebSocket)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: Colors.black,
                border: Border.all(color: const Color(0xFF38bdf8)),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("🔴 المراقبة الحية للسيرفر:", style: TextStyle(color: Colors.grey)),
                  const SizedBox(height: 10),
                  Text(_liveStatus, style: const TextStyle(color: Colors.greenAccent, fontFamily: 'monospace')),
                ],
              ),
            ),
            const SizedBox(height: 20),
            
            // أزرار التحكم بالميكروسيرفسات
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
                children: [
                  _buildControlCard("درع الحماية", Icons.shield, () => sendEmpireCommand("sovereign_protection_bot", "force_lockdown")),
                  _buildControlCard("نقل الأعضاء", Icons.group_add, () => sendEmpireCommand("sovereign_session_transfer", "start_transfer")),
                  _buildControlCard("الذكاء الاصطناعي", Icons.psychology, () => sendEmpireCommand("sovereign_ai_forge", "train_bot")),
                  _buildControlCard("مولد التصميمات", Icons.brush, () => sendEmpireCommand("design_engine", "generate_receipt")),
                  _buildControlCard("تداول و Web3", Icons.candlestick_chart, () => sendEmpireCommand("web3_nexus", "audit_contract")),
                  _buildControlCard("حالة الأسطول", Icons.memory, () => sendEmpireCommand("sovereign_session_transfer", "audit_fleet")),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildControlCard(String title, IconData icon, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: const Color(0xFF38bdf8)),
            const SizedBox(height: 10),
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
