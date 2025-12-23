import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import psycopg2
from sqlalchemy import create_engine
import numpy as np
import altair as alt


st.set_page_config(layout="wide")

st.title("📈50 Stock Performance Dashboard")

st.image(
    "C:/Users/Karthika/Downloads/OIP.webp",
    width=800
)

engine = create_engine(
    "postgresql+psycopg2://postgres:Yeira23@localhost:5432/Stock_analysis"
)

#Market Summary

query = "SELECT * FROM public.market_summary"
df = pd.read_sql(query, engine)

st.subheader("📊 Market Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🟢 Green Stocks", 44)
col2.metric("🔴 Red Stocks", 6)
col3.metric("💰 Average Price", "2293.87")
col4.metric("📊 Avg Volume", "6833474")

#Top 10 Most Volatile Stocks
st.subheader("⚡ Top 10 Most Volatile Stocks")

query = "SELECT * FROM top_10_volatility"
df = pd.read_sql(query, engine)
st.dataframe(df, use_container_width=True)

fig_vol = px.bar(
    df,
    x="Ticker",
    y="Std_Dev",
    title="Top 10 Volatile Stocks"
)

st.plotly_chart(fig_vol, use_container_width=True)

#Cumulative Return Over Time

st.subheader("📈 Cumulative Return - Top 5 Performing Stocks")

query = "SELECT * FROM top_5_cumlative"
df = pd.read_sql(query, engine)
st.dataframe(df, use_container_width=True)

query ="SELECT * FROM plot_df"
df = pd.read_sql(query, engine)

st.subheader("Stock Price Change: 2023 → 2024")
plot_df = df

chart = alt.Chart(plot_df).mark_line(point=True).encode(
    x='Year:N',
    y='Price:Q',
    color='Ticker:N',
    tooltip=['Ticker', 'Year', 'Price']
).interactive()

st.altair_chart(chart, use_container_width=True)




#Sector-wise Performance
st.subheader("🏭 Sector-wise Average Return")

query = "SELECT * FROM sector_stock_df"
df = pd.read_sql(query, engine)

st.dataframe(df, use_container_width=True)

fig_sector = px.bar(
    df,                   
    x="sector",
    y="Return_%",
    title="Average Yearly Return by Sector"
)

st.plotly_chart(fig_sector, use_container_width=True)

#Stock Price Correlation

st.subheader("Stock Correlation")

query = "SELECT * FROM heatmap_df"
df = pd.read_sql(query, engine)
st.dataframe(df, use_container_width=True)

fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(df, cmap="coolwarm", center=0, ax=ax)
st.pyplot(fig)


st.subheader("📊 Monthly Top 5 Gainers & Losers")

query = "SELECT * FROM top_5_gainers"
df = pd.read_sql(query, engine)



df["month_str"] = pd.to_datetime(df["month"]).dt.strftime("%B %Y")

months = df["month_str"].unique().tolist()


tabs = st.tabs(months)

for tab, month in zip(tabs, months):
    with tab:
        st.subheader(f"📊 {month}")

        month_df = df[df["month_str"] == month]


        st.dataframe(
            month_df,
            use_container_width=True
        )


fig_sector = px.bar(
    data_frame=df,
    x='month',  
    y='monthly_return',
    color='Ticker',
    title='Monthly Returns by Stock'
)

st.plotly_chart(fig_sector, use_container_width=True)

query = "SELECT * FROM top_5_losers"
df = pd.read_sql(query, engine)


df["month_str"] = pd.to_datetime(df["month"]).dt.strftime("%B %Y")

months = df["month_str"].unique().tolist()


tabs = st.tabs(months)

for tab, month in zip(tabs, months):
    with tab:
        st.subheader(f"📊 {month}")

        month_df = df[df["month_str"] == month]


        st.dataframe(
            month_df,
            use_container_width=True
        )

fig_sector = px.bar(
    df,                   
    x="month",
    y="monthly_return",
    color='Ticker',
    title="bottom_5_monthly"
)

st.plotly_chart(fig_sector, use_container_width=True)


































