-- ============================================================
-- Migration 003: Functions and Triggers
-- Created: 2025-12-12
-- Description: Add utility functions and triggers
-- ============================================================

-- ============================================================
-- FUNCTIONS
-- ============================================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

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

-- Function to calculate average order value
CREATE OR REPLACE FUNCTION calculate_aov(
    total_revenue DECIMAL,
    total_orders INTEGER
) RETURNS DECIMAL(10,2) AS $$
BEGIN
    IF total_orders = 0 OR total_orders IS NULL THEN
        RETURN 0;
    END IF;
    RETURN ROUND(total_revenue / total_orders, 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ============================================================
-- TRIGGERS
-- ============================================================

-- Trigger for daily_metrics
DROP TRIGGER IF EXISTS trg_daily_metrics_updated ON daily_metrics;
CREATE TRIGGER trg_daily_metrics_updated
    BEFORE UPDATE ON daily_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for products_summary
DROP TRIGGER IF EXISTS trg_products_updated ON products_summary;
CREATE TRIGGER trg_products_updated
    BEFORE UPDATE ON products_summary
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for ab_test_scenarios
DROP TRIGGER IF EXISTS trg_ab_scenarios_updated ON ab_test_scenarios;
CREATE TRIGGER trg_ab_scenarios_updated
    BEFORE UPDATE ON ab_test_scenarios
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Record this migration
INSERT INTO schema_migrations (version, description)
VALUES ('003', 'Added utility functions and automated triggers')
ON CONFLICT (version) DO NOTHING;
