#!/bin/bash
# Quick data verification script for Grafana dashboards

echo "🔍 Verifying PostgreSQL Data for Grafana Dashboards"
echo "=================================================="
echo ""

# Check daily_metrics
echo "📊 Daily Metrics:"
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -t -c "
SELECT 
  'Date Range: ' || MIN(date) || ' to ' || MAX(date),
  'Total Rows: ' || COUNT(*),
  'Total Users: ' || SUM(total_users)::bigint,
  'Total Revenue: €' || ROUND(SUM(total_revenue)::numeric, 2)
FROM daily_metrics;
" | grep -v '^$'

echo ""
echo "🏷️  Products:"
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -t -c "
SELECT 
  'Total Products: ' || COUNT(*),
  'Total Revenue: €' || ROUND(SUM(total_revenue)::numeric, 2)
FROM products_summary
WHERE total_revenue > 0;
" | grep -v '^$'

echo ""
echo "🧪 A/B Tests:"
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -t -c "
SELECT 
  'Total Scenarios: ' || COUNT(DISTINCT scenario_id),
  'Total Results: ' || COUNT(*)
FROM ab_test_results;
" | grep -v '^$'

echo ""
echo "🔄 Funnel Stages:"
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -t -c "
SELECT 
  'Total Stages: ' || COUNT(DISTINCT stage_name),
  'Total Records: ' || COUNT(*)
FROM funnel_stages;
" | grep -v '^$'

echo ""
echo "🚦 Traffic Sources:"
docker exec ecommerce-postgres psql -U dashuser -d ecommerce_db -t -c "
SELECT 
  'Total Sources: ' || COUNT(DISTINCT source || '-' || medium),
  'Total Sessions: ' || SUM(total_sessions)::bigint
FROM traffic_sources;
" | grep -v '^$'

echo ""
echo "=================================================="
echo "✅ Data verification complete!"
echo ""
echo "📍 Grafana Dashboard URLs:"
echo "   Main Dashboard: http://localhost:3000/d/ecommerce-main-dashboard"
echo "   KPIs Dashboard: http://localhost:3000/d/ecommerce-kpis"
echo "   A/B Testing: http://localhost:3000/d/ab-testing-analysis"
echo ""
echo "🔑 Login: admin / admin123"
echo ""
