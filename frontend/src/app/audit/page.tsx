"use client";

import { useEffect, useState } from "react";
import { AuditLog } from "@/lib/types";
import { api } from "@/lib/api";
import { FileText, ShieldAlert, CheckCircle, Search, Code } from "lucide-react";

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [eventTypeFilter, setEventTypeFilter] = useState<string>("ALL");

  const loadLogs = async () => {
    try {
      const data = await api.getAuditLogs(eventTypeFilter === "ALL" ? undefined : eventTypeFilter);
      if (data && data.length > 0) {
        setLogs(data);
      } else {
        // Sample default audit logs
        setLogs([
          {
            id: "audit-1",
            user_id: "demo",
            event_type: "ANOMALY_FLAGGED",
            reference_id: "tx-1",
            evidence_payload: {
              amount: 18499,
              historical_mean: 4200,
              std_dev: 1100,
              z_score: 12.99,
              anomaly_score: 0.87,
              flagged: true,
              isolation_forest_raw_score: -0.28,
            },
            ai_generated_explanation:
              "Transaction of ₹18,499 was flagged because Z=12.99 exceeds historical category baseline (₹4,200).",
            created_at: new Date().toISOString(),
          },
          {
            id: "audit-2",
            user_id: "demo",
            event_type: "SIMULATION",
            reference_id: "sim-1",
            evidence_payload: {
              simulation: { amount: 20000, category: "Electronics" },
              feasible: true,
              projected_end_of_month_balance: 26500,
            },
            ai_generated_explanation:
              "Purchase simulation of ₹20,000 in Electronics. Projected EOM balance remains above ₹10,000 reserve floor.",
            created_at: new Date(Date.now() - 3600000).toISOString(),
          },
        ]);
      }
    } catch (e) {}
  };

  useEffect(() => {
    loadLogs();
  }, [eventTypeFilter]);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">System Audit Registry</h1>
          <p className="text-xs text-slate-400">Immutable Audit Trail of Anomaly Flags, Policy Breaches & Copilot Queries</p>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        {["ALL", "ANOMALY_FLAGGED", "POLICY_BREACH", "SIMULATION", "COPILOT_QUERY"].map((evt) => (
          <button
            key={evt}
            onClick={() => setEventTypeFilter(evt)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              eventTypeFilter === evt
                ? "bg-blue-600 text-white shadow"
                : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            {evt}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {logs.map((log) => (
          <div key={log.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <span className="font-mono text-xs text-slate-500">{new Date(log.created_at).toLocaleString()}</span>
                <span className="bg-blue-500/20 text-blue-400 text-xs px-2.5 py-0.5 rounded-full border border-blue-500/30 font-semibold">
                  {log.event_type}
                </span>
              </div>
              <span className="text-xs font-mono text-slate-500">ID: {log.id}</span>
            </div>

            <p className="text-sm text-slate-200 font-medium mb-4">{log.ai_generated_explanation}</p>

            <details className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs text-slate-400">
              <summary className="cursor-pointer font-mono font-semibold text-blue-400 hover:underline flex items-center space-x-1.5">
                <Code className="w-3.5 h-3.5" />
                <span>Expand Full Statistical & Policy Evidence Payload</span>
              </summary>
              <pre className="mt-3 font-mono text-[11px] text-emerald-400 overflow-x-auto bg-slate-900/60 p-3 rounded border border-slate-800">
                {JSON.stringify(log.evidence_payload, null, 2)}
              </pre>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}
