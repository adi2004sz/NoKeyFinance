"""Stooq data via pandas_datareader. No API key required."""

from datetime import datetime
from typing import Any

import pandas as pd

from ..utils.exceptions import DataSourceError
from ..utils.logger import get_logger
from .base import BaseDataSource

_log = get_logger(__name__)


def _get_stooq_reader():
    """Lazy import to avoid loading pandas_datareader.data (has compat issues on Python 3.13)."""
    from pandas_datareader.stooq import StooqDailyReader
    return StooqDailyReader


class StooqSource(BaseDataSource):
    """Fetches OHLCV from Stooq using pandas_datareader StooqDailyReader."""

    @property
    def name(self) -> str:
        return "stooq"

    def fetch(
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Download historical data for ticker from Stooq. Raises DataSourceError
        on failure or empty result. Stooq may require suffixes (e.g. .US for US stocks).
        """
        if not ticker or not ticker.strip():
            raise DataSourceError("Ticker cannot be empty.")
        ticker = ticker.strip().upper()
        try:
            StooqDailyReader = _get_stooq_reader()
            reader = StooqDailyReader(symbols=ticker, start=start, end=end)
            df = reader.read()
        except Exception as e:
            _log.exception("Stooq failed for %s", ticker)
            raise DataSourceError(f"Stooq fetch failed for {ticker}: {e}") from e
        if df is None or df.empty:
            raise DataSourceError(f"No data returned from Stooq for {ticker}.")
        return self._normalize(df)
