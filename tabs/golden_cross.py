"""
Golden Cross tab for SparkVibe Finance application
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from utils.constants import STOCKS


def create_golden_cross_tab(all_stock_data):
    """Create the Golden Cross tab content"""
    st.subheader("Golden Cross Stocks")
    # Filter stocks with golden cross and remove any None values
    golden_cross_stocks = {symbol: data for symbol, data in all_stock_data.items()
                          if data is not None and data.get("golden_cross", False)}

    if golden_cross_stocks:
        st.success(f"Found {len(golden_cross_stocks)} stocks with a golden cross in the past 30 days")

        # Create a table with stock information - using markdown to avoid st.table's non-interactive nature
        st.markdown("### Golden Cross Stocks")

        # Create a DataFrame for display
        golden_cross_data = []
        for symbol, data in golden_cross_stocks.items():
            # Format Golden Cross with traffic light system
            days_ago = data.get("golden_cross_days_ago", 0)
            if days_ago <= 15:
                golden_cross_display = f"🟢 {days_ago}d ago"
            elif days_ago <= 30:
                golden_cross_display = f"🟡 {days_ago}d ago"
            else:
                golden_cross_display = f"🔴 {days_ago}d ago"

            golden_cross_data.append({
                "Symbol": symbol,
                "Company": STOCKS[symbol],
                "Current Price": data['current_price'],
                "Daily Change": data['percentage_change'],
                "Golden Cross": golden_cross_display,
                "Golden Cross Days": days_ago
            })

        golden_cross_df = pd.DataFrame(golden_cross_data)

        # Display the dataframe with built-in sorting
        st.dataframe(
            golden_cross_df,
            use_container_width=True,
            height=400,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol 🔤"),
                "Company": st.column_config.TextColumn("Company 🏢"),
                "Current Price": st.column_config.NumberColumn("Price 💲", format="$%.1f"),
                "Daily Change": st.column_config.NumberColumn("Change % 📈", format="%.1f%%"),
                "Golden Cross": st.column_config.TextColumn("Golden Cross ✓"),
                "Golden Cross Days": st.column_config.NumberColumn("Days Ago", format="%.0f"),
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
