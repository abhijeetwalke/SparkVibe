"""
Volume Analysis tab for SparkVibe Finance application
"""

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.constants import STOCKS


def create_volume_analysis_tab(all_stock_data):
    """Create the Volume Analysis tab content"""

    # Add CSS for center-aligned table
    st.markdown("""
    <style>
    .stDataFrame > div > div > div > div > table {
        text-align: center !important;
    }
    .stDataFrame > div > div > div > div > table th {
        text-align: center !important;
        padding: 8px !important;
    }
    .stDataFrame > div > div > div > div > table td {
        text-align: center !important;
        padding: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Volume Analysis")
    st.write("Compare trading volume with average volume over time for each stock.")

    # Define a list of important stocks to show volume charts for
    # Start with locked symbols (VIX, SPY, QQQ) then add all remaining stocks from STOCKS dictionary
    locked_symbols = ["^VIX", "SPY", "QQQ"]
    remaining_stocks = [symbol for symbol in STOCKS.keys() if symbol not in locked_symbols]
    important_stocks = locked_symbols + remaining_stocks

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

    # Display the dataframe with built-in sorting using NumberColumn for proper sorting
    st.dataframe(
        sort_volume_df,
        use_container_width=True,
        height=400,
        column_config={
            "Symbol": st.column_config.TextColumn("Symbol 🔤"),
            "Company": st.column_config.TextColumn("Company 🏢"),
            "Current Price": st.column_config.NumberColumn("Price 💲", format="$%.1f"),
            "Daily Change": st.column_config.NumberColumn("Change % 📈", format="%.1f%%"),
            "Volume": st.column_config.NumberColumn("Volume (M) 📊", format="%.1f"),
            "Avg Volume": st.column_config.NumberColumn("Avg Vol (M) 📊", format="%.1f"),
            "Volume/Avg Ratio": st.column_config.NumberColumn("Vol/Avg Ratio 📈", format="%.1fx"),
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
                    f"{current_volume/1e6:.1f}M"
                )

            with col2:
                st.metric(
                    "30-Day Avg Volume (M)",
                    f"{avg_volume/1e6:.1f}M"
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
