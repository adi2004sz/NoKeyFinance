"""HTTP caching helpers (optional)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from ..config import CACHE_DIR, CACHE_ENABLED, CACHE_TTL_SECONDS
from .logger import get_logger

_log = get_logger(__name__)

_INSTALLED: bool = False


def install_http_cache(
    cache_dir: Optional[Path] = None,
    enabled: Optional[bool] = None,
    ttl_seconds: Optional[int] = None,
) -> None:
    """
    Enable a local HTTP cache using requests-cache.

    This speeds up repeated lookups and reduces upstream requests. If requests-cache
    is not installed, this is a no-op.

    Can be disabled by setting env var NOKEYFINANCE_CACHE=0.
    """
    global _INSTALLED
    if _INSTALLED:
        return

    env = os.getenv("NOKEYFINANCE_CACHE")
    if env is not None and env.strip() in {"0", "false", "False", "no", "NO"}:
        _log.info("HTTP cache disabled via NOKEYFINANCE_CACHE=%s", env)
        _INSTALLED = True
        return

    enabled = CACHE_ENABLED if enabled is None else enabled
    if not enabled:
        _INSTALLED = True
        return

    ttl_seconds = CACHE_TTL_SECONDS if ttl_seconds is None else ttl_seconds
    cache_dir = CACHE_DIR if cache_dir is None else cache_dir
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "http_cache"

    try:
        import requests_cache
    except Exception:
        _log.info("requests-cache not installed; skipping HTTP cache")
        _INSTALLED = True
        return

    # Cache GETs in a local SQLite DB
    requests_cache.install_cache(
        cache_name=str(cache_path),
        backend="sqlite",
        expire_after=ttl_seconds,
        allowable_methods=("GET",),
        stale_if_error=True,
    )
    _log.info("HTTP cache enabled (ttl=%ss, path=%s)", ttl_seconds, cache_path)
    _INSTALLED = True
