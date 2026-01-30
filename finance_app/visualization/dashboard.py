"""Streamlit dashboard: ticker, date range, charts with optional indicators."""

import io
from datetime import datetime, timedelta
from typing import Optional

import matplotlib.pyplot as plt
import streamlit as st

from ..config import DEFAULT_LOOKBACK_DAYS
from ..services import get_ohlcv_with_indicators
from ..utils.exceptions import DataSourceError, ValidationError
from .charts import plot_price_with_indicators, plot_rsi, plot_volume


def _safe_filename_part(value: str) -> str:
    out = []
    for ch in (value or "").strip():
        if ch.isalnum() or ch in {"-", "_"}:
            out.append(ch)
        else:
            out.append("_")
    return "".join(out) or "export"


def _fig_to_png_bytes(fig: plt.Figure) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    return buf.getvalue()


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

    export_ticker = _safe_filename_part(stock.ticker)
    export_source = _safe_filename_part(stock.source)
    date_suffix = ""
    if stock.date_range:
        date_suffix = f"_{stock.date_range[0].date()}_{stock.date_range[1].date()}"

    csv_bytes = df.to_csv(index=True).encode("utf-8")
    st.download_button(
        "Download data (CSV)",
        data=csv_bytes,
        file_name=f"{export_ticker}_{export_source}{date_suffix}.csv",
        mime="text/csv",
    )

    fig_price = plot_price_with_indicators(
        df,
        ticker,
        sma_cols=list(df.columns[df.columns.str.startswith("sma_")]) if show_indicators else [],
        ema_cols=list(df.columns[df.columns.str.startswith("ema_")]) if show_indicators else [],
    )
    price_png = _fig_to_png_bytes(fig_price)
    st.pyplot(fig_price)
    st.download_button(
        "Download price chart (PNG)",
        data=price_png,
        file_name=f"{export_ticker}_{export_source}{date_suffix}_price.png",
        mime="image/png",
    )
    plt.close(fig_price)

    fig_vol = plot_volume(df, ticker)
    vol_png = _fig_to_png_bytes(fig_vol)
    st.pyplot(fig_vol)
    st.download_button(
        "Download volume chart (PNG)",
        data=vol_png,
        file_name=f"{export_ticker}_{export_source}{date_suffix}_volume.png",
        mime="image/png",
    )
    plt.close(fig_vol)

    if show_indicators:
        fig_rsi = plot_rsi(df, ticker)
        if fig_rsi is not None:
            rsi_png = _fig_to_png_bytes(fig_rsi)
            st.pyplot(fig_rsi)
            st.download_button(
                "Download RSI chart (PNG)",
                data=rsi_png,
                file_name=f"{export_ticker}_{export_source}{date_suffix}_rsi.png",
                mime="image/png",
            )
            plt.close(fig_rsi)
