"""Central logging setup."""

import logging
import sys
from typing import Optional

from ..config import LOG_FORMAT, LOG_LEVEL


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Return a configured logger. Uses app LOG_LEVEL unless overridden.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    logger.setLevel(level or LOG_LEVEL)
    return logger
