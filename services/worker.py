import time
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.queue_manager import MessageQueueManager

def start_worker():
    print("[*] AymnGuard Background Worker Started & Listening to Redis Queue...")
    while True:
        try:
            update_data = MessageQueueManager.pop_from_queue("telegram_updates_queue")
            
            if update_data:
                update_id = update_data.get("update_id", "N/A")
                print(f"[+] Worker Processing Update ID: {update_id}")
            else:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"[-] Worker Loop Exception -> {e}")
            time.sleep(1)

if __name__ == "__main__":
    start_worker()
