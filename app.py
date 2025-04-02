import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# App setup
st.set_page_config(page_title="FinSight Pro", layout="wide")
st.title("📊 FinSight Pro - Real-Time Investment Dashboard")
st.subheader("Welcome to the future of portfolio intelligence.")
st.markdown("<div style='text-align: center; color: grey; font-size: 16px;'>Created by <b>ABIODUN ADEBAYO</b></div>", unsafe_allow_html=True)

# Sample stock selection
ticker = st.selectbox("Choose a stock to view data:", ["AAPL", "GOOGL", "MSFT", "AMZN"])

# Fetch data
data = yf.download(ticker, period="1mo", interval="1d")
st.write(f"Showing data for **{ticker}**")

# Plot with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price"))
fig.update_layout(title=f"{ticker} Closing Prices", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# Show table
st.dataframe(data.tail())
