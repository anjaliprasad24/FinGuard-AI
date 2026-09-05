export interface UserProfile {
  id: string;
  email: string;
  risk_tolerance: string;
  min_reserve_threshold: number;
  created_at: string;
}

export interface Transaction {
  id: string;
  user_id: string;
  raw_merchant: string;
  clean_merchant: string;
  amount: number;
  currency: string;
  category: string;
  transaction_type: 'EXPENSE' | 'INCOME';
  confidence_score: number;
  is_recurring: boolean;
  anomaly_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  source: string;
  transaction_date: string;
  created_at: string;
  evidence_payload?: Record<string, any>;
}

export interface IngestResponse {
  transaction: Transaction;
  is_anomaly: boolean;
  policy_breach: boolean;
  policy_warning?: string;
  evidence_payload: Record<string, any>;
}

export interface BudgetPolicy {
  id: string;
  user_id: string;
  category: string;
  monthly_limit: number;
  hard_cap: boolean;
  current_spend: number;
  status: 'NORMAL' | 'WARNING' | 'BREACHED';
  created_at: string;
}

export interface FinancialGoal {
  id: string;
  user_id: string;
  title: string;
  target_amount: number;
  current_savings: number;
  target_date: string;
  priority: number;
  status: 'ON_TRACK' | 'AT_RISK' | 'DELAYED' | 'COMPLETED';
  required_monthly_savings: number;
  projected_completion_date?: string;
  created_at: string;
}

export interface SimulationRequest {
  amount: number;
  category: string;
  merchant?: string;
}

export interface SimulationResponse {
  feasible: boolean;
  policy_breach: boolean;
  reserve_breach: boolean;
  current_category_spend: number;
  monthly_limit?: number;
  projected_end_of_month_balance: number;
  impacted_goals: Array<{
    title: string;
    status: string;
    months_delayed: number;
    projected_completion_date: string;
  }>;
  explanation: string;
}

export interface AuditLog {
  id: string;
  user_id: string;
  event_type: string;
  reference_id?: string;
  evidence_payload: Record<string, any>;
  ai_generated_explanation?: string;
  created_at: string;
}
