-- ============================================================
-- Migration 002: Indexes and Views
-- Created: 2025-12-12
-- Description: Add performance indexes and useful views
-- ============================================================

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

-- Record this migration
INSERT INTO schema_migrations (version, description)
VALUES ('002', 'Added performance indexes and analytical views')
ON CONFLICT (version) DO NOTHING;
