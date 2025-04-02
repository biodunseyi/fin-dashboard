import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import random

st.set_page_config(page_title="📊 Stock Analysis", layout="wide")
st.title("📊 Stock Analysis")
API_KEY = "4v4VmgQ54xf0jMOt81Xug3IzWbDVswg0"

# --- Sidebar collapsible sections ---
with st.sidebar.expander("🔍 Analyze a Stock"):
    ticker = st.text_input("Enter any stock symbol", placeholder="e.g. AAPL", help="Search by ticker like AAPL, TSLA, etc.")

with st.sidebar.expander("⚙️ Settings"):
    theme = st.selectbox("Theme", ["Light", "Dark"], index=0)

if ticker:
    try:
        # Company profile
        prof_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey={API_KEY}"
        prof_res = requests.get(prof_url).json()
        if prof_res:
            profile = prof_res[0]
            st.subheader("🏢 Company Profile")

            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(profile["image"], width=80)
            with col2:
                st.markdown(f"**{profile['companyName']}**")
                st.write(f"Ticker: {profile['symbol']}  |  Exchange: {profile['exchangeShortName']}")
                st.write(f"Industry: {profile['industry']}")
                st.markdown(f"[🔗 Website]({profile['website']})")

            st.markdown(f"**Description**: {profile['description']}")

        # Historical price data
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

            # Candlestick + MA
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df['date'], open=df['open'], high=df['high'],
                low=df['low'], close=df['close'], name='Candlestick'))

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

            # RSI chart
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

            # FinScore
            with st.expander("📊 FinScore – How healthy is this stock?"):
                st.markdown("Custom score based on volatility, momentum, and sentiment.")

                df['return'] = df['close'].pct_change()
                volatility = df['return'].rolling(window=10).std().iloc[-1] * 100
                volatility_score = max(0, 100 - volatility * 10)

                perf = ((df['close'].iloc[-1] - df['close'].iloc[-10]) / df['close'].iloc[-10]) * 100
                perf_score = min(max(perf + 50, 0), 100)

                sentiment_score = random.randint(40, 90)

                finscore = int((0.4 * perf_score) + (0.3 * sentiment_score) + (0.3 * volatility_score))

                st.metric("📈 FinScore", f"{finscore}/100")
                st.progress(finscore)

                st.write("🔍 Breakdown:")
                st.write(f"• Performance Score: `{round(perf_score)}`")
                st.write(f"• Volatility Score: `{round(volatility_score)}`")
                st.write(f"• Sentiment Score: `{sentiment_score}` (simulated)")

    except Exception as e:
        st.error(f"An error occurred: {e}")
