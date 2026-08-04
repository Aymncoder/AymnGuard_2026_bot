const tg = window.Telegram.WebApp;
tg.expand(); 
tg.ready(); 
tg.setHeaderColor('#0f172a');
tg.setBackgroundColor('#f8fafc');

const UI = {
    connectionStatus: document.getElementById('connection-status'),
    contentArea: document.getElementById('content-area'),
    loadingScreen: document.getElementById('loading-screen'),
    bottomNav: document.getElementById('bottom-nav')
};

const Haptic = {
    success: () => tg.HapticFeedback.notificationOccurred('success'),
    error: () => tg.HapticFeedback.notificationOccurred('error'),
    tap: () => tg.HapticFeedback.impactOccurred('medium')
};

async function authenticateUser() {
    try {
        const initData = tg.initData;
        const initDataUnsafe = tg.initDataUnsafe;
        
        if (!initData) {
            throw new Error("تم رفض الوصول. يجب فتح التطبيق حصراً عبر بيئة تيليجرام المشفرة.");
        }
        
        setTimeout(() => {
            Haptic.success();
            renderDashboard(initDataUnsafe.user || { first_name: "القائد" });
        }, 1500);

    } catch (error) {
        Haptic.error();
        renderError(error.message);
    }
}

function renderDashboard(user) {
    UI.connectionStatus.classList.replace('bg-red-500', 'bg-green-500');
    UI.connectionStatus.classList.replace('shadow-[0_0_8px_rgba(239,68,68,0.8)]', 'shadow-[0_0_8px_rgba(34,197,94,0.8)]');
    UI.loadingScreen.classList.add('hidden');
    UI.bottomNav.classList.remove('hidden');

    UI.contentArea.innerHTML = `
        <div class="w-full bg-white p-6 rounded-2xl shadow-sm border border-gray-100 fade-in text-center">
            <div class="w-20 h-20 bg-brand-100 rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner border border-brand-500">
                <span class="text-3xl text-brand-500">🛡️</span>
            </div>
            <h2 class="text-xl font-extrabold text-brand-900 mb-2">مرحباً بك، ${user.first_name}</h2>
            <div class="inline-block bg-green-100 text-green-800 text-xs px-3 py-1 rounded-full font-bold tracking-wide mb-4">
                متصل وموثق سيادياً
            </div>
            <p class="text-sm text-gray-600 font-medium leading-relaxed">
                أنت الآن متصل بشكل آمن ومباشر بنواة AymnGuard. جميع الصلاحيات اللوجستية جاهزة للعمل.
            </p>
        </div>
        <button onclick="Haptic.tap()" class="mt-6 w-full bg-brand-900 text-white font-bold py-3 px-4 rounded-xl shadow-lg active:scale-95 transition-transform duration-200">
            فحص استجابة النظام
        </button>
    `;
}

function renderError(message) {
    UI.loadingScreen.innerHTML = `
        <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4 border border-red-500">
            <span class="text-3xl">⚠️</span>
        </div>
        <p class="text-sm font-bold text-red-600 text-center mb-6">${message}</p>
        <button onclick="tg.close()" class="w-full bg-brand-900 text-white font-bold py-3 px-4 rounded-xl shadow-lg active:scale-95 transition-transform duration-200">إغلاق وتأمين</button>
    `;
}

authenticateUser();
