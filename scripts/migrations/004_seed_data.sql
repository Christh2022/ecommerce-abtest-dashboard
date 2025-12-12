-- ============================================================
-- Migration 004: Seed Data
-- Created: 2025-12-12
-- Description: Insert initial/sample data
-- ============================================================

-- ============================================================
-- A/B TEST SCENARIOS - Sample Data
-- ============================================================

INSERT INTO ab_test_scenarios (scenario_id, scenario_name, description, hypothesis, status)
VALUES 
    ('S1', 'Homepage Hero Image', 
     'Test different hero images on homepage', 
     'Product-focused hero image will increase engagement by 15%',
     'active'),
    ('S2', 'Checkout Button Color', 
     'Test green vs orange checkout button', 
     'Orange button will increase conversions by 10%',
     'active'),
    ('S3', 'Free Shipping Banner', 
     'Test impact of free shipping banner', 
     'Free shipping banner will increase AOV by 20%',
     'completed'),
    ('S4', 'Product Page Layout', 
     'Test vertical vs horizontal product layout', 
     'Horizontal layout will improve mobile conversion by 12%',
     'planned'),
    ('S5', 'Email Subject Lines', 
     'Test personalized vs generic subject lines', 
     'Personalized subjects will increase open rate by 25%',
     'planned')
ON CONFLICT (scenario_id) DO NOTHING;

-- ============================================================
-- PERMISSIONS (Re-apply if needed)
-- ============================================================

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dashuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dashuser;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO dashuser;

-- Record this migration
INSERT INTO schema_migrations (version, description)
VALUES ('004', 'Added seed data for A/B test scenarios')
ON CONFLICT (version) DO NOTHING;

-- ============================================================
-- COMPLETION MESSAGE
-- ============================================================

DO $$
DECLARE
    table_count INTEGER;
    index_count INTEGER;
    view_count INTEGER;
BEGIN
    -- Count tables
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    
    -- Count indexes
    SELECT COUNT(*) INTO index_count
    FROM pg_indexes
    WHERE schemaname = 'public';
    
    -- Count views
    SELECT COUNT(*) INTO view_count
    FROM information_schema.views
    WHERE table_schema = 'public';
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'All migrations completed successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Tables created: %', table_count;
    RAISE NOTICE 'Indexes created: %', index_count;
    RAISE NOTICE 'Views created: %', view_count;
    RAISE NOTICE '========================================';
END $$;
