"""
Cache utility module.
This module provides caching functions for the application.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# In-memory cache storage
# Structure: {cache_key: {"data": any_data, "expires_at": datetime}}
_cache: Dict[str, Dict[str, Any]] = {}

def set_cache(key: str, data: Any, ttl_minutes: int = 5) -> None:
    """
    Set a value in the cache with a TTL.
    
    Args:
        key (str): The cache key.
        data (Any): The data to cache.
        ttl_minutes (int): Time to live in minutes.
    """
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    _cache[key] = {
        "data": data,
        "expires_at": expires_at
    }

def get_cache(key: str) -> Optional[Any]:
    """
    Get a value from the cache.
    
    Args:
        key (str): The cache key.
        
    Returns:
        Optional[Any]: The cached data if found and not expired, None otherwise.
    """
    cache_item = _cache.get(key)
    
    if not cache_item:
        return None
    
    if datetime.utcnow() > cache_item["expires_at"]:
        # Cache expired, remove it and return None
        del _cache[key]
        return None
    
    return cache_item["data"]

def clear_cache(key: str) -> None:
    """
    Remove a value from the cache.
    
    Args:
        key (str): The cache key.
    """
    if key in _cache:
        del _cache[key]

def clear_all_cache() -> None:
    """
    Clear all cached data.
    """
    _cache.clear()

def generate_post_cache_key(user_id: int) -> str:
    """
    Generate a cache key for posts.
    
    Args:
        user_id (int): The user ID.
        
    Returns:
        str: The cache key.
    """
    return f"user_posts_{user_id}" 