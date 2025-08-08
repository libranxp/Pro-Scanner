# utils/cache.py
_cache = {}

def get_from_cache(key):
    return _cache.get(key)

def set_in_cache(key, value):
    _cache[key] = value
