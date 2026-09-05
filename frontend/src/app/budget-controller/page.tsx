"use client";

import { useEffect, useState } from "react";
import { BudgetPolicy } from "@/lib/types";
import { api } from "@/lib/api";
import { ShieldAlert, Plus, ShieldCheck, AlertTriangle } from "lucide-react";

export default function BudgetControllerPage() {
  const [policies, setPolicies] = useState<BudgetPolicy[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [category, setCategory] = useState("Electronics");
  const [monthlyLimit, setMonthlyLimit] = useState("");
  const [hardCap, setHardCap] = useState(false);
  const [saving, setSaving] = useState(false);

  const loadPolicies = async () => {
    try {
      const data = await api.getPolicies();
      if (data && data.length > 0) {
        setPolicies(data);
      } else {
        // Sample default budget policy presets
        setPolicies([
          {
            id: "pol-1",
            user_id: "demo",
            category: "Electronics",
            monthly_limit: 15000,
            hard_cap: true,
            current_spend: 18499,
            status: "BREACHED",
            created_at: new Date().toISOString(),
          },
          {
            id: "pol-2",
            user_id: "demo",
            category: "Dining & Food",
            monthly_limit: 10000,
            hard_cap: false,
            current_spend: 4500,
            status: "NORMAL",
            created_at: new Date().toISOString(),
          },
          {
            id: "pol-3",
            user_id: "demo",
            category: "Groceries",
            monthly_limit: 12000,
            hard_cap: false,
            current_spend: 9800,
            status: "WARNING",
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch (e) {}
  };

  useEffect(() => {
    loadPolicies();
  }, []);

  const handleSavePolicy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!category || !monthlyLimit) return;
    setSaving(true);
    try {
      const res = await api.createPolicy({
        category,
        monthly_limit: parseFloat(monthlyLimit),
        hard_cap: hardCap,
      });
      setPolicies((prev) => {
        const filtered = prev.filter((p) => p.category !== category);
        return [...filtered, res];
      });
      setShowModal(false);
      setMonthlyLimit("");
    } catch (err) {
      alert("Failed to save policy");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Budget Guardrails & Policies</h1>
          <p className="text-xs text-slate-400">Hard Cap Enforcements & Category Spend Limits</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2.5 rounded-lg shadow-lg shadow-blue-500/20 flex items-center space-x-2 text-sm transition"
        >
          <Plus className="w-4 h-4" />
          <span>Set Category Limit</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {policies.map((p) => {
          const pct = Math.min(100, Math.round((p.current_spend / p.monthly_limit) * 100));
          return (
            <div key={p.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-bold text-slate-200 text-base">{p.category}</h3>
                  {p.status === "BREACHED" ? (
                    <span className="flex items-center space-x-1 text-xs bg-rose-500/20 text-rose-400 px-2.5 py-0.5 rounded-full border border-rose-500/30">
                      <ShieldAlert className="w-3.5 h-3.5" />
                      <span>Breached</span>
                    </span>
                  ) : p.status === "WARNING" ? (
                    <span className="flex items-center space-x-1 text-xs bg-amber-500/20 text-amber-400 px-2.5 py-0.5 rounded-full border border-amber-500/30">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      <span>Near Limit</span>
                    </span>
                  ) : (
                    <span className="flex items-center space-x-1 text-xs bg-emerald-500/20 text-emerald-400 px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>Compliant</span>
                    </span>
                  )}
                </div>

                <div className="flex items-baseline justify-between text-sm mb-2">
                  <span className="text-slate-400">Spent: <strong className="text-white">₹{p.current_spend.toLocaleString('en-IN')}</strong></span>
                  <span className="text-slate-400">Limit: <strong className="text-slate-300">₹{p.monthly_limit.toLocaleString('en-IN')}</strong></span>
                </div>

                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden mb-4">
                  <div
                    className={`h-full rounded-full transition-all ${
                      pct >= 100 ? "bg-rose-500" : pct >= 80 ? "bg-amber-500" : "bg-blue-500"
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>

              <div className="border-t border-slate-800 pt-3 flex items-center justify-between text-xs text-slate-500">
                <span>Hard Cap Mode:</span>
                <span className={p.hard_cap ? "text-rose-400 font-bold" : "text-slate-400"}>
                  {p.hard_cap ? "STRICT BLOCK" : "SOFT ADVISORY"}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Set Policy Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1">Set Category Budget Policy</h3>
            <p className="text-xs text-slate-400 mb-4">Enforce spending caps for automated policy controller checks</p>

            <form onSubmit={handleSavePolicy} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Category</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
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
                <label className="block text-xs font-semibold text-slate-400 mb-1">Monthly Limit (₹)</label>
                <input
                  type="number"
                  value={monthlyLimit}
                  onChange={(e) => setMonthlyLimit(e.target.value)}
                  placeholder="20000"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  required
                />
              </div>

              <div className="flex items-center space-x-2 pt-2">
                <input
                  type="checkbox"
                  id="hardCapCheckbox"
                  checked={hardCap}
                  onChange={(e) => setHardCap(e.target.checked)}
                  className="rounded bg-slate-950 border-slate-800 text-blue-600 focus:ring-0"
                />
                <label htmlFor="hardCapCheckbox" className="text-xs text-slate-300 cursor-pointer">
                  Enforce Hard Cap (Strict breach alert on excess)
                </label>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded-lg text-sm transition"
                >
                  {saving ? "Saving..." : "Save Policy"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
