-- ============================================================
-- E-Commerce A/B Test Dashboard - PostgreSQL Initialization
-- ============================================================
-- This script creates the database schema for the dashboard
-- and sets up tables for analytics and monitoring
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
-- INDEXES FOR PERFORMANCE
-- ============================================================

-- Daily metrics indexes
CREATE INDEX IF NOT EXISTS idx_daily_metrics_date ON daily_metrics(date DESC);

-- User behavior indexes
CREATE INDEX IF NOT EXISTS idx_user_behavior_user_id ON user_behavior(user_id);
CREATE INDEX IF NOT EXISTS idx_user_behavior_session_date ON user_behavior(session_date DESC);
CREATE INDEX IF NOT EXISTS idx_user_behavior_device ON user_behavior(device_type);
CREATE INDEX IF NOT EXISTS idx_user_behavior_country ON user_behavior(country);
CREATE INDEX IF NOT EXISTS idx_user_behavior_converted ON user_behavior(converted);

-- Product indexes
CREATE INDEX IF NOT EXISTS idx_products_category ON products_summary(category);
CREATE INDEX IF NOT EXISTS idx_products_revenue ON products_summary(total_revenue DESC);

-- Traffic source indexes
CREATE INDEX IF NOT EXISTS idx_traffic_date ON traffic_sources(date DESC);
CREATE INDEX IF NOT EXISTS idx_traffic_source ON traffic_sources(source);

-- A/B testing indexes
CREATE INDEX IF NOT EXISTS idx_ab_scenarios_status ON ab_test_scenarios(status);
CREATE INDEX IF NOT EXISTS idx_ab_results_scenario ON ab_test_results(scenario_id);
CREATE INDEX IF NOT EXISTS idx_ab_results_date ON ab_test_results(date DESC);

-- Funnel indexes
CREATE INDEX IF NOT EXISTS idx_funnel_date ON funnel_stages(date DESC);
CREATE INDEX IF NOT EXISTS idx_funnel_stage_order ON funnel_stages(stage_order);

-- Logs indexes
CREATE INDEX IF NOT EXISTS idx_logs_created ON dashboard_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_logs_level ON dashboard_logs(log_level);

-- ============================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================

-- Daily KPIs summary view
CREATE OR REPLACE VIEW v_daily_kpis AS
SELECT 
    date,
    total_users,
    total_sessions,
    total_revenue,
    total_conversions,
    conversion_rate,
    avg_order_value,
    avg_session_duration,
    ROUND(total_revenue / NULLIF(total_sessions, 0), 2) AS revenue_per_session
FROM daily_metrics
ORDER BY date DESC;

-- Product performance view
CREATE OR REPLACE VIEW v_top_products AS
SELECT 
    product_id,
    product_name,
    category,
    total_purchases,
    total_revenue,
    conversion_rate,
    avg_rating,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM products_summary
WHERE total_purchases > 0
ORDER BY total_revenue DESC;

-- A/B test summary view
CREATE OR REPLACE VIEW v_ab_test_summary AS
SELECT 
    s.scenario_id,
    s.scenario_name,
    s.status,
    s.start_date,
    s.end_date,
    COUNT(DISTINCT r.date) as days_running,
    SUM(CASE WHEN r.variant = 'A' THEN r.visitors ELSE 0 END) as variant_a_visitors,
    SUM(CASE WHEN r.variant = 'B' THEN r.visitors ELSE 0 END) as variant_b_visitors,
    AVG(CASE WHEN r.variant = 'A' THEN r.conversion_rate ELSE NULL END) as variant_a_conv_rate,
    AVG(CASE WHEN r.variant = 'B' THEN r.conversion_rate ELSE NULL END) as variant_b_conv_rate,
    MAX(r.statistical_significance) as max_significance
FROM ab_test_scenarios s
LEFT JOIN ab_test_results r ON s.scenario_id = r.scenario_id
GROUP BY s.scenario_id, s.scenario_name, s.status, s.start_date, s.end_date;

-- ============================================================
-- FUNCTIONS
-- ============================================================

-- Function to update daily metrics
CREATE OR REPLACE FUNCTION update_daily_metrics()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for daily metrics
DROP TRIGGER IF EXISTS trg_daily_metrics_updated ON daily_metrics;
CREATE TRIGGER trg_daily_metrics_updated
    BEFORE UPDATE ON daily_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_daily_metrics();

-- Function to calculate conversion rate
CREATE OR REPLACE FUNCTION calculate_conversion_rate(
    conversions INTEGER,
    visitors INTEGER
) RETURNS DECIMAL(5,4) AS $$
BEGIN
    IF visitors = 0 OR visitors IS NULL THEN
        RETURN 0;
    END IF;
    RETURN ROUND((conversions::DECIMAL / visitors::DECIMAL) * 100, 4);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ============================================================
-- INITIAL DATA / SEED DATA
-- ============================================================

-- Insert sample A/B test scenarios (will be replaced by actual data)
INSERT INTO ab_test_scenarios (scenario_id, scenario_name, description, status)
VALUES 
    ('S1', 'Homepage Hero Image', 'Test different hero images on homepage', 'active'),
    ('S2', 'Checkout Button Color', 'Test green vs orange checkout button', 'active'),
    ('S3', 'Free Shipping Banner', 'Test impact of free shipping banner', 'completed')
ON CONFLICT (scenario_id) DO NOTHING;

-- ============================================================
-- PERMISSIONS
-- ============================================================

-- Grant permissions to dashuser
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dashuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dashuser;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO dashuser;

-- ============================================================
-- COMPLETION MESSAGE
-- ============================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Database initialization completed!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Tables created: 11';
    RAISE NOTICE 'Indexes created: 15+';
    RAISE NOTICE 'Views created: 3';
    RAISE NOTICE 'Functions created: 2';
    RAISE NOTICE '========================================';
END $$;
