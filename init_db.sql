CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    risk_tolerance VARCHAR(32) DEFAULT 'MODERATE', -- LOW, MODERATE, HIGH
    min_reserve_threshold NUMERIC(12, 2) DEFAULT 10000.00,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    raw_merchant VARCHAR(255) NOT NULL,
    clean_merchant VARCHAR(255) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    category VARCHAR(64) NOT NULL,
    transaction_type VARCHAR(16) DEFAULT 'EXPENSE', -- EXPENSE, INCOME
    confidence_score NUMERIC(5, 4) DEFAULT 1.0000,
    is_recurring BOOLEAN DEFAULT FALSE,
    anomaly_score NUMERIC(5, 4) DEFAULT 0.0000,
    risk_level VARCHAR(16) DEFAULT 'LOW', -- LOW, MEDIUM, HIGH, CRITICAL
    source VARCHAR(32) DEFAULT 'CSV',     -- CSV, OCR, SIMULATOR
    transaction_date DATE NOT NULL,
    embedding vector(1536),              -- For semantic search / RAG
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 3. Budget Policies
CREATE TABLE IF NOT EXISTS budget_policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(64) NOT NULL,
    monthly_limit NUMERIC(12, 2) NOT NULL,
    hard_cap BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, category)
);

-- 4. Financial Goals
CREATE TABLE IF NOT EXISTS financial_goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(128) NOT NULL,
    target_amount NUMERIC(12, 2) NOT NULL,
    current_savings NUMERIC(12, 2) DEFAULT 0.00,
    target_date DATE NOT NULL,
    priority INT DEFAULT 1,
    status VARCHAR(32) DEFAULT 'ON_TRACK' -- ON_TRACK, AT_RISK, DELAYED
);

-- 5. Audit Registry
CREATE TABLE IF NOT EXISTS system_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(64) NOT NULL,      -- ANOMALY_FLAGGED, POLICY_BREACH, SIMULATION, COPILOT_QUERY
    reference_id UUID,
    evidence_payload JSONB NOT NULL,      -- Full statistical and policy trace
    ai_generated_explanation TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_txn_user_date ON transactions(user_id, transaction_date);
CREATE INDEX IF NOT EXISTS idx_audit_user_event ON system_audit_logs(user_id, event_type);
