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
"""
