"use client";

import { Transaction } from "@/lib/types";
import { AlertCircle, CheckCircle2, ShieldAlert } from "lucide-react";

interface Props {
  transactions: Transaction[];
  onIngestClick?: () => void;
}

export default function TransactionFeed({ transactions, onIngestClick }: Props) {
  const getRiskBadge = (risk: string) => {
    switch (risk) {
      case "CRITICAL":
      case "HIGH":
        return (
          <span className="flex items-center space-x-1 text-xs bg-rose-500/20 text-rose-400 px-2 py-0.5 rounded border border-rose-500/30">
            <ShieldAlert className="w-3 h-3" />
            <span>{risk} RISK</span>
          </span>
        );
      case "MEDIUM":
        return (
          <span className="flex items-center space-x-1 text-xs bg-amber-500/20 text-amber-400 px-2 py-0.5 rounded border border-amber-500/30">
            <AlertCircle className="w-3 h-3" />
            <span>MEDIUM RISK</span>
          </span>
        );
      default:
        return (
          <span className="flex items-center space-x-1 text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>CLEARED</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">Live Transaction Feed</h3>
          <p className="text-xs text-slate-500">Real-time PII Scrubbed & Categorized Stream</p>
        </div>
        {onIngestClick && (
          <button
            onClick={onIngestClick}
            className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow transition"
          >
            + Ingest Raw Txn
          </button>
        )}
      </div>

      {transactions.length === 0 ? (
        <div className="text-center py-8 text-slate-500 text-sm">No transactions ingested yet.</div>
      ) : (
        <div className="divide-y divide-slate-800/80 overflow-x-auto">
          {transactions.map((t) => (
            <div key={t.id} className="py-3.5 flex items-center justify-between hover:bg-slate-800/30 px-2 rounded-lg transition">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-lg bg-slate-800 flex items-center justify-center font-bold text-slate-300 text-xs">
                  {t.category.slice(0, 2).toUpperCase()}
                </div>
                <div>
                  <div className="font-semibold text-slate-200 text-sm">{t.clean_merchant}</div>
                  <div className="text-xs text-slate-500 flex items-center space-x-2 mt-0.5">
                    <span>{t.category}</span>
                    <span>•</span>
                    <span>{t.transaction_date}</span>
                    <span>•</span>
                    <span className="font-mono text-slate-400">{t.source}</span>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <div className="font-bold text-slate-100 text-sm font-mono">
                  {t.transaction_type === 'EXPENSE' ? '-' : '+'}₹{t.amount.toLocaleString('en-IN')}
                </div>
                <div className="mt-1 flex justify-end">{getRiskBadge(t.risk_level)}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
