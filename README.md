# NoKeyFinance

Financial data visualization using free sources only (no API keys). Data from Yahoo Finance and Stooq.

## Run the app

From the project root:

```bash
pip install -r requirements.txt
streamlit run finance_app/main.py
```

Or:

```bash
python -m finance_app.main
```

Use the sidebar to enter a ticker, optional date range, and data source (Yahoo or Stooq). Charts show price, volume, and optional indicators (SMA, EMA, RSI).
