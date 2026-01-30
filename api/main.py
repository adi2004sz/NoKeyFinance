"""
NoKeyFinance API: REST endpoints for OHLCV + indicators.
Run: uvicorn api.main:app --reload
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on path so finance_app is importable
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from finance_app.services import get_ohlcv_with_indicators
from finance_app.utils.exceptions import DataSourceError, ValidationError

app = FastAPI(title="NoKeyFinance API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _df_to_records(df: pd.DataFrame) -> list[dict]:
    df = df.reset_index()
    df["date"] = df["date"].astype(str)
    df = df.replace({np.nan: None})
    return df.to_dict(orient="records")


@app.get("/api/ohlcv")
def ohlcv(
    ticker: str = Query(..., min_length=1, max_length=20),
    start: str | None = Query(None),
    end: str | None = Query(None),
    source: str = Query("yahoo"),
    show_indicators: bool = Query(True),
):
    """
    Fetch OHLCV and optional indicators. Returns JSON: ticker, source, dateRange, rows.
    """
    try:
        stock, df = get_ohlcv_with_indicators(
            ticker=ticker,
            start=start,
            end=end,
            source=source.strip().lower() or "yahoo",
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except DataSourceError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if df.empty:
        return {
            "ticker": stock.ticker,
            "source": stock.source,
            "dateRange": None,
            "rows": [],
        }

    date_range = None
    if stock.date_range:
        date_range = [
            str(stock.date_range[0].date()),
            str(stock.date_range[1].date()),
        ]

    return {
        "ticker": stock.ticker,
        "source": stock.source,
        "dateRange": date_range,
        "rows": _df_to_records(df),
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
