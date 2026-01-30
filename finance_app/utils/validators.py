"""Input validation helpers."""

import re
from datetime import datetime
from typing import Optional, Tuple

from .exceptions import ValidationError

# Limits to prevent abuse / resource exhaustion
MAX_TICKER_LENGTH: int = 20
MAX_DATE_RANGE_DAYS: int = 365 * 20  # 20 years


def validate_ticker(ticker: str) -> str:
    """
    Basic ticker validation: non-empty, alphanumeric plus common symbols, max length.
    Raises ValidationError if invalid.
    """
    if not ticker or not isinstance(ticker, str):
        raise ValidationError("Ticker must be a non-empty string.")
    cleaned = ticker.strip().upper()
    if not cleaned:
        raise ValidationError("Ticker cannot be blank.")
    if len(cleaned) > MAX_TICKER_LENGTH:
        raise ValidationError(f"Ticker must be at most {MAX_TICKER_LENGTH} characters.")
    if not re.match(r"^[A-Z0-9.\-]+$", cleaned):
        raise ValidationError(
            "Ticker may only contain letters, numbers, dot, and hyphen."
        )
    return cleaned


def validate_date_range(
    start: Optional[str],
    end: Optional[str],
    max_days: Optional[int] = None,
) -> Tuple[datetime, datetime]:
    """
    Parse and validate start/end date strings. Returns (start_dt, end_dt).
    Raises ValidationError if invalid, start > end, or range exceeds max_days.
    """
    if not start or not end:
        raise ValidationError("Both start and end dates are required.")
    if not isinstance(start, str) or not isinstance(end, str):
        raise ValidationError("Start and end must be strings (YYYY-MM-DD).")
    try:
        start_dt = datetime.strptime(start.strip(), "%Y-%m-%d")
        end_dt = datetime.strptime(end.strip(), "%Y-%m-%d")
    except ValueError as e:
        raise ValidationError(
            "Dates must be in YYYY-MM-DD format."
        ) from e
    if start_dt > end_dt:
        raise ValidationError("Start date must be before or equal to end date.")
    if max_days is not None:
        if (end_dt - start_dt).days > max_days:
            raise ValidationError(
                f"Date range must not exceed {max_days} days."
            )
    return start_dt, end_dt
