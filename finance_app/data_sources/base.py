"""Base contract for data source adapters."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import pandas as pd


# Normalized OHLCV column names used across all sources
OHLCV_COLUMNS = ("open", "high", "low", "close", "volume")


class BaseDataSource(ABC):
    """Abstract base for fetching OHLCV data. All sources must return the same shape."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Source identifier (e.g. 'yahoo', 'stooq')."""
        pass

    @abstractmethod
    def fetch(
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV for the given ticker and date range.

        Returns a DataFrame with DatetimeIndex and columns: open, high, low, close, volume.
        Missing or invalid data should raise DataSourceError.
        """
        pass

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure index is timezone-naive DatetimeIndex and columns are lowercase.
        Drops rows with all NaN and fills missing volume with 0.
        """
        if df is None or df.empty:
            return pd.DataFrame(columns=list(OHLCV_COLUMNS))
        out = df.copy()
        if isinstance(out.columns, pd.MultiIndex):
            out.columns = out.columns.get_level_values(0)
        out.index = pd.to_datetime(out.index)
        if out.index.tz is not None:
            out.index = out.index.tz_convert("UTC").tz_localize(None)
        out.index.name = "date"
        out.columns = [str(c).lower().strip() for c in out.columns]
        # Prefer close over adj close; drop other non-OHLCV columns
        if "adj close" in out.columns and "close" not in out.columns:
            out = out.rename(columns={"adj close": "close"})
        for col in list(out.columns):
            if col not in OHLCV_COLUMNS:
                out = out.drop(columns=[col], errors="ignore")
        for c in OHLCV_COLUMNS:
            if c not in out.columns:
                out[c] = float("nan")
        out = out[list(OHLCV_COLUMNS)]
        out = out.dropna(how="all", subset=["open", "high", "low", "close"])
        vol = out["volume"].fillna(0)
        vol = vol.clip(lower=0)  # disallow negative volume from bad data
        out["volume"] = vol.astype("int64")
        return out.sort_index()
