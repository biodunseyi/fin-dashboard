# 📊 FinSight: Real-Time Finance Dashboard

![badge](https://img.shields.io/badge/Built%20With-Streamlit-blue?style=for-the-badge)
![badge](https://img.shields.io/badge/API%20Powered-FMP%2C%20NewsData.io%2C%20yFinance-green?style=for-the-badge)

**FinSight** is a professional-grade, real-time finance dashboard for investors, analysts, and students.  
Built with Streamlit, Plotly, and multiple APIs, it provides live insights, technical analysis, portfolio optimization, and sentiment analysis — all in one place.

---

### 🚀 Live Demo  
👉 [Click here to explore the live app](https://fin-dashboard-djx73uumq4pjhejxsvlyj8.streamlit.app/)

---

## 📸 Screenshots

### 1️⃣ Portfolio Overview
Upload your CSV portfolio and get real-time valuation + visual table.

![portfolio](screenshots/portfolio_overview1.png)  
![portfolio](screenshots/portfolio_overview2.png)  
![portfolio](screenshots/portfolio_overview3.png)

---

### 2️⃣ Market Insights
Track global ETF indices, top gainers and losers in real-time.

![insights](screenshots/optimization_lab2.png)

---

### 3️⃣ Stock Analysis
Analyze individual stocks with candlestick charts, RSI, SMA, and EMA overlays.

![stock](screenshots/stock_analysis1.png)  
![stock](screenshots/stock_analysis2.png)

---

### 4️⃣ Optimization Lab (MPT)
Run Modern Portfolio Theory to optimize your asset allocation using Sharpe Ratio.

![optimization](screenshots/optimization_lab1.png)  
![optimization](screenshots/optimization_lab3.png)

---

### 5️⃣ News & Sentiment
Fetch real-time financial news and run NLP-powered sentiment analysis.

![sentiment](screenshots/news_sentiment1.png)  
![sentiment](screenshots/news_sentiment2.png)

---

## 🚀 Features

| Module                | Description                                                                  |
|------------------------|------------------------------------------------------------------------------|
| **Portfolio Overview** | Upload a CSV and visualize real-time value with Plotly                      |
| **Market Insights**    | Live global ETF prices, market gainers/losers                                |
| **Stock Analysis**     | Ticker chart with candlesticks, SMA/EMA, RSI                                 |
| **Optimization Lab**   | Markowitz Efficient Frontier optimizer (maximize Sharpe Ratio)              |
| **News & Sentiment**   | NLP sentiment on financial headlines using TextBlob & NewsData.io           |

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit + Plotly
- **Backend:** Python
- **Data APIs:**
  - [Financial Modeling Prep](https://financialmodelingprep.com/)
  - [Yahoo Finance via yFinance](https://pypi.org/project/yfinance/)
  - [NewsData.io](https://newsdata.io/)
- **NLP:** TextBlob
- **Others:** pandas, numpy, scipy, requests

---

## 🧪 CSV Format Example

```csv
Ticker,Quantity
AAPL,10
TSLA,5
MSFT,8
