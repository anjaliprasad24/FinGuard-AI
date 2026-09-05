"use client";

import { AlertTriangle, ShieldAlert, X } from "lucide-react";
import { useState } from "react";

interface Anomaly {
  id: string;
  merchant: string;
  amount: number;
  zScore: number;
  category: string;
  reason: string;
}

interface Props {
  anomalies?: Anomaly[];
}

export default function AnomalyAlertBanner({ anomalies = [] }: Props) {
  const [dismissed, setDismissed] = useState<string[]>([]);

  const sampleAnomalies: Anomaly[] = anomalies.length > 0 ? anomalies : [
    {
      id: "anom-1",
      merchant: "AMAZON.IN",
      amount: 18499,
      zScore: 12.99,
      category: "Electronics",
      reason: "Spending ₹18,499 is 12.99 standard deviations above historical category mean (₹4,200)."
    }
  ];

  const activeAnomalies = sampleAnomalies.filter((a) => !dismissed.includes(a.id));

  if (activeAnomalies.length === 0) return null;

  return (
    <div className="space-y-3 mb-6">
      {activeAnomalies.map((item) => (
        <div
          key={item.id}
          className="bg-rose-950/40 border border-rose-500/40 rounded-xl p-4 flex items-start justify-between backdrop-blur-sm"
        >
          <div className="flex items-start space-x-3">
            <div className="p-2 rounded-lg bg-rose-500/20 text-rose-400 mt-0.5 border border-rose-500/30">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-rose-200 text-sm">XAI Anomaly Detected</span>
                <span className="bg-rose-500/20 text-rose-300 text-xs px-2 py-0.5 rounded border border-rose-500/30 font-mono">
                  Z = {item.zScore}
                </span>
                <span className="bg-slate-800 text-slate-300 text-xs px-2 py-0.5 rounded border border-slate-700">
                  {item.category}
                </span>
              </div>
              <p className="text-xs text-rose-300/90 mt-1 font-medium leading-relaxed">
                Merchant <strong className="text-white">{item.merchant}</strong> charged{" "}
                <strong className="text-white">₹{item.amount.toLocaleString('en-IN')}</strong>. {item.reason}
              </p>
            </div>
          </div>

          <button
            onClick={() => setDismissed([...dismissed, item.id])}
            className="text-slate-400 hover:text-slate-200 p-1 rounded-lg hover:bg-slate-800/60"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
}
