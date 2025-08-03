"""
Constants and configuration for SparkVibe Finance application
"""

# Define global decimal precision
DECIMAL_PRECISION = 1

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

# CSS styling for the application
CSS_STYLES = """
<style>
    .main > div {
        padding-top: 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #1f77b4;
    }

    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }

    .stDataFrame {
        border: 2px solid #e6e6e6;
        border-radius: 10px;
        overflow: hidden;
    }

    .stDataFrame > div {
        border-radius: 10px;
    }

    /* Center align table content */
    .stDataFrame table {
        text-align: center;
        width: 100%;
    }

    .stDataFrame th {
        text-align: center !important;
        padding: 8px 4px !important;
    }

    .stDataFrame td {
        text-align: center !important;
        padding: 8px 4px !important;
    }

    /* Control column widths to prevent Company column from being too wide */
    .stDataFrame table th:nth-child(1),
    .stDataFrame table td:nth-child(1) {
        max-width: 120px !important;
        width: 120px !important;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* Ensure other columns have reasonable widths */
    .stDataFrame table th:nth-child(2),
    .stDataFrame table td:nth-child(2) {
        width: 80px !important;
    }

    .stDataFrame table th:nth-child(3),
    .stDataFrame table td:nth-child(3) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(4),
    .stDataFrame table td:nth-child(4) {
        width: 80px !important;
    }

    .stDataFrame table th:nth-child(5),
    .stDataFrame table td:nth-child(5) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(6),
    .stDataFrame table td:nth-child(6) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(7),
    .stDataFrame table td:nth-child(7) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(8),
    .stDataFrame table td:nth-child(8) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(9),
    .stDataFrame table td:nth-child(9) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(10),
    .stDataFrame table td:nth-child(10) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(11),
    .stDataFrame table td:nth-child(11) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(12),
    .stDataFrame table td:nth-child(12) {
        width: 90px !important;
    }

    .stDataFrame table th:nth-child(13),
    .stDataFrame table td:nth-child(13) {
        width: 100px !important;
    }
</style>
"""
