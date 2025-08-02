Requirements Document: Tech Stock Monitor Application

1. Introduction

1.1 Purpose

This document outlines the requirements for a web-based Tech Stock Monitor application, designed to provide real-time stock prices and trading metrics for a predefined set of technology companies, indices, ETFs, and cryptocurrencies. The application aims to deliver a user-friendly interface with comprehensive stock data visualization and analysis tools, accessible via a web browser.

1.2 Scope

The Tech Stock Monitor application will:





Fetch and display real-time stock data for a predefined list of symbols using the Yahoo Finance API.



Present data in a tabular format with sorting capabilities and interactive charts.



Provide technical analysis indicators, including Golden Cross and Death Cross signals.



Offer volume analysis with comparisons to historical averages.



Include a customizable, visually appealing interface with a professional theme inspired by Visual Studio Code aesthetics.



Support auto-refresh and manual refresh functionalities for data updates.

1.3 Definitions, Acronyms, and Abbreviations





Golden Cross: A bullish technical indicator where the 50-day moving average crosses above the 200-day moving average.



Death Cross: A bearish technical indicator where the 50-day moving average crosses below the 200-day moving average.



MA: Moving Average (e.g., 50-day MA, 200-day MA).



P/E Ratio: Price-to-Earnings ratio (Trailing Twelve Months).



EPS: Earnings Per Share (Trailing Twelve Months).



PEG Ratio: Price/Earnings to Growth ratio.



P/B Ratio: Price-to-Book ratio.



Streamlit: An open-source Python framework for building web applications.



Yahoo Finance (yf): A Python library (yfinance) for accessing financial data from Yahoo Finance.



Plotly: A Python library for creating interactive charts.

2. Overall Description

2.1 User Needs

The application targets users interested in monitoring stock market performance, particularly for technology companies, indices, ETFs, and select cryptocurrencies. Users include:





Individual investors seeking real-time stock data and technical indicators.



Financial analysts requiring quick access to key metrics and trends.



Traders interested in volume analysis and market signals (e.g., Golden Cross, Death Cross).

2.2 Assumptions and Dependencies





Assumptions:





Users have a stable internet connection to fetch real-time data from Yahoo Finance.



Yahoo Finance API (via yfinance library) remains available and reliable.



Users are familiar with basic stock market terminology and metrics.



Dependencies:





Python libraries: streamlit, yfinance, pandas, numpy, plotly.



Web browser compatibility for Streamlit applications.



No local file I/O or network calls beyond Yahoo Finance API requests.

3. System Features

3.1 Stock Data Retrieval

3.1.1 Description

The application shall fetch real-time and historical stock data for a predefined list of stock symbols using the Yahoo Finance API.

3.1.2 Functional Requirements





FR1.1: Retrieve data for a predefined list of 36 stock symbols, including indices (e.g., ^VIX), ETFs (e.g., SPY, QQQ), cryptocurrencies (e.g., BTC-USD), and individual companies (e.g., AAPL, MSFT).



FR1.2: For each symbol, fetch the following metrics:





Current price, open price, high price, low price, volume, average volume.



Daily change (absolute and percentage).



Market capitalization.



50-day and 200-day moving averages.



P/E ratio, EPS, PEG ratio, P/B ratio, short percentage of float.



Earnings date (upcoming or most recent past).



FR1.3: Handle special cases:





Skip earnings date retrieval for indices, ETFs, and cryptocurrencies.



Provide hardcoded earnings dates for specific companies (e.g., META) if API data is unavailable.



Use estimated earnings dates based on typical earnings months for select companies if no data is available.



FR1.4: Implement error handling for API failures (e.g., HTTP 404, 429, 401) with appropriate user notifications (warnings or errors).



FR1.5: Format numerical data:





Display market capitalization in billions (B) or millions (M) as appropriate.



Display volume and average volume in millions (M).



Limit all numerical displays to one decimal place.

3.2 User Interface

3.2.1 Description

The application shall provide a web-based interface using Streamlit with a professional, customizable theme inspired by Visual Studio Code.

3.2.2 Functional Requirements





FR2.1: Configure the Streamlit page with:





Page title: "Tech Stock Monitor VSCode".



Page icon: 📈.



Wide layout for optimal data display.



Expanded sidebar by default.



FR2.2: Apply a custom CSS theme with:





Primary color (#1E88E5), secondary color (#5E35B1), background color (#f0f2f6), text color (#212529), header color (#1a237e).



Styled headers, sidebar, metric cards, buttons, tables, tabs, and charts.



Hover effects for metric cards and buttons.



Responsive table styling with alternating row colors and hover effects.



FR2.3: Display a centered title "SparkVibe Finance" with a trumpet emoji (🎺) and a subtitle describing the application's purpose.



FR2.4: Provide a sidebar with:





A title ("Controls").



A checkbox for enabling/disabling auto-refresh every 30 seconds.



A manual refresh button to trigger immediate data updates.



A placeholder for displaying the last update timestamp.



FR2.5: Include a footer with a disclaimer about data delays and informational use only.

3.3 Data Visualization

3.3.1 Description

The application shall display stock data in multiple views, including a summary table, Golden Cross analysis, Death Cross analysis, and volume analysis, using interactive tables and charts.

3.3.2 Functional Requirements





FR3.1 Summary Table:





Display a table with columns: Symbol, Company, Current Price, P/E (TTM), EPS (TTM), PEG Ratio, P/B Ratio, Daily Change, Golden Cross, Death Cross, 50-Day MA, 200-Day MA, Short % Float, Volume, Avg Volume, Market Cap, Earnings Date.



Prioritize display order: ^VIX, SPY, QQQ at the top, followed by other symbols alphabetically.



Allow sorting by clicking column headers.



Format numerical columns with one decimal place and appropriate units (e.g., $ for prices, % for percentages, M for volumes).



Display Golden Cross and Death Cross with colored indicators (green/red) and days since occurrence.



Mark earnings dates as "upcoming" or "past" with a calendar emoji for upcoming dates.



FR3.2 Golden Cross Tab:





Filter and display stocks with a Golden Cross in the past 30 days.



Show a table with columns: Symbol, Company, Current Price, Daily Change, Golden Cross (with days ago).



Include clickable symbols for potential future interactivity.



Display line charts for each stock showing price, 50-day MA, and 200-day MA over 250 days.



Annotate charts with the date and price of the latest Golden Cross.



Provide an explanation of the Golden Cross indicator.



FR3.3 Death Cross Tab:





Filter and display stocks with a Death Cross in the past 30 days.



Show a table with columns: Symbol, Company, Current Price, Daily Change, Death Cross (with days ago).



Include clickable symbols for potential future interactivity.



Display line charts for each stock showing price, 50-day MA, and 200-day MA over 250 days.



Annotate charts with the date and price of the latest Death Cross.



Provide an explanation of the Death Cross indicator.



FR3.4 Volume Analysis Tab:





Display volume analysis for a subset of 11 key stocks (^VIX, SPY, QQQ, AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, AMD).



Show a table with columns: Symbol, Company, Current Price, Daily Change, Volume, Avg Volume, Volume/Avg Ratio.



Highlight Volume/Avg Ratio in red (>1.5x) or green (<0.5x) to indicate high or low volume.



Display interactive Plotly charts for each stock showing:





Volume bars (in millions) over 2 years.



30-day average volume line.



Price line on a secondary y-axis.



Earnings date markers (yellow stars for general stocks, red stars for META) with hover information.



Include an expandable section listing earnings dates with volume and price data.



Provide metrics for latest volume, 30-day average volume, and volume/avg ratio with color-coded indicators.



Offer textual analysis of volume trends (e.g., high/low volume alerts, weekly volume change).

3.4 Data Refresh

3.4.1 Description

The application shall support both manual and automatic data refresh to ensure up-to-date information.

3.4.2 Functional Requirements





FR4.1: Provide a manual refresh button in the sidebar to trigger immediate data updates.



FR4.2: Offer an auto-refresh option (default: off) to update data every 30 seconds.



FR4.3: Display a spinner during data fetching to indicate loading.



FR4.4: Show the last update timestamp in the sidebar.

3.5 Error Handling and Notifications

3.5.1 Description

The application shall handle errors gracefully and provide user-friendly notifications for API failures or data unavailability.

3.5.2 Functional Requirements





FR5.1: Display warning messages for specific API errors (e.g., 404: symbol not found, 429: rate limit exceeded, 401: unauthorized access).



FR5.2: Show error messages for general data fetching failures.



FR5.3: Skip symbols with no recent data and notify the user with a warning.



FR5.4: Use Streamlit's built-in notification components (st.warning, st.error, st.info, st.success) with custom styling.

4. Non-Functional Requirements

4.1 Performance





NFR1.1: Data fetching for all 36 symbols should complete within 10 seconds under normal network conditions.



NFR1.2: Charts and tables should render within 2 seconds after data is fetched.



NFR1.3: Auto-refresh should not cause noticeable UI lag.

4.2 Usability





NFR2.1: The interface should be intuitive, with clear labels and instructions for sorting tables.



NFR2.2: Visual elements (e.g., colors, fonts) should be consistent with the Visual Studio Code-inspired theme.



NFR2.3: The application should be accessible on desktop and tablet browsers.

4.3 Reliability





NFR3.1: The application should handle intermittent API failures gracefully without crashing.



NFR3.2: Fallback mechanisms (e.g., hardcoded earnings dates, estimated dates) should ensure data availability for key stocks.

4.4 Maintainability





NFR4.1: Code should be modular, with separate functions for data fetching, formatting, and display.



NFR4.2: Use descriptive variable names and comments for maintainability.



NFR4.3: Maintain a single source of truth for stock symbols and company names.

4.5 Security





NFR5.1: No local file I/O or external network calls beyond Yahoo Finance API.



NFR5.2: Sanitize all data inputs from the API to prevent injection attacks.

5. System Architecture

5.1 Technology Stack





Frontend: Streamlit for web interface, Plotly for interactive charts.



Backend: Python with yfinance for data retrieval, pandas for data processing, numpy for numerical computations.



Styling: Custom CSS for Visual Studio Code-inspired theme.

5.2 Data Flow





Data Retrieval: The application queries Yahoo Finance API for each stock symbol to fetch real-time and historical data.



Data Processing: Data is processed to calculate moving averages, daily changes, and technical indicators (Golden Cross, Death Cross).



Data Display: Processed data is displayed in tables and charts across four tabs (Summary, Golden Cross, Death Cross, Volume Analysis).



User Interaction: Users can sort tables, toggle auto-refresh, and manually refresh data.

6. Constraints





The application relies on the availability and rate limits of the Yahoo Finance API.



No support for user-defined stock symbols in the initial version.



Limited to a predefined set of 36 symbols.



Earnings date fetching may be incomplete for some stocks due to API limitations.



Plotly charts are used for volume analysis, with a fallback to Streamlit charts if Plotly fails.

7. Future Enhancements





Support for user-defined stock symbols.



Additional technical indicators (e.g., RSI, MACD).



Integration with other financial data sources for redundancy.



Enhanced interactivity (e.g., clicking a symbol to view detailed stock profiles).



Mobile optimization for the Streamlit interface.

8. Acceptance Criteria





AC1: The application successfully fetches and displays data for at least 90% of the predefined stock symbols under normal conditions.



AC2: All tables are sortable by clicking column headers, with correct ordering of numerical and categorical data.



AC3: Golden Cross and Death Cross tabs correctly identify and display stocks with recent crossovers, including charts with annotations.



AC4: Volume Analysis tab displays interactive charts with earnings date markers for all 11 key stocks.



AC5: The interface adheres to the Visual Studio Code-inspired theme with consistent styling across all components.



AC6: Auto-refresh updates data every 30 seconds when enabled, and manual refresh triggers immediate updates.



AC7: Error messages are displayed for API failures, and the application remains functional for unaffected symbols.

9. Appendices

9.1 Stock Symbols and Company Names

The application shall support the following symbols, prioritized with ^VIX, SPY, QQQ at the top, followed by others alphabetically:





^VIX: CBOE Volatility Index



SPY: SPDR S&P 500 ETF Trust



QQQ: Invesco QQQ Trust



AAPL: Apple Inc.



AMD: Advanced Micro Devices Inc.



AMZN: Amazon.com Inc.



ASML: ASML Holding N.V.



AVGO: Broadcom Inc.



BLK: BlackRock Inc.



BKNG: Booking Holdings Inc.



BTC-USD: Bitcoin USD



CDNS: Cadence Design Systems Inc.



COST: Costco Wholesale Corporation



CRM: Salesforce Inc.



CRSP: CRISPR Therapeutics AG



CRWD: CrowdStrike Holdings Inc.



EXPE: Expedia Group Inc.



GLD: SPDR Gold Shares



GOOGL: Alphabet Inc. (Class A)



INTU: Intuit Inc.



LCID: Lucid Group Inc.



META: Meta Platforms Inc.



MSFT: Microsoft Corporation



NFLX: Netflix Inc.



NTLA: Intellia Therapeutics Inc.



NVDA: NVIDIA Corporation



PLTR: Palantir Technologies Inc.



QCOM: Qualcomm Inc.



RIVN: Rivian Automotive Inc.



SHOP: Shopify Inc.



SLV: iShares Silver Trust



SNOW: Snowflake Inc.



SNPS: Synopsys Inc.



TGT: Target Corporation



TSLA: Tesla Inc.



TSM: Taiwan Semiconductor Manufacturing Co. Ltd.



WMT: Walmart Inc.

9.2 Hardcoded Earnings Dates

For robustness, the application shall include hardcoded earnings dates for META and estimated earnings months for key stocks:





META Earnings Dates:





July 30, 2025 (Q2 2025)



April 30, 2025 (Q1 2025)



January 29, 2025 (Q4 2024)



October 29, 2024 (Q3 2024)



July 30, 2024 (Q2 2024)



April 24, 2024 (Q1 2024)



February 1, 2024 (Q4 2023)



October 25, 2023 (Q3 2023)



Estimated Earnings Months:





AAPL, MSFT, AMZN, GOOGL, META, TSLA, AMD: January, April, July, October



NVDA: February, May, August, November
