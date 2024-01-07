from cachetools import LRUCache


class Mycache:
    def __init__ (self, max_size = 100):
        self.cache = LRUCache(maxsize = max_size)

    def get(self, key):
        return self.cache.get(key, None)
    
    def set(self, key, value):
        self.cache[key] = value

cache = Mycache(max_size=3)

cache.set("key1", "value1")
cache.set("key2", "value2")
cache.set("key3", "value3")

print(cache.get("key1"))
print(cache.get("key2"))
print(cache.get("key3"))

cache.set("key4", "value4")

print(cache.get("key1"))
        
    
