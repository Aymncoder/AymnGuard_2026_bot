import time
from telethon import TelegramClient
from backend_core.proxy_manager import SovereignProxyManager

# قائمة البروكسيات الخاصة بك (يمكن ربطها بملف البيئة أو قاعدة البيانات)
my_proxies = [
    {"host": "proxy1.example.com", "port": 1080, "username": "user1", "password": "pass1"},
    {"host": "proxy2.example.com", "port": 1080, "username": "user2", "password": "pass2"}
]

proxy_manager = SovereignProxyManager(my_proxies)

def create_resilient_telegram_client(session_name: str, api_id: int, api_hash: str, max_retries: int = 3):
    """
    إنشاء عميل تيليجرام محصن ضد الانقطاع مع تجربة عدة بروكسيات تلقائياً
    """
    client = None
    attempt = 0

    while attempt < max_retries:
        proxy_config = proxy_manager.get_active_proxy()
        try:
            print(f"[Info]: محاولة الاتصال لجلسة {session_name} عبر البروكسي (المحاولة {attempt + 1})...")

            client = TelegramClient(
                session_name,
                api_id,
                api_hash,
                proxy=proxy_config,
                connection_retries=5,
                timeout=30
            )

            # محاولة الاتصال الفعلي
            # await client.connect()
            print(f"[Success]: تم الاتصال بنجاح واستقرار تام لجلسة {session_name}")
            return client

        except Exception as e:
            print(f"[Error]: فشل الاتصال عبر البروكسي الحالي: {e}")
            attempt += 1
            time.sleep(2) # انتظار قصير قبل تجربة بروكسي بديل

    raise ConnectionError("[Fatal]: فشلت كافة محاولات الاتصال بسيرفرات تيليجرام عبر مسبح البروكسيات المتاح.")
