import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class MessageQueueManager:
    @staticmethod
    def push_to_queue(queue_name: str, data: dict) -> bool:
        try:
            redis_client.rpush(queue_name, json.dumps(data))
            return True
        except Exception as e:
            print(f"[CRITICAL] Redis Queue Push Error -> {e}")
            return False

    @staticmethod
    def pop_from_queue(queue_name: str) -> dict | None:
        try:
            item = redis_client.lpop(queue_name)
            return json.loads(item) if item else None
        except Exception as e:
            print(f"[CRITICAL] Redis Queue Pop Error -> {e}")
            return None
