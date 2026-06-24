import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Dashboard")

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv("retail_sales_cleaned.csv")

df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.header("Filters")

# Date Filter

start_date = st.sidebar.date_input(
    "Start Date",
    df['OrderDate'].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['OrderDate'].max().date()
)

# Region Filter

region = st.sidebar.multiselect(
    "Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category Filter

category = st.sidebar.multiselect(
    "Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# SubCategory Filter

subcategory = st.sidebar.multiselect(
    "SubCategory",
    options=df['SubCategory'].unique(),
    default=df['SubCategory'].unique()
)

# Segment Filter

segment = st.sidebar.multiselect(
    "Segment",
    options=df['Segment'].unique(),
    default=df['Segment'].unique()
)

# ======================================
# APPLY FILTERS
# ======================================

filtered_df = df[
    (df['OrderDate'].dt.date >= start_date) &
    (df['OrderDate'].dt.date <= end_date) &
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['SubCategory'].isin(subcategory)) &
    (df['Segment'].isin(segment))
]

# ======================================
# KPI CARDS
# ======================================

total_revenue = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['OrderID'].nunique()

aov = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"{total_revenue:,.0f}")
col2.metric("Profit", f"{total_profit:,.0f}")
col3.metric("AOV", f"{aov:,.0f}")
col4.metric("Orders", total_orders)

st.markdown("---")

# ======================================
# MONTHLY SALES TREND
# ======================================

filtered_df['YearMonth'] = (
    filtered_df['OrderDate']
    .dt.to_period('M')
    .astype(str)
)

monthly_sales = (
    filtered_df
    .groupby('YearMonth')['Sales']
    .sum()
    .reset_index()
)

# ======================================
# CATEGORY SALES
# ======================================

category_sales = (
    filtered_df
    .groupby('Category')['Sales']
    .sum()
    .reset_index()
)

# ======================================
# TOP CUSTOMERS
# ======================================

top_customers = (
    filtered_df
    .groupby('CustomerName')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# ======================================
# REGION SALES
# ======================================

region_sales = (
    filtered_df
    .groupby('Region')['Sales']
    .sum()
    .reset_index()
)

# ======================================
# 2 × 2 MATRIX LAYOUT
# ======================================

col1, col2 = st.columns(2)

with col1:

    fig1 = px.line(
        monthly_sales,
        x='YearMonth',
        y='Sales',
        markers=True,
        title='Monthly Sales Trend'
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    fig2 = px.bar(
        category_sales,
        x='Category',
        y='Sales',
        title='Sales by Category'
    )

    st.plotly_chart(fig2, use_container_width=True)

# ======================================

col3, col4 = st.columns(2)

with col3:

    fig3 = px.bar(
        top_customers,
        x='CustomerName',
        y='Sales',
        title='Top 10 Customers'
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:

    fig4 = px.bar(
        region_sales,
        x='Region',
        y='Sales',
        title='Sales by Region'
    )

    st.plotly_chart(fig4, use_container_width=True)

# ======================================
# SUBCATEGORY ANALYSIS
# ======================================

st.markdown("---")

subcategory_sales = (
    filtered_df
    .groupby('SubCategory')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    subcategory_sales,
    x='SubCategory',
    y='Sales',
    title='Top 10 SubCategories by Sales'
)

st.plotly_chart(fig5, use_container_width=True)

# ======================================
# DATA TABLE
# ======================================

st.markdown("---")

st.subheader("Filtered Data")

st.dataframe(filtered_df)