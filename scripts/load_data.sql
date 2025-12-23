-- ============================================================
-- Load sample data from CSV files into PostgreSQL
-- ============================================================

-- Load AB Test scenarios
\COPY ab_test_scenarios FROM '/data/clean/ab_test_scenarios.csv' WITH (FORMAT CSV, HEADER true);

-- Load AB Test results 
\COPY ab_test_results FROM '/data/clean/ab_test_simulation_results.csv' WITH (FORMAT CSV, HEADER true);

-- Load products summary
\COPY products_summary FROM '/data/clean/top_products_comprehensive.csv' WITH (FORMAT CSV, HEADER true);

-- Load daily metrics
\COPY daily_metrics (date, total_users, total_sessions, total_revenue, total_conversions) 
FROM '/data/clean/traffic_daily.csv' WITH (FORMAT CSV, HEADER true);

-- Display row counts
SELECT 'ab_test_scenarios' as table_name, COUNT(*) as rows FROM ab_test_scenarios
UNION SELECT 'ab_test_results', COUNT(*) FROM ab_test_results
UNION SELECT 'products_summary', COUNT(*) FROM products_summary
UNION SELECT 'daily_metrics', COUNT(*) FROM daily_metrics;
