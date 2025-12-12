#!/bin/bash
# Test script for database migrations
# Usage: ./test_migrations.sh

set -e

echo "========================================"
echo "🧪 Testing Database Migrations"
echo "========================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_CONTAINER="ecommerce-postgres"
DB_NAME="ecommerce_db"
DB_USER="dashuser"

echo ""
echo "📋 Pre-flight checks..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker is running"

# Check if PostgreSQL container exists and is running
if ! docker ps | grep -q $DB_CONTAINER; then
    echo -e "${YELLOW}⚠${NC} PostgreSQL container not running"
    echo "Starting PostgreSQL..."
    docker-compose up -d postgres
    sleep 5
fi
echo -e "${GREEN}✓${NC} PostgreSQL container is running"

# Check database connectivity
if ! docker exec $DB_CONTAINER pg_isready -U $DB_USER > /dev/null 2>&1; then
    echo -e "${RED}❌ Cannot connect to database${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Database is ready"

echo ""
echo "📊 Current migration status:"
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT version, description, applied_at FROM schema_migrations ORDER BY version;" 2>/dev/null || echo "No migrations table yet"

echo ""
echo "🔄 Running migrations..."
python scripts/run_migrations.py

echo ""
echo "✅ Verifying database structure..."

# Check tables
TABLE_COUNT=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';" | tr -d ' ')
echo "Tables created: $TABLE_COUNT"

# Check indexes
INDEX_COUNT=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';" | tr -d ' ')
echo "Indexes created: $INDEX_COUNT"

# Check views
VIEW_COUNT=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public';" | tr -d ' ')
echo "Views created: $VIEW_COUNT"

# Check functions
FUNCTION_COUNT=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM pg_proc WHERE pronamespace = 'public'::regnamespace;" | tr -d ' ')
echo "Functions created: $FUNCTION_COUNT"

echo ""
echo "📋 Testing sample queries..."

# Test view queries
echo "Testing v_daily_kpis view..."
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM v_daily_kpis;" > /dev/null 2>&1 && echo -e "${GREEN}✓${NC} v_daily_kpis OK" || echo -e "${RED}✗${NC} v_daily_kpis FAILED"

echo "Testing v_top_products view..."
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM v_top_products;" > /dev/null 2>&1 && echo -e "${GREEN}✓${NC} v_top_products OK" || echo -e "${RED}✗${NC} v_top_products FAILED"

echo "Testing v_ab_test_summary view..."
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM v_ab_test_summary;" > /dev/null 2>&1 && echo -e "${GREEN}✓${NC} v_ab_test_summary OK" || echo -e "${RED}✗${NC} v_ab_test_summary FAILED"

# Test functions
echo "Testing calculate_conversion_rate function..."
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT calculate_conversion_rate(100, 1000);" > /dev/null 2>&1 && echo -e "${GREEN}✓${NC} calculate_conversion_rate OK" || echo -e "${RED}✗${NC} calculate_conversion_rate FAILED"

echo "Testing calculate_aov function..."
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT calculate_aov(10000.00, 50);" > /dev/null 2>&1 && echo -e "${GREEN}✓${NC} calculate_aov OK" || echo -e "${RED}✗${NC} calculate_aov FAILED"

echo ""
echo "📊 Checking seed data..."
AB_SCENARIOS=$(docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM ab_test_scenarios;" | tr -d ' ')
echo "A/B test scenarios: $AB_SCENARIOS"

echo ""
echo "========================================"
echo -e "${GREEN}✅ Migration tests completed!${NC}"
echo "========================================"

echo ""
echo "📈 Final Status:"
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "
SELECT 
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE') as tables,
    (SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public') as indexes,
    (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public') as views,
    (SELECT COUNT(*) FROM schema_migrations) as migrations_applied;
"
