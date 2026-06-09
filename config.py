"""
Configuration management for Croma Analytics Dashboard.
Centralized settings for pipeline, logging, and dashboard behavior.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT
LOG_DIR = PROJECT_ROOT

# File paths
CSV_FILES = {
    'campaigns': DATA_DIR / 'campaigns.csv',
    'customers': DATA_DIR / 'customers.csv',
    'products': DATA_DIR / 'products.csv',
    'transactions': DATA_DIR / 'transactions.csv',
}

OUTPUT_FILE = DATA_DIR / 'cleaned_sales_insights.csv'

# Logging configuration
LOG_CONFIG = {
    'pipeline_log': LOG_DIR / 'eda_pipeline.log',
    'dashboard_log': LOG_DIR / 'croma_dashboard.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Data validation rules
DATA_VALIDATION = {
    'required_transaction_columns': ['product_id', 'customer_id', 'gross_revenue', 'timestamp'],
    'numeric_columns': ['product_id', 'customer_id', 'gross_revenue', 'quantity'],
    'date_columns': {
        'customers': 'signup_date',
        'products': 'launch_date',
        'campaigns': ['start_date', 'end_date'],
        'transactions': 'timestamp'
    },
    'min_revenue': 0,  # Revenue should not be negative (except refunds)
    'min_quantity': 1   # Quantity should be at least 1
}

# Dashboard settings
DASHBOARD_CONFIG = {
    'page_title': "Croma Corporate Insights Portal",
    'layout': "wide",
    'sidebar_state': "expanded",
    'cache_enabled': True,
    'cache_ttl': 3600,  # 1 hour in seconds
}

# Visualization settings
CHART_CONFIG = {
    'color_scheme': 'Blues',
    'template': 'plotly_white',
    'hovermode': 'x unified',
    'responsive': True,
    'height': 500,
}

# Performance settings
PERFORMANCE = {
    'batch_size': 10000,
    'max_cache_entries': 1000,
    'enable_profiling': False,
}

# Data quality thresholds
QUALITY_THRESHOLDS = {
    'min_clean_record_percentage': 85.0,  # Alert if < 85% clean
    'max_anomaly_percentage': 15.0,        # Alert if > 15% anomalies
}


def get_config() -> Dict[str, Any]:
    """
    Retrieve complete configuration dictionary.
    
    Returns:
        Dict containing all configuration settings
    """
    return {
        'project_root': str(PROJECT_ROOT),
        'csv_files': {k: str(v) for k, v in CSV_FILES.items()},
        'output_file': str(OUTPUT_FILE),
        'logging': LOG_CONFIG,
        'validation': DATA_VALIDATION,
        'dashboard': DASHBOARD_CONFIG,
        'charts': CHART_CONFIG,
        'performance': PERFORMANCE,
        'quality': QUALITY_THRESHOLDS,
    }


def validate_data_files() -> bool:
    """
    Check if all required CSV files exist.
    
    Returns:
        bool: True if all files exist, False otherwise
    """
    missing_files = []
    for name, path in CSV_FILES.items():
        if not path.exists():
            missing_files.append(f"{name}: {path}")
    
    if missing_files:
        print("❌ Missing data files:")
        for file_info in missing_files:
            print(f"   - {file_info}")
        return False
    
    return True


if __name__ == "__main__":
    # Display configuration when run directly
    config = get_config()
    import json
    print(json.dumps(config, indent=2))
