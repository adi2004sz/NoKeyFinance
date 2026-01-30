"""Application configuration. No secrets, no API keys."""

from pathlib import Path

# Project root (parent of finance_app)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# Default date range when none given (days back from today)
DEFAULT_LOOKBACK_DAYS: int = 365

# Cache (optional, for later use)
CACHE_DIR: Path = PROJECT_ROOT / ".cache"
CACHE_ENABLED: bool = False

# Logging
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# Data source names
SOURCE_YAHOO: str = "yahoo"
SOURCE_STOOQ: str = "stooq"
