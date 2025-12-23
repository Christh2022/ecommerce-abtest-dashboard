-- Generate sample AB test data for dashboards

-- Insert AB Test Scenarios
INSERT INTO ab_test_scenarios (scenario_id, scenario_name, description, hypothesis, status, start_date, end_date) VALUES
('S1', 'Improved Product Photos', 'HD photos, multi-angle, zoom, product videos', 'Better visuals will increase conversion rate', 'active', CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE + INTERVAL '30 days'),
('S2', 'Checkout Optimization', 'One-click checkout, save payment methods', 'Simplified checkout reduces cart abandonment', 'active', CURRENT_DATE - INTERVAL '25 days', CURRENT_DATE + INTERVAL '35 days'),
('S3', 'Personalized Recommendations', 'AI-powered product suggestions', 'Personalization increases average order value', 'active', CURRENT_DATE - INTERVAL '20 days', CURRENT_DATE + INTERVAL '40 days'),
('S4', 'Free Shipping Threshold', 'Free shipping over $50', 'Free shipping incentive increases order value', 'completed', CURRENT_DATE - INTERVAL '60 days', CURRENT_DATE - INTERVAL '10 days'),
('S5', 'Live Chat Support', '24/7 customer support chat', 'Immediate support increases conversion', 'active', CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE + INTERVAL '45 days')
ON CONFLICT (scenario_id) DO NOTHING;

-- Insert AB Test Results (Control vs Variants)
INSERT INTO ab_test_results (scenario_id, variant, visitors, conversions, revenue, date) VALUES
-- Scenario S1
('S1', 'control', 5000, 130, 6500.00, CURRENT_DATE - 5),
('S1', 'variant_a', 5000, 180, 9000.00, CURRENT_DATE - 5),
('S1', 'control', 4800, 125, 6250.00, CURRENT_DATE - 4),
('S1', 'variant_a', 4900, 175, 8750.00, CURRENT_DATE - 4),
-- Scenario S2
('S2', 'control', 4500, 270, 20250.00, CURRENT_DATE - 5),
('S2', 'variant_a', 4600, 368, 27600.00, CURRENT_DATE - 5),
('S2', 'control', 4400, 264, 19800.00, CURRENT_DATE - 4),
('S2', 'variant_a', 4550, 364, 27300.00, CURRENT_DATE - 4),
-- Scenario S3
('S3', 'control', 3800, 266, 26600.00, CURRENT_DATE - 3),
('S3', 'variant_a', 3900, 351, 35100.00, CURRENT_DATE - 3),
('S3', 'control', 3750, 262, 26200.00, CURRENT_DATE - 2),
('S3', 'variant_a', 3850, 347, 34700.00, CURRENT_DATE - 2),
-- Scenario S4 (completed)
('S4', 'control', 6000, 300, 24000.00, CURRENT_DATE - 30),
('S4', 'variant_a', 6100, 427, 36295.00, CURRENT_DATE - 30),
-- Scenario S5
('S5', 'control', 5500, 385, 28875.00, CURRENT_DATE - 1),
('S5', 'variant_a', 5600, 504, 37800.00, CURRENT_DATE - 1)
ON CONFLICT (scenario_id, date, variant) DO NOTHING;

-- Insert Daily Metrics (last 90 days)
INSERT INTO daily_metrics (date, total_users, total_sessions, total_revenue, total_conversions, conversion_rate, avg_order_value)
SELECT 
    CURRENT_DATE - (n || ' days')::INTERVAL AS date,
    7000 + (random() * 3000)::INT AS total_users,
    8000 + (random() * 4000)::INT AS total_sessions,
    (50000 + random() * 30000) AS total_revenue,
    800 + (random() * 400)::INT AS total_conversions,
    0.08 + (random() * 0.04) AS conversion_rate,
    55 + (random() * 40) AS avg_order_value
FROM generate_series(0, 89) AS n
ON CONFLICT (date) DO NOTHING;

-- Insert Products Summary
INSERT INTO products_summary (product_id, product_name, category, total_views, total_purchases, total_revenue, avg_rating) VALUES
('P1001', 'Wireless Bluetooth Headphones', 'Electronics', 15420, 892, 44600.00, 4.5),
('P1002', 'Smart Fitness Watch', 'Electronics', 12350, 654, 65400.00, 4.3),
('P1003', 'Organic Cotton T-Shirt', 'Clothing', 9800, 1245, 24900.00, 4.7),
('P1004', 'Leather Wallet', 'Accessories', 8520, 432, 17280.00, 4.6),
('P1005', 'Stainless Steel Water Bottle', 'Home & Kitchen', 11200, 876, 21900.00, 4.8),
('P1006', 'Yoga Mat Premium', 'Sports', 7650, 543, 21720.00, 4.4),
('P1007', 'Desk Organizer Set', 'Office', 6400, 389, 11670.00, 4.2),
('P1008', 'LED Desk Lamp', 'Electronics', 9100, 512, 25600.00, 4.5),
('P1009', 'Running Shoes', 'Sports', 13200, 765, 68850.00, 4.6),
('P1010', 'Coffee Maker', 'Home & Kitchen', 10500, 623, 62300.00, 4.7),
('P1011', 'Backpack Travel', 'Accessories', 8900, 501, 30060.00, 4.4),
('P1012', 'Phone Case', 'Electronics', 16500, 1987, 39740.00, 4.3),
('P1013', 'Sunglasses', 'Accessories', 7200, 423, 25380.00, 4.5),
('P1014', 'Portable Charger', 'Electronics', 14300, 856, 34240.00, 4.6),
('P1015', 'Kitchen Knife Set', 'Home & Kitchen', 5600, 298, 14900.00, 4.8);

-- Insert Funnel Stages (last 7 days)
INSERT INTO funnel_stages (date, stage_name, stage_order, visitors, conversion_rate)
SELECT 
    CURRENT_DATE - n AS date,
    'Homepage Visit' AS stage_name,
    1 AS stage_order,
    10000 - (n * 50) AS visitors,
    1.0 AS conversion_rate
FROM generate_series(0, 6) AS n
UNION ALL
SELECT 
    CURRENT_DATE - n AS date,
    'Product View' AS stage_name,
    2 AS stage_order,
    7500 - (n * 40) AS visitors,
    0.75 AS conversion_rate
FROM generate_series(0, 6) AS n
UNION ALL
SELECT 
    CURRENT_DATE - n AS date,
    'Add to Cart' AS stage_name,
    3 AS stage_order,
    2500 - (n * 20) AS visitors,
    0.25 AS conversion_rate
FROM generate_series(0, 6) AS n
UNION ALL
SELECT 
    CURRENT_DATE - n AS date,
    'Checkout' AS stage_name,
    4 AS stage_order,
    1500 - (n * 15) AS visitors,
    0.15 AS conversion_rate
FROM generate_series(0, 6) AS n
UNION ALL
SELECT 
    CURRENT_DATE - n AS date,
    'Purchase' AS stage_name,
    5 AS stage_order,
    1000 - (n * 10) AS visitors,
    0.10 AS conversion_rate
FROM generate_series(0, 6) AS n
ON CONFLICT (date, stage_name) DO NOTHING;

-- Insert Traffic Sources
INSERT INTO traffic_sources (source, visitors, conversions, revenue, avg_session_duration)
SELECT * FROM (VALUES
    ('Organic Search', 45000, 3600, 324000.00, 180),
    ('Direct', 28000, 2240, 201600.00, 150),
    ('Social Media', 18000, 900, 81000.00, 120),
    ('Email Campaign', 12000, 1440, 129600.00, 200),
    ('Paid Ads', 15000, 1350, 121500.00, 140),
    ('Referral', 8000, 560, 50400.00, 160)
) AS v(source, visitors, conversions, revenue, avg_session_duration);

-- Insert User Behavior (sample data for last 30 days)
INSERT INTO user_behavior (user_id, session_date, device_type, browser, country, page_views, session_duration, converted, revenue)
SELECT 
    'U' || (10000 + (random() * 90000)::INT) AS user_id,
    CURRENT_DATE - (random() * 30)::INT AS session_date,
    CASE (random() * 3)::INT 
        WHEN 0 THEN 'mobile'
        WHEN 1 THEN 'desktop'
        ELSE 'tablet'
    END AS device_type,
    CASE (random() * 4)::INT 
        WHEN 0 THEN 'Chrome'
        WHEN 1 THEN 'Firefox'
        WHEN 2 THEN 'Safari'
        ELSE 'Edge'
    END AS browser,
    CASE (random() * 5)::INT
        WHEN 0 THEN 'USA'
        WHEN 1 THEN 'UK'
        WHEN 2 THEN 'France'
        WHEN 3 THEN 'Germany'
        ELSE 'Spain'
    END AS country,
    (1 + random() * 20)::INT AS page_views,
    (30 + random() * 1800)::INT AS session_duration,
    random() > 0.85 AS converted,
    CASE WHEN random() > 0.85 THEN (20 + random() * 180) ELSE 0 END AS revenue
FROM generate_series(1, 1000);

-- Show counts
SELECT 'ab_test_scenarios' AS table_name, COUNT(*) AS rows FROM ab_test_scenarios
UNION SELECT 'ab_test_results', COUNT(*) FROM ab_test_results
UNION SELECT 'daily_metrics', COUNT(*) FROM daily_metrics
UNION SELECT 'products_summary', COUNT(*) FROM products_summary
UNION SELECT 'funnel_stages', COUNT(*) FROM funnel_stages
UNION SELECT 'traffic_sources', COUNT(*) FROM traffic_sources
UNION SELECT 'user_behavior', COUNT(*) FROM user_behavior
ORDER BY table_name;
