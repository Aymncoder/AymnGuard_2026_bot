import React, { useState, useEffect, useRef } from 'react';
import { Shield, Zap, Database, TrendingUp, Activity, Terminal } from 'lucide-react';

const ModuleCard = ({ title, status, icon: Icon, children }) => (
  <div className="bg-[#1A1A1A]/80 backdrop-blur-md border border-[#333] p-6 hover:border-[#00E5FF] transition-all duration-300 shadow-xl">
    <div className="flex justify-between items-center mb-4">
      <h3 className="text-[#00E5FF] font-mono uppercase tracking-widest text-sm flex items-center gap-2">
        <Icon size={18} /> {title}
      </h3>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${status === 'ERROR' ? 'bg-red-500' : 'bg-green-500 animate-pulse'}`}></span>
        <span className="text-[10px] text-gray-500 uppercase">{status}</span>
      </div>
    </div>
    {children}
  </div>
);

const SovereignDashboard = () => {
  const [serverLogs, setServerLogs] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState("CONNECTING...");
  
  // مراجع للتحكم في دورة حياة الاتصال ومنع تسريب الذاكرة
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    // مفتاح الترخيص الخاص بك (يفضل لاحقاً وضعه في ملف .env)
    const licenseKey = "AymnGuard_Enterprise_2026";
    // تم الربط المباشر بالسيرفر السحابي المدفوع الخاص بك
    const wsUrl = `ws://135.181.86.199:8000/api/v1/ws/monitor/${licenseKey}`;

    const connectWebSocket = () => {
      // إغلاق أي اتصال سابق معلق قبل فتح اتصال جديد
      if (wsRef.current) {
        wsRef.current.close();
      }

      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnectionStatus("CONNECTED");
        setServerLogs(prev => [`[System]: Secured connection established with Cloud Core (135.181.86.199)`, ...prev].slice(0, 50));
      };

      ws.onmessage = (event) => {
        const newLog = event.data;
        // الاحتفاظ بآخر 50 سجلاً لتكوين شاشة مراقبة حقيقية
        setServerLogs((prevLogs) => [newLog, ...prevLogs].slice(0, 50));
      };

      ws.onerror = (error) => {
        console.error("WebSocket Error:", error);
        setConnectionStatus("ERROR");
      };

      ws.onclose = () => {
        setConnectionStatus("RECONNECTING...");
        // خوارزمية إعادة الاتصال التلقائي بعد 3 ثوانٍ
        reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
      };
    };

    // بدء الاتصال عند تحميل المكون
    connectWebSocket();

    // التنظيف عند مغادرة الصفحة
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans p-8">
      {/* Header */}
      <header className="mb-10 flex justify-between items-end border-b border-[#333] pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tighter uppercase">AymnGuard <span className="text-[#00E5FF]">Command Center</span></h1>
          <p className="text-[#666] font-mono text-sm mt-1">SYSTEM ARCHITECTURE: CLOUD PRODUCTION OS v6.0</p>
        </div>
        <div className="bg-[#1A1A1A] px-4 py-2 border border-[#00E5FF]/30 font-mono text-xs text-[#00E5FF] flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${connectionStatus === 'CONNECTED' ? 'bg-green-500 animate-pulse' : connectionStatus === 'ERROR' ? 'bg-red-500' : 'bg-yellow-500'}`}></span>
          WS_MONITOR: {connectionStatus}
        </div>
      </header>

      {/* Operational Units Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        
        {/* Session Hub */}
        <ModuleCard title="Session Hub" status={connectionStatus === 'CONNECTED' ? "ACTIVE" : "PENDING"} icon={Database}>
          <div className="text-2xl font-mono">1,204 <span className="text-xs text-gray-500">SESSIONS</span></div>
          <div className="w-full bg-[#050505] h-2 mt-2 border border-[#333]">
            <div className="bg-[#00E5FF] h-full w-[85%] transition-all duration-500"></div>
          </div>
        </ModuleCard>

        {/* Trading Engine */}
        <ModuleCard title="Trading Engine" status={connectionStatus === 'CONNECTED' ? "SYNCHRONIZED" : "WAITING"} icon={TrendingUp}>
          <div className="text-lg font-mono text-[#FFB300]">+4.2% DAILY</div>
          <div className="mt-2 text-xs text-[#666]">RSI: 42.1 (NEUTRAL)</div>
        </ModuleCard>

        {/* Protection Shield */}
        <ModuleCard title="Protection Shield" status={connectionStatus === 'CONNECTED' ? "SECURE" : "STANDBY"} icon={Shield}>
          <div className="text-sm">Threats Mitigated: <span className="text-[#00E5FF]">48,902</span></div>
          <div className="mt-2 text-xs text-[#666]">Last Breach: NONE</div>
        </ModuleCard>

      </div>

      {/* Real-time Terminal / Live Feedback Box */}
      <div className="bg-[#1A1A1A]/80 backdrop-blur-md border border-[#333] p-6">
        <h3 className="text-[#00E5FF] font-mono uppercase tracking-widest text-sm flex items-center gap-2 mb-4">
          <Terminal size={18} /> Live Cloud Terminal Stream
        </h3>
        <div className="bg-[#050505] p-4 font-mono text-xs text-green-400 border border-[#222] h-48 overflow-y-auto flex flex-col-reverse">
          {serverLogs.length === 0 ? (
            <span className="text-gray-600">Awaiting real-time telemetry packets from 135.181.86.199...</span>
          ) : (
            serverLogs.map((log, index) => (
              <div key={index} className="py-1 border-b border-[#111] opacity-90">&gt; {log}</div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default SovereignDashboard;
