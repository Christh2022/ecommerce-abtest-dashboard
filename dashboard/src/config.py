"""
Configuration centralisée de l'application
Chemins, paramètres, constants
"""
from pathlib import Path
import os

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DASHBOARD_ROOT = Path(__file__).parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
DATA_CLEAN = DATA_ROOT / "clean"
DATA_RAW = DATA_ROOT / "raw"

# Application settings
APP_TITLE = "E-Commerce A/B Test Dashboard"
APP_HOST = os.environ.get('DASH_HOST', '0.0.0.0')
APP_PORT = int(os.environ.get('DASH_PORT', 8050))
DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')

# Security settings
RATE_LIMIT_GENERAL = int(os.environ.get('RATE_LIMIT_GENERAL', 200))  # req/min
RATE_LIMIT_AUTH = int(os.environ.get('RATE_LIMIT_AUTH', 20))  # req/min
BLOCK_DURATION = int(os.environ.get('BLOCK_DURATION', 300))  # seconds

# Data files
DATA_FILES = {
    'daily_metrics': DATA_CLEAN / 'daily_metrics.csv',
    'ab_simulations': DATA_CLEAN / 'ab_test_simulation.csv',
    'products_summary': DATA_CLEAN / 'products_summary.csv',
    'funnel_daily': DATA_CLEAN / 'funnel_daily_detailed.csv',
    'cohort_analysis': DATA_CLEAN / 'cohort_analysis_monthly.csv',
    'hourly_analysis': DATA_CLEAN / 'hourly_analysis.csv',
    'segment_performance': DATA_CLEAN / 'segment_performance.csv',
}

# Business constants
AVG_ORDER_VALUE = 255.36  # EUR
CONVERSION_TARGET = 2.57  # %
USERS_TOTAL = 1_649_534
EVENTS_TOTAL = 2_756_101
DAYS_ANALYSIS = 139

# UI constants
THEME = "DARKLY"
SIDEBAR_WIDTH = "280px"
HEADER_HEIGHT = "100px"
COLORS = {
    'primary': '#375a7f',
    'success': '#00bc8c',
    'info': '#3498db',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'background': '#0d1117',
    'card_bg': '#161b22',
    'border': '#30363d',
}

# Statistical settings
CONFIDENCE_LEVEL = 0.95
SIGNIFICANCE_ALPHA = 0.05
MONTE_CARLO_SIMULATIONS = 10000
BOOTSTRAP_ITERATIONS = 10000
