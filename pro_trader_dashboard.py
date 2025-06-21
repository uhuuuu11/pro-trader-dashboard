import streamlit as st
import streamlit.components.v1 as components
from gnews import GNews
from textblob import TextBlob

# Page setup
st.set_page_config(page_title="Pro Trader News Dashboard", layout="wide")
st.title("🚀 Live Trading News & Charts")

# Coins list
coins = ["BTCUSDT", "ETHUSDT", "ALGOUSDT", "SOLUSDT"]

# 1️⃣ Display TradingView charts
st.markdown("### 📊 Live Price Charts")
cols = st.columns(len(coins))
for i, symbol in enumerate(coins):
    cols[i].markdown(f"**{symbol.replace('USDT','/USDT')}**")
    components.iframe(
        f"https://www.tradingview.com/widgetembed/?frameElementId=&symbol=BINANCE:{symbol}&interval=5&theme=dark&style=1&locale=en",
        height=300,
        scrolling=True,
    )

# 2️⃣ Aggregate news
st.markdown("### 📰 Top Market-Moving News")

# Initialize GNews
gn = GNews(language='en', country='US', max_results=20)
news_items = gn.get_top_news()

def analyze_sentiment(text):
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    if pol > 0.1:
        return "Bullish 🔺", "green"
    elif pol < -0.1:
        return "Bearish 🔻", "red"
    else:
        return "Neutral ⚪", "gray"

# Display with sentiment
for item in news_items[:10]:  # Top 10 headlines
    title = item['title']
    url = item['url']
    sentiment, color = analyze_sentiment(title)
    st.markdown(f"<a href='{url}' style='color:{color}'><b>{sentiment}</b> {title}</a>", unsafe_allow_html=True)

# 3️⃣ Category tabs
tabs = st.tabs(["Macro/Political", "Crypto Regulation", "Tech"])

for tab in tabs:
    with tab:
        st.markdown(f"#### {tab.title} News")
        for item in news_items:
            cat = None
            t = item['title'].lower()
            if tab.title == "Macro/Political" and any(k in t for k in ["election", "war", "inflation", "fed", "cpi", "gdp", "unemployment"]):
                cat = True
            if tab.title == "Crypto Regulation" and any(k in t for k in ["crypto", "sec", "regulation", "ban", "tokyo", "mi ca", "law"]):
                cat = True
            if tab.title == "Tech" and any(k in t for k in ["ai", "chip", "cyber", "tech", "cloud", "apple", "microsoft"]):
                cat = True
            if cat:
                sentiment, color = analyze_sentiment(item['title'])
                st.markdown(f"<a href='{item['url']}' style='color:{color}'><b>{sentiment}</b> {item['title']}</a>", unsafe_allow_html=True)

# Auto-refresh
st.markdown("⏱️ Refreshes every 60 seconds.")
st.experimental_rerun()
