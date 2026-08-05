/**
 * ==============================================================================
 * AymnGuard Enterprise - Sovereign Mini App Logic
 * المعالج الرئيسي لواجهة تيليجرام المصغرة والربط الأمني مع النواة
 * ==============================================================================
 */

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

        // 1. حجب الوصول من خارج بيئة تيليجرام
        if (!initData) {
            throw new Error("تم رفض الوصول. يجب فتح النظام عبر منصة تيليجرام الموثوقة.");
        }

        // 2. الاتصال السيادي بالنواة المركزية (Backend) للتحقق الكريبتوغرافي
        // ملاحظة: تأكد من أن مسار الـ API يطابق المسار الفعلي في FastAPI
        const response = await fetch('/api/v1/auth/telegram/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `tma ${initData}` // إرسال التشفير الخاص بتيليجرام
            },
            body: JSON.stringify({
                user_id: initDataUnsafe.user?.id,
                username: initDataUnsafe.user?.username,
                first_name: initDataUnsafe.user?.first_name
            })
        });

        if (!response.ok) {
            throw new Error("فشل التحقق الأمني من الخادم المركزي.");
        }

        const authData = await response.json();
        
        // 3. تخزين رمز المرور (JWT) بأمان لاستخدامه في الطلبات القادمة
        localStorage.setItem('aymnguard_access_token', authData.access_token);

        // 4. تفعيل الاستجابة الحسية وتقديم لوحة القيادة
        Haptic.success();
        renderDashboard(initDataUnsafe.user || { first_name: "أيها القائد" });

    } catch (error) {
        Haptic.error();
        renderError(error.message);
    }
}

function renderDashboard(user) {
    UI.connectionStatus.classList.replace('bg-red-500', 'bg-green-500');
    UI.connectionStatus.classList.replace('shadow-[0_0_8px_rgba(239,68,68,0.5)]', 'shadow-[0_0_8px_rgba(34,197,94,0.5)]');
    UI.loadingScreen.classList.add('hidden');
    UI.bottomNav.classList.remove('hidden');

    // استخدام textContent لاحقاً للبيانات الحساسة لمنع ثغرات XSS
    const userName = user.first_name || 'مستخدم النظام';

    UI.contentArea.innerHTML = `
        <div class="w-full bg-white p-6 rounded-2xl shadow-sm border border-gray-100 text-center animate-fade-in">
            <div class="w-20 h-20 bg-brand-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-3xl text-brand-500">🛡️</span>
            </div>
            <h2 class="text-xl font-extrabold text-brand-900 mb-2">مرحباً بك، ${userName}</h2>
            <div class="inline-block bg-green-100 text-green-800 text-xs px-3 py-1 rounded-full font-bold mb-4">
                متصل وموثق سيادياً
            </div>
            <p class="text-sm text-gray-600 font-medium leading-relaxed">
                قنوات الاتصال اللوجستية جاهزة للعمل. أنت الآن متصل بشكل آمن ومباشر بنواة AymnGuard.
            </p>
        </div>
        <button onclick="Haptic.tap()" class="mt-6 w-full bg-brand-900 text-white font-bold py-4 rounded-xl shadow-lg active:scale-95 transition-all">
            فحص استجابة النظام
        </button>
    `;
}

function renderError(message) {
    UI.loadingScreen.innerHTML = `
        <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span class="text-3xl">⚠️</span>
        </div>
        <p class="text-sm font-bold text-red-600 text-center mb-6">${message}</p>
        <button onclick="tg.close()" class="w-full bg-brand-900 text-white font-bold py-3 rounded-xl shadow-lg active:scale-95 transition-all">
            إغلاق التطبيق
        </button>
    `;
}

// بدء دورة حياة التطبيق
authenticateUser();
