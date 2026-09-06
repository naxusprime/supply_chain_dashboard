# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from engine import load_processed_data, get_summary_metrics

st.set_page_config(page_title="Supply Chain Cost & Bottleneck Dashboard", layout="wide")

@st.cache_data
def fetch_data():
    return load_processed_data()

df, wh_caps = fetch_data()
metrics = get_summary_metrics(df, wh_caps)

st.title("Supply Chain Network & Route Cost Analytics")

# Top KPI Metric Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Supply Chain Cost", f"${metrics['total_cost']:,.2f}")
kpi2.metric("Warehouse Cost", f"${metrics['total_wh_cost']:,.2f}")
kpi3.metric("Freight Cost", f"${metrics['total_freight_cost']:,.2f}")
kpi4.metric("Total Order Volume", f"{metrics['total_units']:,} units")

st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_plant = st.sidebar.multiselect("Select Plant Code", df['Plant Code'].unique(), default=df['Plant Code'].unique())
selected_carrier = st.sidebar.multiselect("Select Carrier", df['Carrier'].unique(), default=df['Carrier'].unique())

filtered_df = df[(df['Plant Code'].isin(selected_plant)) & (df['Carrier'].isin(selected_carrier))]

# Row 1: Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Order Volume Distribution by Plant")
    plant_counts = filtered_df.groupby('Plant Code')['Unit quantity'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=plant_counts, x='Plant Code', y='Unit quantity', ax=ax1, palette='Blues_r')
    ax1.set_ylabel("Total Units Processed")
    st.pyplot(fig1)

with col_right:
    st.subheader("Carrier Cost Share")
    carrier_costs = filtered_df.groupby('Carrier')['freight_cost'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(carrier_costs['freight_cost'], labels=carrier_costs['Carrier'], autopct='%1.1f%%', colors=sns.color_palette('Set2'))
    st.pyplot(fig2)

# Row 2: Plant Bottleneck Table
st.subheader("Plant Handling & Unit Cost Efficiency")
plant_summary = metrics['plant_summary']
st.dataframe(plant_summary[['Plant Code', 'total_orders', 'total_units', 'Daily Capacity', 'total_wh_cost', 'cost_per_unit']].style.format({
    'total_units': '{:,}',
    'Daily Capacity': '{:,}',
    'total_wh_cost': '${:,.2f}',
    'cost_per_unit': '${:,.4f}'
}), use_container_width=True)

# Row 3: Export Filtered Data
st.subheader("Export Shipment Report")
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Orders (CSV)", csv_data, "filtered_orders_report.csv", "text/csv")