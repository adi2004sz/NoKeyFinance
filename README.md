# NoKeyFinance

Historical market data and charts with no API keys or signup. Uses Yahoo Finance and Stooq only.

## Features

- OHLCV data with optional date range (max 20 years)
- Technical indicators: SMA (20, 50), EMA (12, 26), RSI, daily returns
- Data sources: Yahoo (`yfinance`) and Stooq (`pandas-datareader`)
- Export: CSV (dataset) and PNG (per chart)
- Two UIs: React + FastAPI or Streamlit

## Run (React + FastAPI)

**Backend**

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Or: `python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000`

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/api` to the backend.

## Run (Streamlit)

```bash
pip install -r requirements.txt
streamlit run finance_app/main.py
```

Or: `python -m finance_app.main`

## Testing the API

With the backend running:

```bash
# Health
curl http://127.0.0.1:8000/api/health

# OHLCV (example)
curl "http://127.0.0.1:8000/api/ohlcv?ticker=AAPL&start=2024-01-01&end=2024-06-01&source=yahoo&show_indicators=true"
```

Query params: `ticker` (required), `start`, `end` (YYYY-MM-DD), `source` (yahoo | stooq), `show_indicators` (true | false).

## Usage

Sidebar: ticker, optional date range, source (Yahoo / Stooq), "Show indicators" for SMA/EMA/RSI. Fetch loads data; export CSV or PNG per chart.

## Tech

- **Backend**: Python, FastAPI, pandas, numpy, yfinance, pandas-datareader
- **Frontend**: React (Vite), TypeScript, Recharts, html2canvas
- **Legacy UI**: Streamlit

## Notes

- HTTP cache enabled by default (5 min). Disable with `NOKEYFINANCE_CACHE=0`.
- Ticker length and date range are limited to avoid abuse.
