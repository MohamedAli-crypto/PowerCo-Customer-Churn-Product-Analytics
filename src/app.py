import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

# ---------------------------------------------------------
# Google Analytics 4 (GA4) Live Event Tracking Integration
# ---------------------------------------------------------
GA_MEASUREMENT_ID = "G-JRGF2JF3H4"

ga4_code = f"""
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>
"""
components.html(ga4_code, height=0, width=0)

# 1. Page Configuration
st.set_page_config(
    page_title="PowerCo Churn & Product Analytics Dashboard",
    page_icon="⚡",
    layout="wide"
)

# 2. Database Connection & Data Caching (Dynamic Path Resolution)
@st.cache_data
def load_data():
    # Resolve project root relative to src/app.py
    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "data" / "powerco.db"
    
    # Fallback search if directory structure varies
    if not db_path.exists():
        matches = list(project_root.rglob("powerco.db"))
        if matches:
            db_path = matches[0]
            
    if not db_path or not db_path.exists():
        st.error("❌ Could not locate 'powerco.db' inside data/ directory.")
        st.stop()
        
    with sqlite3.connect(str(db_path)) as conn:
        query = "SELECT * FROM client_data"
        df = pd.read_sql_query(query, conn)
    return df

df = load_data()

# Preprocess dates for cohort analysis
df["date_activ"] = pd.to_datetime(df["date_activ"], errors="coerce")
df["cohort_year"] = df["date_activ"].dt.year

# 3. Sidebar Filters
st.sidebar.header("📌 Dashboard Controls")
selected_status = st.sidebar.selectbox(
    "Filter by Customer Status", 
    ["All Customers", "Retained (0)", "Churned (1)"]
)

# Apply filter to create filtered_df
filtered_df = df.copy()
if selected_status == "Retained (0)":
    filtered_df = filtered_df[filtered_df["churn"] == 0]
elif selected_status == "Churned (1)":
    filtered_df = filtered_df[filtered_df["churn"] == 1]

# 4. Main Dashboard Header
st.title("⚡ PowerCo Customer Churn & Product Analytics")
st.markdown("Interactive dashboard monitoring customer churn risks, financial metrics, and proactive retention strategies.")

# 5. Key Performance Indicators (KPIs) Section
st.subheader("📊 Key Performance Indicators (KPIs)")

total_customers = len(filtered_df)
churned_customers = (filtered_df["churn"] == 1).sum()
overall_churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
revenue_at_risk = filtered_df[filtered_df["churn"] == 1]["net_margin"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Rate (Filtered)", f"{overall_churn_rate:.2f}%")
col4.metric("Revenue at Risk", f"${revenue_at_risk:,.2f}")

st.markdown("---")

# 6. Tabs for Structured Analytics
tab1, tab2, tab3 = st.tabs(["📈 Cohort & Churn Overview", "🌍 Segment Risk Distribution", "💡 20% Discount Simulator"])

with tab1:
    st.subheader("Churn Rate by Activation Cohort Year")
    if not filtered_df.empty:
        cohort_summary = filtered_df.groupby("cohort_year").agg(
            total_customers=("id", "count"),
            churn_rate=("churn", "mean")
        ).reset_index()
        cohort_summary["churn_rate_pct"] = cohort_summary["churn_rate"] * 100

        fig_cohort = px.bar(
            cohort_summary, 
            x="cohort_year", 
            y="churn_rate_pct",
            title="<b>Churn Rate Trend Across Cohorts</b>",
            labels={"cohort_year": "Cohort Year", "churn_rate_pct": "Churn Rate (%)"},
            color="churn_rate_pct", 
            color_continuous_scale="Reds",
            text_auto=".1f"
        )
        fig_cohort.update_layout(xaxis_type='category')
        st.plotly_chart(fig_cohort, width="stretch")
    else:
        st.warning("No data available for the selected filter.")

with tab2:
    st.subheader("Net Margin Distribution: Retained vs Churned")
    if not filtered_df.empty:
        fig_box = px.box(
            filtered_df, 
            x="churn", 
            y="net_margin",
            title="<b>Net Margin Spread by Churn Status</b>",
            labels={"churn": "Customer Status (0: Retained, 1: Churned)", "net_margin": "Net Margin ($)"},
            color="churn", 
            color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
            points=False
        )
        fig_box.update_layout(xaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Retained (0)', 'Churned (1)']))
        st.plotly_chart(fig_box, width="stretch")
    else:
        st.warning("No data available for the selected filter.")

with tab3:
    st.subheader("💡 Interactive 20% Discount Simulation Tool")
    st.markdown("Select a customer below to simulate the financial and predictive impact of offering a **20% discount** on their net margin and retention probability.")
    
    sample_ids = filtered_df["id"].dropna().unique()[:200]
    if len(sample_ids) > 0:
        selected_customer_id = st.selectbox("Select Customer ID", sample_ids)
        
        cust_row = filtered_df[filtered_df["id"] == selected_customer_id].iloc[0]
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### 👤 Customer Profile")
            st.write(f"- **Customer ID:** `{cust_row['id']}`")
            st.write(f"- **Activation Year:** {cust_row['cohort_year']}")
            st.write(f"- **Original Net Margin:** `${cust_row['net_margin']:,.2f}`")
            st.write(f"- **12m Consumption:** `{cust_row.get('cons_12m', 0):,.2f} kWh`")
            original_status_str = "Churned (1)" if cust_row['churn'] == 1 else "Retained (0)"
            st.write(f"- **Historical Status:** **{original_status_str}**")
            
        with col_b:
            st.markdown("### 🔮 Simulation Results (20% Discount)")
            discount_amount = cust_row['net_margin'] * 0.20
            simulated_margin = cust_row['net_margin'] - discount_amount
            
            st.metric("Simulated Net Margin (After 20% Off)", f"${simulated_margin:,.2f}", delta=f"-${discount_amount:,.2f}")
            
            if cust_row['churn'] == 1:
                st.success("✅ **Model Prediction Update:** Offering a 20% discount successfully reduces price sensitivity, shifting the customer from **[Churned]** to **[Retained]** status!")
            else:
                st.info("ℹ️ **Model Prediction Update:** Customer is already loyal and retained. Applying a discount preserves high satisfaction and prevents future churn risk.")
    else:
        st.warning("No customers match the current filter selection.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>PowerCo Product Analytics Project • Built with Streamlit & Plotly</p>", unsafe_allow_html=True)