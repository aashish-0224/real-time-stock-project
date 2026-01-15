import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Live Stock Dashboard", layout="wide")
st.title("📈 Real-Time Multi-Stock Analysis Dashboard")

# Refresh every 60 seconds
st.experimental_set_query_params(refresh="true")
st.autorefresh(interval=60_000, key="datarefresh")

CSV_FILE = "data/stock_live_data.csv"

if not os.path.exists(CSV_FILE):
    st.warning("Waiting for live data...")
    st.stop()

df = pd.read_csv(CSV_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

stocks = sorted(df["symbol"].dropna().unique())
selected_stock = st.selectbox("Select Stock", stocks)

stock_df = df[df["symbol"] == selected_stock]

stock_df["MA_3"] = stock_df["close"].rolling(3).mean()
stock_df["MA_5"] = stock_df["close"].rolling(5).mean()

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📊 {selected_stock} Price")
    st.line_chart(stock_df.set_index("timestamp")["close"])

with col2:
    st.subheader("📉 Moving Averages")
    st.line_chart(stock_df.set_index("timestamp")[["MA_3", "MA_5"]])

st.subheader("🔥 Latest Records")
st.dataframe(stock_df.tail(10), use_container_width=True)
