/**
 * ==============================================================================
 * AymnGuard Enterprise - Sovereign Advanced API Gateway
 * Enterprise-grade API communication gateway for cloud production environments.
 * ==============================================================================
 */

import { GlobalState } from './state.js';

// استخدام الرابط السحابي المدفوع للإنتاج بدلاً من المسار النسبي المحلي لمنع انقطاع الاتصال
const CLOUD_API_BASE_URL = window.ENV_API_URL || "https://api.aymnguard.cloud/api/v1";

export const ApiGateway = {
    async request(endpoint, options = {}, retries = 2, timeoutMs = 25000) {
        const token = GlobalState.get('token');
        const tgInitData = window.Telegram?.WebApp?.initData || '';

        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(tgInitData ? { 'Authorization': `tma ${tgInitData}` } : {}),
            ...options.headers
        };

        const controller = new AbortController();
        // زيادة مهلة الاتصال إلى 25 ثانية لمنع أخطاء انتهاء المهلة (Timeout) مع السيرفرات السحابية
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
            const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
            const targetUrl = `${CLOUD_API_BASE_URL}${cleanEndpoint}`;

            const response = await fetch(targetUrl, {
                ...options,
                headers,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                if (response.status === 401 && retries > 0) {
                    console.warn("Session expired or unauthorized, attempting automatic retry.");
                    return await this.request(endpoint, options, retries - 1, timeoutMs);
                }
                
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Server error with status code: ${response.status}`);
            }

            return await response.json();

        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                console.error("API Gateway Error: Request timed out reaching the cloud server.");
                throw new Error("انتهت مهلة الاتصال بالخادم السحابي. يجدر التحقق من جودة الشبكة واستقرار الاتصال.");
            }
            
            console.error(`API Gateway Error on route [${endpoint}]:`, error.message);
            throw error;
        }
    }
};
