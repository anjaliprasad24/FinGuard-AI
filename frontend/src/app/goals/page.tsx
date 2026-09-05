"use client";

import { useEffect, useState } from "react";
import { FinancialGoal } from "@/lib/types";
import { api } from "@/lib/api";
import { Target, Plus, CheckCircle2, Clock, AlertTriangle } from "lucide-react";

export default function GoalsPage() {
  const [goals, setGoals] = useState<FinancialGoal[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState("");
  const [targetAmount, setTargetAmount] = useState("");
  const [savings, setSavings] = useState("");
  const [targetDate, setTargetDate] = useState("2026-12-31");
  const [saving, setSaving] = useState(false);

  const loadGoals = async () => {
    try {
      const data = await api.getGoals();
      if (data && data.length > 0) {
        setGoals(data);
      } else {
        // Sample default goals
        setGoals([
          {
            id: "goal-1",
            user_id: "demo",
            title: "Emergency Reserve Fund",
            target_amount: 100000,
            current_savings: 45000,
            target_date: "2026-12-31",
            priority: 1,
            status: "ON_TRACK",
            required_monthly_savings: 13750,
            projected_completion_date: "2026-12-31",
            created_at: new Date().toISOString(),
          },
          {
            id: "goal-2",
            user_id: "demo",
            title: "MacBook M4 Pro Upgrade",
            target_amount: 220000,
            current_savings: 60000,
            target_date: "2027-03-31",
            priority: 2,
            status: "DELAYED",
            required_monthly_savings: 22850,
            projected_completion_date: "2027-05-15",
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch (e) {}
  };

  useEffect(() => {
    loadGoals();
  }, []);

  const handleCreateGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !targetAmount) return;
    setSaving(true);
    try {
      const res = await api.createGoal({
        title,
        target_amount: parseFloat(targetAmount),
        current_savings: savings ? parseFloat(savings) : 0,
        target_date: targetDate,
      });
      setGoals((prev) => [...prev, res]);
      setShowModal(false);
      setTitle("");
      setTargetAmount("");
      setSavings("");
    } catch (err) {
      alert("Failed to create goal");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Financial Goal Trajectories</h1>
          <p className="text-xs text-slate-400">Dynamic Timeline Optimization & Required Monthly Saving Calculations</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2.5 rounded-lg shadow-lg shadow-blue-500/20 flex items-center space-x-2 text-sm transition"
        >
          <Plus className="w-4 h-4" />
          <span>New Financial Goal</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {goals.map((g) => {
          const pct = Math.min(100, Math.round((g.current_savings / g.target_amount) * 100));
          return (
            <div key={g.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <div className="p-2 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30">
                      <Target className="w-4 h-4" />
                    </div>
                    <h3 className="font-bold text-slate-200 text-base">{g.title}</h3>
                  </div>
                  {g.status === "DELAYED" ? (
                    <span className="flex items-center space-x-1 text-xs bg-amber-500/20 text-amber-400 px-2.5 py-0.5 rounded-full border border-amber-500/30">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Delayed Timeline</span>
                    </span>
                  ) : (
                    <span className="flex items-center space-x-1 text-xs bg-emerald-500/20 text-emerald-400 px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>On Track</span>
                    </span>
                  )}
                </div>

                <div className="flex items-baseline justify-between text-sm mb-2">
                  <span className="text-slate-400">Saved: <strong className="text-white">₹{g.current_savings.toLocaleString('en-IN')}</strong></span>
                  <span className="text-slate-400">Target: <strong className="text-slate-300">₹{g.target_amount.toLocaleString('en-IN')}</strong></span>
                </div>

                <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mb-4">
                  <div className="h-full bg-blue-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
                </div>
              </div>

              <div className="border-t border-slate-800 pt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
                <div>
                  <span className="block text-slate-500">Required Monthly</span>
                  <strong className="text-slate-200">₹{g.required_monthly_savings.toLocaleString('en-IN')} / mo</strong>
                </div>
                <div>
                  <span className="block text-slate-500">Target Date</span>
                  <strong className="text-slate-200">{g.target_date}</strong>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* New Goal Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1">Create Financial Goal</h3>
            <p className="text-xs text-slate-400 mb-4">Controller automatically recalculates timeline based on discretionary budget deficit</p>

            <form onSubmit={handleCreateGoal} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Goal Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Home Down Payment"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Target Amount (₹)</label>
                  <input
                    type="number"
                    value={targetAmount}
                    onChange={(e) => setTargetAmount(e.target.value)}
                    placeholder="500000"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Initial Savings (₹)</label>
                  <input
                    type="number"
                    value={savings}
                    onChange={(e) => setSavings(e.target.value)}
                    placeholder="50000"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Target Date</label>
                <input
                  type="date"
                  value={targetDate}
                  onChange={(e) => setTargetDate(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  required
                />
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
                  {saving ? "Creating..." : "Save Goal"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
