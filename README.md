Croma Executive Performance & Commercial Optimization Portal

A production-grade analytics dashboard built with Streamlit for sales performance analysis, revenue diagnostics, customer retention insights, and operational monitoring.

Project Overview

The dashboard provides interactive analysis across three core business areas:

Merchandise Performance
Revenue contribution by product category
Premium vs. regular product analysis
Product performance comparison
Customer Loyalty & Retention
Customer segmentation by loyalty tier
Revenue concentration analysis
Retention and churn insights
Data Quality & Governance
Data validation monitoring
Anomaly detection
Operational quality reporting
System Requirements
Python 3.8+
Windows, macOS, or Linux
Minimum 500 MB disk space
Recommended 2 GB RAM
Setup and Execution
Install Dependencies
pip install -r requirements.txt
Required Data Files

Place the following files in the project directory:

campaigns.csv
customers.csv
products.csv
transactions.csv
Run Data Processing Pipeline
python eda_pipeline.py

Output:

cleaned_sales_insights.csv

The pipeline performs:

Data validation
Data cleaning
Anomaly detection
Data enrichment
Metric generation
Business insight creation
Launch Dashboard
streamlit run app.py

Default URL:

http://localhost:8501
Project Structure
croma_internship/
│
├── app.py
├── eda_pipeline.py
├── requirements.txt
├── README.md
├── cleaned_sales_insights.csv
├── croma_dashboard.log
├── eda_pipeline.log
│
├── campaigns.csv
├── customers.csv
├── products.csv
└── transactions.csv
Dashboard Features
Key Performance Indicators
Gross Revenue
Total Orders
Average Order Value (AOV)
Premium Mix Percentage
Interactive Filters
Product Category
Loyalty Tier

All visualizations update dynamically based on selected filters.

Analysis Modules
Merchandise Analysis
Category revenue distribution
Premium vs. regular product performance
Cross-selling opportunity identification
Loyalty & Retention Analysis
Revenue contribution by loyalty tier
Customer concentration analysis
Retention recommendations
Data Quality Monitoring
Data validation metrics
Clean vs. corrupted records
Quality event tracking
Data Processing Workflow
Data Validation
Load source files
Verify required columns
Validate data types
Standardize date formats
Data Cleaning
Detect anomalies
Missing Product IDs
Missing Revenue Values
Negative Revenue
Invalid Quantities
Isolate corrupted records
Retain clean records
Data Enrichment
Merge transaction and product data
Merge customer information
Calculate net revenue
Generate derived attributes
Analytics Generation
Product category ranking
Loyalty tier contribution analysis
Premium product performance evaluation
Executive insight generation
Executive Analysis Report

The dashboard includes a dedicated Executive Report module providing strategic recommendations for customer retention and revenue growth.

Report Highlights
Key Insights
74% of customers fall into churn-risk or inactive segments
Retention challenges are concentrated in Bronze-tier customers
Loyal customers generate significantly higher revenue
Purchase frequency strongly predicts retention
Customer retention provides higher ROI than acquisition
Estimated annual revenue opportunity: ₹2.5 Million
Strategic Recommendations
Short-Term (0–30 Days)
Win-back campaigns
Bronze-tier retention offers
Second-purchase incentives

Estimated Impact:

₹176,000 Revenue Recovery
Medium-Term (1–3 Months)
Loyalty tier optimization
Predictive customer monitoring
Segment-specific engagement programs

Expected ROI:

2.8x – 4.2x
Long-Term (3+ Months)
Predictive churn modeling
Customer lifetime value optimization
Lifecycle management framework

Estimated Annual Benefit:

₹2.49 Million
Business Metrics Tracked
Revenue Metrics
Gross Revenue
Net Revenue
Average Order Value
Revenue by Category
Revenue by Loyalty Tier
Customer Metrics
Transaction Count
Customer Count
Premium Mix Percentage
Loyalty Distribution
Data Quality Metrics
Clean Record Percentage
Anomaly Detection Rate
Data Quality Score
Troubleshooting
Data File Not Found

Run:

python eda_pipeline.py

before launching the dashboard.

Missing CSV Files

Ensure all required input files are present in the project directory.

Empty Dashboard Results

Adjust filters or select "All" categories.

View Logs
tail -f croma_dashboard.log
tail -f eda_pipeline.log
Production Readiness
Error handling implemented
Logging configured
Data validation integrated
Performance optimization applied
Type hints included
Documentation completed
Audit logging enabled
User-friendly error reporting provided
Deployment
Local Deployment
streamlit run app.py
Streamlit Cloud
Push project to GitHub
Connect repository to Streamlit Cloud
Deploy application
Docker
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
Technology Stack
Streamlit
Pandas
NumPy
Plotly
License

Internship Project – Croma Analytics.
