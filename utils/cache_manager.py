from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Optional, Tuple

from config import settings
from models import SearchResults
from utils.logging_config import LoggingConfig

logger = LoggingConfig.get_logger(__name__)


class CacheManager:
    """Manages in-memory LRU caching with expiration and size limits"""

    def __init__(self):
        self._cache: OrderedDict[str, Tuple[SearchResults, datetime]] = OrderedDict()

    def _get_cache_key(self, query: str, country: str) -> str:
        return f"{query.lower().strip()}:{country.lower().strip()}"

    def _is_cache_valid(self, timestamp: datetime) -> bool:
        return datetime.now() - timestamp < timedelta(days=settings.cache_expiry_days)

    def _cleanup_expired_entries(self):
        expired_keys = []

        for key, (_, timestamp) in self._cache.items():
            if not self._is_cache_valid(timestamp):
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]
            logger.info(f"Removed expired cache entry: {key}")

    def _enforce_size_limit(self):
        while len(self._cache) >= settings.max_cache_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.info(f"Cache size limit reached, removed oldest entry: {oldest_key}")

    def _move_to_end(self, key: str):
        self._cache.move_to_end(key)

    def get(self, query: str, country: str) -> Optional[SearchResults]:
        cache_key = self._get_cache_key(query, country)

        if cache_key in self._cache:
            filtered_results, timestamp = self._cache[cache_key]
            if self._is_cache_valid(timestamp):
                logger.info(f"Cache hit for key: {cache_key}")
                # Move to end to mark as most recently used
                self._move_to_end(cache_key)
                return filtered_results
            else:
                # Remove expired entry
                del self._cache[cache_key]
                logger.info(f"Cache expired for key: {cache_key}")

        logger.info(f"Cache miss for key: {cache_key}")
        return None

    def set(self, query: str, country: str, filtered_results: SearchResults):
        cache_key = self._get_cache_key(query, country)

        self._cleanup_expired_entries()

        # If key already exists, update it and move to end
        if cache_key in self._cache:
            self._cache[cache_key] = (filtered_results, datetime.now())
            self._move_to_end(cache_key)
            logger.info(f"Updated existing cache entry: {cache_key}")
        else:
            # Add new entry
            self._cache[cache_key] = (filtered_results, datetime.now())
            logger.info(f"Cached new filtered results for key: {cache_key}")

        # Enforce size limit after adding
        self._enforce_size_limit()


cache_manager = CacheManager()
