"use client";

import { useState } from "react";
import CopilotChat from "@/components/CopilotChat";
import { api } from "@/lib/api";
import { SimulationResponse } from "@/lib/types";
import { Calculator, CheckCircle2, AlertTriangle, ShieldAlert } from "lucide-react";

export default function CopilotPage() {
  const [simAmount, setSimAmount] = useState("20000");
  const [simCategory, setSimCategory] = useState("Electronics");
  const [simMerchant, setSimMerchant] = useState("Apple Store");
  const [simulating, setSimulating] = useState(false);
  const [simResult, setSimResult] = useState<SimulationResponse | null>(null);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!simAmount) return;
    setSimulating(true);
    try {
      const res = await api.simulatePurchase({
        amount: parseFloat(simAmount),
        category: simCategory,
        merchant: simMerchant,
      });
      setSimResult(res);
    } catch (err) {
      alert("Simulation failed");
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">AI Copilot & Purchase Simulator</h1>
        <p className="text-xs text-slate-400">RAG Grounded Intelligence & Counterfactual What-If Analysis</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-7">
          <CopilotChat />
        </div>

        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30">
                <Calculator className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">"What-If" Purchase Simulator</h3>
                <p className="text-xs text-slate-400">Test impact on reserve floor & goal completion dates</p>
              </div>
            </div>

            <form onSubmit={handleSimulate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Simulated Purchase Amount (₹)</label>
                <input
                  type="number"
                  value={simAmount}
                  onChange={(e) => setSimAmount(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Category</label>
                  <select
                    value={simCategory}
                    onChange={(e) => setSimCategory(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="Electronics">Electronics</option>
                    <option value="Dining & Food">Dining & Food</option>
                    <option value="Groceries">Groceries</option>
                    <option value="Utilities & Bills">Utilities & Bills</option>
                    <option value="Travel & Transport">Travel & Transport</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Merchant</label>
                  <input
                    type="text"
                    value={simMerchant}
                    onChange={(e) => setSimMerchant(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={simulating}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold py-2.5 rounded-lg shadow-lg shadow-blue-500/20 text-sm transition"
              >
                {simulating ? "Calculating Impact..." : "Run Purchase Simulation"}
              </button>
            </form>

            {simResult && (
              <div className="mt-6 border-t border-slate-800 pt-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400">Simulation Status:</span>
                  {simResult.feasible ? (
                    <span className="flex items-center space-x-1 text-xs bg-emerald-500/20 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/30">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>FEASIBLE</span>
                    </span>
                  ) : (
                    <span className="flex items-center space-x-1 text-xs bg-rose-500/20 text-rose-400 px-2.5 py-1 rounded-full border border-rose-500/30">
                      <ShieldAlert className="w-3.5 h-3.5" />
                      <span>NOT RECOMMENDED</span>
                    </span>
                  )}
                </div>

                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 space-y-1 font-mono">
                  <div>Projected EOM Balance: ₹{simResult.projected_end_of_month_balance.toLocaleString('en-IN')}</div>
                  <div>Policy Breach: {simResult.policy_breach ? "YES" : "NO"}</div>
                  <div>Reserve Floor Breach: {simResult.reserve_breach ? "YES" : "NO"}</div>
                </div>

                <p className="text-xs text-slate-300 bg-slate-800/60 p-3 rounded-lg border border-slate-700 leading-relaxed">
                  {simResult.explanation}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
