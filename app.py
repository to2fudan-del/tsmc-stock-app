import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="TSMC Stock Dashboard", layout="wide")

st.title("TSMC (2330.TW) Stock Price Analysis")
st.sidebar.header("Settings")

# 1. Date input
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", datetime.now())

if start_date > end_date:
    st.sidebar.error("Error: Start date must be before end date")
else:
    # 2. Fetch data
    ticker = "2330.TW"
    df = yf.download(ticker, start=start_date, end=end_date)

    if not df.empty:
        # 3. Create Plotly Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick',
            increasing_line_color='red',
            decreasing_line_color='green'
        )])

        # Moving Average
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20', line=dict(color='blue', width=1)))

        fig.update_layout(
            title=f"TSMC Stock Price ({start_date} to {end_date})",
            yaxis_title="Price (TWD)",
            xaxis_rangeslider_visible=True,
            template="plotly_white",
            height=600
        )

        # 4. Show Chart and Data
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Recent Data (Latest 5 Days)")
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.warning("No data found for the selected range.")

st.info("Tip: You can zoom and pan the chart with your mouse.")
