"use client";

import CashFlowChart from "@/components/CashFlowChart";
import { TrendingUp, Clock, Flame, ShieldAlert } from "lucide-react";

export default function ForecastPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Cash Flow Forecast & Runway</h1>
        <p className="text-xs text-slate-400">Predictive Financial Modeling (30 / 60 / 90-Day Time Horizon)</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-blue-600/20 text-blue-400 rounded-lg border border-blue-500/30">
              <TrendingUp className="w-5 h-5" />
            </div>
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Projected 30-Day Balance</span>
          </div>
          <div className="text-3xl font-extrabold text-white">₹32,000</div>
          <p className="text-xs text-emerald-400 mt-2 font-medium">Safely above ₹10,000 reserve floor</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-amber-600/20 text-amber-400 rounded-lg border border-amber-500/30">
              <Flame className="w-5 h-5" />
            </div>
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Avg Daily Burn Rate</span>
          </div>
          <div className="text-3xl font-extrabold text-white">₹1,200 / day</div>
          <p className="text-xs text-slate-400 mt-2">Calculated over 90-day moving window</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-emerald-600/20 text-emerald-400 rounded-lg border border-emerald-500/30">
              <Clock className="w-5 h-5" />
            </div>
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Estimated Financial Runway</span>
          </div>
          <div className="text-3xl font-extrabold text-white">37 Days</div>
          <p className="text-xs text-slate-400 mt-2">Until reserve threshold is tested</p>
        </div>
      </div>

      <CashFlowChart data={[]} minReserve={10000} />
    </div>
  );
}
