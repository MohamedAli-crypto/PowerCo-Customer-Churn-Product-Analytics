# ⚡ PowerCo Customer Churn & Product Analytics

An end-to-end data product & retention analytics system built to analyze customer churn, simulate price sensitivity interventions, and map user behavior funnels for PowerCo.

## 🎯 Business Problem
PowerCo, a major gas and electricity utility, is facing a significant churn rate among its Small & Medium Enterprise (SME) customers. The prevailing hypothesis is that churn is driven by high price sensitivity. The business needs to identify at-risk customers and evaluate if offering a targeted 20% discount is a financially viable retention strategy.

## 💡 The Solution (Data Product)
Instead of a static analysis notebook, I built an end-to-end **Retention Analytics Dashboard**. 
* **Data Pipeline:** Engineered using SQLite and SQL Window Functions to extract historical churn metrics and calculate Revenue at Risk.
* **Prescriptive Analytics (The Simulator):** Developed an interactive 20% Discount Simulator. It empowers decision-makers to select at-risk customers and instantly calculate the **Cost of Retention vs. Cost of Churn**, ensuring discounts are only offered when the saved revenue outweighs the discount cost.
* **Behavioral Tracking:** Integrated Google Analytics 4 (GA4) directly into the Streamlit app to monitor user interactions and funnel drop-offs.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

---

## 📌 Executive Summary & Key Metrics

* **Overall Churn Rate:** `9.72%`
* **Total Revenue at Risk (Net Margin):** `$324,045.59`
* **Highest Risk Cohorts:** Activation years **2012 (12.3%)** and **2013 (15.3%)** exhibit the highest customer drop-offs.
* **Retention Window:** Primary churn risks occur between **Month 12 and Month 36**. Proactive retention offers must trigger around **Month 10**.

---

## 🛠️ Repository Architecture

```text
PowerCo-Customer-Churn-Product-Analytics/
│
├── data/                       # Database files (SQLite) & CSV Datasets
│   ├── powerco.db
│   └── client_data.csv
│
├── sql/                        # Analytical SQL Queries & Feature Engineering
│   └── 02_feature_engineering_window_functions.sql
│
├── notebooks/                  # EDA & Cohort Retention Analytics
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_cohort_retention_analysis.ipynb
│   └── 03_feature_engineering_and_modeling.ipynb
│
├── src/                        # Interactive Streamlit Web App
│   └── app.py
│
├── reports/                    # Visualizations & Funnel Reports
│   └── funnel_chart.html
│
├── build_sqlite_db.py          # Automatic Database Builder Script
├── requirements.txt            # Python Dependencies
└── README.md                   # Project Documentation

---

## 💡 Key Features & Dashboard Capabilities

1. **Real-Time KPIs:** Tracks overall retention, churn percentage, and at-risk revenue.
2. **Cohort & Segment Analysis:** Visual breakdown of churn trends across joining years and net margin spreads.
3. **20% Discount Simulator:** Interactive tool simulating price sensitivity interventions to test customer retention predictions.
4. **Funnel Analysis (GA4 Context):** Maps user journey drop-offs across web event steps.
5. **GA4 Event Tracking & Analytics:** Integrated Google Analytics 4 (`gtag.js`) event tracking snippet directly within the Streamlit interface for user session monitoring and funnel mapping.

---

## 🚀 How to Run the Project Locally

```bash
# 1. Clone the repository
git clone [https://github.com/MohamedAli-crypto/PowerCo-Customer-Churn-Product-Analytics.git](https://github.com/MohamedAli-crypto/PowerCo-Customer-Churn-Product-Analytics.git)
cd PowerCo-Customer-Churn-Product-Analytics

# 2. Build the SQLite Database
python build_sqlite_db.py

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Launch Streamlit Dashboard
streamlit run src/app.py
