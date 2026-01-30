# NoKeyFinance

Small Streamlit app for exploring historical market data (no API keys).

Data sources: Yahoo Finance (via `yfinance`) and Stooq (via `pandas-datareader`).

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt`

## Run

```bash
pip install -r requirements.txt
streamlit run finance_app/main.py
```

Or: `python -m finance_app.main`

## Usage

Use the sidebar to choose a ticker, optional date range, and data source. Turn on “Show indicators” to overlay SMA/EMA and show the RSI panel.

## Tech

Python, Streamlit, pandas, numpy, matplotlib.

## Notes

- A small local HTTP cache is enabled by default (5 min TTL). Disable with `NOKEYFINANCE_CACHE=0`.
