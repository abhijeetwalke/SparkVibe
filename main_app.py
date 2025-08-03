"""
Main SparkVibe Finance application
Refactored version with modular structure
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Import utilities
from utils.constants import STOCKS, CSS_STYLES
from utils.data_fetcher import fetch_stock_data
from utils.formatters import format_currency, format_volume

# Development mode flag - set to True to use mock data for faster iteration
DEVELOPMENT_MODE = False

# Import tab modules
from tabs.golden_cross import create_golden_cross_tab
from tabs.death_cross import create_death_cross_tab
from tabs.volume_analysis import create_volume_analysis_tab
from tabs.inflation import create_inflation_tab

import random
import numpy as np


def generate_mock_stock_data(symbol):
    """Generate realistic mock stock data for development purposes"""
    # Base prices for different stocks to make them realistic
    base_prices = {
        "^VIX": 20.5,
        "SPY": 445.2,
        "QQQ": 375.8,
        "AAPL": 185.3,
        "MSFT": 378.9,
        "AMZN": 145.7,
        "GOOGL": 138.4,
        "META": 325.6,
        "TSLA": 248.5,
        "NVDA": 875.2,
        "AMD": 142.8,
        "NFLX": 485.3,
        "CRM": 245.7,
        "ADBE": 578.9,
        "ORCL": 115.4,
        "INTC": 43.2,
        "IBM": 165.8,
        "CSCO": 51.7,
        "V": 245.9,
        "MA": 425.3,
        "JPM": 158.7,
        "BAC": 32.4,
        "WFC": 45.8,
        "GS": 385.2,
        "MS": 87.6,
        "C": 58.9,
        "BRK-B": 385.4,
        "JNJ": 162.3,
        "PFE": 28.7,
        "UNH": 525.8,
        "ABBV": 158.9,
        "MRK": 115.6,
        "LLY": 785.4,
        "TMO": 545.7,
        "ABT": 108.9,
        "DHR": 245.3,
        "BMY": 52.1,
        "AMGN": 285.7,
        "GILD": 78.4,
        "REGN": 875.2,
        "VRTX": 425.8,
        "BIIB": 245.7,
        "XOM": 115.8,
        "CVX": 158.4,
        "COP": 125.7,
        "SLB": 48.9,
        "EOG": 125.4,
        "PXD": 245.8,
        "KMI": 18.7,
        "OKE": 95.4,
        "WMB": 38.9,
        "EPD": 15.2,
        "GLD": 185.4,
        "SLV": 22.8,
        "BTC-USD": 42500.0,
    }

    base_price = base_prices.get(symbol, 100.0)

    # Add some random variation to the base price
    current_price = base_price * (1 + random.uniform(-0.05, 0.05))

    # Generate percentage change
    percentage_change = random.uniform(-5.0, 5.0)
    daily_change = current_price * (percentage_change / 100)
    previous_close = current_price - daily_change

    # Generate volume data
    base_volume = random.randint(10_000_000, 100_000_000)
    volume = int(base_volume * random.uniform(0.5, 2.0))
    avg_volume = base_volume

    # Generate market cap
    market_cap = random.randint(50_000_000_000, 3_000_000_000_000)

    # Generate financial ratios
    pe_ratio = random.uniform(10.0, 35.0) if random.random() > 0.1 else None
    eps = random.uniform(1.0, 15.0) if random.random() > 0.1 else None
    peg_ratio = random.uniform(0.5, 3.0) if random.random() > 0.15 else None
    pb_ratio = random.uniform(1.0, 8.0) if random.random() > 0.1 else None

    # Generate moving averages
    ma_50d = current_price * random.uniform(0.95, 1.05)
    ma_200d = current_price * random.uniform(0.90, 1.10)

    # Generate golden cross and death cross
    golden_cross = ma_50d > ma_200d and random.random() > 0.7
    death_cross = ma_50d < ma_200d and random.random() > 0.8

    golden_cross_days_ago = random.randint(1, 30) if golden_cross else None
    death_cross_days_ago = random.randint(1, 30) if death_cross else None

    # Generate earnings date
    earnings_date = None
    if symbol not in ["^VIX", "SPY", "QQQ", "GLD", "SLV", "BTC-USD"]:
        # Generate a random future date within next 90 days
        days_ahead = random.randint(1, 90)
        earnings_date = pd.Timestamp.now() + pd.Timedelta(days=days_ahead)

    return {
        "symbol": symbol,
        "current_price": current_price,
        "pe_ratio": pe_ratio,
        "eps": eps,
        "peg_ratio": peg_ratio,
        "pb_ratio": pb_ratio,
        "short_percent_float": random.uniform(1.0, 15.0) if random.random() > 0.2 else "N/A",
        "open_price": current_price * random.uniform(0.98, 1.02),
        "high_price": current_price * random.uniform(1.00, 1.05),
        "low_price": current_price * random.uniform(0.95, 1.00),
        "volume": volume,
        "avg_volume": avg_volume,
        "daily_change": daily_change,
        "percentage_change": percentage_change,
        "market_cap": market_cap,
        "previous_close": previous_close,
        "ma_50d": ma_50d,
        "ma_200d": ma_200d,
        "golden_cross": golden_cross,
        "golden_cross_days_ago": golden_cross_days_ago,
        "death_cross": death_cross,
        "death_cross_days_ago": death_cross_days_ago,
        "earnings_date": earnings_date,
        "timestamp": datetime.now(),
    }


def create_summary_table_tab(all_stock_data):
    """Create the Summary Table tab content (Tab 1)"""
    st.subheader("Stock Summary Table")

    # Create a list to store table data with locked symbols first
    locked_symbols = ["^VIX", "SPY", "QQQ"]
    remaining_symbols = [symbol for symbol in STOCKS.keys() if symbol not in locked_symbols]
    ordered_symbols = locked_symbols + remaining_symbols

    table_data = []

    for symbol in ordered_symbols:
        if symbol in all_stock_data and all_stock_data[symbol] is not None:
            data = all_stock_data[symbol]

            # Format earnings date
            earnings_date_display = "N/A"
            if data.get("earnings_date") is not None:
                earnings_date = data["earnings_date"]
                earnings_date_display = earnings_date.strftime("%Y-%m-%d")

            # Format Golden Cross with traffic light symbols based on days ago
            if data.get("golden_cross", False) and data.get("golden_cross_days_ago") is not None:
                days_ago = data['golden_cross_days_ago']
                if days_ago <= 15:
                    golden_cross_display = f"🟢 ({days_ago}d ago)"
                elif days_ago <= 30:
                    golden_cross_display = f"🟡 ({days_ago}d ago)"
                else:
                    golden_cross_display = f"🔴 ({days_ago}d ago)"
            elif data.get("golden_cross", False):
                golden_cross_display = "🟢"
            else:
                golden_cross_display = "🔴"

            # Format Death Cross with traffic light symbols based on days ago
            if data.get("death_cross", False) and data.get("death_cross_days_ago") is not None:
                days_ago = data['death_cross_days_ago']
                if days_ago <= 15:
                    death_cross_display = f"🟢 ({days_ago}d ago)"
                elif days_ago <= 30:
                    death_cross_display = f"🟡 ({days_ago}d ago)"
                else:
                    death_cross_display = f"🔴 ({days_ago}d ago)"
            elif data.get("death_cross", False):
                death_cross_display = "🟢"
            else:
                death_cross_display = "🔴"

            # Helper function to safely convert to float or None
            def safe_float(value):
                if value is None or value == "N/A" or pd.isna(value):
                    return None
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None

            table_data.append({
                "Symbol": symbol,
                "Company": STOCKS[symbol],
                "Price": safe_float(data["current_price"]),
                "Change %": safe_float(data["percentage_change"]),
                "Volume": safe_float(data["volume"]),
                "Avg Volume": safe_float(data["avg_volume"]),
                "Market Cap (B)": safe_float(data["market_cap"]),
                "P/E": safe_float(data["pe_ratio"]),
                "EPS": safe_float(data["eps"]),
                "PEG": safe_float(data["peg_ratio"]),
                "P/B": safe_float(data["pb_ratio"]),
                "50-Day MA": safe_float(data["ma_50d"]),
                "200-Day MA": safe_float(data["ma_200d"]),
                "Golden Cross": golden_cross_display,
                "Death Cross": death_cross_display,
                "Earnings Date": earnings_date_display,
            })

    if table_data:
        # Create DataFrame
        df = pd.DataFrame(table_data)

        # Convert market cap to billions for proper sorting
        df["Market Cap (B)"] = df["Market Cap (B)"].apply(lambda x: x/1e9 if pd.notna(x) and x is not None else None)

        # Convert volume to millions for proper sorting
        df["Volume (M)"] = df["Volume"].apply(lambda x: x/1e6 if pd.notna(x) and x is not None else None)
        df["Avg Volume (M)"] = df["Avg Volume"].apply(lambda x: x/1e6 if pd.notna(x) and x is not None else None)

        # Remove the original Volume and Avg Volume columns
        df = df.drop(["Volume", "Avg Volume"], axis=1)

        # Reorder columns to ensure Earnings Date is rightmost
        column_order = [
            "Symbol", "Company", "Price", "Change %", "Volume (M)", "Avg Volume (M)",
            "Market Cap (B)", "P/E", "EPS", "PEG", "P/B", "50-Day MA", "200-Day MA",
            "Golden Cross", "Death Cross", "Earnings Date"
        ]
        df = df[column_order]

        # Display the dataframe with custom column configuration
        st.dataframe(
            df,
            use_container_width=True,
            height=600,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol 🔤", width="small"),
                "Company": st.column_config.TextColumn("Company 🏢", width="large"),
                "Price": st.column_config.NumberColumn("Price 💲", width="small", format="$%.1f"),
                "Change %": st.column_config.NumberColumn("Change % 📈", width="small", format="%.1f%%"),
                "Volume (M)": st.column_config.NumberColumn("Volume 📊", width="small", format="%.1fM"),
                "Avg Volume (M)": st.column_config.NumberColumn("Avg Vol 📊", width="small", format="%.1fM"),
                "Market Cap (B)": st.column_config.NumberColumn("Market Cap (B) 💰", width="small", format="$%.1fB"),
                "P/E": st.column_config.NumberColumn("P/E 📊", width="small", format="%.1f"),
                "EPS": st.column_config.NumberColumn("EPS 💵", width="small", format="$%.2f"),
                "PEG": st.column_config.NumberColumn("PEG 📈", width="small", format="%.2f"),
                "P/B": st.column_config.NumberColumn("P/B 📊", width="small", format="%.2f"),
                "50-Day MA": st.column_config.NumberColumn("50-Day MA 📈", width="small", format="$%.1f"),
                "200-Day MA": st.column_config.NumberColumn("200-Day MA 📈", width="small", format="$%.1f"),
                "Golden Cross": st.column_config.TextColumn("Golden Cross ✨", width="small"),
                "Death Cross": st.column_config.TextColumn("Death Cross ⚠️", width="small"),
                "Earnings Date": st.column_config.TextColumn("Earnings Date 📅", width="medium"),
            },
            hide_index=True,
        )

        # Add legend for traffic light symbols
        st.markdown("### Legend")
        st.markdown("🟢 = True/Present | 🔴 = False/Absent")

        # Display summary statistics
        st.subheader("Market Summary")

        # Calculate summary stats
        total_stocks = len([data for data in all_stock_data.values() if data is not None])
        positive_stocks = len([data for data in all_stock_data.values()
                             if data is not None and data["percentage_change"] > 0])
        negative_stocks = total_stocks - positive_stocks

        golden_cross_count = len([data for data in all_stock_data.values()
                                if data is not None and data.get("golden_cross", False)])
        death_cross_count = len([data for data in all_stock_data.values()
                               if data is not None and data.get("death_cross", False)])

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Stocks", total_stocks)

        with col2:
            st.metric("Positive", positive_stocks, delta=f"{positive_stocks/total_stocks*100:.1f}%")

        with col3:
            st.metric("Negative", negative_stocks, delta=f"{negative_stocks/total_stocks*100:.1f}%")

        with col4:
            st.metric("Golden Cross", golden_cross_count)

        with col5:
            st.metric("Death Cross", death_cross_count)

    else:
        st.error("No stock data available to display")


def main():
    """Main application function"""
    # Set page configuration
    st.set_page_config(
        page_title="SparkVibe Finance Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS
    st.markdown(CSS_STYLES, unsafe_allow_html=True)

    # Main title
    st.title("📈 SparkVibe Finance Dashboard")
    st.markdown("Real-time stock analysis with technical indicators")

    # Sidebar for controls
    with st.sidebar:
        st.header("Dashboard Controls")

        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)

        # Manual refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()

        # Display last update time
        st.info(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

        # Add some spacing
        st.markdown("---")

        # Display market status
        st.subheader("Market Status")
        current_time = datetime.now()
        market_hours = 9 <= current_time.hour < 16  # Simplified market hours

        if market_hours:
            st.success("🟢 Market Open")
        else:
            st.error("🔴 Market Closed")

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(30)
        st.rerun()

    # Fetch data for all stocks with progress bar
    if DEVELOPMENT_MODE:
        st.info("🚀 Development Mode: Using mock data for faster iteration...")
        progress_bar = st.progress(0)
        status_text = st.empty()

        all_stock_data = {}
        total_stocks = len(STOCKS)

        for i, (symbol, company_name) in enumerate(STOCKS.items()):
            status_text.text(f"Generating mock data for {symbol} - {company_name}")
            progress_bar.progress((i + 1) / total_stocks)

            stock_data = generate_mock_stock_data(symbol)
            all_stock_data[symbol] = stock_data

            # Small delay for visual effect
            time.sleep(0.01)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        st.success("✅ Mock data loaded successfully!")
    else:
        st.info("Fetching real-time stock data...")
        progress_bar = st.progress(0)
        status_text = st.empty()

        all_stock_data = {}
        total_stocks = len(STOCKS)

        for i, (symbol, company_name) in enumerate(STOCKS.items()):
            status_text.text(f"Fetching data for {symbol} - {company_name}")
            progress_bar.progress((i + 1) / total_stocks)

            stock_data = fetch_stock_data(symbol)
            all_stock_data[symbol] = stock_data

            # Small delay to prevent rate limiting
            time.sleep(0.1)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

    # Create tabs (5 tabs including inflation)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Summary Table",
        "🌟 Golden Cross",
        "💀 Death Cross",
        "📈 Volume Analysis",
        "📊 Inflation (CPI)"
    ])

    # Tab 1: Summary Table
    with tab1:
        create_summary_table_tab(all_stock_data)

    # Tab 2: Golden Cross
    with tab2:
        create_golden_cross_tab(all_stock_data)

    # Tab 3: Death Cross
    with tab3:
        create_death_cross_tab(all_stock_data)

    # Tab 4: Volume Analysis
    with tab4:
        create_volume_analysis_tab(all_stock_data)

    # Tab 5: Inflation (CPI)
    with tab5:
        create_inflation_tab(development_mode=DEVELOPMENT_MODE)

    # Footer
    st.markdown("---")
    st.markdown("*Data provided by Yahoo Finance. This is not financial advice.*")


if __name__ == "__main__":
    main()
