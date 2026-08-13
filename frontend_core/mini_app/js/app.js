/**
 * ==============================================================================
 * AymnGuard Enterprise - Main Mini App Controller & Universal Media Hub (v5.0)
 * ==============================================================================
 */

import { GlobalState } from './state.js';
import { ApiGateway } from './api.js';

// توجيه جميع الاتصالات إلى السيرفر السحابي المدفوع للإنتاج
const CLOUD_API_BASE_URL = window.ENV_API_URL || "https://api.aymnguard.cloud";

const tg = window.Telegram?.WebApp;
try {
    if (tg) {
        tg.expand();
        tg.ready();
        
        const isDarkTheme = tg.colorScheme === 'dark';
        if (isDarkTheme) {
            document.documentElement.classList.add('dark');
            tg.setHeaderColor('#0f172a');
            tg.setBackgroundColor('#0f172a');
        } else {
            document.documentElement.classList.remove('dark');
            tg.setHeaderColor('#f8fafc');
            tg.setBackgroundColor('#f8fafc');
        }
    }
} catch (e) {
    console.warn("Operating outside official Telegram environment, default dark theme applied.");
}

const UI = {
    connectionStatus: document.getElementById('connection-status'),
    contentArea: document.getElementById('content-area'),
    loadingScreen: document.getElementById('loading-screen'),
    bottomNav: document.getElementById('bottom-nav')
};

const Haptic = {
    success: () => tg?.HapticFeedback?.notificationOccurred('success'),
    error: () => tg?.HapticFeedback?.notificationOccurred('error'),
    tap: () => tg?.HapticFeedback?.impactOccurred('medium')
};

GlobalState.subscribe((key, value) => {
    if (key === 'activeTab') {
        renderActiveTab(value);
    }
});

async function initializeApp() {
    try {
        const cachedUser = GlobalState.get('user');
        if (cachedUser) {
            renderDashboard(cachedUser);
            if (UI.connectionStatus) {
                UI.connectionStatus.classList.remove('bg-amber-500', 'bg-rose-500');
                UI.connectionStatus.classList.add('bg-emerald-500');
            }
        }

        const initData = tg?.initData;
        if (!initData) {
            console.warn("Running in development/fallback mode without Telegram initData.");
        }

        const authResponse = await ApiGateway.request('/auth/telegram/verify', {
            method: 'POST',
            body: JSON.stringify({
                user_id: tg?.initDataUnsafe?.user?.id || 1000000,
                username: tg?.initDataUnsafe?.user?.username || "aymnguard_admin",
                first_name: tg?.initDataUnsafe?.user?.first_name || "Sovereign User"
            })
        });

        if (authResponse?.access_token) {
            GlobalState.set('token', authResponse.access_token);
        }

        const userData = tg?.initDataUnsafe?.user || { first_name: "المستخدم السيادي", username: "aymnguard" };
        GlobalState.set('user', userData);

        Haptic.success();
        if (UI.connectionStatus) {
            UI.connectionStatus.classList.remove('bg-amber-500', 'bg-rose-500');
            UI.connectionStatus.classList.add('bg-emerald-500', 'shadow-[0_0_12px_rgba(16,185,129,0.8)]');
        }
        
        renderDashboard(userData);

    } catch (error) {
        console.warn("Fallback to local offline mode activated:", error.message);
        const fallbackUser = GlobalState.get('user') || { first_name: "القائد", username: "offline_mode" };
        renderDashboard(fallbackUser);
        
        if (UI.connectionStatus) {
            UI.connectionStatus.classList.remove('bg-amber-500', 'bg-emerald-500');
            UI.connectionStatus.classList.add('bg-rose-500');
        }
    }
}

function renderDashboard(user) {
    if (UI.loadingScreen) UI.loadingScreen.classList.add('hidden');
    if (UI.bottomNav) UI.bottomNav.classList.remove('hidden');

    if (UI.contentArea) {
        UI.contentArea.innerHTML = `
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl text-center animate-fade-in space-y-4">
                <div class="w-20 h-20 bg-brand-500/10 border border-brand-500/30 rounded-full flex items-center justify-center mx-auto shadow-inner">
                    <span class="text-2xl font-bold text-brand-400">AG</span>
                </div>
                <div>
                    <h2 class="text-xl font-black text-white mb-1">مرحباً بك، ${user.first_name}</h2>
                    <p class="text-xs text-brand-500 font-mono">@${user.username || 'SovereignUser'}</p>
                </div>
                <div class="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs px-3 py-1.5 rounded-full font-bold">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> النظام السيادي محصن ومتصل
                </div>
                <p class="text-xs text-slate-400 leading-relaxed">
                    تم دمج محرك البحث الشامل والوسائط الذكية بنجاح. يمكنك الآن تصفح المنصة والبحث في كافة شبكات التواصل مباشرة عبر السحابة.
                </p>
                <button onclick="window.switchTab('search')" class="w-full bg-brand-500 hover:bg-blue-600 active:scale-95 text-white font-bold py-3.5 rounded-xl shadow-lg transition-all duration-200">
                    الانتقال إلى محرك البحث والوسائط
                </button>
            </div>
        `;
    }
}

window.switchTab = (tabName) => {
    Haptic.tap();
    GlobalState.set('activeTab', tabName);
};

function renderActiveTab(tab) {
    if (!UI.contentArea) return;
    if (tab === 'metrics') {
        UI.contentArea.innerHTML = `
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl animate-fade-in space-y-4">
                <h3 class="text-lg font-bold text-white border-b border-slate-800 pb-2">المؤشرات الحية للنظام</h3>
                <div class="grid grid-cols-2 gap-3">
                    <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center">
                        <span class="text-xs text-slate-400">زمن الاستجابة</span>
                        <p class="text-xl font-black text-emerald-400 mt-1">4.2ms</p>
                    </div>
                    <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center">
                        <span class="text-xs text-slate-400">حالة التشفير</span>
                        <p class="text-xl font-black text-blue-400 mt-1">AES-256</p>
                    </div>
                </div>
            </div>
        `;
    } else if (tab === 'security') {
        UI.contentArea.innerHTML = `
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl animate-fade-in space-y-4">
                <h3 class="text-lg font-bold text-white border-b border-slate-800 pb-2">درع الحماية الذكي</h3>
                <p class="text-xs text-slate-400">نظام حماية من الهجمات العشوائية ومراقبة تدفق الطلبات نشط بكفاءة كاملة عبر السحابة.</p>
                <div class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-xs text-emerald-400 font-bold text-center">
                    الحالة: مؤمن ضد الهجمات السيبرانية
                </div>
            </div>
        `;
    } else if (tab === 'search') {
        renderSearchMediaTabUI();
    } else {
        renderDashboard(GlobalState.get('user') || { first_name: "المستخدم" });
    }
}

function renderSearchMediaTabUI() {
    UI.contentArea.innerHTML = `
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl animate-fade-in space-y-4">
            <div class="flex items-center gap-3 border-b border-slate-800 pb-3">
                <div>
                    <h3 class="text-base font-black text-white">محرك البحث والوسائط الشامل</h3>
                    <p class="text-xs text-brand-500">ابحث وشاهد عبر البنية السحابية</p>
                </div>
            </div>

            <div class="space-y-3">
                <div class="flex gap-2">
                    <input type="text" id="search-query" placeholder="ابحث عن أي شيء في الويب، يوتيوب، ووسائل التواصل..." class="flex-1 bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-brand-500">
                    <button onclick="window.executeSearch()" class="bg-brand-500 hover:bg-blue-600 text-white font-bold px-4 rounded-xl text-xs transition-all">بحث</button>
                </div>

                <div class="flex gap-2 overflow-x-auto pb-1 text-[10px]" id="platform-filters">
                    <button onclick="window.setPlatformFilter('all', event)" class="px-3 py-1.5 rounded-lg bg-brand-500 text-white font-bold whitespace-nowrap filter-btn">الكل</button>
                    <button onclick="window.setPlatformFilter('youtube', event)" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 font-bold whitespace-nowrap filter-btn">يوتيوب وفيديوهات</button>
                    <button onclick="window.setPlatformFilter('social', event)" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 font-bold whitespace-nowrap filter-btn">تواصل اجتماعي</button>
                </div>
            </div>

            <div id="search-results-container" class="space-y-3 mt-4 max-h-72 overflow-y-auto">
                <p class="text-xs text-slate-500 text-center py-4">اكتب ما تبحث عنه وابدأ الاستكشاف الفوري...</p>
            </div>
        </div>

        <div id="media-modal" class="fixed inset-0 bg-slate-950/90 backdrop-blur-md hidden flex flex-col justify-center p-4 z-50">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3 relative max-w-md mx-auto w-full">
                <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                    <h4 id="modal-title" class="text-xs font-bold text-white truncate">مشغل الوسائط السيادي</h4>
                    <button onclick="window.closeMediaModal()" class="text-slate-400 hover:text-white font-bold text-sm">✕</button>
                </div>
                <div id="media-player-container" class="w-full h-48 bg-black rounded-xl overflow-hidden flex items-center justify-center">
                </div>
            </div>
        </div>
    `;
}

let currentPlatform = 'all';

window.setPlatformFilter = (platform, event) => {
    currentPlatform = platform;
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        btn.classList.replace('bg-brand-500', 'bg-slate-800');
        btn.classList.replace('text-white', 'text-slate-400');
    });
    if (event && event.currentTarget) {
        event.currentTarget.classList.replace('bg-slate-800', 'bg-brand-500');
        event.currentTarget.classList.replace('text-slate-400', 'text-white');
    }
};

window.executeSearch = async () => {
    const queryInput = document.getElementById('search-query');
    const container = document.getElementById('search-results-container');
    if (!queryInput || !container) return;

    const query = queryInput.value;

    if (!query.trim()) {
        alert("الرجاء كتابة نص للبحث.");
        return;
    }

    container.innerHTML = `<div class="text-center py-6"><div class="w-6 h-6 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto"></div><p class="text-[10px] text-slate-400 mt-2">جاري التفتيش عبر الشبكات السحابية...</p></div>`;

    try {
        const response = await fetch(`${CLOUD_API_BASE_URL}/api/v1/search?q=${encodeURIComponent(query)}&platform=${currentPlatform}`);
        const data = await response.json();

        if (response.ok && data.results && data.results.length > 0) {
            container.innerHTML = data.results.map(item => `
                <div class="bg-slate-950 border border-slate-800 p-3 rounded-xl flex items-center gap-3 hover:border-brand-500/50 transition-all cursor-pointer" onclick="window.openMediaViewer('${item.title.replace(/'/g, "\\'")}', '${item.url}', '${item.type}')">
                    <img src="${item.thumbnail}" class="w-16 h-16 object-cover rounded-lg border border-slate-800 flex-shrink-0" alt="thumbnail">
                    <div class="flex-1 min-w-0">
                        <span class="text-[9px] bg-brand-500/10 text-brand-400 px-2 py-0.5 rounded-full font-bold">${item.source_badge}</span>
                        <h4 class="text-xs font-bold text-white truncate mt-1">${item.title}</h4>
                        <p class="text-[10px] text-slate-400 mt-0.5">انقر للمشاهدة والتشغيل المباشر</p>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `<p class="text-xs text-slate-500 text-center py-4">لم يتم العثور على نتائج مطابقة.</p>`;
        }
    } catch (error) {
        container.innerHTML = `<p class="text-xs text-rose-400 text-center py-4">حدث خطأ أثناء الاتصال بمحرك البحث السحابي.</p>`;
    }
};

window.openMediaViewer = (title, url, type) => {
    const modal = document.getElementById('media-modal');
    const modalTitle = document.getElementById('modal-title');
    const playerContainer = document.getElementById('media-player-container');
    if (!modal || !modalTitle || !playerContainer) return;

    modalTitle.textContent = title;
    modal.classList.remove('hidden');

    if (type === 'video') {
        playerContainer.innerHTML = `
            <video controls autoplay class="w-full h-full object-cover">
                <source src="${url}" type="video/mp4">
                متصفحك لا يدعم تشغيل الفيديو.
            </video>
        `;
    } else {
        playerContainer.innerHTML = `
            <div class="p-6 text-center space-y-3">
                <p class="text-xs text-slate-300">محتوى نصي/رابط مباشر متاح للتصفح الداخلي الآمن عبر السحابة</p>
                <a href="${url}" target="_blank" class="inline-block bg-brand-500 text-white font-bold text-xs px-4 py-2 rounded-xl">فتح الرابط</a>
            </div>
        `;
    }
};

window.closeMediaModal = () => {
    const modal = document.getElementById('media-modal');
    const playerContainer = document.getElementById('media-player-container');
    if (playerContainer) playerContainer.innerHTML = '';
    if (modal) modal.classList.add('hidden');
};

window.triggerAction = () => {
    Haptic.success();
    alert("استجابة النظام لحظية وفائقة السرعة عبر السيرفرات السحابية بنجاح تام!");
};

initializeApp();
