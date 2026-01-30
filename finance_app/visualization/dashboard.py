"""Streamlit dashboard: ticker, date range, charts with optional indicators."""

from datetime import datetime, timedelta
from typing import Optional

import matplotlib.pyplot as plt
import streamlit as st

from ..config import DEFAULT_LOOKBACK_DAYS
from ..services import get_ohlcv_with_indicators
from ..utils.exceptions import DataSourceError, ValidationError
from .charts import plot_price_with_indicators, plot_rsi, plot_volume


def run() -> None:
    """Render the Streamlit dashboard. Call from main or run this module with streamlit."""
    st.set_page_config(page_title="NoKeyFinance", layout="wide")
    st.title("NoKeyFinance")
    st.caption("Free data only, no API keys")

    with st.sidebar:
        ticker = st.text_input("Ticker", value="AAPL", max_chars=20).strip().upper() or "AAPL"
        use_custom_dates = st.checkbox("Custom date range", value=False)
        start: Optional[str] = None
        end: Optional[str] = None
        if use_custom_dates:
            end_default = datetime.now()
            start_default = end_default - timedelta(days=DEFAULT_LOOKBACK_DAYS)
            start = st.date_input("Start", value=start_default).strftime("%Y-%m-%d")
            end = st.date_input("End", value=end_default).strftime("%Y-%m-%d")
        source = st.selectbox("Data source", options=["yahoo", "stooq"], index=0)
        show_indicators = st.checkbox("Show indicators (SMA, EMA, RSI)", value=True)

    if not ticker:
        st.warning("Enter a ticker symbol.")
        return

    try:
        stock, df = get_ohlcv_with_indicators(
            ticker,
            start=start,
            end=end,
            source=source,
        )
    except ValidationError as e:
        st.error(f"Invalid input: {e}")
        return
    except DataSourceError as e:
        st.error(f"Data error: {e}")
        return

    if df.empty:
        st.warning(f"No data for {ticker} in the selected range.")
        return

    st.subheader(f"{stock.ticker} ({stock.source})")
    if stock.date_range:
        st.caption(f"From {stock.date_range[0].date()} to {stock.date_range[1].date()}")

    fig_price = plot_price_with_indicators(
        df,
        ticker,
        sma_cols=list(df.columns[df.columns.str.startswith("sma_")]) if show_indicators else [],
        ema_cols=list(df.columns[df.columns.str.startswith("ema_")]) if show_indicators else [],
    )
    st.pyplot(fig_price)
    plt.close(fig_price)

    fig_vol = plot_volume(df, ticker)
    st.pyplot(fig_vol)
    plt.close(fig_vol)

    if show_indicators:
        fig_rsi = plot_rsi(df, ticker)
        if fig_rsi is not None:
            st.pyplot(fig_rsi)
            plt.close(fig_rsi)
