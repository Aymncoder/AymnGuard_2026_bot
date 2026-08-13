/**
 * ==============================================================================
 * AymnGuard Enterprise - Reactive State Management Engine
 * Enterprise-grade state synchronization and local caching module.
 * ==============================================================================
 */

class StateManager {
    constructor() {
        this._state = {
            user: this._safeStorageGet('aymnguard_user_cache'),
            token: localStorage.getItem('aymnguard_access_token') || null,
            systemStatus: 'connecting',
            activeTab: 'dashboard',
            metrics: { latency: '4.2ms', requestsCount: 1420 }
        };
        this._listeners = new Set();
    }

    _safeStorageGet(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.warn(`Failed to parse storage item for key ${key}:`, error);
            return null;
        }
    }

    _safeStorageSet(key, value) {
        try {
            if (value === null || value === undefined) {
                localStorage.removeItem(key);
            } else {
                localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value));
            }
        } catch (error) {
            console.warn(`Failed to save item to storage for key ${key}:`, error);
        }
    }

    get(key) {
        return this._state[key];
    }

    set(key, value) {
        this._state[key] = value;

        if (key === 'user') {
            this._safeStorageSet('aymnguard_user_cache', value);
        }
        if (key === 'token') {
            this._safeStorageSet('aymnguard_access_token', value);
        }

        this._notifyListeners(key, value);
    }

    subscribe(listener) {
        this._listeners.add(listener);
        return () => this._listeners.delete(listener);
    }

    _notifyListeners(key, value) {
        this._listeners.forEach(listener => {
            try {
                listener(key, value);
            } catch (error) {
                console.error("Error in state listener execution:", error);
            }
        });
    }

    clear() {
        this._state.user = null;
        this._state.token = null;
        this._safeStorageSet('aymnguard_user_cache', null);
        this._safeStorageSet('aymnguard_access_token', null);
        this._notifyListeners('clear', null);
    }
}

export const GlobalState = new StateManager();
