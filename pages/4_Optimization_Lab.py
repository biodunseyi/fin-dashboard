import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from scipy.optimize import minimize

st.title("📈 Optimization Lab — Modern Portfolio Theory")

st.markdown("""
Upload a CSV of your portfolio to find the optimal allocation using **Markowitz Efficient Frontier**.
""")

with st.expander("📄 Example Format"):
    st.code("Ticker,Quantity\nAAPL,10\nTSLA,5\nMSFT,8", language="csv")

uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        tickers = df['Ticker'].tolist()
        st.success(f"Loaded {len(tickers)} assets: {', '.join(tickers)}")

        # ⏳ Download historical data (force unadjusted so we get 'Adj Close')
        st.info("📥 Fetching historical price data (1Y)...")
        prices_raw = yf.download(tickers, period="1y", auto_adjust=False)
        prices = prices_raw['Adj Close']
        returns = prices.pct_change().dropna()
        st.write("Returns Sample:")
        st.dataframe(returns.head())

        # 🔢 Mean returns and covariance matrix
        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        # 🎯 Optimization functions
        def portfolio_performance(weights):
            port_return = np.dot(weights, mean_returns)
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe = port_return / port_volatility
            return port_return, port_volatility, sharpe

        def negative_sharpe(weights):
            return -portfolio_performance(weights)[2]

        def constraint_sum(weights):
            return np.sum(weights) - 1

        # 🧠 Run optimization
        num_assets = len(tickers)
        bounds = tuple((0, 1) for _ in range(num_assets))
        constraints = {'type': 'eq', 'fun': constraint_sum}
        init_guess = [1. / num_assets] * num_assets

        st.info("🔧 Running optimization...")
        result = minimize(negative_sharpe, init_guess, method='SLSQP',
                          bounds=bounds, constraints=constraints)

        opt_weights = result.x
        opt_return, opt_volatility, opt_sharpe = portfolio_performance(opt_weights)

        st.subheader("✅ Optimal Portfolio Allocation")
        df_opt = pd.DataFrame({
            'Ticker': tickers,
            'Weight': opt_weights
        })
        st.dataframe(df_opt.style.format({"Weight": "{:.2%}"}))

        st.metric("📊 Expected Return", f"{opt_return:.2%}")
        st.metric("⚠️ Expected Volatility", f"{opt_volatility:.2%}")
        st.metric("💹 Sharpe Ratio", f"{opt_sharpe:.2f}")

        # 🥧 Pie Chart
        fig = px.pie(df_opt, names='Ticker', values='Weight', title='Optimized Allocation')
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error during optimization: {e}")
