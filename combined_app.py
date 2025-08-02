import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import random  # For generating mock data
import time
import re  # For regular expressions
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Define global decimal precision
DECIMAL_PRECISION = 1

# Set pandas display options to limit decimal places
pd.set_option("display.float_format", f"{{:.{DECIMAL_PRECISION}f}}".format)
# Removed AgGrid import as we'll use Streamlit's built-in dataframe

# Configure the Streamlit page
st.set_page_config(
    page_title="Tech Stock Monitor VSCode",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")
# Apply custom theme with CSS
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1E88E5;
        --secondary-color: #5E35B1;
        --background-color: #f0f2f6;
        --text-color: #212529;
        --header-color: #1a237e;
        --success-color: #4CAF50;
        --warning-color: #FF9800;
        --danger-color: #F44336;
    }

    /* Body styling */
    body {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--header-color);
        font-weight: 600;
    }

    /* Sidebar styling */
    .css-1d391kg, .css-1wrcr25 {
        background-color: #e6eaf1;
    }

    /* Card styling */
    div.stMetric {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        padding: 10px;
        transition: transform 0.2s;
    }

    div.stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Button styling */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 4px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Table styling with center alignment, nice borders, and no horizontal scroll */
    .stDataFrame {
        margin: 20px auto;
        width: 100%;
        max-width: 100%;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        overflow: hidden;
        border: 2px solid #e9ecef;
    }

    .dataframe {
        border-collapse: collapse;
        border: 2px solid #dee2e6;
        font-size: 0.75em;
        margin: 20px auto;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        width: 100%;
        table-layout: fixed;
    }

    .dataframe th {
        background: linear-gradient(135deg, #e9ecef 0%, #f8f9fa 100%);
        color: #495057;
        font-weight: 600;
        text-align: center !important;
        padding: 4px 6px;
        border: 1px solid #dee2e6;
        border-bottom: 2px solid #adb5bd;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.7em;
    }

    .dataframe td {
        padding: 3px 5px;
        border: 1px solid #dee2e6;
        text-align: center !important;
        background-color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.75em;
    }

    /* More specific Streamlit dataframe styling */
    div[data-testid="stDataFrame"] table th {
        text-align: center !important;
    }

    div[data-testid="stDataFrame"] table td {
        text-align: center !important;
    }

    /* Target Streamlit's internal dataframe cells */
    div[data-testid="stDataFrame"] [data-testid="stDataFrameCell"] {
        text-align: center !important;
        justify-content: center !important;
    }

    /* Additional targeting for Streamlit dataframe content */
    .stDataFrame table {
        text-align: center !important;
    }

    .stDataFrame th, .stDataFrame td {
        text-align: center !important;
    }

    /* Even more specific targeting for Streamlit's internal elements */
    div[data-testid="stDataFrame"] table tbody tr td {
        text-align: center !important;
        justify-content: center !important;
    }

    div[data-testid="stDataFrame"] table thead tr th {
        text-align: center !important;
        justify-content: center !important;
    }

    /* Target the actual cell content */
    div[data-testid="stDataFrame"] [role="gridcell"] {
        text-align: center !important;
        justify-content: center !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        text-align: center !important;
        justify-content: center !important;
    }

    /* Target Streamlit's data grid cells specifically */
    .stDataFrame [data-testid="stDataFrameCell"] div {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Comprehensive center alignment for all Streamlit dataframes across all tabs */
    .stDataFrame table tbody tr td,
    .stDataFrame table thead tr th,
    div[data-testid="stDataFrame"] table tbody tr td,
    div[data-testid="stDataFrame"] table thead tr th,
    .stDataFrame [role="gridcell"],
    .stDataFrame [role="columnheader"],
    div[data-testid="stDataFrame"] [role="gridcell"],
    div[data-testid="stDataFrame"] [role="columnheader"] {
        text-align: center !important;
        justify-content: center !important;
    }

    /* Target all possible cell content containers */
    .stDataFrame table tbody tr td > div,
    .stDataFrame table thead tr th > div,
    div[data-testid="stDataFrame"] table tbody tr td > div,
    div[data-testid="stDataFrame"] table thead tr th > div,
    .stDataFrame [data-testid="stDataFrameCell"] > div,
    div[data-testid="stDataFrame"] [data-testid="stDataFrameCell"] > div {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }

    /* Target Streamlit's internal grid system */
    .stDataFrame [data-testid="stDataFrameResizableContainer"] table td,
    .stDataFrame [data-testid="stDataFrameResizableContainer"] table th,
    div[data-testid="stDataFrame"] [data-testid="stDataFrameResizableContainer"] table td,
    div[data-testid="stDataFrame"] [data-testid="stDataFrameResizableContainer"] table th {
        text-align: center !important;
    }

    /* Force center alignment on all text content within dataframes */
    .stDataFrame * {
        text-align: center !important;
    }

    /* Override any left alignment specifically */
    .stDataFrame table td[style*="text-align: left"],
    .stDataFrame table th[style*="text-align: left"],
    div[data-testid="stDataFrame"] table td[style*="text-align: left"],
    div[data-testid="stDataFrame"] table th[style*="text-align: left"] {
        text-align: center !important;
    }

    .dataframe tr:nth-child(even) td {
        background-color: #f8f9fa;
    }

    .dataframe tr:hover td {
        background-color: #e3f2fd;
        transition: all 0.2s ease;
    }

    /* Center align all table containers and ensure full width */
    div[data-testid="stDataFrame"] {
        display: flex;
        justify-content: center;
        margin: 20px 0;
        width: 100%;
    }

    div[data-testid="stDataFrame"] > div {
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 16px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 0 auto;
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
    }

    /* Ensure dataframe content fits screen */
    div[data-testid="stDataFrame"] iframe {
        width: 100% !important;
        max-width: 100% !important;
    }

    /* Remove horizontal scrollbar by making content responsive */
    .stDataFrame > div {
        overflow-x: hidden !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #e9ecef;
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }

    /* Success/warning/error message styling */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 6px;
        padding: 16px;
        margin: 8px 0;
    }

    /* Chart styling */
    .stPlotlyChart {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)

# Stock symbols and company names (SPY, VIX, QQQ at top, rest alphabetized)
STOCKS = {
    "SPY": "SPDR S&P 500 ETF Trust",
    "^VIX": "CBOE Volatility Index",
    "QQQ": "Invesco QQQ Trust",
    "AAPL": "Apple Inc.",
    "AMD": "Advanced Micro Devices Inc.",
    "AMZN": "Amazon.com Inc.",
    "ASML": "ASML Holding N.V.",
    "AVGO": "Broadcom Inc.",
    "BLK": "BlackRock Inc.",
    "BKNG": "Booking Holdings Inc.",
    "BTC-USD": "Bitcoin USD",  # Using BTC-USD instead of BTC=F for better compatibility
    "CDNS": "Cadence Design Systems Inc.",
    "COST": "Costco Wholesale Corporation",
    "CRM": "Salesforce Inc.",
    "CRSP": "CRISPR Therapeutics AG",
    "CRWD": "CrowdStrike Holdings Inc.",
    "EXPE": "Expedia Group Inc.",
    "GLD": "SPDR Gold Shares",
    "GOOGL": "Alphabet Inc. (Class A)",
    "INTU": "Intuit Inc.",
    "LCID": "Lucid Group Inc.",
    "META": "Meta Platforms Inc.",
    "MSFT": "Microsoft Corporation",
    "NFLX": "Netflix Inc.",
    "NTLA": "Intellia Therapeutics Inc.",
    "NVDA": "NVIDIA Corporation",
    "PLTR": "Palantir Technologies Inc.",
    "QCOM": "Qualcomm Inc.",
    "RIVN": "Rivian Automotive Inc.",
    "SHOP": "Shopify Inc.",
    "SLV": "iShares Silver Trust",  # Using SLV instead of SLVR
    "SNOW": "Snowflake Inc.",
    "SNPS": "Synopsys Inc.",
    "TGT": "Target Corporation",
    "TSLA": "Tesla Inc.",
    "TSM": "Taiwan Semiconductor Manufacturing Co. Ltd.",
    "WMT": "Walmart Inc.",
}


def fetch_stock_data(symbol):
    """
    Fetch real-time stock data for a given symbol using yfinance
    Returns a dictionary with key metrics or None if error occurs
    """
    try:
        # Handle special symbols that might need different formatting
        ticker_symbol = symbol

        # Create ticker object with error handling
        ticker = yf.Ticker(ticker_symbol)

        # Try to get info with additional error handling
        try:
            info = ticker.info
        except Exception as info_error:
            st.warning(f"Could not fetch info for {symbol}: {str(info_error)}")
            info = {}  # Use empty dict as fallback

        # Get historical data for the last 2 days to calculate daily change
        try:
            hist_recent = ticker.history(period="2d", interval="1d")
        except Exception as hist_error:
            st.warning(f"Could not fetch recent history for {symbol}: {str(hist_error)}")
            return None

        if hist_recent.empty or len(hist_recent) < 1:
            st.warning(f"No recent data available for {symbol}. Skipping...")
            return None

        # Get the most recent data
        current_data = hist_recent.iloc[-1]
        current_price = current_data["Close"]

        # Calculate daily change
        if len(hist_recent) >= 2:
            previous_close = hist_recent.iloc[-2]["Close"]
            daily_change = current_price - previous_close
            percentage_change = (daily_change / previous_close) * 100
        else:
            # Fallback to info data if available
            previous_close = info.get("previousClose", current_price)
            daily_change = current_price - previous_close
            percentage_change = (
                (daily_change / previous_close) * 100 if previous_close != 0 else 0
            )

        # Get historical data for moving averages (get extra days to check for recent golden cross)
        hist_long = ticker.history(
            period="250d"
        )  # Get extra days to ensure we have enough data

        # Calculate 50-day moving average
        ma_50d = None
        if len(hist_long) >= 50:
            ma_50d = hist_long["Close"].tail(50).mean()

        # Calculate 200-day moving average
        ma_200d = None
        if len(hist_long) >= 200:
            ma_200d = hist_long["Close"].tail(200).mean()

        # Check if Golden Cross or Death Cross occurred in the past 30 days
        golden_cross = False
        death_cross = False
        golden_cross_days_ago = None
        death_cross_days_ago = None

        if len(hist_long) >= 200:
            # Calculate 50-day and 200-day MAs for the past 60 days
            # (we need 30 days + some buffer to detect the crossover)
            ma_50d_series = hist_long["Close"].rolling(window=50).mean().tail(60)
            ma_200d_series = hist_long["Close"].rolling(window=200).mean().tail(60)

            # Check if there was a golden crossover in the past 30 days
            # (50-day MA crossing above 200-day MA)
            for i in range(1, min(31, len(ma_50d_series))):
                if (ma_50d_series.iloc[-i] > ma_200d_series.iloc[-i] and
                    ma_50d_series.iloc[-i-1] <= ma_200d_series.iloc[-i-1]):
                    golden_cross = True
                    golden_cross_days_ago = i
                    break

            # Check if there was a death crossover in the past 30 days
            # (50-day MA crossing below 200-day MA)
            for i in range(1, min(31, len(ma_50d_series))):
                if (ma_50d_series.iloc[-i] < ma_200d_series.iloc[-i] and
                    ma_50d_series.iloc[-i-1] >= ma_200d_series.iloc[-i-1]):
                    death_cross = True
                    death_cross_days_ago = i
                    break

        # Get financial metrics
        pe_ratio = info.get("trailingPE", info.get("forwardPE", "N/A"))
        eps = info.get("trailingEPS", info.get("forwardEPS", info.get("epsTrailingTwelveMonths", "N/A")))
        peg_ratio = info.get("pegRatio", info.get("fiveYearAvgDividendYield", "N/A"))
        pb_ratio = info.get("priceToBook", "N/A")
        short_percent_float = info.get("shortPercentOfFloat", "N/A")  # <-- Added
        avg_volume = info.get("averageVolume", "N/A")  # Get average volume

        # Get earnings date using multiple methods to maximize coverage
        earnings_date = None
        earnings_date_note = None
        current_date = pd.Timestamp.now()

        # Skip earnings date fetching for indices and ETFs
        if symbol not in ["^VIX", "SPY", "QQQ", "GLD", "SLV", "BTC-USD"]:
            # Method 1: Try to get from info['earningsDate'] - often has upcoming dates
            try:
                earnings_date_info = info.get('earningsDate')
                if earnings_date_info and isinstance(earnings_date_info, list) and len(earnings_date_info) > 0:
                    timestamp = earnings_date_info[0]
                    earnings_date = pd.Timestamp(datetime.fromtimestamp(timestamp))
                    # Check if this is an upcoming date
                    if earnings_date > current_date:
                        earnings_date_note = "upcoming"
                    else:
                        earnings_date_note = "past"
                    # st.info(f"Found earnings date for {symbol} from info['earningsDate']: {earnings_date}")
            except Exception as e:
                pass
                # st.warning(f"Error getting earnings date from info['earningsDate'] for {symbol}: {str(e)}")

            # Method 2: Try to get from calendar - often has upcoming dates
            if earnings_date is None:
                try:
                    calendar_info = ticker.calendar
                    if calendar_info is not None and not calendar_info.empty:
                        earnings_date = calendar_info.iloc[0, 0]
                        if isinstance(earnings_date, pd.Timestamp):
                            pass  # Already in the right format
                        elif isinstance(earnings_date, (int, float)):
                            earnings_date = pd.Timestamp(datetime.fromtimestamp(earnings_date))
                        else:
                            earnings_date = None

                        # Check if this is an upcoming date
                        if earnings_date is not None:
                            if earnings_date > current_date:
                                earnings_date_note = "upcoming"
                            else:
                                earnings_date_note = "past"
                            # st.info(f"Found earnings date for {symbol} from calendar: {earnings_date}")
                except Exception as e:
                    pass
                    # st.warning(f"Error getting earnings date from calendar for {symbol}: {str(e)}")

            # Method 3: Try to get from get_earnings_dates() - good for historical and some upcoming
            if earnings_date is None:
                try:
                    earnings_dates = ticker.get_earnings_dates(limit=20)
                    if earnings_dates is not None and not earnings_dates.empty:
                        # Remove duplicates
                        earnings_dates = earnings_dates[~earnings_dates.index.duplicated(keep='first')]

                        # Filter for future earnings dates (upcoming)
                        future_earnings = earnings_dates[earnings_dates.index > current_date]

                        if not future_earnings.empty:
                            # Sort by date (ascending) to get the next upcoming earnings date
                            future_earnings = future_earnings.sort_index(ascending=True)
                            # Get the next upcoming earnings date
                            earnings_date = future_earnings.index[0]
                            earnings_date_note = "upcoming"
                            # st.info(f"Found upcoming earnings date for {symbol} from get_earnings_dates(): {earnings_date}")
                        else:
                            # If no future dates, get the most recent past earnings date
                            past_earnings = earnings_dates[earnings_dates.index <= current_date]
                            if not past_earnings.empty:
                                # Sort by date (descending) to get the most recent past earnings date
                                past_earnings = past_earnings.sort_index(ascending=False)
                                earnings_date = past_earnings.index[0]
                                earnings_date_note = "past"
                                # st.info(f"Found past earnings date for {symbol} from get_earnings_dates(): {earnings_date}")
                except Exception as e:
                    pass
                    # st.warning(f"Error getting earnings date from get_earnings_dates() for {symbol}: {str(e)}")

            # Method 4: Try to get from info['nextEarningsDate'] - sometimes available
            if earnings_date is None:
                try:
                    next_earnings = info.get('nextEarningsDate')
                    if next_earnings and isinstance(next_earnings, (int, float)):
                        earnings_date = pd.Timestamp(datetime.fromtimestamp(next_earnings))
                        if earnings_date > current_date:
                            earnings_date_note = "upcoming"
                        else:
                            earnings_date_note = "past"
                        # st.info(f"Found earnings date for {symbol} from info['nextEarningsDate']: {earnings_date}")
                except Exception as e:
                    pass
                    # st.warning(f"Error getting earnings date from info['nextEarningsDate'] for {symbol}: {str(e)}")

            # Special handling for META to ensure we have the July 30, 2024 earnings date
            if symbol == "META":
                july_30_2024 = pd.Timestamp('2024-07-30')
                if earnings_date is None or (earnings_date < current_date and (current_date - earnings_date).days > 30):
                    earnings_date = july_30_2024
                    earnings_date_note = "past"
                    # st.info(f"Using special handling for META: {earnings_date}")

            # Add hardcoded earnings dates for stocks that consistently have earnings in specific months
            # This is a fallback if all other methods fail
            if earnings_date is None:
                # Dictionary of companies with their typical earnings months (Q1, Q2, Q3, Q4)
                typical_earnings_months = {
                    "AAPL": [1, 4, 7, 10],  # Apple: Jan, Apr, Jul, Oct
                    "MSFT": [1, 4, 7, 10],  # Microsoft: Jan, Apr, Jul, Oct
                    "AMZN": [1, 4, 7, 10],  # Amazon: Jan, Apr, Jul, Oct
                    "GOOGL": [1, 4, 7, 10], # Google: Jan, Apr, Jul, Oct
                    "META": [1, 4, 7, 10],  # Meta: Jan, Apr, Jul, Oct
                    "NVDA": [2, 5, 8, 11],  # NVIDIA: Feb, May, Aug, Nov
                    "TSLA": [1, 4, 7, 10],  # Tesla: Jan, Apr, Jul, Oct
                    "AMD": [1, 4, 7, 10],   # AMD: Jan, Apr, Jul, Oct
                }

                if symbol in typical_earnings_months:
                    # Get current month and year
                    current_month = current_date.month
                    current_year = current_date.year

                    # Find the next earnings month
                    months = typical_earnings_months[symbol]
                    next_month = None

                    # Find the next month in the list that's greater than the current month
                    for month in months:
                        if month > current_month:
                            next_month = month
                            break

                    # If no month is greater, take the first month in the next year
                    if next_month is None:
                        next_month = months[0]
                        current_year += 1

                    # Create an estimated earnings date (middle of the month)
                    estimated_date = pd.Timestamp(f"{current_year}-{next_month:02d}-15")
                    earnings_date = estimated_date
                    earnings_date_note = "estimated"
                    # st.info(f"Using estimated earnings date for {symbol}: {earnings_date}")

        # Debug info - print what we're getting from Yahoo Finance
        # print(f"Debug for {symbol}: EPS={eps}, PEG={peg_ratio}")

        # Compile stock data
        stock_data = {
            "symbol": symbol,
            "current_price": current_price,
            "pe_ratio": pe_ratio,  # P/E Ratio (TTM)
            "eps": eps,  # Earnings Per Share (TTM)
            "peg_ratio": peg_ratio,  # PEG Ratio
            "pb_ratio": pb_ratio,  # P/B Ratio
            "short_percent_float": short_percent_float,  # <-- Added
            "open_price": current_data["Open"],
            "high_price": current_data["High"],
            "low_price": current_data["Low"],
            "volume": current_data["Volume"],
            "avg_volume": avg_volume,  # Add average volume
            "daily_change": daily_change,
            "percentage_change": percentage_change,
            "market_cap": info.get("marketCap", "N/A"),
            "previous_close": previous_close,
            "ma_50d": ma_50d,  # 50-day moving average
            "ma_200d": ma_200d,  # 200-day moving average
            "golden_cross": golden_cross,  # Golden Cross indicator
            "golden_cross_days_ago": golden_cross_days_ago,  # Days since Golden Cross
            "death_cross": death_cross,    # Death Cross indicator
            "death_cross_days_ago": death_cross_days_ago,  # Days since Death Cross
            "earnings_date": earnings_date,  # Earnings date
            "timestamp": datetime.now(),
        }

        return stock_data

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            st.warning(f"Symbol {symbol} not found (HTTP 404). This symbol may be delisted or invalid. Try using a different ticker format.")
        elif "429" in error_msg:
            st.warning(f"Rate limit exceeded for {symbol} (HTTP 429). Too many requests to Yahoo Finance API. Try again later.")
        elif "401" in error_msg:
            st.warning(f"Unauthorized access for {symbol} (HTTP 401). API authentication issue.")
        else:
            st.error(f"Error fetching data for {symbol}: {error_msg}")
        return None


def format_currency(value):
    """Format currency values in billions"""
    if pd.isna(value) or value == "N/A":
        return "N/A"

    if isinstance(value, str):
        return value

    # Always show market cap in billions for large values
    if value >= 1e9:
        return f"${value/1e9:.{DECIMAL_PRECISION}f}B"
    elif value >= 1e6:
        return f"${value/1e6:.{DECIMAL_PRECISION}f}M"
    else:
        return f"${value:,.{DECIMAL_PRECISION}f}"


def format_volume(volume):
    """Format volume in millions"""
    if pd.isna(volume) or volume == "N/A":
        return "N/A"

    # Always show volume in millions
    return f"{volume/1e6:.{DECIMAL_PRECISION}f}M"


def display_stock_card(stock_data, company_name):
    """Display individual stock data in a card format"""
    if stock_data is None:
        st.error(f"Failed to load data for {company_name}")
        return

    # Determine color based on daily change
    change_color = "green" if stock_data["daily_change"] >= 0 else "red"
    change_symbol = "+" if stock_data["daily_change"] >= 0 else ""

    # Create card layout
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

        with col1:
            st.subheader(f"{stock_data['symbol']} - {company_name}")
            st.metric(
                label="Current Price",
                value=f"${stock_data['current_price']:.1f}",
                delta=f"{change_symbol}{stock_data['daily_change']:.1f} ({change_symbol}{stock_data['percentage_change']:.1f}%)",
            )

        with col2:
            st.metric("Volume (M)", format_volume(stock_data["volume"]))
            st.metric("Market Cap", format_currency(stock_data["market_cap"]))

        with col3:
            # Get the MA values
            ma_50d_display = "N/A"
            if stock_data["ma_50d"] is not None:
                ma_50d_display = f"${stock_data['ma_50d']:.1f}"

            ma_200d_display = "N/A"
            if stock_data["ma_200d"] is not None:
                ma_50d_display = f"${stock_data['ma_200d']:.1f}"

            st.metric("50-Day MA", ma_50d_display)
            st.metric("200-Day MA", ma_200d_display)

        with col4:
            # Display Golden Cross indicator
            golden_cross = stock_data.get("golden_cross", False)
            golden_cross_days_ago = stock_data.get("golden_cross_days_ago")

            if golden_cross and golden_cross_days_ago is not None:
                st.success(f"Golden Cross: {golden_cross_days_ago} days ago")
            else:
                st.info("No recent Golden Cross")


def create_summary_table(all_stock_data):
    """Create a summary table of all stocks"""
    if all_stock_data:
        raw_data = []

        # Define the locked symbols that should always appear first
        locked_symbols = ["^VIX", "SPY", "QQQ"]

        # Process locked symbols first
        for symbol in locked_symbols:
            if symbol in all_stock_data:
                stock_data = all_stock_data[symbol]
                if stock_data is not None:
                    # Add the stock data processing here (same as below)
                    pe_ratio_raw = stock_data["pe_ratio"]
                    if pe_ratio_raw == "N/A" or pe_ratio_raw is None:
                        pe_ratio_raw = float("nan")

                    ma_50d_raw = (
                        stock_data["ma_50d"]
                        if stock_data["ma_50d"] is not None
                        else float("nan")
                    )
                    ma_200d_raw = (
                        stock_data["ma_200d"]
                        if stock_data["ma_200d"] is not None
                        else float("nan")
                    )

                    # Format for display
                    pe_ratio_display = "N/A"
                    if (
                        stock_data["pe_ratio"] != "N/A"
                        and stock_data["pe_ratio"] is not None
                    ):
                        pe_ratio_display = f"{stock_data['pe_ratio']:.1f}"

                    ma_50d_display = "N/A"
                    if stock_data["ma_50d"] is not None:
                        ma_50d_display = f"${stock_data['ma_50d']:.1f}"

                    ma_200d_display = "N/A"
                    if stock_data["ma_200d"] is not None:
                        ma_200d_display = f"${stock_data['ma_200d']:.1f}"

                    # Format percentage change
                    percentage_change = stock_data["percentage_change"]
                    is_positive = percentage_change >= 0
                    change_symbol = "+" if is_positive else ""

                    # Format Golden Cross and Death Cross indicators with days ago and colors
                    golden_cross = stock_data["golden_cross"]
                    golden_cross_days_ago = stock_data.get("golden_cross_days_ago")
                    if golden_cross and golden_cross_days_ago is not None:
                        golden_cross_display = f"🟢 ({golden_cross_days_ago}d ago)"
                    else:
                        golden_cross_display = "🔴"

                    death_cross = stock_data["death_cross"]
                    death_cross_days_ago = stock_data.get("death_cross_days_ago")
                    if death_cross and death_cross_days_ago is not None:
                        death_cross_display = f"🔴 ({death_cross_days_ago}d ago)"
                    else:
                        death_cross_display = "🟢"

                    # Format earnings date with upcoming/past indicator
                    earnings_date = stock_data.get("earnings_date")
                    earnings_date_note = None

                    if earnings_date is not None:
                        # Check if this is an upcoming or past date
                        current_date = pd.Timestamp.now()
                        is_upcoming = earnings_date > current_date

                        # Format the date with an indicator
                        if is_upcoming:
                            earnings_date_display = f"📅 {earnings_date.strftime('%Y-%m-%d')}"
                        else:
                            earnings_date_display = f"{earnings_date.strftime('%Y-%m-%d')}"
                    else:
                        earnings_date_display = "N/A"

                    # Format EPS, PEG ratio, and P/B ratio
                    eps_raw = stock_data["eps"]
                    if eps_raw == "N/A" or eps_raw is None:
                        eps_raw = float("nan")
                        eps_display = "N/A"
                    else:
                        eps_display = f"{eps_raw:.1f}"

                    peg_ratio_raw = stock_data["peg_ratio"]
                    if peg_ratio_raw == "N/A" or peg_ratio_raw is None:
                        peg_ratio_raw = float("nan")
                        peg_ratio_display = "N/A"
                    else:
                        peg_ratio_display = f"{peg_ratio_raw:.1f}"

                    pb_ratio_raw = stock_data["pb_ratio"]
                    if pb_ratio_raw == "N/A" or pb_ratio_raw is None:
                        pb_ratio_raw = float("nan")
                        pb_ratio_display = "N/A"
                    else:
                        pb_ratio_display = f"{pb_ratio_raw:.1f}"

                    short_percent_float_raw = stock_data.get("short_percent_float", "N/A")
                    if short_percent_float_raw == "N/A" or short_percent_float_raw is None:
                        short_percent_float_val = float("nan")
                        short_percent_float_display = "N/A"
                    else:
                        short_percent_float_val = short_percent_float_raw * 100
                        short_percent_float_display = f"{short_percent_float_val:.1f}%"

                    # Add sort priority for locked symbols (0 = highest priority)
                    sort_priority = locked_symbols.index(symbol)

                    raw_data.append(
                        {
                            "Sort Priority": sort_priority,  # Hidden column for maintaining order
                            "Symbol": symbol,
                            "Company": STOCKS[symbol],
                            "Current Price": stock_data["current_price"],
                            "Current Price Display": f"${stock_data['current_price']:.1f}",
                            "P/E (TTM)": pe_ratio_raw,
                            "P/E (TTM) Display": pe_ratio_display,
                            "EPS (TTM)": eps_raw,
                            "EPS (TTM) Display": eps_display,
                            "PEG Ratio": peg_ratio_raw,
                            "PEG Ratio Display": peg_ratio_display,
                            "P/B Ratio": pb_ratio_raw,
                            "P/B Ratio Display": pb_ratio_display,
                            "Daily Change": percentage_change,  # Store percentage change for sorting
                            "Daily Change Display": f"{change_symbol}{percentage_change:.1f}%",  # Percentage only display
                            "Golden Cross": golden_cross,  # Boolean for sorting
                            "Golden Cross Display": golden_cross_display,  # Display value
                            "Death Cross": death_cross,  # Boolean for sorting
                            "Death Cross Display": death_cross_display,  # Display value
                            "200-Day MA": ma_200d_raw,
                            "200-Day MA Display": ma_200d_display,
                            "50-Day MA Display": ma_50d_display,
                            "50-Day MA": ma_50d_raw,
                            "Short % Float": short_percent_float_val,  # For sorting
                            "Short % Float Display": short_percent_float_display,
                            # Convert volume to millions for sorting and display
                            "Volume": (
                                stock_data["volume"] / 1e6
                                if stock_data["volume"] != "N/A"
                                else float("nan")
                            ),
                            "Volume Display": format_volume(stock_data["volume"]),
                            # Convert average volume to millions for sorting and display
                            "Avg Volume": (
                                stock_data["avg_volume"] / 1e6
                                if stock_data["avg_volume"] != "N/A"
                                else float("nan")
                            ),
                            "Avg Volume Display": format_volume(stock_data["avg_volume"]),
                            # Convert market cap to billions for sorting and display
                            "Market Cap": (
                                stock_data["market_cap"] / 1e9
                                if stock_data["market_cap"] != "N/A"
                                else float("nan")
                            ),
                            "Market Cap Display": format_currency(stock_data["market_cap"]),
                            # Earnings date
                            "Earnings Date": earnings_date,  # Raw date for sorting
                            "Earnings Date Display": earnings_date_display,  # Formatted date for display
                        }
                    )

        # Process remaining symbols (excluding the locked ones)
        for symbol, stock_data in all_stock_data.items():
            if symbol not in locked_symbols and stock_data is not None:
                # Get raw numerical values for sorting
                pe_ratio_raw = stock_data["pe_ratio"]
                if pe_ratio_raw == "N/A" or pe_ratio_raw is None:
                    pe_ratio_raw = float("nan")

                ma_50d_raw = (
                    stock_data["ma_50d"]
                    if stock_data["ma_50d"] is not None
                    else float("nan")
                )
                ma_200d_raw = (
                    stock_data["ma_200d"]
                    if stock_data["ma_200d"] is not None
                    else float("nan")
                )

                # Format for display
                pe_ratio_display = "N/A"
                if (
                    stock_data["pe_ratio"] != "N/A"
                    and stock_data["pe_ratio"] is not None
                ):
                    pe_ratio_display = f"{stock_data['pe_ratio']:.1f}"

                ma_50d_display = "N/A"
                if stock_data["ma_50d"] is not None:
                    ma_50d_display = f"${stock_data['ma_50d']:.1f}"

                ma_200d_display = "N/A"
                if stock_data["ma_200d"] is not None:
                    ma_200d_display = f"${stock_data['ma_200d']:.1f}"

                # Format percentage change
                percentage_change = stock_data["percentage_change"]
                is_positive = percentage_change >= 0
                change_symbol = "+" if is_positive else ""

                # Add to raw data for DataFrame
                # Format Golden Cross and Death Cross indicators with days ago and colors
                golden_cross = stock_data["golden_cross"]
                golden_cross_days_ago = stock_data.get("golden_cross_days_ago")
                if golden_cross and golden_cross_days_ago is not None:
                    golden_cross_display = f"🟢 ({golden_cross_days_ago}d ago)"
                else:
                    golden_cross_display = "🔴"

                death_cross = stock_data["death_cross"]
                death_cross_days_ago = stock_data.get("death_cross_days_ago")
                if death_cross and death_cross_days_ago is not None:
                    death_cross_display = f"🔴 ({death_cross_days_ago}d ago)"
                else:
                    death_cross_display = "🟢"

                # Format earnings date with upcoming/past indicator
                earnings_date = stock_data.get("earnings_date")
                earnings_date_note = None

                if earnings_date is not None:
                    # Check if this is an upcoming or past date
                    current_date = pd.Timestamp.now()
                    is_upcoming = earnings_date > current_date

                    # Format the date with an indicator
                    if is_upcoming:
                        earnings_date_display = f"📅 {earnings_date.strftime('%Y-%m-%d')}"
                    else:
                        earnings_date_display = f"{earnings_date.strftime('%Y-%m-%d')}"
                else:
                    earnings_date_display = "N/A"
                # Format EPS, PEG ratio, and P/B ratio
                eps_raw = stock_data["eps"]
                if eps_raw == "N/A" or eps_raw is None:
                    eps_raw = float("nan")
                    eps_display = "N/A"
                else:
                    eps_display = f"{eps_raw:.1f}"

                peg_ratio_raw = stock_data["peg_ratio"]
                if peg_ratio_raw == "N/A" or peg_ratio_raw is None:
                    peg_ratio_raw = float("nan")
                    peg_ratio_display = "N/A"
                else:
                    peg_ratio_display = f"{peg_ratio_raw:.1f}"

                pb_ratio_raw = stock_data["pb_ratio"]
                if pb_ratio_raw == "N/A" or pb_ratio_raw is None:
                    pb_ratio_raw = float("nan")
                    pb_ratio_display = "N/A"
                else:
                    pb_ratio_display = f"{pb_ratio_raw:.1f}"

                short_percent_float_raw = stock_data.get("short_percent_float", "N/A")
                if short_percent_float_raw == "N/A" or short_percent_float_raw is None:
                    short_percent_float_val = float("nan")
                    short_percent_float_display = "N/A"
                else:
                    short_percent_float_val = short_percent_float_raw * 100
                    short_percent_float_display = f"{short_percent_float_val:.1f}%"

                # Add sort priority for remaining symbols (starting from 3)
                sort_priority = len(locked_symbols) + list(all_stock_data.keys()).index(symbol)

                raw_data.append(
                    {
                        "Sort Priority": sort_priority,  # Hidden column for maintaining order
                        "Symbol": symbol,
                        "Company": STOCKS[symbol],
                        "Current Price": stock_data["current_price"],
                        "Current Price Display": f"${stock_data['current_price']:.1f}",
                        "P/E (TTM)": pe_ratio_raw,
                        "P/E (TTM) Display": pe_ratio_display,
                        "EPS (TTM)": eps_raw,
                        "EPS (TTM) Display": eps_display,
                        "PEG Ratio": peg_ratio_raw,
                        "PEG Ratio Display": peg_ratio_display,
                        "P/B Ratio": pb_ratio_raw,
                        "P/B Ratio Display": pb_ratio_display,
                        "Daily Change": percentage_change,  # Store percentage change for sorting
                        "Daily Change Display": f"{change_symbol}{percentage_change:.1f}%",  # Percentage only display
                        "Golden Cross": golden_cross,  # Boolean for sorting
                        "Golden Cross Display": golden_cross_display,  # Display value
                        "Death Cross": death_cross,  # Boolean for sorting
                        "Death Cross Display": death_cross_display,  # Display value
                        "200-Day MA": ma_200d_raw,
                        "200-Day MA Display": ma_200d_display,
                        "50-Day MA Display": ma_50d_display,
                        "50-Day MA": ma_50d_raw,
                        "Short % Float": short_percent_float_val,  # For sorting
                        "Short % Float Display": short_percent_float_display,
                        # Convert volume to millions for sorting and display
                        "Volume": (
                            stock_data["volume"] / 1e6
                            if stock_data["volume"] != "N/A"
                            else float("nan")
                        ),
                        "Volume Display": format_volume(stock_data["volume"]),
                        # Convert average volume to millions for sorting and display
                        "Avg Volume": (
                            stock_data["avg_volume"] / 1e6
                            if stock_data["avg_volume"] != "N/A"
                            else float("nan")
                        ),
                        "Avg Volume Display": format_volume(stock_data["avg_volume"]),
                        # Convert market cap to billions for sorting and display
                        "Market Cap": (
                            stock_data["market_cap"] / 1e9
                            if stock_data["market_cap"] != "N/A"
                            else float("nan")
                        ),
                        "Market Cap Display": format_currency(stock_data["market_cap"]),
                        # Earnings date
                        "Earnings Date": earnings_date,  # Raw date for sorting
                        "Earnings Date Display": earnings_date_display,  # Formatted date for display
                    }
                )

        # Create DataFrame with both raw and display values
        df_raw = pd.DataFrame(raw_data)

        # Sort by Sort Priority to ensure locked symbols appear first
        df_raw = df_raw.sort_values('Sort Priority')

        # Add a colored display for Golden Cross and Death Cross with symbols and days ago
        def format_golden_cross(row):
            if row["Golden Cross"]:
                days_ago = row.get("Golden Cross Days Ago")
                if days_ago is not None:
                    return f'<span style="color: green; font-weight: bold;">✓ ({days_ago}d ago)</span>'
                return '<span style="color: green; font-weight: bold;">✓</span>'
            return '<span style="color: red; font-weight: bold;">✗</span>'

        def format_death_cross(row):
            if row["Death Cross"]:
                days_ago = row.get("Death Cross Days Ago")
                if days_ago is not None:
                    return f'<span style="color: red; font-weight: bold;">✓ ({days_ago}d ago)</span>'
                return '<span style="color: red; font-weight: bold;">✓</span>'
            return '<span style="color: green; font-weight: bold;">✗</span>'

        # Add days ago to the DataFrame
        df_raw["Golden Cross Days Ago"] = [data.get("golden_cross_days_ago") for data in all_stock_data.values() if data is not None]
        df_raw["Death Cross Days Ago"] = [data.get("death_cross_days_ago") for data in all_stock_data.values() if data is not None]

        # Apply formatting
        df_raw["Golden Cross Colored"] = df_raw.apply(format_golden_cross, axis=1)
        df_raw["Death Cross Colored"] = df_raw.apply(format_death_cross, axis=1)

                # Create a display DataFrame with clickable symbols and other columns
        # (This is now handled by display_df_html below)
        # Create a clean DataFrame for sorting with the raw values (excluding Sort Priority column)
        sort_df = pd.DataFrame(
            {
                "Symbol": df_raw["Symbol"],
                "Company": df_raw["Company"],
                "Current Price": df_raw["Current Price"],
                "P/E (TTM)": df_raw["P/E (TTM)"],
                "EPS (TTM)": df_raw["EPS (TTM)"],
                "PEG Ratio": df_raw["PEG Ratio"],
                "P/B Ratio": df_raw["P/B Ratio"],
                "Daily Change": df_raw["Daily Change"],
                "Golden Cross": df_raw["Golden Cross Display"],
                "Death Cross": df_raw["Death Cross Display"],
                "200-Day MA": df_raw["200-Day MA"],
                "50-Day MA": df_raw["50-Day MA"],
                "Volume": df_raw["Volume"],
                "Avg Volume": df_raw["Avg Volume"],
                "Market Cap": df_raw["Market Cap"],
                "Short % Float": df_raw["Short % Float"],
                "Earnings Date": df_raw["Earnings Date Display"],
            }
        )

        # Format the numeric columns with 1 decimal place
        sort_df["Current Price"] = sort_df["Current Price"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["P/E (TTM)"] = sort_df["P/E (TTM)"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["EPS (TTM)"] = sort_df["EPS (TTM)"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["PEG Ratio"] = sort_df["PEG Ratio"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["P/B Ratio"] = sort_df["P/B Ratio"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["Daily Change"] = sort_df["Daily Change"].map(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")
        sort_df["200-Day MA"] = sort_df["200-Day MA"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["50-Day MA"] = sort_df["50-Day MA"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["Volume"] = sort_df["Volume"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_df["Avg Volume"] = sort_df["Avg Volume"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        # Use the formatted display values for Market Cap (already includes B/M suffix)
        sort_df["Market Cap"] = df_raw["Market Cap Display"]
        sort_df["Short % Float"] = sort_df["Short % Float"].map(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")

        # Create a styled dataframe with Streamlit's built-in sorting
        st.markdown("### 📊 Stock Summary Table")
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <strong>📌 Sorting Instructions:</strong> Click on any column header to sort. Click again to reverse the sort order.
        </div>
        """, unsafe_allow_html=True)

        # Display the dataframe with built-in sorting
        st.dataframe(
            sort_df,
            use_container_width=True,
            height=500,
            column_config={
                "Symbol": st.column_config.TextColumn("Sym", width="small"),
                "Company": st.column_config.TextColumn("Company", width="medium"),
                "Current Price": st.column_config.TextColumn("Price", width="small"),
                "P/E (TTM)": st.column_config.TextColumn("P/E", width="small"),
                "EPS (TTM)": st.column_config.TextColumn("EPS", width="small"),
                "PEG Ratio": st.column_config.TextColumn("PEG", width="small"),
                "P/B Ratio": st.column_config.TextColumn("P/B", width="small"),
                "Daily Change": st.column_config.TextColumn("Chg%", width="small"),
                "Golden Cross": st.column_config.TextColumn("Golden Cross", width="small"),
                "Death Cross": st.column_config.TextColumn("Death Cross", width="small"),
                "200-Day MA": st.column_config.TextColumn("MA200", width="small"),
                "50-Day MA": st.column_config.TextColumn("MA50", width="small"),
                "Volume": st.column_config.TextColumn("Vol", width="small"),
                "Avg Volume": st.column_config.TextColumn("AvgVol", width="small"),
                "Market Cap": st.column_config.TextColumn("MCap", width="small"),
                "Short % Float": st.column_config.TextColumn("Short%", width="small"),
                "Earnings Date": st.column_config.TextColumn("Earnings", width="medium"),
            },
            hide_index=True,
        )
    else:
        st.error("No stock data available to display in summary table")


def main():
    """Main application function"""
    # Initialize session state for selected tab
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = 0

    # Custom styled title - SparkVibe with trumpet logo (reduced header space)
    st.markdown("""
    <h1 style="text-align: center; font-family: 'Times New Roman', serif; font-size: 28px; color: #1E3A8A; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); margin-top: -15px; margin-bottom: -10px;">
        🎺 SparkVibe <span style="font-size: 22px; color: #4B5563;">Finance</span>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #4B5563; margin-top: -5px; margin-bottom: 5px;'>Real-time stock prices and trading metrics for leading tech companies</p>", unsafe_allow_html=True)

    # Sidebar controls
    st.sidebar.title("Controls")

    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30 seconds)", value=False)

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    # Display last update time
    last_update = st.sidebar.empty()

    # Main content area
    with st.spinner("Fetching stock data..."):
        # Fetch data for all stocks
        all_stock_data = {}

        for symbol in STOCKS.keys():
            stock_data = fetch_stock_data(symbol)
            all_stock_data[symbol] = stock_data

    # Update timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_update.text(f"Last updated: {current_time}")

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary Table", "🔍 Golden Cross", "⚠️ Death Cross", "📈 Volume Analysis"])


    with tab1:
        st.subheader("Tech Stocks Summary")
        create_summary_table(all_stock_data)

    with tab2:
        st.subheader("Golden Cross Stocks")
        # Filter stocks with golden cross and remove any None values
        golden_cross_stocks = {symbol: data for symbol, data in all_stock_data.items()
                              if data is not None and data.get("golden_cross", False)}

        if golden_cross_stocks:
            st.success(f"Found {len(golden_cross_stocks)} stocks with a golden cross in the past 30 days")

            # Create a table with stock information - using markdown to avoid st.table's non-interactive nature
            st.markdown("### Golden Cross Stocks")

            # Create a DataFrame for display with clickable symbols
            golden_cross_data = []
            for symbol, data in golden_cross_stocks.items():
                # Format daily change with color
                daily_change = data['percentage_change']
                change_color = "green" if daily_change >= 0 else "red"
                change_symbol = "+" if daily_change >= 0 else ""
                formatted_change = f'<span style="color: {change_color};">{change_symbol}{daily_change:.1f}%</span>'

                golden_cross_data.append({
                    "Symbol": f'<a href="#" onclick="parent.postMessage({{cmd: \'streamlit:setComponentValue\', componentValue: \'{symbol}\', componentKey: \'stock_click\'}}, \'*\'); return false;" style="text-decoration: none; color: #1E88E5; font-weight: bold;">{symbol}</a>',
                    "Company": STOCKS[symbol],
                    "Current Price": f"${data['current_price']:.1f}",
                    "Daily Change": formatted_change,
                    "Golden Cross": f'<span style="color: green; font-weight: bold;">✓ ({data.get("golden_cross_days_ago", "")}d ago)</span>'
                })

            golden_cross_df = pd.DataFrame(golden_cross_data)

            # Create a clean DataFrame for sorting (without HTML formatting)
            sort_golden_cross_df = pd.DataFrame({
                "Symbol": [symbol for symbol in golden_cross_stocks.keys()],
                "Company": [STOCKS[symbol] for symbol in golden_cross_stocks.keys()],
                "Current Price": [data['current_price'] for data in golden_cross_stocks.values()],
                "Daily Change": [data['percentage_change'] for data in golden_cross_stocks.values()],
                "Golden Cross Days": [data.get("golden_cross_days_ago", 0) for data in golden_cross_stocks.values()]
            })

            # Format the numeric columns with 1 decimal place
            sort_golden_cross_df["Current Price"] = sort_golden_cross_df["Current Price"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
            sort_golden_cross_df["Daily Change"] = sort_golden_cross_df["Daily Change"].map(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")
            sort_golden_cross_df["Golden Cross Days"] = sort_golden_cross_df["Golden Cross Days"].map(lambda x: f"{x:.0f}" if not pd.isna(x) else "N/A")

            # Convert numeric columns to strings to preserve formatting
            sort_golden_cross_df = sort_golden_cross_df.astype({"Current Price": str, "Daily Change": str, "Golden Cross Days": str})

            # Display the dataframe with built-in sorting
            st.dataframe(
                sort_golden_cross_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Symbol": st.column_config.TextColumn("Symbol 🔤"),
                    "Company": st.column_config.TextColumn("Company 🏢"),
                    "Current Price": st.column_config.TextColumn("Price 💲"),
                    "Daily Change": st.column_config.TextColumn("Change % 📈"),
                    "Golden Cross Days": st.column_config.TextColumn("Golden Cross (days ago) ✓"),
                },
                hide_index=True,
            )

            # Display charts for all golden cross stocks
            st.markdown("### Golden Cross Charts")

            # Show charts for each stock with golden cross
            for symbol, stock_data in golden_cross_stocks.items():
                st.subheader(f"📊 {symbol} - {STOCKS[symbol]}")

                # Fetch historical data for the past 250 days
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="250d")

                if not hist.empty and len(hist) >= 200:
                    # Calculate moving averages
                    hist['MA50'] = hist['Close'].rolling(window=50).mean()
                    hist['MA200'] = hist['Close'].rolling(window=200).mean()

                    # Create a DataFrame for the chart
                    chart_data = pd.DataFrame({
                        'Date': hist.index,
                        'Price': hist['Close'],
                        '50-Day MA': hist['MA50'],
                        '200-Day MA': hist['MA200']
                    })

                    # Find the crossover point(s)
                    crossover_points = []
                    for i in range(1, len(hist)):
                        if (hist['MA50'].iloc[i] > hist['MA200'].iloc[i] and
                            hist['MA50'].iloc[i-1] <= hist['MA200'].iloc[i-1]):
                            crossover_points.append(i)

                    # Create the chart
                    chart = st.line_chart(
                        chart_data.set_index('Date')[['Price', '50-Day MA', '200-Day MA']]
                    )

                    # Add annotation about the crossover
                    if crossover_points:
                        latest_crossover = crossover_points[-1]
                        crossover_date = hist.index[latest_crossover].strftime('%Y-%m-%d')
                        crossover_price = hist['Close'].iloc[latest_crossover]
                        st.caption(f"⭐ Golden Cross occurred on {crossover_date} at price ${crossover_price:.1f}")

                st.markdown("---")  # Add a separator between charts

            # Add explanation
            st.markdown("### About Golden Cross")
            st.write("A golden cross occurs when the 50-day moving average crosses above the 200-day moving average. "
                     "This is often considered a bullish signal by technical analysts.")
            st.write("The charts above show stocks that have experienced a golden cross in the past 30 days.")
        else:
            st.warning("No stocks with a golden cross in the past 30 days were found")

    with tab3:
        st.subheader("Death Cross Stocks")
        # Filter stocks with death cross and remove any None values
        death_cross_stocks = {symbol: data for symbol, data in all_stock_data.items()
                             if data is not None and data.get("death_cross", False)}

        if death_cross_stocks:
            st.warning(f"Found {len(death_cross_stocks)} stocks with a death cross in the past 30 days")

            # Create a table with stock information - using markdown to avoid st.table's non-interactive nature
            st.markdown("### Death Cross Stocks")

            # Create a DataFrame for display with clickable symbols
            death_cross_data = []
            for symbol, data in death_cross_stocks.items():
                # Format daily change with color
                daily_change = data['percentage_change']
                change_color = "green" if daily_change >= 0 else "red"
                change_symbol = "+" if daily_change >= 0 else ""
                formatted_change = f'<span style="color: {change_color};">{change_symbol}{daily_change:.1f}%</span>'

                death_cross_data.append({
                    "Symbol": f'<a href="#" onclick="parent.postMessage({{cmd: \'streamlit:setComponentValue\', componentValue: \'{symbol}\', componentKey: \'stock_click\'}}, \'*\'); return false;" style="text-decoration: none; color: #1E88E5; font-weight: bold;">{symbol}</a>',
                    "Company": STOCKS[symbol],
                    "Current Price": f"${data['current_price']:.1f}",
                    "Daily Change": formatted_change,
                    "Death Cross": f'<span style="color: red; font-weight: bold;">✓ ({data.get("death_cross_days_ago", "")}d ago)</span>'
                })

            death_cross_df = pd.DataFrame(death_cross_data)

            # Create a clean DataFrame for sorting (without HTML formatting)
            sort_death_cross_df = pd.DataFrame({
                "Symbol": [symbol for symbol in death_cross_stocks.keys()],
                "Company": [STOCKS[symbol] for symbol in death_cross_stocks.keys()],
                "Current Price": [data['current_price'] for data in death_cross_stocks.values()],
                "Daily Change": [data['percentage_change'] for data in death_cross_stocks.values()],
                "Death Cross Days": [data.get("death_cross_days_ago", 0) for data in death_cross_stocks.values()]
            })

            # Format the numeric columns with 1 decimal place
            sort_death_cross_df["Current Price"] = sort_death_cross_df["Current Price"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
            sort_death_cross_df["Daily Change"] = sort_death_cross_df["Daily Change"].map(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")
            sort_death_cross_df["Death Cross Days"] = sort_death_cross_df["Death Cross Days"].map(lambda x: f"{x:.0f}" if not pd.isna(x) else "N/A")

            # Convert numeric columns to strings to preserve formatting
            sort_death_cross_df = sort_death_cross_df.astype({"Current Price": str, "Daily Change": str, "Death Cross Days": str})

            # Display the dataframe with built-in sorting
            st.dataframe(
                sort_death_cross_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Symbol": st.column_config.TextColumn("Symbol 🔤"),
                    "Company": st.column_config.TextColumn("Company 🏢"),
                    "Current Price": st.column_config.TextColumn("Price 💲"),
                    "Daily Change": st.column_config.TextColumn("Change % 📈"),
                    "Death Cross Days": st.column_config.TextColumn("Death Cross (days ago) ⚠️"),
                },
                hide_index=True,
            )

            # Display charts for all death cross stocks
            st.markdown("### Death Cross Charts")

            # Show charts for each stock with death cross
            for symbol, stock_data in death_cross_stocks.items():
                st.subheader(f"📊 {symbol} - {STOCKS[symbol]}")

                # Fetch historical data for the past 250 days
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="250d")

                if not hist.empty and len(hist) >= 200:
                    # Calculate moving averages
                    hist['MA50'] = hist['Close'].rolling(window=50).mean()
                    hist['MA200'] = hist['Close'].rolling(window=200).mean()

                    # Create a DataFrame for the chart
                    chart_data = pd.DataFrame({
                        'Date': hist.index,
                        'Price': hist['Close'],
                        '50-Day MA': hist['MA50'],
                        '200-Day MA': hist['MA200']
                    })

                    # Find the crossover point(s)
                    crossover_points = []
                    for i in range(1, len(hist)):
                        if (hist['MA50'].iloc[i] < hist['MA200'].iloc[i] and
                            hist['MA50'].iloc[i-1] >= hist['MA200'].iloc[i-1]):
                            crossover_points.append(i)

                    # Create the chart
                    chart = st.line_chart(
                        chart_data.set_index('Date')[['Price', '50-Day MA', '200-Day MA']]
                    )

                    # Add annotation about the crossover
                    if crossover_points:
                        latest_crossover = crossover_points[-1]
                        crossover_date = hist.index[latest_crossover].strftime('%Y-%m-%d')
                        crossover_price = hist['Close'].iloc[latest_crossover]
                        st.caption(f"⚠️ Death Cross occurred on {crossover_date} at price ${crossover_price:.1f}")

                st.markdown("---")  # Add a separator between charts

            # Add explanation
            st.markdown("### About Death Cross")
            st.write("A death cross occurs when the 50-day moving average crosses below the 200-day moving average. "
                     "This is often considered a bearish signal by technical analysts.")
            st.write("The charts above show stocks that have experienced a death cross in the past 30 days.")
        else:
            st.info("No stocks with a death cross in the past 30 days were found")

    with tab4:
        st.subheader("Volume Analysis")
        st.write("Compare trading volume with average volume over time for each stock.")

        # Define a list of important stocks to show volume charts for
        # Start with market indices and ETFs, then add major tech stocks
        important_stocks = ["^VIX", "SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "AMD"]

        # Display a message about the stocks being shown
        st.info(f"Showing volume analysis for {len(important_stocks)} key stocks. Scroll down to view all charts.")

        # Create a table with stock information
        st.markdown("### Volume Analysis Stocks")

        # Create a DataFrame for display with clickable symbols
        volume_analysis_data = []
        for symbol in important_stocks:
            if symbol in all_stock_data and all_stock_data[symbol] is not None:
                data = all_stock_data[symbol]
                # Format daily change with color
                daily_change = data['percentage_change']
                change_color = "green" if daily_change >= 0 else "red"
                change_symbol = "+" if daily_change >= 0 else ""
                formatted_change = f'<span style="color: {change_color};">{change_symbol}{daily_change:.1f}%</span>'

                # Calculate volume ratio
                current_volume = data['volume']
                avg_volume = data['avg_volume']
                if avg_volume != "N/A" and avg_volume > 0:
                    volume_ratio = current_volume / avg_volume
                    volume_ratio_display = f"{volume_ratio:.1f}x"
                    # Color code the volume ratio
                    if volume_ratio > 1.5:
                        volume_ratio_display = f'<span style="color: red; font-weight: bold;">{volume_ratio:.1f}x</span>'
                    elif volume_ratio < 0.5:
                        volume_ratio_display = f'<span style="color: green; font-weight: bold;">{volume_ratio:.1f}x</span>'
                else:
                    volume_ratio_display = "N/A"

                volume_analysis_data.append({
                    "Symbol": f'<a href="#" onclick="parent.postMessage({{cmd: \'streamlit:setComponentValue\', componentValue: \'{symbol}\', componentKey: \'stock_click\'}}, \'*\'); return false;" style="text-decoration: none; color: #1E88E5; font-weight: bold;">{symbol}</a>',
                    "Company": STOCKS[symbol],
                    "Current Price": f"${data['current_price']:.2f}",
                    "Daily Change": formatted_change,
                    "Volume": f"{data['volume']/1e6:.1f}M",
                    "Avg Volume": f"{data['avg_volume']/1e6:.1f}M" if data['avg_volume'] != "N/A" else "N/A",
                    "Volume/Avg Ratio": volume_ratio_display
                })

        volume_analysis_df = pd.DataFrame(volume_analysis_data)

        # Create a clean DataFrame for sorting (without HTML formatting)
        sort_volume_df = pd.DataFrame({
            "Symbol": [symbol for symbol in important_stocks if symbol in all_stock_data and all_stock_data[symbol] is not None],
            "Company": [STOCKS[symbol] for symbol in important_stocks if symbol in all_stock_data and all_stock_data[symbol] is not None],
            "Current Price": [all_stock_data[symbol]['current_price'] for symbol in important_stocks if symbol in all_stock_data and all_stock_data[symbol] is not None],
            "Daily Change": [all_stock_data[symbol]['percentage_change'] for symbol in important_stocks if symbol in all_stock_data and all_stock_data[symbol] is not None],
            "Volume": [all_stock_data[symbol]['volume']/1e6 for symbol in important_stocks if symbol in all_stock_data and all_stock_data[symbol] is not None],
            "Avg Volume": [all_stock_data[symbol]['avg_volume']/1e6 if all_stock_data[symbol]['avg_volume'] != "N/A" else float('nan') for symbol in important_stocks if symbol in all_stock_data and all_stock_data[symbol] is not None]
        })

        # Calculate Volume/Avg Ratio
        volume_ratios = []
        for symbol in important_stocks:
            if symbol in all_stock_data and all_stock_data[symbol] is not None:
                data = all_stock_data[symbol]
                current_volume = data['volume']
                avg_volume = data['avg_volume']
                if avg_volume != "N/A" and avg_volume > 0:
                    volume_ratio = current_volume / avg_volume
                else:
                    volume_ratio = float('nan')
                volume_ratios.append(volume_ratio)

        # Add Volume/Avg Ratio to the DataFrame
        sort_volume_df["Volume/Avg Ratio"] = volume_ratios

        # Format the numeric columns with 1 decimal place
        sort_volume_df["Volume"] = sort_volume_df["Volume"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_volume_df["Avg Volume"] = sort_volume_df["Avg Volume"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_volume_df["Current Price"] = sort_volume_df["Current Price"].map(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        sort_volume_df["Daily Change"] = sort_volume_df["Daily Change"].map(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")
        sort_volume_df["Volume/Avg Ratio"] = sort_volume_df["Volume/Avg Ratio"].map(lambda x: f"{x:.1f}x" if not pd.isna(x) else "N/A")

        # Display the dataframe with built-in sorting
        st.dataframe(
            sort_volume_df,
            use_container_width=True,
            height=400,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol 🔤"),
                "Company": st.column_config.TextColumn("Company 🏢"),
                "Current Price": st.column_config.TextColumn("Price 💲"),
                "Daily Change": st.column_config.TextColumn("Change % 📈"),
                "Volume": st.column_config.TextColumn("Volume (M) 📊"),
                "Avg Volume": st.column_config.TextColumn("Avg Vol (M) 📊"),
                "Volume/Avg Ratio": st.column_config.TextColumn("Vol/Avg Ratio 📈"),
            },
            hide_index=True,
        )

        # Display charts for all important stocks
        st.markdown("### Volume Charts")

        # Show charts for each important stock
        for symbol in important_stocks:
            st.subheader(f"📊 {symbol} - {STOCKS[symbol]}")

            with st.spinner(f"Fetching volume data for {symbol}..."):
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2y")  # Get 2 years of data

            # Get earnings dates
            earnings_dates = pd.DataFrame()  # Initialize empty DataFrame

            # For META, use the provided list of earnings dates
            if symbol == "META":
                # Use the list of META earnings dates provided by the user
                meta_earnings_dates = [
                    ("July 30, 2025", "Q2 2025"),
                    ("April 30, 2025", "Q1 2025"),
                    ("January 29, 2025", "Q4 2024"),
                    ("October 29, 2024", "Q3 2024"),
                    ("July 30, 2024", "Q2 2024"),
                    ("April 24, 2024", "Q1 2024"),
                    ("February 1, 2024", "Q4 2023"),
                    ("October 25, 2023", "Q3 2023")
                ]

                # Convert to timestamps and create DataFrame
                meta_dates = [pd.Timestamp(date) for date, quarter in meta_earnings_dates]
                meta_quarters = [quarter for date, quarter in meta_earnings_dates]

                # Create DataFrame with dates as index and quarters as a column
                earnings_dates = pd.DataFrame({'Quarter': meta_quarters}, index=meta_dates)

                st.success(f"Using {len(meta_earnings_dates)} provided META earnings dates")
            # For other stocks, try to fetch from Yahoo Finance
            elif symbol not in ["^VIX", "SPY", "QQQ", "GLD", "SLV", "BTC-USD"]:
                try:
                    # Get earnings dates from Yahoo Finance API
                    api_earnings_dates = ticker.get_earnings_dates(limit=20)
                    if api_earnings_dates is not None and not api_earnings_dates.empty:
                        earnings_dates = api_earnings_dates[~api_earnings_dates.index.duplicated(keep='first')]
                        st.success(f"Found {len(earnings_dates)} earnings dates from Yahoo Finance")
                    else:
                        st.warning("No earnings dates found from Yahoo Finance")
                except Exception as e:
                    st.warning(f"Could not fetch earnings dates: {str(e)}")

            if not hist.empty:
                # Calculate the average volume (30-day moving average)
                hist['Avg_Volume'] = hist['Volume'].rolling(window=30).mean()

                # Create a DataFrame for the chart
                volume_data = pd.DataFrame({
                    'Date': hist.index,
                    'Volume': hist['Volume'],
                    'Avg Volume (30-day MA)': hist['Avg_Volume']
                })

                # Display the chart
                st.subheader(f"Volume Analysis for {symbol} - {STOCKS[symbol]}")

                # Convert volume to millions for better readability
                volume_data['Volume (M)'] = volume_data['Volume'] / 1e6
                volume_data['Avg Volume (M)'] = volume_data['Avg Volume (30-day MA)'] / 1e6

                # Create the chart with earnings dates marked
                try:
                    # Create figure with secondary y-axis
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    # Add volume bars
                    fig.add_trace(
                        go.Bar(
                            x=volume_data['Date'],
                            y=volume_data['Volume (M)'],
                            name="Volume (M)",
                            marker_color='rgba(58, 71, 80, 0.6)',
                            opacity=0.7
                        ),
                        secondary_y=False,
                    )

                    # Add average volume line
                    fig.add_trace(
                        go.Scatter(
                            x=volume_data['Date'],
                            y=volume_data['Avg Volume (M)'],
                            name="30-Day Avg Volume (M)",
                            line=dict(color='rgba(246, 78, 139, 1.0)', width=2)
                        ),
                        secondary_y=False,
                    )

                    # Add price line on secondary axis
                    fig.add_trace(
                        go.Scatter(
                            x=hist.index,
                            y=hist['Close'],
                            name="Price",
                            line=dict(color='rgba(31, 119, 180, 1.0)', width=1)
                        ),
                        secondary_y=True,
                    )

                    # Initialize lists for earnings data
                    valid_earnings_dates = []
                    earnings_notes = []

                    # Add earnings date markers if available
                    if not earnings_dates.empty:
                        # Filter earnings dates to only include those within our historical data range
                        for date in earnings_dates.index:
                            try:
                                if date in hist.index or date >= hist.index[0]:
                                    # Find the closest date in our historical data
                                    closest_date = min(hist.index, key=lambda x: abs(x - date))

                                    # Get the volume and price for this date
                                    if closest_date in volume_data.set_index('Date').index:
                                        volume_value = volume_data.set_index('Date').loc[closest_date, 'Volume (M)']
                                        price_value = hist.loc[closest_date, 'Close']

                                        valid_earnings_dates.append({
                                            'date': date,
                                            'volume': volume_value,
                                            'price': price_value
                                        })

                                        # Format the earnings date for display
                                        earnings_notes.append(f"• {date.strftime('%Y-%m-%d')}: ${price_value:.1f}, Vol: {volume_value:.1f}M")
                            except Exception as e:
                                st.warning(f"Error processing earnings date {date}: {str(e)}")
                                pass  # Continue with other dates

                    # DIRECT META EARNINGS DATE HANDLING - ADD ALL META EARNINGS DATES
                    if symbol == "META":
                        # Use the list of META earnings dates provided by the user
                        meta_earnings_dates = [
                            ("July 30, 2025", "Q2 2025"),
                            ("April 30, 2025", "Q1 2025"),
                            ("January 29, 2025", "Q4 2024"),
                            ("October 29, 2024", "Q3 2024"),
                            ("July 30, 2024", "Q2 2024"),
                            ("April 24, 2024", "Q1 2024"),
                            ("February 1, 2024", "Q4 2023"),
                            ("October 25, 2023", "Q3 2023")
                        ]

                        # Create a separate trace just for META's earnings dates
                        try:
                            # Use the most recent date in historical data for volume/price values
                            closest_date = hist.index[-1]

                            # Get the volume and price for this date
                            volume_value = volume_data.set_index('Date').loc[closest_date, 'Volume (M)']
                            price_value = hist.loc[closest_date, 'Close']

                            # Convert dates to timestamps
                            meta_dates = [pd.Timestamp(date) for date, quarter in meta_earnings_dates]
                            meta_quarters = [quarter for date, quarter in meta_earnings_dates]

                            # Add a special trace for META's earnings dates with large red star markers
                            fig.add_trace(
                                go.Scatter(
                                    x=meta_dates,
                                    y=[volume_value * 1.2] * len(meta_dates),  # Make them stand out
                                    mode='markers',
                                    name='META Earnings',
                                    marker=dict(
                                        symbol='star',
                                        size=15,  # Larger than regular earnings markers
                                        color='red',  # Different color to stand out
                                        line=dict(color='black', width=2)
                                    ),
                                    hovertemplate='META Earnings: %{x}<br>Quarter: %{text}<extra></extra>',
                                    text=meta_quarters
                                ),
                                secondary_y=False,
                            )

                            # Add markers on price line too
                            fig.add_trace(
                                go.Scatter(
                                    x=meta_dates,
                                    y=[price_value] * len(meta_dates),
                                    mode='markers',
                                    name='META Earnings (Price)',
                                    marker=dict(
                                        symbol='star',
                                        size=10,  # Smaller on the price line
                                        color='red',  # Different color to stand out
                                        line=dict(color='black', width=1)
                                    ),
                                    hovertemplate='META Earnings: %{x}<br>Quarter: %{text}<extra></extra>',
                                    text=meta_quarters,
                                    showlegend=False
                                ),
                                secondary_y=True,
                            )

                            # Add to earnings notes for the expander section
                            for date, quarter in meta_earnings_dates:
                                earnings_notes.append(f"• {date} (META {quarter}): ${price_value:.1f}")

                            st.success(f"✅ Successfully added {len(meta_earnings_dates)} META earnings dates with red star markers")
                        except Exception as e:
                            st.error(f"Could not add META earnings date markers: {str(e)}")

                    # Add markers for earnings dates if we found any valid ones
                    if valid_earnings_dates:
                        earnings_x = [item['date'] for item in valid_earnings_dates]
                        earnings_y_volume = [item['volume'] for item in valid_earnings_dates]
                        earnings_y_price = [item['price'] for item in valid_earnings_dates]

                        # Add markers on volume bars for earnings dates
                        fig.add_trace(
                            go.Scatter(
                                x=earnings_x,
                                y=earnings_y_volume,
                                mode='markers',
                                name='Earnings Date',
                                marker=dict(
                                    symbol='star',
                                    size=12,
                                    color='yellow',
                                    line=dict(color='black', width=1)
                                ),
                                hovertemplate='Earnings Date: %{x}<br>Volume: %{y:.1f}M<extra></extra>'
                            ),
                            secondary_y=False,
                        )

                        # Add markers on price line for earnings dates
                        fig.add_trace(
                            go.Scatter(
                                x=earnings_x,
                                y=earnings_y_price,
                                mode='markers',
                                name='Earnings Date (Price)',
                                marker=dict(
                                    symbol='star',
                                    size=8,
                                    color='gold',
                                    line=dict(color='black', width=1)
                                ),
                                hovertemplate='Earnings Date: %{x}<br>Price: $%{y:.1f}<extra></extra>',
                                showlegend=False
                            ),
                            secondary_y=True,
                        )

                    # Update layout
                    fig.update_layout(
                        title=f"Volume (M) Analysis for {symbol} with Earnings Dates",
                        xaxis_title="Date",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        hovermode="x unified",
                        height=500,
                    )

                    # Set y-axes titles
                    fig.update_yaxes(title_text="Volume (M)", secondary_y=False)
                    fig.update_yaxes(title_text="Price ($)", secondary_y=True)

                    # Display the interactive chart
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    # Fallback to Streamlit's built-in charts
                    st.warning(f"Could not create interactive chart with earnings dates: {str(e)}")
                    st.line_chart(
                        volume_data.set_index('Date')[['Volume (M)', 'Avg Volume (M)']]
                    )

                # Display earnings dates in a separate section if available
                if not earnings_dates.empty and len(earnings_notes) > 0:
                    with st.expander("View Earnings Dates (Past 2 Years)", expanded=True):
                        st.markdown("### Earnings Dates")
                        st.markdown("\n".join(earnings_notes))
                        st.markdown("*Yellow stars on the chart mark earnings announcement dates*")

                # Calculate and display volume metrics
                current_volume = hist['Volume'].iloc[-1]
                avg_volume = hist['Avg_Volume'].iloc[-1] if not pd.isna(hist['Avg_Volume'].iloc[-1]) else 0
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Latest Volume (M)",
                        format_volume(current_volume)
                    )

                with col2:
                    st.metric(
                        "30-Day Avg Volume (M)",
                        format_volume(avg_volume)
                    )

                with col3:
                    # Format the ratio with color based on whether volume is above or below average
                    ratio_delta = f"{volume_ratio:.1f}x" if volume_ratio > 0 else "N/A"
                    ratio_color = "normal"
                    if volume_ratio > 1.5:
                        ratio_color = "off"  # High volume (red in Streamlit)
                    elif volume_ratio < 0.5:
                        ratio_color = "inverse"  # Low volume (green in Streamlit)

                    st.metric(
                        "Volume/Avg Ratio",
                        ratio_delta,
                        delta_color=ratio_color
                    )

                # Add some analysis text
                st.markdown("### Volume Analysis")

                if volume_ratio > 1.5:
                    st.info(f"**High Volume Alert**: {symbol} is trading at {volume_ratio:.1f}x its 30-day average volume. "
                           "Unusually high volume may indicate significant market interest or news affecting the stock.")
                elif volume_ratio < 0.5:
                    st.info(f"**Low Volume Alert**: {symbol} is trading at only {volume_ratio:.1f}x its 30-day average volume. "
                           "Low volume may indicate reduced market interest or a quiet trading period.")
                else:
                    st.info(f"{symbol} is trading at normal volume levels relative to its 30-day average.")

                # Show volume trend over time
                st.subheader("Volume (M) Trend Analysis")

                # Calculate weekly average volumes
                weekly_vol = hist['Volume'].resample('W').mean()

                # Compare recent weeks
                if len(weekly_vol) >= 4:
                    recent_week = weekly_vol.iloc[-1]
                    previous_week = weekly_vol.iloc[-2]
                    week_change = ((recent_week - previous_week) / previous_week) * 100 if previous_week > 0 else 0

                    week_change_text = f"increased by {week_change:.1f}%" if week_change > 0 else f"decreased by {abs(week_change):.1f}%"

                    st.write(f"Weekly average volume has {week_change_text} compared to the previous week.")

            else:
                st.error(f"Could not fetch volume data for {symbol}")

    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(30)
        st.rerun()

    # Footer information
    st.markdown("---")
    st.markdown(
        "**Note:** Stock prices are fetched from Yahoo Finance and may have a slight delay. This application is for informational purposes only and should not be used as the sole basis for investment decisions."
    )


if __name__ == "__main__":
    main()
