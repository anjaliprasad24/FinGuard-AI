import axios from 'axios';
import {
  UserProfile,
  Transaction,
  IngestResponse,
  BudgetPolicy,
  FinancialGoal,
  SimulationRequest,
  SimulationResponse,
  AuditLog,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Auth
  async getMe(): Promise<UserProfile> {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },

  // Transactions
  async getTransactions(category?: string): Promise<Transaction[]> {
    const params = category ? { category } : {};
    const res = await apiClient.get('/transactions/', { params });
    return res.data;
  },

  async ingestTransaction(data: {
    raw_merchant: string;
    amount: number;
    category?: string;
    transaction_date?: string;
  }): Promise<IngestResponse> {
    const res = await apiClient.post('/transactions/ingest', data);
    return res.data;
  },

  // OCR
  async uploadOCR(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post('/ocr/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  // Policies
  async getPolicies(): Promise<BudgetPolicy[]> {
    const res = await apiClient.get('/policies/');
    return res.data;
  },

  async createPolicy(data: { category: string; monthly_limit: number; hard_cap: boolean }): Promise<BudgetPolicy> {
    const res = await apiClient.post('/policies/', data);
    return res.data;
  },

  // Goals
  async getGoals(): Promise<FinancialGoal[]> {
    const res = await apiClient.get('/goals/');
    return res.data;
  },

  async createGoal(data: {
    title: string;
    target_amount: number;
    current_savings: number;
    target_date: string;
    priority?: number;
  }): Promise<FinancialGoal> {
    const res = await apiClient.post('/goals/', data);
    return res.data;
  },

  // Copilot & Simulation
  async simulatePurchase(req: SimulationRequest): Promise<SimulationResponse> {
    const res = await apiClient.post('/copilot/simulate', req);
    return res.data;
  },

  async chatCopilot(query: string): Promise<{ answer: string; evidence_citation: Record<string, any> }> {
    const res = await apiClient.post('/copilot/chat', { query });
    return res.data;
  },

  // Audit Logs
  async getAuditLogs(event_type?: string): Promise<AuditLog[]> {
    const params = event_type ? { event_type } : {};
    const res = await apiClient.get('/audit/logs', { params });
    return res.data;
  },
};
