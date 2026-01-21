# Cryptocurrency Transactional Data Analysis & Insights Dashboard  
**Bitcoin & Ethereum – 2025–2026**

End-to-end portfolio project demonstrating full data analytics workflow — from API ingestion to interactive dashboard.

## Live Demo

[![Streamlit App](https://img.shields.io/badge/Streamlit-Open%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://crypto-insights-dashboard-gzzwrbrp3enttzaqfhlrwq.streamlit.app/)

Click the badge above to launch the interactive dashboard!

**Features**: Coin filter · Date range · Price trends · Volatility charts · Prophet forecast · Top transaction days table

## Project Overview

Analyzed **one year** of daily Bitcoin and Ethereum data (Jan 14, 2025 – Jan 13, 2026):

- Fetched historical prices, volumes, market caps via **CoinGecko Demo API** (free tier, 365-day limit)
- Simulated realistic transactional metrics: transaction_count, avg_txn_fee_usd, total_txn_value_usd (proxy for daily fee throughput)
- Computed daily returns and 14-day rolling volatility
- Performed cleaning, EDA, MySQL SQL analysis, Prophet forecasting, and built an interactive Streamlit dashboard

**Total rows**: 732 (366 per coin)

## Key Findings & Results

- **Volatility**: Ethereum significantly more volatile (~1.8× Bitcoin)  
  - Daily return std: Bitcoin 2.16% | Ethereum 3.90%  
  - 14-day rolling volatility mean: Bitcoin 2.05% | Ethereum 3.71%

- **Returns**: Weak negative correlation between volume and daily return  
  - Bitcoin: -0.090 | Ethereum: -0.004

- **Risk Metrics**:  
  - Bitcoin: worst day -8.63%, best +9.60%, ~49.9% negative days  
  - Ethereum: worst day -14.66%, best +21.39%, ~49.0% negative days

- **Prophet Forecast (Bitcoin price – backtest last 30 days)**:  
  - MAE: $1,796.77  
  - RMSE: $2,334.93  
  - MAPE: **2.01%**  
  - 90-day outlook: gradual softening toward ~$63,900–$65,500 range (wide uncertainty bands)

- **Top transaction days** dominated by late 2025 spikes (simulated total_txn_value_usd up to ~$6.7M)

 ## Tech Stack

- **Language**: Python 3.12  
- **Data**: pandas, numpy  
- **Visualization**: matplotlib, seaborn, plotly  
- **Forecasting**: Prophet  
- **Database**: MySQL (local)  
- **Dashboard**: Streamlit  
- **API**: CoinGecko Demo API (free tier)                                       
