# app/streamlit_app.py

import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

sys.path.append(os.path.abspath("."))

st.set_page_config(
    page_title="Retail Sales Forecasting Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Retail Sales Forecasting & Inventory Optimization Dashboard")
st.markdown("Interactive dashboard for sales trends, forecasting metrics, and inventory alerts.")

# File paths
sales_file = "data/retail_sales_clean.csv"
inventory_file = "outputs/reports/inventory_optimization_report.csv"
metrics_file = "outputs/reports/model_metrics.csv"

# Check if required files exist
missing_files = []
for f in [sales_file, inventory_file, metrics_file]:
    if not os.path.exists(f):
        missing_files.append(f)

if missing_files:
    st.error("Some required files are missing. Run `python main.py` first.")
    st.write("Missing files:")
    for f in missing_files:
        st.write("-", f)
    st.stop()

# Load data
df = pd.read_csv(sales_file, parse_dates=["date"])
inv = pd.read_csv(inventory_file)
metrics = pd.read_csv(metrics_file, index_col=0)

# Sidebar filters
st.sidebar.header("Filters")
selected_store = st.sidebar.selectbox("Select Store", ["All"] + sorted(df["store"].unique().tolist()))
selected_category = st.sidebar.selectbox("Select Category", ["All"] + sorted(df["category"].unique().tolist()))

filtered_df = df.copy()

if selected_store != "All":
    filtered_df = filtered_df[filtered_df["store"] == selected_store]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

# KPIs
total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["units_sold"].sum()
avg_daily_revenue = filtered_df.groupby("date")["revenue"].sum().mean()
reorder_count = (inv["alert"].astype(str).str.contains("REORDER")).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Units Sold", f"{total_units:,}")
col3.metric("Avg Daily Revenue", f"₹{avg_daily_revenue:,.0f}")
col4.metric("Products to Reorder", int(reorder_count))

st.markdown("---")

# Monthly sales trend
st.subheader("Monthly Revenue Trend")
monthly = (
    filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["revenue"]
    .sum()
    .reset_index()
)
monthly["date"] = monthly["date"].astype(str)

fig1 = px.line(
    monthly,
    x="date",
    y="revenue",
    markers=True,
    title="Monthly Revenue Trend"
)
st.plotly_chart(fig1, use_container_width=True)

# Category-wise revenue
st.subheader("Category-wise Revenue")
cat_rev = (
    filtered_df.groupby("category")["revenue"]
    .sum()
    .reset_index()
    .sort_values("revenue", ascending=False)
)

fig2 = px.bar(
    cat_rev,
    x="category",
    y="revenue",
    color="category",
    title="Category Revenue"
)
st.plotly_chart(fig2, use_container_width=True)

# Store-wise revenue
st.subheader("Store-wise Revenue")
store_rev = (
    filtered_df.groupby("store")["revenue"]
    .sum()
    .reset_index()
    .sort_values("revenue", ascending=False)
)

fig3 = px.bar(
    store_rev,
    x="store",
    y="revenue",
    color="store",
    title="Store Revenue"
)
st.plotly_chart(fig3, use_container_width=True)

# Model metrics
st.subheader("Forecast Model Performance")
st.dataframe(metrics)

# Inventory alerts
st.subheader("Inventory Reorder Alerts")
reorder_df = inv[inv["alert"].astype(str).str.contains("REORDER")]

if reorder_df.empty:
    st.success("No immediate reorder alerts found.")
else:
    st.dataframe(
        reorder_df[[
            "store", "category", "product",
            "avg_daily_demand", "safety_stock",
            "reorder_point", "eoq", "days_of_stock", "alert"
        ]],
        use_container_width=True
    )

st.markdown("---")
st.caption("Built with Python, Pandas, Plotly, and Streamlit")