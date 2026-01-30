import { useRef } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { OHLCVRow } from "../types";

interface Props {
  rows: OHLCVRow[];
  exportFilename: string;
}

export default function RSIChart({ rows, exportFilename }: Props) {
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
      <ResponsiveContainer width="100%" height={180}>
        <LineChart data={rows} margin={{ top: 8, right: 8, left: 8, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#999", fontSize: 11 }}
            stroke="#555"
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fill: "#999", fontSize: 11 }}
            stroke="#555"
          />
          <Tooltip
            contentStyle={{ background: "#222", border: "1px solid #444" }}
            labelStyle={{ color: "#ccc" }}
          />
          <ReferenceLine y={70} stroke="#555" strokeDasharray="3 3" />
          <ReferenceLine y={30} stroke="#555" strokeDasharray="3 3" />
          <Line
            type="monotone"
            dataKey="rsi"
            name="RSI"
            stroke="#a66fcf"
            strokeWidth={1.5}
            dot={false}
            connectNulls
          />
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
