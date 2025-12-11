# Scripts Organization

This directory contains all analysis and data processing scripts organized by milestone.

## Structure
### 🗄️ Database Scripts

#### Initialization & Migrations
- `init_db.sql` - Complete database initialization (auto-run with Docker)
- `run_migrations.py` - Migration runner with version tracking
- `test_migrations.sh` - Migration test suite
- `import_data_to_postgres.py` - Import CSV data to PostgreSQL

#### migrations/
Versioned SQL migration files:
- `001_initial_schema.sql` - Core tables (analytics, A/B testing, monitoring)
- `002_indexes_and_views.sql` - Performance indexes + 3 analytical views
- `003_functions_and_triggers.sql` - Utility functions + automated triggers
- `004_seed_data.sql` - Initial A/B test scenarios

**Documentation:** See `MIGRATIONS.md` for detailed migration guide

---
### ��� data_prep/ - Milestone 1: Data Preparation & Cleaning
Data acquisition, cleaning, preprocessing, and preparation scripts.

**Scripts:**
- `download_dataset.py` - Download RetailRocket dataset
- `clean_events.py` - Clean events data
- `clean_item_properties.py` - Clean item properties
- `preprocess_retailrocket.py` - Preprocess raw data
- `load_retailrocket_to_db.py` - Load data to database
- `compress_data.py` - Compress data files
- `merge_data.py` - Merge multiple data sources
- `generate_data_clean_simple.py` - Generate clean simple dataset
- `generate_daily_metrics.py` - Generate daily aggregated metrics
- `generate_products_summary.py` - Generate product-level summary
- `inspect_csv.py` - Utility to inspect CSV files

**Output:** `data/clean/` directory with cleaned datasets

---

### ��� kpi_analysis/ - Milestone 2: KPI & Metrics Analysis
Analysis scripts for traffic, behavior, conversion, products, and funnel (Issues #9-#13).

**Scripts:**
- `traffic_analysis.py` - Issue #9: Traffic analysis (1.6M visitors, +42% growth)
- `user_behavior_analysis.py` - Issue #10: User behavior (95.82% drop-off, segments)
- `conversion_analysis.py` - Issue #11: Conversion rates (32.56% cart→purchase)
- `product_category_analysis.py` - Issue #12: Product/category (94.9% dead stock)
- `funnel_analysis.py` - Issue #13: Funnel view→cart→purchase (97.41% loss)

**Output:** 31 analysis files (CSV/JSON) in `data/clean/`

**Key Findings:**
- 97.41% loss view→cart (critical issue)
- 94.9% catalog dead stock (223K products)
- Weekend conversion -30%
- Premium segment 30x more profitable
- Potential revenue: +€1.95M

---

### ��� ab_testing/ - Milestone 3: A/B Testing Simulation
A/B testing simulation and optimization scenarios.

**Scripts:**
- `ab_test_simulation.py` - Issue #14: Simulate 8 optimization scenarios

**Output:** 5 analysis files in `data/clean/`
- `ab_test_simulation_summary.json`
- `ab_test_scenarios.csv`
- `ab_test_simulation_results.csv`
- `ab_test_business_impact.csv`
- `ab_test_roadmap.csv`

**8 Scenarios Simulated:**
1. S8 - Nettoyage Catalogue: ROI +105,309% ⭐
2. S2 - Reviews Clients: ROI +40,056%
3. S4 - Prix Compétitifs: ROI +37,546%
4. S6 - Optimisation Weekend: ROI +33,363%
5. S5 - Paiements Multiples: ROI +22,488%
6. S1 - Photos Produits: ROI +14,958%
7. S3 - Checkout Simplifié: ROI +14,958%
8. S7 - Programme Fidélité: ROI +11,947%

**Portfolio Impact:**
- Investment: €148K
- Annual revenue: €38.4M
- ROI: +25,845%

---

## Usage

### Milestone 1 - Data Preparation
```bash
# Download and prepare data
python data_prep/download_dataset.py
python data_prep/preprocess_retailrocket.py
python data_prep/generate_daily_metrics.py
python data_prep/generate_products_summary.py
```

### Milestone 2 - KPI Analysis
```bash
# Run all analyses (Issues #9-#13)
python kpi_analysis/traffic_analysis.py
python kpi_analysis/user_behavior_analysis.py
python kpi_analysis/conversion_analysis.py
python kpi_analysis/product_category_analysis.py
python kpi_analysis/funnel_analysis.py
```

### Milestone 3 - A/B Testing
```bash
# Run simulation
python ab_testing/ab_test_simulation.py
```

---

## Documentation

Full documentation for each milestone is available in `docs/`:
- `docs/ISSUE9_COMPLETED.md` - Traffic Analysis
- `docs/ISSUE10_COMPLETED.md` - User Behavior
- `docs/ISSUE11_COMPLETED.md` - Conversion Analysis
- `docs/ISSUE12_COMPLETED.md` - Product/Category Analysis
- `docs/ISSUE13_COMPLETED.md` - Funnel Analysis
- `docs/ISSUE14_COMPLETED.md` - A/B Testing Simulation

---

## Requirements

```bash
pip install pandas numpy scipy
```

All scripts are Python 3.12+ compatible.
