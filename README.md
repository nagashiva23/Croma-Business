# Croma Customer Retention & Churn Analysis

## Overview

This project analyzes customer purchasing behavior to identify churn risks, understand loyalty patterns, and recommend retention strategies for Croma.

The objective was to determine what differentiates loyal customers from churn-risk customers and identify business actions that can improve customer retention.

---

## Business Problem

Customer retention is a key driver of long-term profitability.

This analysis focuses on:

* Identifying churn-risk customers
* Understanding loyalty tier performance
* Comparing active and inactive customer behavior
* Finding opportunities to improve repeat purchases
* Recommending actionable retention strategies

---

## Key Findings

### Customer Churn

* Approximately 74% of customers were classified as churn-risk or inactive.
* Only 26% remained active customers.

### Loyalty Tier Performance

* Bronze customers showed the highest churn tendency.
* Gold and Platinum customers demonstrated stronger retention.

### Customer Behaviour

* Loyal customers purchased more frequently.
* Purchase frequency was a stronger retention indicator than website activity.
* Churned customers continued browsing but purchased less often.

### Business Insight

Improving retention and repeat purchases offers a larger opportunity than increasing customer acquisition alone.

---

## Solution

The analysis included:

* Customer Retention Analysis
* Churn Risk Identification
* Loyalty Tier Analysis
* Customer Segmentation
* Revenue Contribution Analysis
* Executive Reporting Dashboard

---

## Dashboard Features

### Retention Analytics

* Active vs Churned Customers
* Customer Behaviour Metrics
* Revenue Contribution Analysis

### Loyalty Analysis

* Loyalty Tier Performance
* Customer Value Comparison
* Retention Trends

### Executive Report

* Downloadable PDF Report
* Key Findings Summary
* Strategic Recommendations
* Methodology Overview

---

## Technology Stack

### Languages & Tools

* Python
* Pandas
* NumPy
* Streamlit
* Plotly

### Analytics Techniques

* Customer Segmentation
* Retention Analysis
* Churn Detection
* Behaviour Analysis
* Revenue Analysis

---

## Project Structure

```text
Croma-Business/
│
├── app.py
├── retention_analytics.py
├── retention_dashboard.py
├── eda_pipeline.py
├── presentation_generator.py
│
├── campaigns.csv
├── customers.csv
├── products.csv
│
├── customer_metrics.csv
├── retention_report.json
├── executive_presentation.md
│
├── requirements.txt
└── README.md
```

---

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Methodology

### Data Preparation

* Data cleaning and validation
* Dataset integration
* Customer-level metric generation

### Analysis

* Retention analysis
* Loyalty tier comparison
* Customer behaviour analysis
* Churn-risk identification

### Assumptions

* Customers inactive for more than 180 days were considered churn-risk.
* Revenue was used as a proxy for customer value.
* Website activity was used as an engagement indicator.

---

## Strategic Recommendations

### Quick Wins

* Win-back campaigns
* Bronze-tier retention offers
* Second-purchase incentives

### Long-Term Initiatives

* Predictive churn modelling
* Customer lifetime value optimization
* Loyalty program enhancement

---

## Author

**Naga Shiva**

B.Tech Artificial Intelligence

Amrita Vishwa Vidyapeetham

