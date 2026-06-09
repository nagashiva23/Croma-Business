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

## 📈 Business Metrics

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
