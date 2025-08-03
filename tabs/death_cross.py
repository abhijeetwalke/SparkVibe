"""
Death Cross tab for SparkVibe Finance application
"""

import streamlit as st
import pandas as pd
import yfinance as yf
from utils.constants import STOCKS


def create_death_cross_tab(all_stock_data):
    """Create the Death Cross tab content"""
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

            # Format death cross with traffic light system
            days_ago = data.get("death_cross_days_ago", 0)
            if days_ago <= 15:
                death_cross_display = f"🟢 {days_ago}d ago"
            elif days_ago <= 30:
                death_cross_display = f"🟡 {days_ago}d ago"
            else:
                death_cross_display = f"🔴 {days_ago}d ago"

            death_cross_data.append({
                "Symbol": f'<a href="#" onclick="parent.postMessage({{cmd: \'streamlit:setComponentValue\', componentValue: \'{symbol}\', componentKey: \'stock_click\'}}, \'*\'); return false;" style="text-decoration: none; color: #1E88E5; font-weight: bold;">{symbol}</a>',
                "Company": STOCKS[symbol],
                "Current Price": f"${data['current_price']:.1f}",
                "Daily Change": formatted_change,
                "Death Cross": death_cross_display
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

        # Display the dataframe with built-in sorting using NumberColumn for proper sorting
        st.dataframe(
            sort_death_cross_df,
            use_container_width=True,
            height=400,
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol 🔤"),
                "Company": st.column_config.TextColumn("Company 🏢"),
                "Current Price": st.column_config.NumberColumn("Price 💲", format="$%.1f"),
                "Daily Change": st.column_config.NumberColumn("Change % 📈", format="%.1f%%"),
                "Death Cross Days": st.column_config.NumberColumn("Death Cross (days ago) ⚠️", format="%.0f"),
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
