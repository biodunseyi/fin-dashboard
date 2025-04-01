import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

st.title("📊 Stock Analysis")

API_KEY = "4v4VmgQ54xf0jMOt81Xug3IzWbDVswg0"

ticker = st.text_input("Enter a stock ticker symbol (e.g., AAPL, TSLA, MSFT):")

if ticker:
    try:
        # Fetch historical OHLCV data
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker.upper()}?timeseries=100&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "historical" not in data or len(data["historical"]) == 0:
            st.error("No data found for this ticker. Try another.")
        else:
            df = pd.DataFrame(data["historical"])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values("date")

            st.subheader(f"📅 Price History for {ticker.upper()}")
            st.write(f"Last updated: {df['date'].iloc[-1].date()}")

            # --- Candlestick Chart with MA ---
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Candlestick'
            ))

            # Add moving averages
            df['SMA_10'] = df['close'].rolling(window=10).mean()
            df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()

            fig.add_trace(go.Scatter(x=df['date'], y=df['SMA_10'],
                                     mode='lines', name='SMA 10', line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_10'],
                                     mode='lines', name='EMA 10', line=dict(color='cyan')))

            fig.update_layout(title=f'{ticker.upper()} - Candlestick with Moving Averages',
                              xaxis_title='Date', yaxis_title='Price (USD)',
                              xaxis_rangeslider_visible=False)

            st.plotly_chart(fig, use_container_width=True)

            # --- RSI Chart ---
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(14).mean()
            avg_loss = loss.rolling(14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=df['date'], y=rsi, mode='lines', name='RSI'))
            fig_rsi.update_layout(title="RSI (Relative Strength Index)",
                                  yaxis=dict(title='RSI', range=[0, 100]),
                                  xaxis_title='Date')

            st.plotly_chart(fig_rsi, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
