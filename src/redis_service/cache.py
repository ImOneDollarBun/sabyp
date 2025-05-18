from . import r


def add_cache_note(key, value, ttl_sec: int = None):
    r.set(key, value, ex=ttl_sec)


def get_cache_note(key):
    return r.get(key)


def delete_cache_note(keys):
    r.delete(keys)
