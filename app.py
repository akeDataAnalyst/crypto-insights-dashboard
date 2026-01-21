import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly

# Page config

st.set_page_config(
    page_title="Crypto Insights Dashboard – Bitcoin & Ethereum",
    page_icon="📈",
    layout="wide"
)

# Title & description
st.title("Cryptocurrency Transactional Insights Dashboard")
st.markdown("""
**Bitcoin & Ethereum Analysis (2025–2026)**  
Data source: CoinGecko API + simulated transactional metrics  
Built for portfolio demonstration – Aklilu Abera
""")

# Load & cache data

@st.cache_data
def load_data():
    df = pd.read_csv("crypto_transactional_data_enriched.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

# Sidebar – Filters
st.sidebar.header("Filters")

selected_coins = st.sidebar.multiselect(
    "Select Coin(s)",
    options=df['coin'].unique(),
    default=df['coin'].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['timestamp'].min().date(), df['timestamp'].max().date()),
    min_value=df['timestamp'].min().date(),
    max_value=df['timestamp'].max().date()
)

filtered_df = df[
    (df['coin'].isin(selected_coins)) &
    (df['timestamp'].dt.date >= date_range[0]) &
    (df['timestamp'].dt.date <= date_range[1])
]

# KPIs – Top row

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_price = filtered_df['price'].mean()
    st.metric("Average Price (USD)", f"${avg_price:,.0f}")

with col2:
    avg_return = filtered_df['daily_return'].mean() * 100
    st.metric("Avg Daily Return (%)", f"{avg_return:.2f}%")

with col3:
    total_volume = filtered_df['volume'].sum()
    st.metric("Total Volume (USD)", f"${total_volume:,.0f}")

with col4:
    avg_volatility = filtered_df['volatility_14d'].mean()
    st.metric("Avg 14-day Volatility", f"{avg_volatility:.4f}")

# Tabs / Sections
tab1, tab2, tab3, tab4 = st.tabs([
    "Price & Volume Trends",
    "Volatility & Risk",
    "Transaction Proxy",
    "Price Forecast (Prophet)"
])

# Tab 1: Price & Volume Trends

with tab1:
    st.subheader("Price Trends")

    fig_price = px.line(
        filtered_df,
        x='timestamp',
        y='price',
        color='coin',
        title="Price Over Time",
        height=500
    )
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("Trading Volume vs Price")
    fig_vol_price = px.scatter(
        filtered_df,
        x='volume',
        y='price',
        color='coin',
        size='total_txn_value_usd',
        hover_data=['timestamp'],
        title="Volume vs Price (size = simulated txn value)",
        log_x=True
    )
    st.plotly_chart(fig_vol_price, use_container_width=True)

# Tab 2: Volatility & Risk
with tab2:
    st.subheader("14-Day Rolling Volatility")

    fig_vol = px.line(
        filtered_df,
        x='timestamp',
        y='volatility_14d',
        color='coin',
        title="Rolling Volatility Comparison",
        height=500
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    st.subheader("Daily Return Distribution")
    fig_hist = px.histogram(
        filtered_df,
        x='daily_return',
        color='coin',
        marginal="violin",
        title="Daily Return Distribution",
        barmode="overlay",
        opacity=0.7
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Tab 3: Transaction Proxy

with tab3:
    st.subheader("Simulated Daily Transaction Value (Fee Throughput Proxy)")

    fig_txn = px.line(
        filtered_df,
        x='timestamp',
        y='total_txn_value_usd',
        color='coin',
        title="Daily Transaction Value Over Time",
        height=500
    )
    st.plotly_chart(fig_txn, use_container_width=True)

    st.subheader("Top 10 Highest Transaction Days")
    top_txn = filtered_df.nlargest(10, 'total_txn_value_usd')[
        ['timestamp', 'coin', 'price', 'total_txn_value_usd', 'volume']
    ].sort_values('total_txn_value_usd', ascending=False)
    st.dataframe(top_txn.style.format({
        'price': '${:,.0f}',
        'total_txn_value_usd': '${:,.0f}',
        'volume': '{:,.0f}'
    }))

# Tab 4: Price Forecast
with tab4:
    st.subheader("Bitcoin Price Forecast – Next 30 Days")

    if st.button("Run Forecast (Prophet)"):
        with st.spinner("Training Prophet model..."):
            btc_df = filtered_df[filtered_df['coin'] == 'Bitcoin'][
                ['timestamp', 'price']
            ].rename(columns={'timestamp': 'ds', 'price': 'y'})

            m = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            m.fit(btc_df)

            future = m.make_future_dataframe(periods=30)
            forecast = m.predict(future)

            fig_forecast = plot_plotly(m, forecast)
            st.plotly_chart(fig_forecast, use_container_width=True)

            st.success("Forecast complete!")
            st.caption("Gray = historical, Blue = forecast, Shaded = uncertainty interval")

# Footer
st.markdown("---")
st.caption("Data period: 2025-01-14 to 2026-01-13 | Simulated transactional metrics | Built with Streamlit")
