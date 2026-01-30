export interface OHLCVRow {
  date: string;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  volume: number | null;
  sma_20?: number | null;
  sma_50?: number | null;
  ema_12?: number | null;
  ema_26?: number | null;
  rsi?: number | null;
  returns?: number | null;
  volatility?: number | null;
}

export interface OHLCVResponse {
  ticker: string;
  source: string;
  dateRange: [string, string] | null;
  rows: OHLCVRow[];
}
