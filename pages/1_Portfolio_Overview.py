import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("💼 Portfolio Overview")

st.markdown("Upload a CSV file with your portfolio holdings in this format:")

with st.expander("📄 Example Format"):
    st.code("Ticker,Quantity\nAAPL,10\nTSLA,5\nMSFT,8", language="csv")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    try:
        # Read uploaded CSV
        portfolio_df = pd.read_csv(uploaded_file)
        st.subheader("📂 Uploaded Portfolio")
        st.dataframe(portfolio_df)

        tickers = portfolio_df["Ticker"].tolist()

        # --- Real-time price fetch (FMP) ---
        def get_price_fmp(ticker):
            try:
                url = f"https://financialmodelingprep.com/api/v3/quote-short/{ticker}?apikey=4v4VmgQ54xf0jMOt81Xug3IzWbDVswg0"
                response = requests.get(url)
                data = response.json()
                return data[0]["price"]
            except:
                return None

        prices = []
        missing_tickers = []
        for ticker in tickers:
            price = get_price_fmp(ticker)
            if price is None:
                missing_tickers.append(ticker)
            prices.append(price)

        # Add prices and compute value
        portfolio_df["Price"] = prices
        portfolio_df["Value"] = portfolio_df["Price"] * portfolio_df["Quantity"]

        # Drop rows with missing data
        clean_df = portfolio_df.dropna(subset=["Price"])

        st.subheader("💰 Portfolio with Real-Time Prices")
        st.dataframe(clean_df.style.format({"Price": "${:.2f}", "Value": "${:,.2f}"}))

        total_value = clean_df["Value"].sum()
        st.metric("📊 Total Portfolio Value", f"${total_value:,.2f}")

        if missing_tickers:
            st.warning(f"Couldn't retrieve prices for: {', '.join(missing_tickers)}")

        # --- Plotly Pie Chart ---
        if not clean_df.empty:
            st.subheader("📊 Asset Allocation")

            fig = px.pie(
                clean_df,
                names="Ticker",
                values="Value",
                title="Portfolio Allocation",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_traces(textinfo='label+percent+value', pull=[0.05]*len(clean_df))
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
