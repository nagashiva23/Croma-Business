import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple
from datetime import datetime

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('eda_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CromaDataPipeline:
    """
    Production-grade EDA pipeline for Croma sales data with comprehensive
    data validation, error handling, and quality assurance.
    """
    
    REQUIRED_FILES = ['campaigns.csv', 'customers.csv', 'products.csv', 'transactions.csv']
    REQUIRED_TRANSACTION_COLS = ['product_id', 'customer_id', 'gross_revenue', 'timestamp']
    
    def __init__(self, base_dir: str = None):
        """Initialize pipeline with directory configuration."""
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.data = {}
        self.quality_report = {}
        logger.info(f"🚀 Croma Pipeline Initialized - Base Dir: {self.base_dir}")
    
    def load_csv_files(self) -> bool:
        """Load and validate all required CSV files."""
        logger.info("📂 Loading CSV files...")
        
        for file in self.REQUIRED_FILES:
            file_path = os.path.join(self.base_dir, file)
            try:
                if not os.path.exists(file_path):
                    logger.error(f"❌ File not found: {file_path}")
                    return False
                
                self.data[file.replace('.csv', '')] = pd.read_csv(file_path)
                logger.info(f"✅ Loaded {file}: {len(self.data[file.replace('.csv', '')])} rows")
                
            except Exception as e:
                logger.error(f"❌ Error loading {file}: {str(e)}")
                return False
        
        logger.info("✅ All core CSV files successfully loaded.\n")
        return True
    
    def validate_data_types(self) -> bool:
        """Validate critical data types across all dataframes."""
        logger.info("🔍 Validating data types...")
        
        try:
            # Check transactions required columns
            transactions = self.data['transactions']
            for col in self.REQUIRED_TRANSACTION_COLS:
                if col not in transactions.columns:
                    logger.error(f"❌ Missing column in transactions: {col}")
                    return False
            
            # Validate numeric columns
            numeric_cols = ['product_id', 'customer_id', 'gross_revenue', 'quantity']
            for col in numeric_cols:
                if col in transactions.columns:
                    non_numeric = transactions[col].apply(lambda x: not (pd.isna(x) or isinstance(x, (int, float, np.number))))
                    if non_numeric.any():
                        logger.warning(f"⚠️ Non-numeric values found in {col}: {non_numeric.sum()} rows")
            
            logger.info("✅ Data type validation passed.\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error during type validation: {str(e)}")
            return False
    
    def standardize_dates(self) -> bool:
        """Standardize all date columns to datetime."""
        logger.info("📅 Standardizing date columns...")
        
        try:
            date_mapping = {
                'customers': 'signup_date',
                'products': 'launch_date',
                'campaigns': ['start_date', 'end_date'],
                'transactions': 'timestamp'
            }
            
            for df_name, date_cols in date_mapping.items():
                if df_name not in self.data:
                    continue
                
                if isinstance(date_cols, str):
                    date_cols = [date_cols]
                
                for col in date_cols:
                    if col in self.data[df_name].columns:
                        before_count = self.data[df_name][col].isna().sum()
                        self.data[df_name][col] = pd.to_datetime(self.data[df_name][col], errors='coerce')
                        after_count = self.data[df_name][col].isna().sum()
                        
                        if after_count > before_count:
                            logger.warning(f"⚠️ {df_name}.{col}: {after_count - before_count} invalid dates coerced to NaT")
            
            logger.info("✅ Date standardization completed.\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error during date standardization: {str(e)}")
            return False
    
    def handle_data_anomalies(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Identify and separate anomalous records from clean data."""
        logger.info("🔍 Detecting data anomalies...")
        
        transactions = self.data['transactions'].copy()
        
        # Define anomaly conditions
        missing_product_revenue = transactions['product_id'].isna() | transactions['gross_revenue'].isna()
        invalid_revenue = (transactions['gross_revenue'] < 0)
        invalid_quantity = (transactions['quantity'] < 1) if 'quantity' in transactions.columns else pd.Series(False, index=transactions.index)
        
        # Separate anomalies
        anomaly_mask = missing_product_revenue | invalid_revenue | invalid_quantity
        df_corrupted = transactions[anomaly_mask].copy()
        transactions_clean = transactions[~anomaly_mask].copy()
        
        logger.info(f"✔️ Anomalies detected: {len(df_corrupted)} rows")
        logger.info(f"✔️ Clean records: {len(transactions_clean)} rows")
        logger.info(f"✔️ Data quality rate: {(len(transactions_clean)/len(transactions)*100):.2f}%\n")
        
        self.quality_report['total_records'] = len(transactions)
        self.quality_report['clean_records'] = len(transactions_clean)
        self.quality_report['corrupted_records'] = len(df_corrupted)
        
        return transactions_clean, df_corrupted
    
    def merge_and_enrich(self, transactions_clean: pd.DataFrame) -> pd.DataFrame:
        """Merge transaction data with dimension tables and calculate metrics."""
        logger.info("🔗 Merging data tables...")
        
        try:
            # Convert IDs to int after removing NaN
            transactions_clean['product_id'] = pd.to_numeric(transactions_clean['product_id'], errors='coerce').astype('Int64')
            transactions_clean['customer_id'] = pd.to_numeric(transactions_clean['customer_id'], errors='coerce').astype('Int64')
            
            # Merge with products
            df_master = transactions_clean.merge(self.data['products'], on='product_id', how='left', suffixes=('', '_product'))
            logger.info(f"✅ Merged with products: {len(df_master)} rows retained")
            
            # Merge with customers
            df_master = df_master.merge(self.data['customers'], on='customer_id', how='left', suffixes=('', '_customer'))
            logger.info(f"✅ Merged with customers: {len(df_master)} rows retained")
            
            # Calculate derived metrics
            df_master['net_revenue'] = np.where(df_master.get('refund_flag', 0) == 1, 0, df_master['gross_revenue'])
            df_master['transaction_month'] = pd.to_datetime(df_master['timestamp'], errors='coerce').dt.to_period('M')
            
            logger.info(f"✅ Data merging and enrichment completed.\n")
            return df_master
            
        except Exception as e:
            logger.error(f"❌ Error during merge: {str(e)}")
            raise

def run_croma_pipeline():
    """Execute complete Croma data pipeline."""
    try:
        pipeline = CromaDataPipeline()
        
        # Step 1: Load files
        if not pipeline.load_csv_files():
            logger.error("❌ Pipeline failed at file loading stage")
            return
        
        # Step 2: Validate data types
        if not pipeline.validate_data_types():
            logger.error("❌ Pipeline failed at validation stage")
            return
        
        # Step 3: Standardize dates
        if not pipeline.standardize_dates():
            logger.error("❌ Pipeline failed at date standardization")
            return
        
        # Step 4: Handle anomalies
        transactions_clean, df_corrupted = pipeline.handle_data_anomalies()
        
        # Step 5: Merge and enrich
        df_master = pipeline.merge_and_enrich(transactions_clean)
        
        # Step 6: Generate Executive Insights
        logger.info("="*60)
        logger.info("📈 EXECUTIVE BUSINESS INSIGHTS")
        logger.info("="*60)
        
        # Category Performance
        logger.info("\n🔹 Top Categories by Gross Revenue:")
        cat_perf = df_master.groupby('category')['gross_revenue'].agg(['sum', 'count', 'mean']).sort_values(by='sum', ascending=False)
        for cat, row in cat_perf.iterrows():
            logger.info(f"  - {cat:<15}: ₹{row['sum']:>12,.2f} | Transactions: {row['count']:>6.0f} | Avg: ₹{row['mean']:>10,.2f}")
        
        # Loyalty Tier Performance
        logger.info("\n🔹 Loyalty Tier Revenue Distribution:")
        loyalty_perf = df_master.groupby('loyalty_tier')['gross_revenue'].sum().sort_values(ascending=False)
        total_rev = loyalty_perf.sum()
        for tier, rev in loyalty_perf.items():
            percentage = (rev / total_rev) * 100
            logger.info(f"  - {tier:<12}: ₹{rev:>12,.2f} ({percentage:>5.1f}%)")
        
        # Premium vs Regular Performance
        logger.info("\n🔹 Premium vs Regular Inventory Performance:")
        premium_perf = df_master.groupby('is_premium').agg(
            Transactions=('transaction_id', 'count'),
            Total_Revenue=('gross_revenue', 'sum'),
            Avg_Ticket=('gross_revenue', 'mean'),
            Total_Units=('quantity', 'sum') if 'quantity' in df_master.columns else ('product_id', 'count')
        )
        for idx, row in premium_perf.iterrows():
            type_label = "Premium" if idx == 1 else "Regular"
            logger.info(f"  {type_label}:")
            logger.info(f"    - Revenue: ₹{row['Total_Revenue']:,.2f}")
            logger.info(f"    - Avg Ticket: ₹{row['Avg_Ticket']:,.2f}")
            logger.info(f"    - Transactions: {row['Transactions']:.0f}")
        
        # Step 7: Save outputs
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(BASE_DIR, 'cleaned_sales_insights.csv')
        df_master.to_csv(output_path, index=False)
        logger.info(f"\n💾 ✅ Master dataset exported: {output_path}")
        
        # Save quality report
        logger.info(f"\n📊 Data Quality Summary:")
        logger.info(f"   Total Records Processed: {pipeline.quality_report['total_records']:,}")
        logger.info(f"   Clean Records: {pipeline.quality_report['clean_records']:,}")
        logger.info(f"   Corrupted Records: {pipeline.quality_report['corrupted_records']:,}")
        logger.info(f"   Quality Rate: {(pipeline.quality_report['clean_records']/pipeline.quality_report['total_records']*100):.2f}%\n")
        
        logger.info("✅ Pipeline execution completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Critical pipeline error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    run_croma_pipeline()