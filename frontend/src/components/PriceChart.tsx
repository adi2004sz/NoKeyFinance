import { useRef } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { OHLCVRow } from "../types";

interface Props {
  rows: OHLCVRow[];
  showIndicators: boolean;
  exportFilename: string;
}

export default function PriceChart({ rows, showIndicators, exportFilename }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  const handleExportPng = async () => {
    const div = containerRef.current;
    if (!div) return;
    try {
      const { default: html2canvas } = await import("html2canvas");
      const canvas = await html2canvas(div, { scale: 2, useCORS: true });
      const url = canvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = url;
      a.download = exportFilename;
      a.click();
    } catch {
      // html2canvas not installed or failed
    }
  };

  return (
    <div ref={containerRef} style={{ background: "#1a1a1a", padding: 16, borderRadius: 8 }}>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={rows} margin={{ top: 8, right: 8, left: 8, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#999", fontSize: 11 }}
            stroke="#555"
          />
          <YAxis
            domain={["auto", "auto"]}
            tick={{ fill: "#999", fontSize: 11 }}
            stroke="#555"
          />
          <Tooltip
            contentStyle={{ background: "#222", border: "1px solid #444" }}
            labelStyle={{ color: "#ccc" }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          <Line
            type="monotone"
            dataKey="close"
            name="Close"
            stroke="#eee"
            strokeWidth={1.5}
            dot={false}
          />
          {showIndicators && (
            <>
              <Line
                type="monotone"
                dataKey="sma_20"
                name="SMA 20"
                stroke="#6af"
                strokeWidth={1}
                dot={false}
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="sma_50"
                name="SMA 50"
                stroke="#a6f"
                strokeWidth={1}
                dot={false}
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="ema_12"
                name="EMA 12"
                stroke="#6f6"
                strokeWidth={1}
                dot={false}
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="ema_26"
                name="EMA 26"
                stroke="#fa6"
                strokeWidth={1}
                dot={false}
                connectNulls
              />
            </>
          )}
        </LineChart>
      </ResponsiveContainer>
      <button
        type="button"
        onClick={handleExportPng}
        style={{
          marginTop: 8,
          padding: "6px 12px",
          fontSize: 12,
          background: "#333",
          border: "1px solid #555",
          color: "#ccc",
          borderRadius: 4,
          cursor: "pointer",
        }}
      >
        Download chart (PNG)
      </button>
    </div>
  );
}
