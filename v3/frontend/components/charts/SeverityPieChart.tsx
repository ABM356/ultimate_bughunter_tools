"use client";

import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { Severity } from "@/lib/types";

export interface SeveritySlice {
  name: Severity | string;
  value: number;
}

interface SeverityPieChartProps {
  data: SeveritySlice[];
  height?: number;
}

const COLORS: Record<string, string> = {
  critical: "#ff1744",
  high: "#ff6b35",
  medium: "#ffc400",
  low: "#2979ff",
  info: "#00c853",
};

export function SeverityPieChart({ data, height = 240 }: SeverityPieChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          innerRadius={50}
          outerRadius={80}
          paddingAngle={2}
        >
          {data.map((entry) => (
            <Cell key={entry.name} fill={COLORS[entry.name.toLowerCase()] || "#5a5a6a"} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "#111118",
            border: "1px solid #2a2a35",
            borderRadius: 6,
            fontSize: 12,
          }}
        />
        <Legend wrapperStyle={{ fontSize: 12 }} />
      </PieChart>
    </ResponsiveContainer>
  );
}
