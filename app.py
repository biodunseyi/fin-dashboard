import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# App layout
st.set_page_config(page_title="FinSight Pro", layout="wide")
st.title("📊 FinSight Pro - Real-Time Investment Dashboard")
st.subheader("Welcome to the future of portfolio intelligence.")
st.markdown("<div style='text-align: center; color: grey; font-size: 16px;'>Created by <b>ABIODUN ADEBAYO</b></div>", unsafe_allow_html=True)

# Suggested stock symbols
popular_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BABA", "INTC",
    "AMD", "SHOP", "BA", "DIS", "JPM", "V", "MA", "WMT", "T", "XOM", "PFE", "NKE"
]

# Stock selection
stock = st.selectbox(
    "🔎 Start typing or choose a stock symbol:",
    options=popular_tickers,
    index=None,
    placeholder="e.g., AAPL, TSLA, NVDA"
)

# Optional fallback input
if not stock:
    stock = st.text_input("Or enter a stock symbol manually:", "").upper()

# Fetch and display stock data
if stock:
    try:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="6mo")

        st.subheader(f"📈 Stock Price for {stock}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="Close"))
        fig.update_layout(title=f"{stock} Stock Price (Last 6 Months)", xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Company Info")
        info = ticker.info
        st.write({
            "Name": info.get("shortName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Website": info.get("website", "N/A"),
        })

    except Exception as e:
        st.error(f"⚠️ Could not fetch data for '{stock}'. Make sure it's a valid ticker symbol.")
