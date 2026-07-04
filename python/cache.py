from collections import OrderedDict
from dataclasses import dataclass
from time import time
from typing import Any

@dataclass
class CacheEntry:
    value: Any
    expires_at: float |  None = None

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time() > self.expires_at

class LRUCache:
    def __init__(self, max_size : int = 100):
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self.max_size = max_size
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()

    def get(self, key: str) -> Any | None:
        
        entry = self._store.get(key) # type: ignore 
        if entry is None:
            return None
        
        if entry.is_expired(): 
            del self._store[key]
            return None
        
        # mark as recently used
        self._store.move_to_end(key)
        
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:

        expires_at = None

        if ttl_seconds is not None: # we se the time at which the entry will expire 
            expires_at = time() + ttl_seconds

        self._store[key] = CacheEntry(value = value, expires_at = expires_at)

        # Mark as recently used
        self._store.move_to_end(key)


        # evict least recently used item if too large

        if len(self._store) > self.max_size:
            self._store.popitem(last = False)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        self._remove_expired()
        return len(self._store)

    def _remove_expired(self) -> None:
        expired_keys = [
            key for key, entry in self._store.items() if entry.is_expired()
        ]

        for key in expired_keys:
            del self._store[key]

            
