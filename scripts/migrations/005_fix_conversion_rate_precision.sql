-- ============================================================
-- Migration 005: Fix Conversion Rate Precision
-- Created: 2025-12-12
-- Description: Adjust conversion_rate columns to handle percentages correctly
-- ============================================================

-- Drop dependent views first
DROP VIEW IF EXISTS v_daily_kpis;
DROP VIEW IF EXISTS v_top_products;
DROP VIEW IF EXISTS v_ab_test_summary;

-- Adjust daily_metrics conversion_rate to DECIMAL(6,2) for percentages (0-100)
ALTER TABLE daily_metrics 
ALTER COLUMN conversion_rate TYPE DECIMAL(6,2);

-- Adjust ab_test_results conversion_rate
ALTER TABLE ab_test_results 
ALTER COLUMN conversion_rate TYPE DECIMAL(6,2);

-- Adjust products_summary conversion_rate
ALTER TABLE products_summary 
ALTER COLUMN conversion_rate TYPE DECIMAL(6,2);

-- Adjust funnel_stages conversion_rate
ALTER TABLE funnel_stages 
ALTER COLUMN conversion_rate TYPE DECIMAL(6,2);

-- Adjust ab_test_results statistical_significance
ALTER TABLE ab_test_results 
ALTER COLUMN statistical_significance TYPE DECIMAL(6,2);

-- Recreate views with updated schema
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
VALUES ('005', 'Fixed conversion_rate precision to handle percentages (0-100)')
ON CONFLICT (version) DO NOTHING;

-- Show completion message
DO $$
BEGIN
    RAISE NOTICE '✅ Conversion rate columns updated to DECIMAL(6,2)';
    RAISE NOTICE '✅ Views recreated with new schema';
END $$;
