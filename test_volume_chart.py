# Handle both second and millisecond timestamps
if timestamp > 1e10:  # If timestamp is in milliseconds
    timestamp = timestamp / 1000
earnings_date = pd.Timestamp(datetime.fromtimestamp(timestamp))# Handle both second and millisecond timestamps
if earnings_date > 1e10:  # If timestamp is in milliseconds
    earnings_date = earnings_date / 1000
earnings_date = pd.Timestamp(datetime.fromtimestamp(earnings_date))# Handle both second and millisecond timestamps
if next_earnings > 1e10:  # If timestamp is in milliseconds
    next_earnings = next_earnings / 1000
earnings_date = pd.Timestamp(datetime.fromtimestamp(next_earnings))import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page title
st.set_page_config(page_title="Volume Chart Test", layout="wide")

st.title("Stock Volume Chart with Earnings Dates")

# Select a stock
selected_stock = st.selectbox(
    "Select a stock:",
    options=["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
    format_func=lambda x: f"{x}"
)

# Fetch data
with st.spinner(f"Fetching data for {selected_stock}..."):
    # Get historical data
    ticker = yf.Ticker(selected_stock)
    hist = ticker.history(period="2y")

    # Try to get earnings dates
    try:
        earnings_dates = ticker.get_earnings_dates(limit=8)
        if earnings_dates is not None:
            earnings_dates = earnings_dates[~earnings_dates.index.duplicated(keep='first')]
            st.write(f"Found {len(earnings_dates)} earnings dates")
        else:
            earnings_dates = pd.DataFrame()
            st.warning("No earnings dates found")
    except Exception as e:
        st.error(f"Error fetching earnings dates: {str(e)}")
        earnings_dates = pd.DataFrame()

# Calculate moving average
hist['Avg_Volume'] = hist['Volume'].rolling(window=30).mean()

# Convert to millions for display
hist['Volume_M'] = hist['Volume'] / 1e6
hist['Avg_Volume_M'] = hist['Avg_Volume'] / 1e6

# Create Plotly chart
try:
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add volume bars
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist['Volume_M'],
            name="Volume",
            marker_color='rgba(58, 71, 80, 0.6)',
            opacity=0.7
        ),
        secondary_y=False,
    )

    # Add average volume line
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist['Avg_Volume_M'],
            name="30-Day Avg Volume",
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

    # Add earnings date markers if available
    if not earnings_dates.empty:
        valid_earnings_dates = []

        for date in earnings_dates.index:
            try:
                if date in hist.index or date >= hist.index[0]:
                    # Find the closest date in our historical data
                    closest_date = min(hist.index, key=lambda x: abs(x - date))

                    # Get the volume and price for this date
                    if closest_date in hist.index:
                        volume_value = hist.loc[closest_date, 'Volume_M']
                        price_value = hist.loc[closest_date, 'Close']

                        valid_earnings_dates.append({
                            'date': date,
                            'volume': volume_value,
                            'price': price_value
                        })
            except Exception as e:
                st.warning(f"Error processing earnings date {date}: {str(e)}")

        # Add markers for earnings dates
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
                    hovertemplate='Earnings Date: %{x}<br>Volume: %{y:.2f}M<extra></extra>'
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
                    hovertemplate='Earnings Date: %{x}<br>Price: $%{y:.2f}<extra></extra>',
                    showlegend=False
                ),
                secondary_y=True,
            )

    # Update layout
    fig.update_layout(
        title=f"Volume Analysis for {selected_stock} with Earnings Dates",
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
    fig.update_yaxes(title_text="Volume (Millions)", secondary_y=False)
    fig.update_yaxes(title_text="Price ($)", secondary_y=True)

    # Display the interactive chart
    st.plotly_chart(fig, use_container_width=True)

    # Display earnings dates in a table if available
    if not earnings_dates.empty:
        st.subheader("Earnings Dates")
        st.dataframe(earnings_dates)

except Exception as e:
    st.error(f"Error creating chart: {str(e)}")
    st.write("Falling back to basic chart")

    # Create a simple chart with Streamlit
    chart_data = pd.DataFrame({
        'Volume (M)': hist['Volume_M'],
        'Avg Volume (M)': hist['Avg_Volume_M']
    }, index=hist.index)

    st.line_chart(chart_data)
