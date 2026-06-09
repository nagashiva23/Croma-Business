# Croma Executive Performance & Commercial Optimization Portal

A production-grade analytics dashboard built with Streamlit for Croma's sales performance analysis and revenue diagnostics.

## 🎯 Project Overview

This project provides an **interactive executive dashboard** that analyzes:
- **Merchandise Performance**: Revenue contribution by product category with premium/regular mix analysis
- **Loyalty & Retention**: Customer segmentation by loyalty tier with revenue concentration risk assessment
- **Data Quality**: Operational integrity monitoring and data governance reporting

## 📋 System Requirements

- **Python**: 3.8+
- **OS**: macOS, Linux, or Windows
- **Disk Space**: 500MB minimum
- **RAM**: 2GB recommended

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Data
Ensure the following CSV files are in the project directory:
- `campaigns.csv`
- `customers.csv`
- `products.csv`
- `transactions.csv`

### 3. Run Data Pipeline
```bash
python eda_pipeline.py
```

This generates `cleaned_sales_insights.csv` with:
- ✅ Data validation & cleaning
- ✅ Anomaly detection & isolation
- ✅ Dimension table merging
- ✅ Derived metric calculations
- ✅ Executive business insights

### 4. Launch Dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
croma_internship/
├── app.py                          # Streamlit web dashboard
├── eda_pipeline.py                 # Data processing & EDA pipeline
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── cleaned_sales_insights.csv      # Output: Processed dataset
├── croma_dashboard.log             # Dashboard execution logs
├── eda_pipeline.log                # Pipeline execution logs
└── [Input CSV files]
    ├── campaigns.csv
    ├── customers.csv
    ├── products.csv
    └── transactions.csv
```

## 🎛️ Dashboard Features

### 📊 Key Performance Indicators (KPIs)
- **Gross Revenue**: Total revenue from filtered transactions
- **Total Orders**: Count of unique transactions
- **Average Order Value**: Mean revenue per transaction
- **Premium Mix %**: Percentage of revenue from premium items

### 🔍 Interactive Filters
- **Product Category**: Filter by merchandise category
- **Loyalty Tier**: Filter by customer engagement level
- Real-time dashboard updates based on selections

### 📑 Analysis Tabs

#### 🎯 Merchandise Deep-Dive
- Category revenue distribution (bar chart)
- Premium vs regular inventory performance analysis
- Cross-selling opportunity identification

#### 💎 Loyalty & Retention Analysis
- Revenue mix by customer tier (pie chart)
- Customer concentration risk assessment
- Tier-graduation campaign recommendations

#### 🚨 Quality Control & Anomalies
- Data quality metrics and validation status
- Clean vs corrupted record counts
- Automated logging of data quality events

## 🔧 Advanced Features

### Error Handling & Logging
- **Comprehensive logging** to `croma_dashboard.log` and `eda_pipeline.log`
- **User-friendly error messages** for data issues
- **Graceful degradation** if data sources are unavailable

### Data Validation
- **Type coercion** with error tracking
- **Null value handling** in critical fields
- **Revenue anomaly detection** (negative values, missing IDs)
- **Data quality reporting** with audit trail

### Performance Optimization
- **Caching** of clean data loads
- **Vectorized operations** using pandas/numpy
- **Lazy evaluation** of computations
- **Efficient groupby aggregations**

## 📊 Data Processing Pipeline

### Input Validation
```
1. Load CSV files with error handling
2. Validate required columns exist
3. Check data types (numeric, datetime, categorical)
4. Standardize date formats
```

### Data Cleaning
```
1. Detect anomalies:
   - Missing product_id or gross_revenue
   - Negative revenue values
   - Invalid quantity values
2. Separate corrupted records for audit
3. Retain clean transactions for analysis
```

### Enrichment & Merging
```
1. Merge transactions with products table
2. Merge with customers table
3. Calculate net revenue (accounting for refunds)
4. Create derived metrics (month, year, tiers)
```

### Analytics
```
1. Category performance ranking
2. Loyalty tier contribution analysis
3. Premium vs regular comparative metrics
4. Executive insights generation
```

## 🎨 UI/UX Enhancements

- **Color-coded metrics** with contextual styling
- **Helpful tooltips** on dashboard elements
- **Consistent emoji usage** for visual hierarchy
- **Responsive layout** with adaptive columns
- **Professional formatting** for currency & percentages
- **Interactive visualizations** with Plotly charts

## � Executive Analysis Report

The dashboard now includes a comprehensive **Executive Report** feature that provides strategic insights and recommendations for customer retention and churn management.

### Features

#### 📊 Interactive Report Tab
Access the Executive Report directly from the main dashboard:
- **Tab**: `📄 Executive Report`
- **Location**: Alongside other dashboard analysis tabs
- **Quick Access**: Click the "📄 Executive Report" button in the top-right corner

#### 📥 PDF Download
- **Feature**: One-click download of the complete analysis report
- **Format**: Professional PDF document
- **Content**: Full internship case study presentation with findings and recommendations
- **File**: `croma analysis pdf.pdf`

#### 🔍 Key Findings Snapshot
The report displays critical insights in professional KPI cards:
- **74% Churn Profile**: Customer distribution among churn-risk and inactive segments
- **Bronze Tier Alert**: Retention challenges specific to lower-tier customers
- **Loyal Customer Value**: Revenue premium from retained customers
- **Frequency Indicator**: Purchase frequency as retention predictor
- **Strategic Focus**: ROI comparison (retention vs. acquisition)
- **Revenue Opportunity**: ₹2.5M annual impact potential

#### 🚀 Strategic Recommendations

**Quick Wins (0-30 Days)**
- Win-back email campaigns
- Bronze-tier retention offers
- Second-purchase incentives
- Expected impact: ₹176K recovery

**Medium-Term Programs (1-3 Months)**
- Loyalty tier optimization (2.8:1 ROI)
- Customer monitoring with predictive scoring (3.5:1 ROI)
- Segment-specific content delivery (4.2:1 ROI)

**Long-Term Framework (3+ Months)**
- Predictive churn modeling (₹831K annual benefit)
- Customer lifetime value optimization (₹998K annual benefit)
- Lifecycle management system (₹499K annual benefit)

### Business Impact

**Total 12-Month Revenue Impact: ₹2,495,069**

This represents potential annual revenue improvement through:
- Strategic customer retention programs
- Churn reduction initiatives
- Loyalty tier progression
- Premium customer focus

### Report Components

1. **Executive Summary**: Key metrics and churn drivers
2. **Segment Analysis**: 7 customer segments with retention profiles
3. **Risk Scoring**: 5-factor churn risk model (0-100 scale)
4. **Recommendations**: Actionable strategies with ROI estimates
5. **Methodology**: Transparent analytical framework
6. **Data Quality**: 87.25% clean records, 89,974 transactions analyzed

### Accessing the Report

1. **Open Dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to Report**
   - Click the `📄 Executive Report` tab
   - Or click the `📄 Executive Report` button in top-right corner

3. **Download PDF**
   - Click `📥 Download Executive Analysis Report`
   - PDF saves as `Croma_Executive_Analysis_Report.pdf`

### Professional Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Executive Styling**: Professional gradient backgrounds and color schemes
- **Interactive Elements**: Expandable sections for detailed recommendations
- **Clean Layout**: Information organized for easy scanning
- **Action-Oriented**: Clear calls-to-action for next steps

## �📈 Business Metrics

### Revenue Metrics
- Gross Revenue (₹)
- Net Revenue (after refunds)
- Average Order Value (AOV)
- Revenue by Category
- Revenue by Loyalty Tier

### Customer Metrics
- Transaction Count
- Unique Customer Count
- Premium Mix Percentage
- Loyalty Tier Distribution

### Quality Metrics
- Clean Record Percentage
- Anomaly Detection Rate
- Data Quality Score

## 🐛 Troubleshooting

### Dashboard won't load
**Issue**: "Data file not found"
**Solution**: Run `python eda_pipeline.py` first to generate `cleaned_sales_insights.csv`

### Pipeline errors
**Issue**: CSV files not found
**Solution**: Ensure all 4 CSV files (campaigns, customers, products, transactions) are in the same directory as the script

### No data appearing after filters
**Issue**: Filter selections resulting in 0 rows
**Solution**: Adjust filter selection or use "All" to show complete dataset

### Check logs
```bash
# View dashboard logs
tail -f croma_dashboard.log

# View pipeline logs
tail -f eda_pipeline.log
```

## 📋 Production Checklist

- ✅ Error handling & logging configured
- ✅ Data validation & quality checks implemented
- ✅ Professional UI/UX styling applied
- ✅ Performance optimization (caching, vectorization)
- ✅ Type hints for code clarity
- ✅ Comprehensive docstrings
- ✅ requirements.txt for dependency management
- ✅ Audit logging for compliance
- ✅ User-friendly error messages
- ✅ README documentation

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with automatic log monitoring

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 📞 Support

For issues or questions:
1. Check the log files (`*.log`)
2. Review error messages in dashboard
3. Verify data sources exist
4. Consult troubleshooting section

## 📝 License

Internship Project - Croma Analytics

## 🙏 Acknowledgments

Built with:
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computing
