"""Orchestrates fetching OHLCV data from configured sources."""

from datetime import datetime, timedelta
from typing import Optional

from ..config import DEFAULT_LOOKBACK_DAYS, SOURCE_STOOQ, SOURCE_YAHOO
from ..data_sources import StooqSource, YahooSource
from ..models.stock import StockData
from ..utils.exceptions import DataSourceError, ValidationError
from ..utils.logger import get_logger
from ..utils import validate_date_range, validate_ticker
from ..utils.validators import MAX_DATE_RANGE_DAYS

_log = get_logger(__name__)

_SOURCES = {
    SOURCE_YAHOO: YahooSource(),
    SOURCE_STOOQ: StooqSource(),
}


def get_ohlcv(
    ticker: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    source: str = SOURCE_YAHOO,
) -> StockData:
    """
    Fetch OHLCV for one ticker and return a StockData instance.

    Dates (YYYY-MM-DD): if both omitted, uses last DEFAULT_LOOKBACK_DAYS; if only
    start given, from start to today; if only end given, from (end - lookback) to end.
    source must be 'yahoo' or 'stooq'. Raises ValidationError or DataSourceError on failure.
    """
    ticker_clean = validate_ticker(ticker)
    now = datetime.now()
    if start is not None and end is not None:
        start_dt, end_dt = validate_date_range(
            start, end, max_days=MAX_DATE_RANGE_DAYS
        )
    elif start is not None:
        start_dt, _ = validate_date_range(
            start, now.strftime("%Y-%m-%d"), max_days=MAX_DATE_RANGE_DAYS
        )
        end_dt = now
    elif end is not None:
        if not isinstance(end, str):
            raise ValidationError("End date must be a string (YYYY-MM-DD).")
        try:
            end_dt = datetime.strptime(end.strip(), "%Y-%m-%d")
        except ValueError as e:
            raise ValidationError("Dates must be in YYYY-MM-DD format.") from e
        start_dt = end_dt - timedelta(days=DEFAULT_LOOKBACK_DAYS)
    else:
        end_dt = now
        start_dt = end_dt - timedelta(days=DEFAULT_LOOKBACK_DAYS)
    source_normalized = (
        (source or "").strip().lower() if isinstance(source, str) else ""
    )
    if source_normalized not in _SOURCES:
        raise ValidationError(
            f"Unknown source: {source!r}. Use {SOURCE_YAHOO} or {SOURCE_STOOQ}."
        )
    adapter = _SOURCES[source_normalized]
    _log.info(
        "Fetching %s from %s for %s to %s",
        ticker_clean,
        source_normalized,
        start_dt.date(),
        end_dt.date(),
    )
    df = adapter.fetch(ticker_clean, start_dt, end_dt)
    return StockData(ticker=ticker_clean, source=source_normalized, df=df)
