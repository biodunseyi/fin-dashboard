import streamlit as st
import requests
from textblob import TextBlob

st.title("📰 News & Sentiment")
st.markdown("Get the latest news and sentiment analysis for any company, stock, or keyword.")

API_KEY = "pub_77572f6622c6af9153ed5e0e0631bf33a1c5a"

query = st.text_input("Search for stock or keyword (e.g., AAPL, Bitcoin, Microsoft):", value="AAPL")

if query:
    st.info(f"🔍 Fetching news for: {query}")
    params = {
        "apikey": API_KEY,
        "q": query,
        "language": "en",
        "category": "business",
    }

    try:
        response = requests.get("https://newsdata.io/api/1/news", params=params)
        data = response.json()

        if "results" not in data:
            st.error("No news results found. Check your keyword or API usage.")
            st.json(data)
        else:
            articles = data["results"]
            sentiment_scores = []

            for article in articles[:10]:
                title = article.get("title", "No Title")
                content = article.get("content", "") or article.get("description", "")
                source = article.get("source_id", "Unknown")
                pub_date = article.get("pubDate", "Unknown Date")

                blob = TextBlob(content)
                polarity = blob.sentiment.polarity
                sentiment = "🟢 Positive" if polarity > 0.1 else "🔴 Negative" if polarity < -0.1 else "🟡 Neutral"

                sentiment_scores.append(polarity)

                with st.expander(f"📰 {title}"):
                    st.write(f"**Source:** {source}  |  **Date:** {pub_date}")
                    st.write(content)
                    st.markdown(f"**Sentiment**: {sentiment} _(Score: {polarity:.2f})_")

            # Summary
            if sentiment_scores:
                avg_sent = sum(sentiment_scores) / len(sentiment_scores)
                st.markdown("---")
                st.subheader("📊 Overall Sentiment Summary")
                summary = "🟢 Positive" if avg_sent > 0.1 else "🔴 Negative" if avg_sent < -0.1 else "🟡 Neutral"
                st.metric("Average Sentiment", f"{summary} ({avg_sent:.2f})")

    except Exception as e:
        st.error(f"Error fetching news: {e}")
