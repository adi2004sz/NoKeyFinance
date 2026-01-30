"""Yahoo Finance data via yfinance. No API key required."""

from datetime import datetime
from typing import Any

import pandas as pd
import yfinance as yf

from ..utils.exceptions import DataSourceError
from ..utils.logger import get_logger
from .base import BaseDataSource, OHLCV_COLUMNS

_log = get_logger(__name__)


class YahooSource(BaseDataSource):
    """Fetches OHLCV from Yahoo Finance using yfinance."""

    @property
    def name(self) -> str:
        return "yahoo"

    def fetch(
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Download historical data for ticker from Yahoo. Raises DataSourceError
        on invalid ticker or empty result.
        """
        if not ticker or not ticker.strip():
            raise DataSourceError("Ticker cannot be empty.")
        ticker = ticker.strip().upper()
        try:
            obj = yf.Ticker(ticker)
            df = obj.history(start=start, end=end, auto_adjust=False)
        except Exception as e:
            _log.exception("yfinance failed for %s", ticker)
            raise DataSourceError(f"Yahoo fetch failed for {ticker}: {e}") from e
        if df is None or df.empty:
            raise DataSourceError(f"No data returned from Yahoo for {ticker}.")
        return self._normalize(df)
