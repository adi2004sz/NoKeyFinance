"""Stock data model: ticker, source, and OHLCV DataFrame."""

from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class StockData:
    """
    Holds normalized OHLCV data for one ticker from one source.
    df must have DatetimeIndex and columns: open, high, low, close, volume.
    """

    ticker: str
    source: str
    df: pd.DataFrame

    def __post_init__(self) -> None:
        if self.ticker is None or not str(self.ticker).strip():
            raise ValueError("ticker cannot be empty")
        if self.source is None or not str(self.source).strip():
            raise ValueError("source cannot be empty")
        if self.df is None:
            raise ValueError("df cannot be None")
        expected = {"open", "high", "low", "close", "volume"}
        if not expected.issubset(self.df.columns):
            missing = expected - set(self.df.columns)
            raise ValueError(f"df missing columns: {missing}")

    @property
    def empty(self) -> bool:
        """True if there are no rows."""
        return self.df.empty

    @property
    def date_range(self) -> Optional[tuple[pd.Timestamp, pd.Timestamp]]:
        """(first date, last date) from the index, or None if empty."""
        if self.df.empty:
            return None
        return self.df.index.min(), self.df.index.max()
