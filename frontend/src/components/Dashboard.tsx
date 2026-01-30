import { useCallback, useState } from "react";
import type { OHLCVResponse } from "../types";
import PriceChart from "./PriceChart";
import VolumeChart from "./VolumeChart";
import RSIChart from "./RSIChart";

const API_BASE = "/api";

function safeFilename(s: string): string {
  return (s || "")
    .trim()
    .replace(/[^a-zA-Z0-9_-]/g, "_")
    .slice(0, 30) || "export";
}

export default function Dashboard() {
  const [ticker, setTicker] = useState("AAPL");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [source, setSource] = useState<"yahoo" | "stooq">("yahoo");
  const [showIndicators, setShowIndicators] = useState(true);
  const [data, setData] = useState<OHLCVResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(async () => {
    setError(null);
    setLoading(true);
    try {
      const params = new URLSearchParams({
        ticker: ticker.trim().toUpperCase() || "AAPL",
        source,
        show_indicators: String(showIndicators),
      });
      if (start) params.set("start", start);
      if (end) params.set("end", end);
      const res = await fetch(`${API_BASE}/ohlcv?${params}`);
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || res.statusText);
      }
      const json: OHLCVResponse = await res.json();
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [ticker, start, end, source, showIndicators]);

  const exportCSV = useCallback(() => {
    if (!data?.rows?.length) return;
    const headers = Object.keys(data.rows[0]).join(",");
    const lines = data.rows.map((r) =>
      Object.values(r)
        .map((v) => (v == null ? "" : String(v)))
        .join(",")
    );
    const csv = [headers, ...lines].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const dateSuffix = data.dateRange
      ? `_${data.dateRange[0]}_${data.dateRange[1]}`
      : "";
    a.download = `${safeFilename(data.ticker)}_${safeFilename(data.source)}${dateSuffix}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }, [data]);

  const dateSuffix = data?.dateRange
    ? `_${data.dateRange[0]}_${data.dateRange[1]}`
    : "";
  const exportTicker = data ? safeFilename(data.ticker) : "export";
  const exportSource = data ? safeFilename(data.source) : "data";

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: 260,
          padding: 16,
          borderRight: "1px solid #333",
          background: "#1a1a1a",
        }}
      >
        <h2 style={{ margin: "0 0 16px", fontSize: 18 }}>NoKeyFinance</h2>
        <p style={{ margin: "0 0 16px", fontSize: 12, color: "#888" }}>
          Free data, no API keys
        </p>
        <label style={{ display: "block", marginBottom: 4, fontSize: 12 }}>
          Ticker
        </label>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="AAPL"
          maxLength={20}
          style={{
            width: "100%",
            padding: 8,
            marginBottom: 12,
            background: "#222",
            border: "1px solid #444",
            color: "#eee",
            borderRadius: 4,
          }}
        />
        <label style={{ display: "block", marginBottom: 4, fontSize: 12 }}>
          Start (YYYY-MM-DD)
        </label>
        <input
          type="text"
          value={start}
          onChange={(e) => setStart(e.target.value)}
          placeholder="optional"
          style={{
            width: "100%",
            padding: 8,
            marginBottom: 12,
            background: "#222",
            border: "1px solid #444",
            color: "#eee",
            borderRadius: 4,
          }}
        />
        <label style={{ display: "block", marginBottom: 4, fontSize: 12 }}>
          End (YYYY-MM-DD)
        </label>
        <input
          type="text"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          placeholder="optional"
          style={{
            width: "100%",
            padding: 8,
            marginBottom: 12,
            background: "#222",
            border: "1px solid #444",
            color: "#eee",
            borderRadius: 4,
          }}
        />
        <label style={{ display: "block", marginBottom: 4, fontSize: 12 }}>
          Source
        </label>
        <select
          value={source}
          onChange={(e) => setSource(e.target.value as "yahoo" | "stooq")}
          style={{
            width: "100%",
            padding: 8,
            marginBottom: 12,
            background: "#222",
            border: "1px solid #444",
            color: "#eee",
            borderRadius: 4,
          }}
        >
          <option value="yahoo">Yahoo</option>
          <option value="stooq">Stooq</option>
        </select>
        <label style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
          <input
            type="checkbox"
            checked={showIndicators}
            onChange={(e) => setShowIndicators(e.target.checked)}
          />
          <span style={{ fontSize: 12 }}>Show indicators (SMA, EMA, RSI)</span>
        </label>
        <button
          onClick={fetchData}
          disabled={loading}
          style={{
            width: "100%",
            padding: 10,
            background: loading ? "#444" : "#2a7",
            border: "none",
            borderRadius: 4,
            color: "#fff",
            fontWeight: 600,
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Loading…" : "Load"}
        </button>
      </aside>

      <main style={{ flex: 1, padding: 24, overflow: "auto" }}>
        {error && (
          <div
            style={{
              padding: 12,
              marginBottom: 16,
              background: "#3a2020",
              border: "1px solid #a44",
              borderRadius: 4,
              color: "#f88",
            }}
          >
            {error}
          </div>
        )}

        {data && (
          <>
            <header style={{ marginBottom: 24 }}>
              <h1 style={{ margin: "0 0 4px", fontSize: 24 }}>
                {data.ticker} ({data.source})
              </h1>
              {data.dateRange && (
                <p style={{ margin: 0, fontSize: 14, color: "#888" }}>
                  {data.dateRange[0]} – {data.dateRange[1]}
                </p>
              )}
              {data.rows.length > 0 && (
                <button
                  onClick={exportCSV}
                  style={{
                    marginTop: 12,
                    padding: "8px 16px",
                    background: "#333",
                    border: "1px solid #555",
                    color: "#eee",
                    borderRadius: 4,
                    cursor: "pointer",
                  }}
                >
                  Download data (CSV)
                </button>
              )}
            </header>

            {data.rows.length === 0 ? (
              <p style={{ color: "#888" }}>No data for this range.</p>
            ) : (
              <>
                <section style={{ marginBottom: 32 }}>
                  <h3 style={{ margin: "0 0 8px", fontSize: 16 }}>Price</h3>
                  <PriceChart
                    rows={data.rows}
                    showIndicators={showIndicators}
                    exportFilename={`${exportTicker}_${exportSource}${dateSuffix}_price.png`}
                  />
                </section>
                <section style={{ marginBottom: 32 }}>
                  <h3 style={{ margin: "0 0 8px", fontSize: 16 }}>Volume</h3>
                  <VolumeChart
                    rows={data.rows}
                    exportFilename={`${exportTicker}_${exportSource}${dateSuffix}_volume.png`}
                  />
                </section>
                {showIndicators && data.rows.some((r) => r.rsi != null) && (
                  <section>
                    <h3 style={{ margin: "0 0 8px", fontSize: 16 }}>RSI</h3>
                    <RSIChart
                      rows={data.rows}
                      exportFilename={`${exportTicker}_${exportSource}${dateSuffix}_rsi.png`}
                    />
                  </section>
                )}
              </>
            )}
          </>
        )}

        {!data && !error && !loading && (
          <p style={{ color: "#666" }}>Enter a ticker and click Load.</p>
        )}
      </main>
    </div>
  );
}
