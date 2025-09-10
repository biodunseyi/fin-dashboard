import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

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

# Helper function to check internet connectivity
def check_connectivity():
    """Check if external APIs are accessible"""
    try:
        response = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/AAPL", timeout=5)
        return True
    except:
        return False

# Helper function to generate sample data
def generate_sample_data(symbol):
    """Generate realistic sample stock data for demo purposes"""
    # Create 6 months of sample data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate realistic price movement
    np.random.seed(hash(symbol) % 1000)  # Consistent data for same symbol
    base_price = 100 + (hash(symbol) % 200)  # Base price between 100-300
    returns = np.random.normal(0.001, 0.02, len(dates))  # Daily returns
    prices = [base_price]
    
    for ret in returns[1:]:
        new_price = prices[-1] * (1 + ret)
        prices.append(new_price)
    
    sample_data = pd.DataFrame({
        'Close': prices,
        'Open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
        'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'Volume': [1000000 + np.random.randint(0, 5000000) for _ in prices]
    }, index=dates)
    
    return sample_data

# Helper function to get sample company info
def get_sample_company_info(symbol):
    """Generate sample company information"""
    company_data = {
        "AAPL": {"shortName": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "marketCap": 3000000000000, "website": "https://www.apple.com"},
        "MSFT": {"shortName": "Microsoft Corporation", "sector": "Technology", "industry": "Software", "marketCap": 2800000000000, "website": "https://www.microsoft.com"},
        "GOOGL": {"shortName": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 1700000000000, "website": "https://www.alphabet.com"},
        "AMZN": {"shortName": "Amazon.com Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "marketCap": 1500000000000, "website": "https://www.amazon.com"},
        "TSLA": {"shortName": "Tesla Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "marketCap": 800000000000, "website": "https://www.tesla.com"},
        "NVDA": {"shortName": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1800000000000, "website": "https://www.nvidia.com"},
        "META": {"shortName": "Meta Platforms Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "marketCap": 900000000000, "website": "https://www.meta.com"},
        "NFLX": {"shortName": "Netflix Inc.", "sector": "Communication Services", "industry": "Entertainment", "marketCap": 200000000000, "website": "https://www.netflix.com"},
    }
    
    return company_data.get(symbol, {
        "shortName": f"{symbol} Corporation",
        "sector": "Technology",
        "industry": "Software",
        "marketCap": 100000000000,
        "website": "N/A"
    })

# Check connectivity and set demo mode
is_connected = check_connectivity()
if not is_connected:
    st.info("🔄 **Demo Mode**: External APIs are not accessible. Showing sample data for demonstration purposes.")

# Fetch and display stock data
if stock:
    try:
        if is_connected:
            # Try to fetch real data
            ticker = yf.Ticker(stock)
            hist = ticker.history(period="6mo")
            
            if hist.empty:
                raise ValueError("No data returned for this symbol")
            
            # Get company info
            info = ticker.info
            data_source = "📊 **Live Data**"
        else:
            # Use sample data in demo mode
            hist = generate_sample_data(stock)
            info = get_sample_company_info(stock)
            data_source = "🎯 **Sample Data** (Demo Mode)"

        st.subheader(f"📈 Stock Price for {stock}")
        st.markdown(data_source)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="Close"))
        fig.update_layout(title=f"{stock} Stock Price (Last 6 Months)", xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Company Info")
        st.write({
            "Name": info.get("shortName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": f"${info.get('marketCap', 0):,}" if info.get('marketCap') else "N/A",
            "Website": info.get("website", "N/A"),
        })

    except requests.exceptions.RequestException:
        st.error("🌐 **Network Error**: Unable to connect to financial data services. Please check your internet connection.")
        st.info("💡 **Tip**: Try refreshing the page or check if you're behind a firewall that blocks financial APIs.")
        
    except ValueError as e:
        if "No data returned" in str(e):
            st.error(f"📊 **Data Not Available**: No data found for '{stock}'. This could mean:")
            st.write("• The ticker symbol doesn't exist")
            st.write("• The stock is delisted or suspended")
            st.write("• There's a temporary issue with the data provider")
            st.info(f"💡 **Suggestion**: Try popular symbols like AAPL, MSFT, GOOGL, or check if '{stock}' is spelled correctly.")
        else:
            st.error(f"❌ **Data Error**: {str(e)}")
            
    except Exception as e:
        error_msg = str(e).lower()
        if "timeout" in error_msg or "connection" in error_msg:
            st.error("⏱️ **Timeout Error**: The request took too long. The financial data service might be slow or overloaded.")
            st.info("🔄 **Try Again**: Please wait a moment and try selecting the stock again.")
        elif "rate limit" in error_msg or "429" in error_msg:
            st.error("🚦 **Rate Limit**: Too many requests to the financial data service.")
            st.info("⏳ **Please Wait**: Try again in a few minutes.")
        else:
            st.error(f"❌ **Unexpected Error**: {str(e)}")
            st.info("🛠️ **Troubleshooting**: Please try a different stock symbol or refresh the page.")
