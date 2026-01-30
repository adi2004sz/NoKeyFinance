"""Input validation helpers."""

import re
from datetime import datetime
from typing import Optional, Tuple

from .exceptions import ValidationError


def validate_ticker(ticker: str) -> str:
    """
    Basic ticker validation: non-empty, alphanumeric plus common symbols.
    Raises ValidationError if invalid.
    """
    if not ticker or not isinstance(ticker, str):
        raise ValidationError("Ticker must be a non-empty string.")
    cleaned = ticker.strip().upper()
    if not cleaned:
        raise ValidationError("Ticker cannot be blank.")
    if not re.match(r"^[A-Z0-9.\-]+$", cleaned):
        raise ValidationError(
            "Ticker may only contain letters, numbers, dot, and hyphen."
        )
    return cleaned


def validate_date_range(
    start: Optional[str],
    end: Optional[str],
) -> Tuple[datetime, datetime]:
    """
    Parse and validate start/end date strings. Returns (start_dt, end_dt).
    Raises ValidationError if invalid or start > end.
    """
    if not start or not end:
        raise ValidationError("Both start and end dates are required.")
    try:
        start_dt = datetime.strptime(start.strip(), "%Y-%m-%d")
        end_dt = datetime.strptime(end.strip(), "%Y-%m-%d")
    except ValueError as e:
        raise ValidationError(
            "Dates must be in YYYY-MM-DD format."
        ) from e
    if start_dt > end_dt:
        raise ValidationError("Start date must be before or equal to end date.")
    return start_dt, end_dt
