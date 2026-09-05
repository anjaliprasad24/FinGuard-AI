"use client";

import { useEffect, useState } from "react";
import FinancialHealthCard from "@/components/FinancialHealthCard";
import CashFlowChart from "@/components/CashFlowChart";
import AnomalyAlertBanner from "@/components/AnomalyAlertBanner";
import TransactionFeed from "@/components/TransactionFeed";
import { Transaction } from "@/lib/types";
import { api } from "@/lib/api";
import { Plus, Upload, RefreshCw } from "lucide-react";

export default function DashboardPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [showIngestModal, setShowIngestModal] = useState(false);
  const [rawText, setRawText] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("Electronics");
  const [ingesting, setIngesting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const loadData = async () => {
    try {
      const data = await api.getTransactions();
      if (data && data.length > 0) {
        setTransactions(data);
      } else {
        setTransactions([
          {
            id: "tx-1",
            user_id: "demo",
            raw_merchant: "AMAZON.IN 18499.00 CARD 9988",
            clean_merchant: "Amazon Electronics",
            amount: 18499,
            currency: "INR",
            category: "Electronics",
            transaction_type: "EXPENSE",
            confidence_score: 0.98,
            is_recurring: false,
            anomaly_score: 0.87,
            risk_level: "HIGH",
            source: "API",
            transaction_date: "2026-09-05",
            created_at: new Date().toISOString(),
          },
          {
            id: "tx-2",
            user_id: "demo",
            raw_merchant: "SWIGGY FOOD DELIVERY",
            clean_merchant: "Swiggy",
            amount: 450,
            currency: "INR",
            category: "Dining & Food",
            transaction_type: "EXPENSE",
            confidence_score: 0.95,
            is_recurring: false,
            anomaly_score: 0.05,
            risk_level: "LOW",
            source: "API",
            transaction_date: "2026-09-04",
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch (err) {
      // Fallback
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rawText || !amount) return;
    setIngesting(true);
    setErrorMessage("");

    try {
      const res = await api.ingestTransaction({
        raw_merchant: rawText,
        amount: parseFloat(amount),
        category: category,
      });
      setTransactions((prev) => [res.transaction, ...prev]);
      setShowIngestModal(false);
      setRawText("");
      setAmount("");
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || "Cannot connect to backend server at http://localhost:8000";
      setErrorMessage(`Failed to ingest: ${detail}. Please ensure backend server is running on port 8000.`);
    } finally {
      setIngesting(false);
    }
  };

  const handleDeleteTransaction = async (id: string) => {
    try {
      await api.deleteTransaction(id);
    } catch (err) {
      // Deleting local state even if offline demo
    }
    setTransactions((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Financial Control Center</h1>
          <p className="text-xs text-slate-400">Autonomous Risk Scoring & Policy Guardrails Engine</p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={loadData}
            className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              setShowIngestModal(true);
              setErrorMessage("");
            }}
            className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2.5 rounded-lg shadow-lg shadow-blue-500/20 flex items-center space-x-2 text-sm transition"
          >
            <Plus className="w-4 h-4" />
            <span>Ingest Transaction</span>
          </button>
        </div>
      </div>

      <AnomalyAlertBanner />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <FinancialHealthCard currentBalance={45000} minReserve={10000} anomalyCount={1} />
        </div>
        <div className="lg:col-span-2">
          <CashFlowChart data={[]} minReserve={10000} />
        </div>
      </div>

      <TransactionFeed
        transactions={transactions}
        onIngestClick={() => setShowIngestModal(true)}
        onDeleteClick={handleDeleteTransaction}
      />

      {/* Ingest Modal */}
      {showIngestModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1">Ingest Raw Transaction</h3>
            <p className="text-xs text-slate-400 mb-4">Pipeline applies PII Scrubbing → Classification → IsolationForest Anomaly Check</p>

            {errorMessage && (
              <div className="mb-4 bg-rose-500/20 border border-rose-500/40 text-rose-300 p-3 rounded-lg text-xs leading-relaxed">
                {errorMessage}
              </div>
            )}

            <form onSubmit={handleIngest} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Raw Merchant / Text (PII scrubbed automatically)</label>
                <input
                  type="text"
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  placeholder="e.g. AMAZON.IN 18499 CARD 4532 1111 2222 9988"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Amount (₹)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="18499"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>
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
              </div>

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowIngestModal(false)}
                  className="px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={ingesting}
                  className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded-lg text-sm transition"
                >
                  {ingesting ? "Ingesting..." : "Process Pipeline"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
