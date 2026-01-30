"""Matplotlib chart builders for price, volume, and indicators."""

from typing import List, Optional, Sequence, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def _ensure_index(df: pd.DataFrame) -> pd.DatetimeIndex:
    """Use index as x-axis; must be DatetimeIndex."""
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame index must be DatetimeIndex")
    return df.index


def plot_price_with_indicators(
    df: pd.DataFrame,
    ticker: str,
    sma_cols: Optional[Sequence[str]] = None,
    ema_cols: Optional[Sequence[str]] = None,
    figsize: Tuple[float, float] = (10, 5),
) -> plt.Figure:
    """
    Plot close price with optional SMA/EMA overlay. Returns a matplotlib Figure.
    """
    if df is None or df.empty or "close" not in df.columns:
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(f"{ticker} (no data)")
        return fig
    idx = _ensure_index(df)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(idx, df["close"].values, label="Close", color="black", linewidth=1)
    # None = auto-detect; explicit empty sequence = no overlay
    if sma_cols is None:
        sma_cols = [c for c in df.columns if c.startswith("sma_")]
    if ema_cols is None:
        ema_cols = [c for c in df.columns if c.startswith("ema_")]
    for col in sma_cols:
        if col in df.columns:
            ax.plot(idx, df[col].values, label=col, alpha=0.8)
    for col in ema_cols:
        if col in df.columns:
            ax.plot(idx, df[col].values, label=col, alpha=0.8)
    ax.set_title(f"{ticker} - Price")
    ax.set_ylabel("Price")
    ax.legend(loc="best", fontsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


def plot_volume(
    df: pd.DataFrame,
    ticker: str,
    figsize: Tuple[float, float] = (10, 2.5),
) -> plt.Figure:
    """Plot volume bars. Returns a matplotlib Figure."""
    if df is None or df.empty or "volume" not in df.columns:
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(f"{ticker} Volume (no data)")
        return fig
    idx = _ensure_index(df)
    fig, ax = plt.subplots(figsize=figsize)
    close_vals = df["close"].values
    open_vals = df["open"].values
    colors = []
    for i in range(len(df)):
        c, o = close_vals[i], open_vals[i]
        if pd.isna(c) or pd.isna(o):
            colors.append("#9e9e9e")  # neutral for missing
        elif c >= o:
            colors.append("#26a69a")
        else:
            colors.append("#ef5350")
    ax.bar(idx, df["volume"].values, color=colors, alpha=0.7, width=0.8)
    ax.set_title(f"{ticker} - Volume")
    ax.set_ylabel("Volume")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


def plot_rsi(
    df: pd.DataFrame,
    ticker: str,
    figsize: Tuple[float, float] = (10, 2),
) -> Optional[plt.Figure]:
    """Plot RSI (0-100) with 30/70 lines. Returns None if no rsi column."""
    if df is None or df.empty or "rsi" not in df.columns:
        return None
    idx = _ensure_index(df)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(idx, df["rsi"].values, label="RSI", color="purple", linewidth=1)
    ax.axhline(y=70, color="gray", linestyle="--", alpha=0.7)
    ax.axhline(y=30, color="gray", linestyle="--", alpha=0.7)
    ax.set_ylim(0, 100)
    ax.set_title(f"{ticker} - RSI")
    ax.set_ylabel("RSI")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


def plot_comparison(
    series_list: List[Tuple[str, pd.Series]],
    title: str = "Comparison",
    figsize: Tuple[float, float] = (10, 5),
) -> plt.Figure:
    """
    Plot multiple series (e.g. close of different tickers) on one chart.
    series_list: [(label, series), ...]; series must have DatetimeIndex.
    """
    fig, ax = plt.subplots(figsize=figsize)
    for label, ser in series_list:
        if ser is not None and not ser.empty and isinstance(ser.index, pd.DatetimeIndex):
            ax.plot(ser.index, ser.values, label=label, alpha=0.8)
    ax.set_title(title)
    ax.set_ylabel("Price")
    ax.legend(loc="best", fontsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig
