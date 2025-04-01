import streamlit as st
import requests
import pandas as pd

st.title("🌍 Market Insights")
st.markdown("Track global ETFs, market movers, and trends in real-time.")

API_KEY = "4v4VmgQ54xf0jMOt81Xug3IzWbDVswg0"

# ---- Index ETFs Instead of Raw Index Symbols ----
st.subheader("📈 Index ETF Performance")

etfs = ["SPY", "QQQ", "DIA", "ISF.L", "EWJ"]
etf_names = ["S&P 500 (SPY)", "NASDAQ 100 (QQQ)", "Dow Jones (DIA)", "FTSE 100 (ISF.L)", "Nikkei 225 (EWJ)"]

def get_price_data(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        return data[0]["price"], data[0]["changesPercentage"]
    except:
        return None, None

etf_data = []
for ticker, name in zip(etfs, etf_names):
    price, change = get_price_data(ticker)
    if price is not None and change is not None:
        etf_data.append({"ETF": name, "Price": price, "Change %": change})

if etf_data:
    df_etfs = pd.DataFrame(etf_data)
    st.dataframe(df_etfs.style.format({"Price": "${:.2f}", "Change %": "{:.2f}%"}))
else:
    st.warning("⚠️ Could not load ETF index data.")

# ---- Market Movers ----
st.subheader("🚀 Top Gainers & 🔻 Top Losers")

def get_movers(type="gainers"):
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock_market/{type}?apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data)[["symbol", "name", "price", "changesPercentage"]]
    except:
        return pd.DataFrame()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Top Gainers")
    gainers = get_movers("gainers")
    if not gainers.empty:
        st.dataframe(gainers.head(5).style.format({"price": "${:.2f}", "changesPercentage": "{:.2f}%"}))
    else:
        st.warning("Could not fetch top gainers.")

with col2:
    st.markdown("### 🔻 Top Losers")
    losers = get_movers("losers")
    if not losers.empty:
        st.dataframe(losers.head(5).style.format({"price": "${:.2f}", "changesPercentage": "{:.2f}%"}))
    else:
        st.warning("Could not fetch top losers.")
