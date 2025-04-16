import json
from src.config.database import redis_client

def cache_order(order_id, order_data):
    redis_client.set(f"order:{order_id}", json.dumps(order_data), ex=3600)

def get_cached_order(order_id):
    cached_data = redis_client.get(f"order:{order_id}")
    return json.loads(cached_data) if cached_data else None
