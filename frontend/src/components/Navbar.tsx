"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Receipt, ShieldAlert, TrendingUp, Target, Bot, FileText } from "lucide-react";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/transactions", label: "Transactions", icon: Receipt },
  { href: "/budget-controller", label: "Budget Policies", icon: ShieldAlert },
  { href: "/forecast", label: "Cash Flow Forecast", icon: TrendingUp },
  { href: "/goals", label: "Financial Goals", icon: Target },
  { href: "/copilot", label: "AI Copilot", icon: Bot },
  { href: "/audit", label: "Audit Registry", icon: FileText },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-slate-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30 shrink-0">
              FG
            </div>
            <div className="flex items-center space-x-2.5">
              <span className="font-bold text-lg tracking-wide text-white whitespace-nowrap">FinGuard AI</span>
              <span className="text-[11px] bg-blue-500/20 text-blue-400 px-2.5 py-0.5 rounded-full border border-blue-500/30 whitespace-nowrap font-medium">
                v1.0 XAI
              </span>
            </div>
          </div>

          <nav className="flex items-center space-x-1 overflow-x-auto">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-all ${
                    isActive
                      ? "bg-blue-600/20 text-blue-400 border border-blue-500/40"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}
