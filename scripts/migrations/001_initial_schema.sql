-- ============================================================
-- Migration 001: Initial Schema
-- Created: 2025-12-12
-- Description: Create initial database schema with all tables
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- ============================================================
-- MAIN ANALYTICS TABLES
-- ============================================================

-- Daily metrics aggregation table
CREATE TABLE IF NOT EXISTS daily_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    total_users INTEGER NOT NULL DEFAULT 0,
    total_sessions INTEGER NOT NULL DEFAULT 0,
    total_revenue DECIMAL(12,2) NOT NULL DEFAULT 0,
    total_conversions INTEGER NOT NULL DEFAULT 0,
    avg_session_duration DECIMAL(10,2),
    conversion_rate DECIMAL(5,4),
    avg_order_value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User behavior tracking
CREATE TABLE IF NOT EXISTS user_behavior (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    session_date DATE NOT NULL,
    device_type VARCHAR(20),
    browser VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    page_views INTEGER DEFAULT 0,
    session_duration INTEGER DEFAULT 0,
    bounce_rate DECIMAL(5,4),
    converted BOOLEAN DEFAULT FALSE,
    revenue DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product performance table
CREATE TABLE IF NOT EXISTS products_summary (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(255),
    category VARCHAR(100),
    total_views INTEGER DEFAULT 0,
    total_purchases INTEGER DEFAULT 0,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    avg_rating DECIMAL(3,2),
    conversion_rate DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Traffic source analysis
CREATE TABLE IF NOT EXISTS traffic_sources (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    source VARCHAR(100) NOT NULL,
    medium VARCHAR(100),
    campaign VARCHAR(255),
    sessions INTEGER DEFAULT 0,
    users INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, source, medium, campaign)
);

-- ============================================================
-- A/B TESTING TABLES
-- ============================================================

-- A/B test scenarios
CREATE TABLE IF NOT EXISTS ab_test_scenarios (
    id SERIAL PRIMARY KEY,
    scenario_id VARCHAR(10) NOT NULL UNIQUE,
    scenario_name VARCHAR(255) NOT NULL,
    description TEXT,
    hypothesis TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- A/B test daily results
CREATE TABLE IF NOT EXISTS ab_test_results (
    id SERIAL PRIMARY KEY,
    scenario_id VARCHAR(10) NOT NULL REFERENCES ab_test_scenarios(scenario_id),
    date DATE NOT NULL,
    variant VARCHAR(20) NOT NULL,
    visitors INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,4),
    revenue DECIMAL(10,2) DEFAULT 0,
    avg_order_value DECIMAL(10,2),
    statistical_significance DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scenario_id, date, variant)
);

-- ============================================================
-- CONVERSION FUNNEL TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS funnel_stages (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    stage_name VARCHAR(100) NOT NULL,
    stage_order INTEGER NOT NULL,
    visitors INTEGER DEFAULT 0,
    drop_off INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, stage_name)
);

-- ============================================================
-- MONITORING & LOGS
-- ============================================================

CREATE TABLE IF NOT EXISTS dashboard_logs (
    id SERIAL PRIMARY KEY,
    log_level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    module VARCHAR(100),
    function_name VARCHAR(100),
    user_id VARCHAR(50),
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS query_performance (
    id SERIAL PRIMARY KEY,
    query_name VARCHAR(255) NOT NULL,
    execution_time_ms INTEGER NOT NULL,
    rows_returned INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- MIGRATION TRACKING TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER
);

-- Record this migration
INSERT INTO schema_migrations (version, description)
VALUES ('001', 'Initial schema with analytics and A/B testing tables')
ON CONFLICT (version) DO NOTHING;
