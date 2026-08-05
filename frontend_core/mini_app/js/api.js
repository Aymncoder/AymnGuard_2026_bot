/**
 * ==============================================================================
 * AymnGuard Enterprise - Sovereign Advanced API Gateway
 * بوابة الاتصال الذكية والمحصنة مع النواة المركزية
 * ==============================================================================
 */

import { GlobalState } from './state.js';

const API_BASE_URL = '/api/v1';

export const ApiGateway = {
    async request(endpoint, options = {}, retries = 2) {
        const token = GlobalState.get('token');
        const tgInitData = window.Telegram?.WebApp?.initData || '';

        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(tgInitData ? { 'Authorization': `tma ${tgInitData}` } : {}),
            ...options.headers
        };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // مهلة 10 ثوانٍ

            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                if (response.status === 401 && retries > 0) {
                    // محاولة تجديد الجلسة أو إعادة المصادقة تلقائياً
                    console.warn("⚠️ انتهاء صلاحية الجلسة، جاري إعادة المحاولة...");
                    return await this.request(endpoint, options, retries - 1);
                }
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `خطأ في الخادم برمز الاستجابة: ${response.status}`);
            }

            return await response.json();

        } catch (error) {
            if (error.name === 'AbortError') {
                console.error("❌ مهلة الاتصال انتهت (Timeout)");
                throw new Error("استجابة الخادم بطيئة جداً. يجدر التحقق من الاتصال.");
            }
            console.error(`❌ [API Gateway Error] على المسار ${endpoint}:`, error.message);
            throw error;
        }
    }
};
