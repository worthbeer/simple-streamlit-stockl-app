# Stock Dashboard — Streamlit App

An interactive stock analysis dashboard built with Python and Streamlit, developed as a demonstration of data application development capabilities.

## Overview

This app lets you explore stock price history and compare multiple tickers side-by-side — all in a clean, browser-based interface with no setup required for the end user.

**Origin:** This project grew out of an extended AI-assisted planning session, from initial concept through research and implementation, resulting in a fully working data app.

## Features

- **Live market data** — fetches real-time and historical price data via Yahoo Finance
- **Candlestick or line chart** — toggle between chart types from the sidebar
- **Key metrics** — last close price, day change, 52-week high/low, and average volume
- **Configurable time range** — 1 month, 3 months, 6 months, 1 year, or 2 years
- **Volume overlay** — color-coded volume bars (green = up day, red = down day) beneath the price chart
- **Multi-ticker comparison** — normalized indexed chart to compare relative performance across any set of tickers
- **Data caching** — 1-hour TTL cache on data fetches keeps the UI fast and avoids redundant API calls

## Tech Stack

| Layer | Library |
|---|---|
| UI / App framework | [Streamlit](https://streamlit.io) |
| Market data | [yfinance](https://github.com/ranaroussi/yfinance) |
| Charting | [Plotly](https://plotly.com/python/) |

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/worthbeer/simple-streamlit-stockl-app.git
cd simple-streamlit-stockl-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

## Usage

1. Enter any valid ticker symbol in the sidebar (default: `AAPL`)
2. Select a time period and chart type
3. View key metrics and the interactive price + volume chart
4. Scroll down to the **Compare Tickers** section and enter a comma-separated list (e.g. `AAPL, MSFT, GOOGL`) to see normalized performance side-by-side

## Project Structure

```
simple-streamlit-stockl-app/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
└── README.md
```

## Background

This app was built to demonstrate Python and Streamlit proficiency — specifically the ability to move quickly from concept to a working, interactive data application. The workflow from planning to deployment used AI-assisted development, reflecting how modern teams accelerate delivery with AI tooling.
