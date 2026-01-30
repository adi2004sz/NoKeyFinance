"""Technical indicators computed on OHLCV DataFrames."""

from typing import Optional, Sequence

import numpy as np
import pandas as pd

from finance_app.utils.exceptions import IndicatorError
from finance_app.utils.logger import get_logger

_log = get_logger(__name__)


def _require_close(df: pd.DataFrame) -> pd.Series:
    """Return close series or raise IndicatorError."""
    if df is None or df.empty:
        raise IndicatorError("DataFrame is empty or None")
    if "close" not in df.columns:
        raise IndicatorError("DataFrame must have a 'close' column")
    return df["close"].astype(float)


def sma(close: pd.Series, period: int) -> pd.Series:
    """Simple moving average of close. Returns Series aligned with close."""
    if period < 1:
        raise IndicatorError("period must be >= 1")
    return close.rolling(window=period, min_periods=1).mean()


def ema(close: pd.Series, period: int) -> pd.Series:
    """Exponential moving average of close. Returns Series aligned with close."""
    if period < 1:
        raise IndicatorError("period must be >= 1")
    return close.ewm(span=period, adjust=False, min_periods=1).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """
    Relative Strength Index. Uses Wilder smoothing (EMA of gain/loss).
    Returns Series in [0, 100] aligned with close.
    """
    if period < 1:
        raise IndicatorError("period must be >= 1")
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False, min_periods=1).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False, min_periods=1).mean()
    rs = np.where(avg_loss == 0, np.where(avg_gain == 0, 1.0, np.inf), avg_gain / avg_loss)
    raw = 100 - (100 / (1 + rs))
    return pd.Series(np.clip(raw, 0.0, 100.0), index=close.index)


def daily_returns(close: pd.Series) -> pd.Series:
    """Day-over-day percentage return. First value is NaN."""
    return close.pct_change()


def volatility(
    close: pd.Series,
    window: int = 20,
    annualize: bool = True,
) -> pd.Series:
    """
    Rolling standard deviation of daily returns. If annualize=True, multiply by sqrt(252).
    """
    if window < 1:
        raise IndicatorError("window must be >= 1")
    ret = close.pct_change()
    vol = ret.rolling(window=window, min_periods=1).std()
    if annualize:
        vol = vol * np.sqrt(252)
    return vol


def add_indicators(
    df: pd.DataFrame,
    sma_periods: Optional[Sequence[int]] = None,
    ema_periods: Optional[Sequence[int]] = None,
    rsi_period: int = 14,
    volatility_window: int = 20,
) -> pd.DataFrame:
    """
    Add indicator columns to a copy of df. Expects columns: open, high, low, close, volume.
    New columns: sma_<n>, ema_<n>, rsi, returns, volatility.
    """
    if df is None or df.empty:
        raise IndicatorError("DataFrame is empty or None")
    out = df.copy()
    c = _require_close(out)
    if sma_periods is None:
        sma_periods = (20, 50)
    if ema_periods is None:
        ema_periods = (12, 26)
    for n in sma_periods:
        out[f"sma_{n}"] = sma(c, n)
    for n in ema_periods:
        out[f"ema_{n}"] = ema(c, n)
    out["rsi"] = rsi(c, rsi_period)
    out["returns"] = daily_returns(c)
    out["volatility"] = volatility(c, window=volatility_window)
    return out
