"""
McKinsey-grade Retention & Churn Intelligence Platform
Senior Analytics Engine for Customer Intelligence

Phases:
1. Data Audit & Quality Check
2. Customer-Level Metrics
3. Customer Segmentation
4. Churn Analysis
5. Churn Risk Scoring
6. Executive Insights
7. Visual Analytics
8. Presentation Generation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.stats import percentileofscore
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('retention_analytics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RetentionAnalytics:
    """Enterprise-grade customer retention and churn intelligence engine"""
    
    def __init__(self, cleaned_data_path: str):
        """Initialize analytics engine with cleaned data"""
        self.data_path = cleaned_data_path
        self.df_master = None
        self.customer_metrics = None
        self.segments = None
        self.churn_drivers = None
        self.risk_scores = None
        self.insights = {}
        self.assumptions = []
        
        logger.info("🚀 Retention Analytics Engine Initialized")
    
    # ============= PHASE 1: DATA AUDIT & QUALITY CHECK =============
    
    def load_and_audit_data(self) -> Dict[str, Any]:
        """Load data and perform comprehensive quality audit"""
        logger.info("📋 PHASE 1: DATA AUDIT & QUALITY CHECK")
        
        try:
            self.df_master = pd.read_csv(self.data_path)
            logger.info(f"✅ Data loaded: {len(self.df_master)} rows, {len(self.df_master.columns)} columns")
            
            audit_report = {
                'total_records': len(self.df_master),
                'total_columns': len(self.df_master.columns),
                'date_range': {
                    'min': self.df_master['timestamp'].min(),
                    'max': self.df_master['timestamp'].max()
                },
                'columns_info': {},
                'data_quality': {},
                'join_keys': [],
                'issues': []
            }
            
            # Column-level audit
            for col in self.df_master.columns:
                audit_report['columns_info'][col] = {
                    'dtype': str(self.df_master[col].dtype),
                    'missing_count': int(self.df_master[col].isna().sum()),
                    'missing_pct': float(self.df_master[col].isna().sum() / len(self.df_master) * 100),
                    'unique_values': int(self.df_master[col].nunique()),
                    'sample_values': self.df_master[col].dropna().head(3).tolist()
                }
            
            # Join key validation
            join_keys = ['customer_id', 'product_id', 'transaction_id']
            audit_report['join_keys'] = [key for key in join_keys if key in self.df_master.columns]
            
            # Data quality issues
            if 'gross_revenue' in self.df_master.columns:
                negative_revenue = (self.df_master['gross_revenue'] < 0).sum()
                if negative_revenue > 0:
                    audit_report['issues'].append(f"⚠️ {negative_revenue} transactions with negative revenue")
                    self.assumptions.append("Negative revenue records treated as refunds")
            
            # Duplicate check
            duplicates = self.df_master.duplicated(subset=['transaction_id']).sum()
            if duplicates > 0:
                audit_report['issues'].append(f"⚠️ {duplicates} duplicate transaction records")
                self.assumptions.append("Duplicate transactions removed")
                self.df_master = self.df_master.drop_duplicates(subset=['transaction_id'])
            
            logger.info(f"✅ Data audit complete: {len(audit_report['issues'])} issues identified")
            return audit_report
        
        except Exception as e:
            logger.error(f"❌ Error in data audit: {str(e)}")
            raise
    
    # ============= PHASE 2: BUILD CUSTOMER-LEVEL METRICS =============
    
    def build_customer_metrics(self) -> pd.DataFrame:
        """Build comprehensive customer-level analytical dataset"""
        logger.info("\n📊 PHASE 2: CUSTOMER-LEVEL METRICS")
        
        # Ensure timestamp is datetime
        self.df_master['timestamp'] = pd.to_datetime(self.df_master['timestamp'])
        
        customer_metrics = self.df_master.groupby('customer_id').agg({
            'transaction_id': 'count',
            'gross_revenue': ['sum', 'mean'],
            'timestamp': ['min', 'max'],
            'loyalty_tier': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Bronze',
            'is_premium': lambda x: (x == 1).sum() / len(x) if len(x) > 0 else 0,
            'category': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Electronics'
        }).reset_index()
        
        # Flatten column names
        customer_metrics.columns = ['customer_id', 'total_orders', 'total_revenue', 
                                     'avg_order_value', 'first_purchase', 'last_purchase',
                                     'loyalty_tier', 'premium_purchase_ratio', 'primary_category']
        
        # Convert to datetime
        customer_metrics['first_purchase'] = pd.to_datetime(customer_metrics['first_purchase'])
        customer_metrics['last_purchase'] = pd.to_datetime(customer_metrics['last_purchase'])
        
        # Calculate additional metrics
        reference_date = pd.to_datetime(self.df_master['timestamp'].max())
        customer_metrics['days_since_last_purchase'] = (reference_date - customer_metrics['last_purchase']).dt.days
        customer_metrics['purchase_frequency_days'] = (customer_metrics['last_purchase'] - customer_metrics['first_purchase']).dt.days
        customer_metrics['purchase_frequency_days'] = customer_metrics['purchase_frequency_days'].replace(0, 1)
        customer_metrics['purchase_frequency'] = customer_metrics['total_orders'] / (customer_metrics['purchase_frequency_days'] / 365 + 0.01)
        
        # Engagement window - active in last 30 days
        thirty_days_ago = reference_date - timedelta(days=30)
        customer_metrics['is_active_30d'] = customer_metrics['last_purchase'] >= thirty_days_ago
        
        # CLV Proxy (simple model)
        customer_metrics['clv_proxy'] = customer_metrics['total_revenue'] * (customer_metrics['purchase_frequency'] / 10)
        
        self.customer_metrics = customer_metrics
        logger.info(f"✅ Customer metrics built: {len(customer_metrics)} unique customers")
        return customer_metrics
    
    # ============= PHASE 3: CUSTOMER SEGMENTATION & RFM =============
    
    def calculate_rfm(self) -> pd.DataFrame:
        """Calculate RFM scores and create customer segments"""
        logger.info("\n🎯 PHASE 3: CUSTOMER SEGMENTATION & RFM")
        
        df = self.customer_metrics.copy()
        reference_date = self.df_master['timestamp'].max()
        
        # RFM Calculation
        df['recency'] = (reference_date - df['last_purchase']).dt.days
        df['frequency'] = df['total_orders']
        df['monetary'] = df['total_revenue']
        
        # Percentile scoring (1-5, where 5 is best)
        df['r_score'] = 6 - pd.qcut(df['recency'], 5, labels=False, duplicates='drop')
        df['f_score'] = pd.qcut(df['frequency'].rank(method='first'), 5, labels=False, duplicates='drop') + 1
        df['m_score'] = pd.qcut(df['monetary'].rank(method='first'), 5, labels=False, duplicates='drop') + 1
        
        df['rfm_score'] = df['r_score'] + df['f_score'] + df['m_score']
        
        # Segment assignment
        def assign_segment(row):
            rfm = row['rfm_score']
            recency = row['recency']
            frequency = row['frequency']
            monetary = row['monetary']
            
            # Champions: Recent, frequent, high spend
            if recency <= 30 and frequency >= df['frequency'].quantile(0.75) and monetary >= df['monetary'].quantile(0.75):
                return 'Champions'
            # Loyal Customers
            elif frequency >= df['frequency'].quantile(0.60) and monetary >= df['monetary'].quantile(0.60):
                return 'Loyal Customers'
            # Potential Loyalists: Recent with good metrics
            elif recency <= 60 and frequency >= df['frequency'].quantile(0.50):
                return 'Potential Loyalists'
            # New Customers: Recent but low frequency
            elif recency <= 30 and frequency < df['frequency'].quantile(0.30):
                return 'New Customers'
            # At-Risk: Haven't purchased recently but were good customers
            elif recency > 90 and frequency >= df['frequency'].quantile(0.50):
                return 'At-Risk Customers'
            # Churn Risk: Low activity and haven't purchased in long time
            elif recency > 180 or (recency > 90 and frequency < df['frequency'].quantile(0.30)):
                return 'Churn Risk Customers'
            # Lost
            else:
                return 'Lost Customers'
        
        df['segment'] = df.apply(assign_segment, axis=1)
        
        self.customer_metrics = df
        logger.info(f"✅ RFM segmentation complete")
        logger.info(f"\nSegment Distribution:")
        for segment, count in df['segment'].value_counts().items():
            pct = count / len(df) * 100
            revenue = df[df['segment'] == segment]['total_revenue'].sum()
            logger.info(f"   {segment:<25}: {count:>7,} customers ({pct:>5.1f}%) | Revenue: ₹{revenue:>12,.0f}")
        
        return df
    
    # ============= PHASE 4: CHURN ANALYSIS =============
    
    def analyze_churn(self) -> Dict[str, Any]:
        """Analyze churn patterns and identify key drivers"""
        logger.info("\n⚠️ PHASE 4: CHURN ANALYSIS")
        
        df = self.customer_metrics.copy()
        
        # Define churn: No purchase in last 180 days
        df['is_churned'] = df['days_since_last_purchase'] > 180
        self.customer_metrics['is_churned'] = df['is_churned']  # Save to main dataframe
        
        churn_metrics = {
            'churn_count': df['is_churned'].sum(),
            'churn_rate': df['is_churned'].sum() / len(df),
            'retention_rate': 1 - (df['is_churned'].sum() / len(df)),
            'churned_revenue_impact': df[df['is_churned']]['total_revenue'].sum(),
            'active_revenue': df[~df['is_churned']]['total_revenue'].sum()
        }
        
        logger.info(f"   Churn Rate: {churn_metrics['churn_rate']*100:.2f}%")
        logger.info(f"   Retention Rate: {churn_metrics['retention_rate']*100:.2f}%")
        logger.info(f"   Revenue from Churned Customers: ₹{churn_metrics['churned_revenue_impact']:,.0f}")
        
        # Analyze churn drivers
        churn_drivers = {}
        
        # By Loyalty Tier
        churn_by_tier = df.groupby('loyalty_tier').agg({
            'is_churned': ['sum', 'mean'],
            'total_revenue': 'sum',
            'customer_id': 'count'
        }).round(4)
        churn_drivers['by_loyalty_tier'] = churn_by_tier
        
        # By Primary Category
        churn_by_category = df.groupby('primary_category').agg({
            'is_churned': ['sum', 'mean'],
            'total_revenue': 'sum',
            'customer_id': 'count'
        }).round(4)
        churn_drivers['by_category'] = churn_by_category
        
        # By Purchase Frequency
        df['freq_bucket'] = pd.cut(df['purchase_frequency'], bins=[0, 1, 5, 10, np.inf], 
                                    labels=['Very Low', 'Low', 'Medium', 'High'])
        churn_by_freq = df.groupby('freq_bucket').agg({
            'is_churned': ['sum', 'mean'],
            'total_revenue': 'sum',
            'customer_id': 'count'
        }).round(4)
        churn_drivers['by_purchase_frequency'] = churn_by_freq
        
        # By Premium Status
        df['premium_status'] = df['premium_purchase_ratio'].apply(lambda x: 'Premium' if x > 0.5 else 'Regular')
        churn_by_premium = df.groupby('premium_status').agg({
            'is_churned': ['sum', 'mean'],
            'total_revenue': 'sum',
            'customer_id': 'count'
        }).round(4)
        churn_drivers['by_premium_status'] = churn_by_premium
        
        self.churn_drivers = churn_drivers
        logger.info(f"✅ Churn analysis complete")
        
        return churn_metrics, churn_drivers
    
    # ============= PHASE 5: CHURN RISK SCORING =============
    
    def calculate_churn_risk_score(self) -> pd.DataFrame:
        """Build predictive churn risk score (0-100)"""
        logger.info("\n🎲 PHASE 5: CHURN RISK SCORING")
        
        df = self.customer_metrics.copy()
        
        # Initialize score
        risk_score = pd.DataFrame({'customer_id': df['customer_id'], 'risk_score': 0.0})
        
        # Factor 1: Recency (most important - 40 points)
        recency_max = df['recency'].quantile(0.95)
        risk_score['recency_factor'] = (df['recency'] / recency_max * 40).clip(0, 40)
        
        # Factor 2: Purchase Frequency Decline (25 points)
        risk_score['frequency_factor'] = (1 - (df['purchase_frequency'] / df['purchase_frequency'].quantile(0.90))) * 25
        risk_score['frequency_factor'] = risk_score['frequency_factor'].clip(0, 25)
        
        # Factor 3: Revenue Contribution (15 points)
        revenue_threshold = df['total_revenue'].quantile(0.75)
        risk_score['revenue_factor'] = ((1 - df['total_revenue'] / revenue_threshold) * 15).clip(0, 15)
        
        # Factor 4: Loyalty Tier (10 points)
        tier_risk = {'Bronze': 8, 'Silver': 5, 'Gold': 3, 'Platinum': 1}
        risk_score['tier_factor'] = df['loyalty_tier'].map(tier_risk).fillna(5)
        
        # Factor 5: Days Since Last Purchase (10 points)
        risk_score['activity_factor'] = (df['days_since_last_purchase'] / 180 * 10).clip(0, 10)
        
        # Combine factors
        risk_score['risk_score'] = (
            risk_score['recency_factor'] + 
            risk_score['frequency_factor'] + 
            risk_score['revenue_factor'] + 
            risk_score['tier_factor'] + 
            risk_score['activity_factor']
        ).clip(0, 100)
        
        # Risk categories
        def categorize_risk(score):
            if score <= 25:
                return 'Safe'
            elif score <= 50:
                return 'Monitor'
            elif score <= 75:
                return 'High Risk'
            else:
                return 'Critical'
        
        risk_score['risk_category'] = risk_score['risk_score'].apply(categorize_risk)
        
        # Merge with metrics
        df = df.merge(risk_score[['customer_id', 'risk_score', 'risk_category']], on='customer_id')
        self.customer_metrics = df
        
        logger.info(f"✅ Churn risk scores calculated")
        logger.info(f"\nRisk Distribution:")
        for cat in ['Safe', 'Monitor', 'High Risk', 'Critical']:
            count = (df['risk_category'] == cat).sum()
            pct = count / len(df) * 100
            logger.info(f"   {cat:<15}: {count:>7,} customers ({pct:>5.1f}%)")
        
        return df
    
    # ============= PHASE 6: EXECUTIVE INSIGHTS =============
    
    def generate_executive_insights(self) -> Dict[str, Any]:
        """Generate 6 key strategic questions answered"""
        logger.info("\n💡 PHASE 6: EXECUTIVE INSIGHTS")
        
        df = self.customer_metrics.copy()
        
        insights = {}
        
        # Q1: What behaviours distinguish loyal customers?
        loyal = df[df['segment'].isin(['Champions', 'Loyal Customers'])]
        insights['loyal_behaviors'] = {
            'avg_purchase_frequency': float(loyal['purchase_frequency'].mean()),
            'avg_order_value': float(loyal['avg_order_value'].mean()),
            'premium_purchase_ratio': float(loyal['premium_purchase_ratio'].mean()),
            'avg_days_since_purchase': float(loyal['days_since_last_purchase'].mean()),
            'most_common_tier': loyal['loyalty_tier'].mode()[0] if len(loyal['loyalty_tier'].mode()) > 0 else 'Bronze'
        }
        
        # Q2: What behaviours distinguish churned customers?
        if 'is_churned' in df.columns:
            churned = df[df['is_churned']]
        else:
            churned = df[df['days_since_last_purchase'] > 180]
        
        insights['churned_behaviors'] = {
            'avg_purchase_frequency': float(churned['purchase_frequency'].mean()),
            'avg_order_value': float(churned['avg_order_value'].mean()),
            'avg_days_since_purchase': float(churned['days_since_last_purchase'].mean()),
            'most_common_tier': churned['loyalty_tier'].mode()[0] if len(churned['loyalty_tier'].mode()) > 0 else 'Bronze'
        }
        
        # Q3: Segment revenue contribution
        segment_value = df.groupby('segment').agg({
            'total_revenue': 'sum',
            'customer_id': 'count',
            'avg_order_value': 'mean'
        }).to_dict()
        insights['segment_contribution'] = {k: {kk: float(vv) for kk, vv in v.items()} 
                                             for k, v in segment_value.items()}
        
        # Q4: Risk score impact on revenue
        high_risk = df[df['risk_score'] > 50]
        insights['at_risk_revenue'] = {
            'count': int(high_risk['customer_id'].count()),
            'total_revenue': float(high_risk['total_revenue'].sum()),
            'avg_ltv': float(high_risk['clv_proxy'].mean()),
            'revenue_at_stake': float(high_risk['total_revenue'].sum() * 0.3)  # Assume 30% could be saved
        }
        
        # Q5: Tier retention rates
        tier_retention_raw = df.groupby('loyalty_tier')['is_churned'].apply(lambda x: 1 - (x.sum() / len(x)) if len(x) > 0 else 0)
        insights['tier_retention'] = {str(k): float(v) for k, v in tier_retention_raw.items()}
        
        # Q6: Top risk factors
        high_risk_customers = df[df['risk_score'] > 50]
        low_risk_customers = df[df['risk_score'] <= 25]
        
        insights['key_differentiators'] = {
            'recency_days': {
                'high_risk': float(high_risk_customers['days_since_last_purchase'].mean()),
                'low_risk': float(low_risk_customers['days_since_last_purchase'].mean())
            },
            'purchase_frequency': {
                'high_risk': float(high_risk_customers['purchase_frequency'].mean()),
                'low_risk': float(low_risk_customers['purchase_frequency'].mean())
            },
            'order_value': {
                'high_risk': float(high_risk_customers['avg_order_value'].mean()),
                'low_risk': float(low_risk_customers['avg_order_value'].mean())
            }
        }
        
        self.insights = insights
        logger.info(f"✅ Executive insights generated")
        return insights
    
    # ============= BONUS: BUSINESS IMPACT =============
    
    def calculate_business_impact(self) -> Dict[str, Any]:
        """Calculate revenue impact of retention improvements"""
        logger.info("\n💰 BUSINESS IMPACT ANALYSIS")
        
        df = self.customer_metrics.copy()
        high_value_customers = df[df['clv_proxy'] > df['clv_proxy'].quantile(0.75)]
        
        # Scenario: Reduce churn among high-value by 10%
        current_churn_high_value = high_value_customers['is_churned'].sum()
        potential_saved = int(current_churn_high_value * 0.10)
        avg_clv_high_value = high_value_customers[~high_value_customers['is_churned']]['clv_proxy'].mean()
        
        revenue_impact = {
            'high_value_customer_count': len(high_value_customers),
            'current_churn_count': int(current_churn_high_value),
            'customers_saveable_10pct_reduction': potential_saved,
            'avg_clv_per_customer': float(avg_clv_high_value),
            'annual_revenue_retained': float(potential_saved * avg_clv_high_value),
            'all_customers_revenue': float(df['total_revenue'].sum()),
            'revenue_at_risk_total': float(df[df['risk_score'] > 50]['total_revenue'].sum())
        }
        
        logger.info(f"   Annual Revenue Potentially Retained: ₹{revenue_impact['annual_revenue_retained']:,.0f}")
        logger.info(f"   Total Revenue at Risk: ₹{revenue_impact['revenue_at_risk_total']:,.0f}")
        
        return revenue_impact
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        logger.info("\n📄 GENERATING COMPREHENSIVE REPORT\n")
        logger.info("="*80)
        
        # Run all phases
        data_audit = self.load_and_audit_data()
        self.build_customer_metrics()
        self.calculate_rfm()
        churn_metrics, churn_drivers = self.analyze_churn()
        self.calculate_churn_risk_score()
        executive_insights = self.generate_executive_insights()
        business_impact = self.calculate_business_impact()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_audit': data_audit,
            'churn_metrics': churn_metrics,
            'executive_insights': executive_insights,
            'business_impact': business_impact,
            'customer_metrics': self.customer_metrics,
            'assumptions': self.assumptions
        }
        
        logger.info("="*80)
        logger.info("✅ COMPREHENSIVE RETENTION ANALYTICS REPORT GENERATED")
        return report


def main():
    """Run analytics pipeline"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, 'cleaned_sales_insights.csv')
    
    analytics = RetentionAnalytics(data_path)
    report = analytics.generate_report()
    
    # Save report
    report_path = os.path.join(BASE_DIR, 'retention_report.json')
    with open(report_path, 'w') as f:
        # Handle non-serializable objects
        report_copy = report.copy()
        report_copy.pop('customer_metrics', None)
        json.dump(report_copy, f, indent=2, default=str)
    
    # Save customer metrics
    customer_metrics_path = os.path.join(BASE_DIR, 'customer_metrics.csv')
    report['customer_metrics'].to_csv(customer_metrics_path, index=False)
    
    logger.info(f"\n📊 Report saved to: {report_path}")
    logger.info(f"📊 Customer metrics saved to: {customer_metrics_path}")
    
    return analytics, report


if __name__ == "__main__":
    analytics, report = main()
