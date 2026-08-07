import React, { useState, useEffect } from 'react';
import { Shield, Zap, Database, TrendingUp, Activity, Terminal } from 'lucide-react';

const ModuleCard = ({ title, status, icon: Icon, children }) => (
  <div className="bg-[#1A1A1A]/80 backdrop-blur-md border border-[#333] p-6 hover:border-[#00E5FF] transition-all duration-300">
    <div className="flex justify-between items-center mb-4">
      <h3 className="text-[#00E5FF] font-mono uppercase tracking-widest text-sm flex items-center gap-2">
        <Icon size={18} /> {title}
      </h3>
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
        <span className="text-[10px] text-gray-500 uppercase">{status}</span>
      </div>
    </div>
    {children}
  </div>
);

const SovereignDashboard = () => {
  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans p-8">
      {/* Header */}
      <header className="mb-10 flex justify-between items-end border-b border-[#333] pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tighter uppercase">AymnGuard <span className="text-[#00E5FF]">Command Center</span></h1>
          <p className="text-[#666] font-mono text-sm mt-1">SYSTEM STATUS: ALL UNITS OPERATIONAL</p>
        </div>
        <div className="bg-[#1A1A1A] px-4 py-2 border border-[#00E5FF]/30 font-mono text-[#00E5FF]">
          LIVE: WS_MONITOR_ACTIVE
        </div>
      </header>

      {/* Operational Units Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Session Hub */}
        <ModuleCard title="Session Hub" status="ACTIVE" icon={Database}>
          <div className="text-2xl font-mono">1,204 <span className="text-xs text-gray-500">SESSIONS</span></div>
          <div className="w-full bg-[#050505] h-2 mt-2 border border-[#333]">
            <div className="bg-[#00E5FF] h-full w-[85%]"></div>
          </div>
        </ModuleCard>

        {/* Trading Engine */}
        <ModuleCard title="Trading Engine" status="SYNCHRONIZED" icon={TrendingUp}>
          <div className="text-lg font-mono text-[#FFB300]">+4.2% DAILY</div>
          <div className="mt-2 text-xs text-[#666]">RSI: 42.1 (NEUTRAL)</div>
        </ModuleCard>

        {/* Protection Shield */}
        <ModuleCard title="Protection Shield" status="SECURE" icon={Shield}>
          <div className="text-sm">Threats Mitigated: <span className="text-[#00E5FF]">48,902</span></div>
          <div className="mt-2 text-xs text-[#666]">Last Breach: NONE</div>
        </ModuleCard>

      </div>
    </div>
  );
};

export default SovereignDashboard;
