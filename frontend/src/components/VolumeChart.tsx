import { useRef } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { OHLCVRow } from "../types";

interface Props {
  rows: OHLCVRow[];
  exportFilename: string;
}

export default function VolumeChart({ rows, exportFilename }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  const data = rows.map((r) => ({
    ...r,
    fill: r.close != null && r.open != null && r.close >= r.open ? "#26a69a" : "#ef5350",
  }));

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
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#999", fontSize: 11 }}
            stroke="#555"
          />
          <YAxis
            tick={{ fill: "#999", fontSize: 11 }}
            stroke="#555"
          />
          <Tooltip
            contentStyle={{ background: "#222", border: "1px solid #444" }}
            labelStyle={{ color: "#ccc" }}
          />
          <Bar dataKey="volume" name="Volume" radius={[2, 2, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={data[i].fill} />
            ))}
          </Bar>
        </BarChart>
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
