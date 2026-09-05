"use client";

import { ShieldCheck, ShieldAlert, DollarSign, Activity } from "lucide-react";

interface Props {
  currentBalance?: number;
  minReserve?: number;
  anomalyCount?: number;
  policyBreaches?: number;
}

export default function FinancialHealthCard({
  currentBalance = 45000,
  minReserve = 10000,
  anomalyCount = 1,
  policyBreaches = 0,
}: Props) {
  const healthScore = Math.max(10, Math.min(100, 100 - anomalyCount * 15 - policyBreaches * 25));
  const isHealthy = healthScore >= 75;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">Financial Health Index</h3>
        {isHealthy ? (
          <span className="flex items-center space-x-1 text-xs bg-emerald-500/20 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/30">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Optimal</span>
          </span>
        ) : (
          <span className="flex items-center space-x-1 text-xs bg-rose-500/20 text-rose-400 px-2.5 py-1 rounded-full border border-rose-500/30">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Action Required</span>
          </span>
        )}
      </div>

      <div className="flex items-baseline space-x-3 mb-4">
        <span className="text-4xl font-extrabold text-white tracking-tight">{healthScore} / 100</span>
        <span className="text-xs text-slate-400">AI Risk Score</span>
      </div>

      <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mb-6">
        <div
          className={`h-full rounded-full transition-all duration-500 ${
            healthScore >= 75 ? "bg-emerald-500" : healthScore >= 50 ? "bg-amber-500" : "bg-rose-500"
          }`}
          style={{ width: `${healthScore}%` }}
        />
      </div>

      <div className="grid grid-cols-2 gap-4 border-t border-slate-800/80 pt-4 text-sm">
        <div>
          <div className="text-slate-400 text-xs">Current Liquidity</div>
          <div className="font-bold text-white text-base">₹{currentBalance.toLocaleString('en-IN')}</div>
        </div>
        <div>
          <div className="text-slate-400 text-xs">Min Reserve Floor</div>
          <div className="font-bold text-slate-300 text-base">₹{minReserve.toLocaleString('en-IN')}</div>
        </div>
      </div>
    </div>
  );
}
