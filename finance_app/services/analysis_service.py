"""Helpers for fetching data and computing indicators."""

from typing import Optional, Sequence

import pandas as pd

from ..models.indicators import add_indicators
from ..models.stock import StockData
from ..utils.logger import get_logger
from .data_service import get_ohlcv

_log = get_logger(__name__)


def get_ohlcv_with_indicators(
    ticker: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    source: str = "yahoo",
    sma_periods: Optional[Sequence[int]] = None,
    ema_periods: Optional[Sequence[int]] = None,
    rsi_period: int = 14,
    volatility_window: int = 20,
) -> tuple[StockData, pd.DataFrame]:
    """
    Fetch OHLCV for the ticker and add technical indicators.

    Returns (StockData with raw OHLCV, DataFrame with OHLCV + indicator columns).
    Uses get_ohlcv for fetch; add_indicators for sma, ema, rsi, returns, volatility.
    """
    stock = get_ohlcv(ticker, start=start, end=end, source=source)
    if stock.empty:
        return stock, stock.df.copy()
    enriched = add_indicators(
        stock.df,
        sma_periods=sma_periods,
        ema_periods=ema_periods,
        rsi_period=rsi_period,
        volatility_window=volatility_window,
    )
    return stock, enriched


def add_indicators_to_stock(
    stock: StockData,
    sma_periods: Optional[Sequence[int]] = None,
    ema_periods: Optional[Sequence[int]] = None,
    rsi_period: int = 14,
    volatility_window: int = 20,
) -> pd.DataFrame:
    """
    Add indicator columns to a copy of the stock's DataFrame.

    Returns the enriched DataFrame.
    """
    if stock.empty:
        return stock.df.copy()
    return add_indicators(
        stock.df,
        sma_periods=sma_periods,
        ema_periods=ema_periods,
        rsi_period=rsi_period,
        volatility_window=volatility_window,
    )
