"use client";

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

interface DataPoint {
  date: string;
  projected_balance: number;
  daily_expense?: number;
  daily_income?: number;
}

interface Props {
  data: DataPoint[];
  minReserve?: number;
}

export default function CashFlowChart({ data, minReserve = 10000 }: Props) {
  const chartData = data.length > 0 ? data : [
    { date: "Day 1", projected_balance: 45000 },
    { date: "Day 15", projected_balance: 38000 },
    { date: "Day 30", projected_balance: 32000 },
    { date: "Day 45", projected_balance: 26000 },
    { date: "Day 60", projected_balance: 19000 },
    { date: "Day 75", projected_balance: 14000 },
    { date: "Day 90", projected_balance: 11000 },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">90-Day Cash Flow Projection</h3>
          <p className="text-xs text-slate-500">ML Forecast Engine (Statsmodels / Prophet)</p>
        </div>
        <div className="flex items-center space-x-4 text-xs">
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 bg-blue-500 rounded-full inline-block" />
            <span className="text-slate-300">Projected Balance</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-0.5 bg-rose-500 border border-dashed border-rose-500 inline-block" />
            <span className="text-slate-400">Reserve Floor (₹{minReserve})</span>
          </div>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="balanceGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
            <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
            <Tooltip
              contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#f8fafc", borderRadius: "8px" }}
              formatter={(val: any) => [`₹${Number(val).toLocaleString('en-IN')}`, 'Balance']}
            />
            <Area type="monotone" dataKey="projected_balance" stroke="#3b82f6" strokeWidth={2.5} fillOpacity={1} fill="url(#balanceGrad)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
