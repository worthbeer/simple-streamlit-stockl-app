import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("Stock Dashboard")

# Sidebar controls
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL").upper()
period_options = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "1 Year": 365, "2 Years": 730}
period_label = st.sidebar.selectbox("Period", list(period_options.keys()), index=3)
chart_type = st.sidebar.radio("Chart Type", ["Candlestick", "Line"])

days = period_options[period_label]
end = date.today()
start = end - timedelta(days=days)

@st.cache_data(ttl=3600)
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end, auto_adjust=True)

with st.spinner(f"Loading {ticker}..."):
    df = load_data(ticker, start, end)

if df.empty:
    st.error(f"No data found for '{ticker}'. Check the ticker symbol.")
    st.stop()

# Key metrics
info = yf.Ticker(ticker).fast_info
col1, col2, col3, col4 = st.columns(4)
last_close = df["Close"].iloc[-1].item()
prev_close = df["Close"].iloc[-2].item()
change = last_close - prev_close
pct_change = (change / prev_close) * 100
col1.metric("Last Close", f"${last_close:.2f}", f"{change:+.2f} ({pct_change:+.2f}%)")
col2.metric("52W High", f"${df['High'].max().item():.2f}")
col3.metric("52W Low", f"${df['Low'].min().item():.2f}")
col4.metric("Avg Volume", f"{int(df['Volume'].mean()):,}")

# Price chart
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25], vertical_spacing=0.03)

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"].squeeze(), high=df["High"].squeeze(),
        low=df["Low"].squeeze(), close=df["Close"].squeeze(), name=ticker
    ), row=1, col=1)
else:
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"].squeeze(), mode="lines", name=ticker,
        line=dict(color="#2196F3", width=2)
    ), row=1, col=1)

# Volume bars
colors = ["#ef5350" if df["Close"].iloc[i].item() < df["Open"].iloc[i].item() else "#26a69a" for i in range(len(df))]
fig.add_trace(go.Bar(x=df.index, y=df["Volume"].squeeze(), name="Volume", marker_color=colors), row=2, col=1)

fig.update_layout(
    height=600, xaxis_rangeslider_visible=False,
    yaxis_title="Price (USD)", yaxis2_title="Volume",
    legend=dict(orientation="h", y=1.02)
)
st.plotly_chart(fig, use_container_width=True)

# Compare multiple tickers
st.divider()
st.subheader("Compare Tickers")
compare_input = st.text_input("Enter tickers separated by commas (e.g. AAPL, MSFT, GOOGL)", value="AAPL, MSFT, GOOGL")
tickers = [t.strip().upper() for t in compare_input.split(",") if t.strip()]

if tickers:
    fig2 = go.Figure()
    for t in tickers:
        data = load_data(t, start, end)
        if not data.empty:
            normalized = (data["Close"].squeeze() / data["Close"].iloc[0].item()) * 100
            fig2.add_trace(go.Scatter(x=data.index, y=normalized, mode="lines", name=t))
    fig2.update_layout(height=400, yaxis_title="Indexed Price (base 100)", legend=dict(orientation="h", y=1.02))
    st.plotly_chart(fig2, use_container_width=True)
