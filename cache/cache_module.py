from cachetools import LRUCache

class PkdexCache:
    def __init__(self, max_size=100):
        self._cache_instance = LRUCache(maxsize=max_size)    

    def get(self, key):
        return self._cache_instance.get(key, None)
    
    
    def set(self, key, value):
        self._cache_instance    [key] = value

