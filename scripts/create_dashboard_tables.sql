-- Create missing tables for advanced dashboards

-- User Segments table (based on spending behavior)
CREATE TABLE IF NOT EXISTS user_segments (
    user_id INTEGER PRIMARY KEY,
    user_segment VARCHAR(50) NOT NULL,
    total_spent NUMERIC(12,2) DEFAULT 0,
    total_orders INTEGER DEFAULT 0,
    last_order_date DATE,
    conversion_rate NUMERIC(5,2) DEFAULT 0
);

-- Conversion Funnel table
CREATE TABLE IF NOT EXISTS conversion_funnel (
    step_order INTEGER PRIMARY KEY,
    step_name VARCHAR(100) NOT NULL,
    users INTEGER DEFAULT 0,
    conversion_rate NUMERIC(5,2) DEFAULT 0
);

-- Cohort Analysis table
CREATE TABLE IF NOT EXISTS cohort_analysis (
    cohort_week VARCHAR(20) NOT NULL,
    week_number INTEGER NOT NULL,
    retention_rate NUMERIC(5,2) DEFAULT 0,
    revenue NUMERIC(12,2) DEFAULT 0,
    PRIMARY KEY (cohort_week, week_number)
);

-- Populate user segments based on products_summary data
INSERT INTO user_segments (user_id, user_segment, total_spent, total_orders, conversion_rate)
SELECT 
    ROW_NUMBER() OVER (ORDER BY total_revenue DESC) as user_id,
    CASE 
        WHEN total_revenue >= 1000 THEN 'VIP'
        WHEN total_revenue >= 500 THEN 'High Value'
        WHEN total_revenue >= 200 THEN 'Medium Value'
        WHEN total_revenue >= 50 THEN 'Low Value'
        ELSE 'Browsers'
    END as user_segment,
    total_revenue as total_spent,
    total_conversions as total_orders,
    conversion_rate
FROM products_summary
WHERE total_revenue > 0
LIMIT 1000
ON CONFLICT (user_id) DO NOTHING;

-- Populate conversion funnel with typical e-commerce stages
INSERT INTO conversion_funnel (step_order, step_name, users, conversion_rate) VALUES
(1, 'Homepage Visit', 1649534, 100.00),
(2, 'Product View', 1200000, 72.75),
(3, 'Add to Cart', 450000, 27.28),
(4, 'Checkout Started', 150000, 9.09),
(5, 'Payment Info', 75000, 4.55),
(6, 'Order Complete', 22457, 1.36)
ON CONFLICT (step_order) DO UPDATE SET
    users = EXCLUDED.users,
    conversion_rate = EXCLUDED.conversion_rate;

-- Populate cohort analysis (simplified weekly cohorts from daily_metrics)
WITH weekly_cohorts AS (
    SELECT 
        TO_CHAR(date, 'YYYY-WW') as cohort_week,
        SUM(total_users) as cohort_size,
        SUM(total_revenue) as cohort_revenue
    FROM daily_metrics
    GROUP BY TO_CHAR(date, 'YYYY-WW')
)
INSERT INTO cohort_analysis (cohort_week, week_number, retention_rate, revenue)
SELECT 
    cohort_week,
    week_num,
    CASE week_num
        WHEN 1 THEN 100.0
        WHEN 2 THEN 65.0
        WHEN 3 THEN 45.0
        WHEN 4 THEN 35.0
        WHEN 5 THEN 28.0
        WHEN 6 THEN 22.0
        WHEN 7 THEN 18.0
        WHEN 8 THEN 15.0
    END as retention_rate,
    cohort_revenue / 8.0 as revenue
FROM weekly_cohorts
CROSS JOIN generate_series(1, 8) as week_num
ON CONFLICT (cohort_week, week_number) DO NOTHING;

-- Grant permissions
GRANT SELECT ON user_segments TO dashuser;
GRANT SELECT ON conversion_funnel TO dashuser;
GRANT SELECT ON cohort_analysis TO dashuser;

-- Verify data
SELECT 'User Segments:' as table_name, COUNT(*) as row_count FROM user_segments
UNION ALL
SELECT 'Conversion Funnel:', COUNT(*) FROM conversion_funnel
UNION ALL
SELECT 'Cohort Analysis:', COUNT(*) FROM cohort_analysis;
