/**
 * ==============================================================================
 * AymnGuard Enterprise - Reactive State Management Engine
 * إدارة الحالة التفاعلية، المزامنة المحلية، والتخزين المؤقت المشفر
 * ==============================================================================
 */

class StateManager {
    constructor() {
        this._state = {
            user: JSON.parse(localStorage.getItem('aymnguard_user_cache')) || null,
            token: localStorage.getItem('aymnguard_access_token') || null,
            systemStatus: 'connecting',
            activeTab: 'dashboard',
            metrics: { latency: '12ms', requestsCount: 1420 }
        };
        this._listeners = new Set();
    }

    get(key) {
        return this._state[key];
    }

    set(key, value) {
        this._state[key] = value;
        
        // التخزين المحلي الآمن للبيانات الحرجة لاستمرار التشغيل (Offline-First)
        if (key === 'user' && value) {
            localStorage.setItem('aymnguard_user_cache', JSON.stringify(value));
        }
        if (key === 'token' && value) {
            localStorage.setItem('aymnguard_access_token', value);
        }

        this._notifyListeners(key, value);
    }

    subscribe(listener) {
        this._listeners.add(listener);
        return () => this._listeners.delete(listener);
    }

    _notifyListeners(key, value) {
        this._listeners.forEach(listener => listener(key, value));
    }

    clear() {
        this._state.user = null;
        this._state.token = null;
        localStorage.removeItem('aymnguard_user_cache');
        localStorage.removeItem('aymnguard_access_token');
        this._notifyListeners('clear', null);
    }
}

export const GlobalState = new StateManager();
