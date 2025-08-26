import time
from collections import deque

# Very small in-memory store. For production move to Redis with TTL.
USER_MEMORY = {}  # user_key -> {"history": deque([...]), "last_order": order_id, "updated": ts}

def add_user_message(user_key: str, message: str):
    rec = USER_MEMORY.setdefault(user_key, {"history": deque(maxlen=20), "last_order": None, "updated": time.time()})
    rec["history"].append({"role": "user", "text": message})
    rec["updated"] = time.time()

def add_bot_message(user_key: str, message: str):
    rec = USER_MEMORY.setdefault(user_key, {"history": deque(maxlen=20), "last_order": None, "updated": time.time()})
    rec["history"].append({"role": "bot", "text": message})
    rec["updated"] = time.time()

def set_last_order(user_key: str, order_id: int):
    rec = USER_MEMORY.setdefault(user_key, {"history": deque(maxlen=20), "last_order": None, "updated": time.time()})
    rec["last_order"] = order_id
    rec["updated"] = time.time()

def get_memory_snippet(user_key: str, lines: int = 6) -> str:
    rec = USER_MEMORY.get(user_key)
    if not rec:
        return ""
    # join last N messages (simple)
    items = list(rec["history"])[-lines:]
    return "\n".join([f"{m['role']}: {m['text']}" for m in items])
