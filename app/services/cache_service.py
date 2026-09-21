from typing import Any, Optional, Dict, List
import json
import pickle
from datetime import datetime, timedelta
import hashlib
import redis
from app.core.config import settings
from functools import wraps

class CacheService:
    """Advanced caching service with Redis and fallback in-memory cache"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection if available"""
        try:
            if settings.CACHE_ENABLED:
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=False,
                    socket_connect_timeout=2
                )
                self.redis_client.ping()
                print("✅ Redis cache connected")
        except Exception as e:
            print(f"⚠️ Redis not available, using in-memory cache: {e}")
            self.redis_client = None
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        # Try Redis first
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    return pickle.loads(value)
            except:
                pass
        
        # Fallback to memory cache
        cache_entry = self.memory_cache.get(key)
        if cache_entry:
            if cache_entry['expires_at'] > datetime.now():
                return cache_entry['value']
            else:
                del self.memory_cache[key]
        
        return None
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: int = None
    ) -> bool:
        """Set value in cache with TTL"""
        if ttl is None:
            ttl = settings.CACHE_TTL
        
        try:
            # Try Redis
            if self.redis_client:
                serialized = pickle.dumps(value)
                self.redis_client.setex(key, ttl, serialized)
                return True
        except:
            pass
        
        # Fallback to memory cache
        self.memory_cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
        
        # Clean old entries if memory cache is too large
        if len(self.memory_cache) > 1000:
            self._clean_memory_cache()
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if self.redis_client:
                self.redis_client.delete(key)
        except:
            pass
        
        self.memory_cache.pop(key, None)
        return True
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        count = 0
        
        # Clear Redis
        if self.redis_client:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    count += self.redis_client.delete(*keys)
            except:
                pass
        
        # Clear memory cache
        keys_to_delete = [
            k for k in self.memory_cache.keys() 
            if pattern.replace('*', '') in k
        ]
        for k in keys_to_delete:
            del self.memory_cache[k]
            count += 1
        
        return count
    
    def _clean_memory_cache(self):
        """Remove expired entries from memory cache"""
        now = datetime.now()
        expired_keys = [
            k for k, v in self.memory_cache.items()
            if v['expires_at'] <= now
        ]
        for k in expired_keys:
            del self.memory_cache[k]
    
    def cache_decorator(self, prefix: str, ttl: int = None):
        """Decorator for caching function results"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                cache_key = self._generate_key(prefix, args, kwargs)
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Call function and cache result
                result = await func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                cache_key = self._generate_key(prefix, args, kwargs)
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Call function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper
        
        return decorator
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        stats = {
            "type": "redis" if self.redis_client else "memory",
            "memory_cache_size": len(self.memory_cache),
            "redis_connected": self.redis_client is not None
        }
        
        if self.redis_client:
            try:
                info = self.redis_client.info()
                stats.update({
                    "redis_used_memory": info.get("used_memory_human"),
                    "redis_connected_clients": info.get("connected_clients"),
                    "redis_keys": info.get("db0", {}).get("keys", 0)
                })
            except:
                pass
        
        return stats

# Create global cache instance
cache_service = CacheService()
