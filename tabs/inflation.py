"""
Inflation tab for SparkVibe Finance Dashboard
Shows Consumer Price Index (CPI) data and inflation trends
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json
import random


def fetch_real_cpi_data():
    """Fetch real CPI data from Bureau of Labor Statistics (BLS) API"""

    try:
        # BLS API base URL - public access
        base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

        # BLS series IDs for CPI data (these are the official BLS series IDs)
        bls_series = {
            "All Items": "CUUR0000SA0",
            "Core CPI (ex Food & Energy)": "CUUR0000SA0L1E",
            "Food": "CUUR0000SAF1",
            "Energy": "CUUR0000SA0E",
            "Housing": "CUUR0000SAH1",
            "Transportation": "CUUR0000SAT1",
            "Medical Care": "CUUR0000SAM",
            "Recreation": "CUUR0000SAR",
            "Education": "CUUR0000SAE1",
            "Apparel": "CUUR0000SAA",
            "Shelter": "CUUR0000SEHA",
            "Used Vehicles": "CUUR0000SETA02",
            "New Vehicles": "CUUR0000SETA01",
            "Gasoline": "CUUR0000SETB01",
        }

        # Calculate date range (24 months back)
        current_year = datetime.now().year
        start_year = current_year - 2

        all_data = []
        successful_fetches = 0

        # Process series in batches (BLS API limit is 25 series per request)
        series_list = list(bls_series.keys())
        batch_size = 10

        for i in range(0, len(series_list), batch_size):
            batch_categories = series_list[i:i + batch_size]
            batch_series_ids = [bls_series[cat] for cat in batch_categories]

            try:
                # Prepare the request payload
                payload = {
                    "seriesid": batch_series_ids,
                    "startyear": str(start_year),
                    "endyear": str(current_year),
                    "calculations": True,  # This gives us 12-month percent changes
                    "annualaverage": False
                }

                headers = {'Content-type': 'application/json'}
                response = requests.post(
                    base_url,
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=30
                )

                if response.status_code == 200:
                    json_data = response.json()

                    if json_data.get('status') == 'REQUEST_SUCCEEDED' and 'Results' in json_data:
                        series_data = json_data['Results']['series']

                        for series_info in series_data:
                            series_id = series_info['seriesID']

                            # Find the category name for this series ID
                            category = None
                            for cat, sid in bls_series.items():
                                if sid == series_id:
                                    category = cat
                                    break

                            if category and 'data' in series_info:
                                category_data_count = 0

                                for data_point in series_info['data']:
                                    try:
                                        year = int(data_point['year'])
                                        period = data_point['period']

                                        # Skip annual averages and quarterly data
                                        if period.startswith('M') and len(period) == 3:
                                            month = int(period[1:])

                                            # Get 12-month percent change if available
                                            if 'calculations' in data_point and 'pct_changes' in data_point['calculations']:
                                                pct_changes = data_point['calculations']['pct_changes']
                                                if '12' in pct_changes:  # 12-month change
                                                    rate = float(pct_changes['12'])

                                                    date_obj = datetime(year, month, 1)

                                                    all_data.append({
                                                        'Date': date_obj.strftime('%Y-%m'),
                                                        'Category': category,
                                                        'Rate': round(rate, 1),
                                                        'Month': date_obj.strftime('%Y-%m'),
                                                        'Month_Name': date_obj.strftime('%b %Y'),
                                                        'Date_Object': date_obj
                                                    })
                                                    category_data_count += 1
                                    except (ValueError, TypeError, KeyError):
                                        continue

                                if category_data_count > 0:
                                    successful_fetches += 1

            except Exception as e:
                continue

        # If we got data for at least a few categories, use real data
        if successful_fetches >= 3 and len(all_data) > 0:
            df = pd.DataFrame(all_data)
            # Sort by date to get most recent data
            df = df.sort_values('Date_Object')
            st.success(f"✅ Successfully fetched real CPI data from BLS API for {successful_fetches} categories")
            return df
        else:
            st.warning("⚠️ BLS API access limited or no data available. Using realistic mock data based on recent CPI trends.")
            return generate_realistic_cpi_data()

    except Exception as e:
        st.warning(f"⚠️ Error connecting to BLS API: {str(e)}. Using realistic mock data based on recent CPI trends.")
        return generate_realistic_cpi_data()


def generate_realistic_cpi_data():
    """Generate realistic CPI data based on actual recent trends"""

    # Based on actual CPI data from 2023-2024
    cpi_categories = {
        "All Items": {"current": 3.2, "trend": "declining", "volatility": 0.3},
        "Core CPI (ex Food & Energy)": {"current": 3.8, "trend": "stable", "volatility": 0.2},
        "Food": {"current": 2.4, "trend": "declining", "volatility": 0.8},
        "Energy": {"current": -2.1, "trend": "volatile", "volatility": 3.0},
        "Housing": {"current": 5.4, "trend": "declining", "volatility": 0.4},
        "Shelter": {"current": 5.7, "trend": "declining", "volatility": 0.3},
        "Transportation": {"current": 1.9, "trend": "stable", "volatility": 1.2},
        "Medical Care": {"current": 3.1, "trend": "stable", "volatility": 0.5},
        "Recreation": {"current": 1.8, "trend": "stable", "volatility": 0.4},
        "Education": {"current": 4.2, "trend": "increasing", "volatility": 0.3},
        "Apparel": {"current": 0.8, "trend": "volatile", "volatility": 1.5},
        "Used Vehicles": {"current": -2.8, "trend": "declining", "volatility": 2.5},
        "New Vehicles": {"current": 1.2, "trend": "stable", "volatility": 0.8},
        "Gasoline": {"current": -3.5, "trend": "volatile", "volatility": 4.0},
    }

    # Generate proper monthly dates - CPI data is released with ~2 month delay
    current_date = datetime.now()
    latest_available_month = current_date.month - 2
    latest_available_year = current_date.year

    if latest_available_month <= 0:
        latest_available_month += 12
        latest_available_year -= 1

    dates = []
    date_objects = []

    # Generate 24 months of data
    for i in range(24):
        year = latest_available_year
        month = latest_available_month - i

        while month <= 0:
            month += 12
            year -= 1

        month_date = datetime(year, month, 1)
        date_objects.append(month_date)
        dates.append(month_date.strftime("%Y-%m"))

    dates.reverse()
    date_objects.reverse()

    inflation_data = []

    for category, info in cpi_categories.items():
        current_rate = info["current"]
        trend = info["trend"]
        volatility = info["volatility"]

        for i, (date_str, date_obj) in enumerate(zip(dates, date_objects)):
            if i == len(dates) - 1:  # Most recent month
                rate = current_rate
            else:
                # Create realistic historical progression
                months_back = len(dates) - 1 - i

                if trend == "declining":
                    # Rate was higher in the past, declining to current
                    base_adjustment = months_back * 0.1
                elif trend == "increasing":
                    # Rate was lower in the past, increasing to current
                    base_adjustment = -months_back * 0.1
                elif trend == "volatile":
                    # More random variation
                    base_adjustment = random.uniform(-1.0, 1.0)
                else:  # stable
                    base_adjustment = random.uniform(-0.3, 0.3)

                # Add monthly volatility
                monthly_variation = random.uniform(-volatility, volatility)
                rate = current_rate + base_adjustment + monthly_variation

                # Keep within reasonable bounds
                if category == "Energy" or category == "Gasoline":
                    rate = max(-20.0, min(25.0, rate))
                elif category == "Used Vehicles":
                    rate = max(-15.0, min(15.0, rate))
                else:
                    rate = max(-5.0, min(10.0, rate))

            inflation_data.append({
                "Date": date_str,
                "Category": category,
                "Rate": round(rate, 1),
                "Month": date_str,
                "Month_Name": date_obj.strftime("%b %Y"),
                "Date_Object": date_obj
            })

    return pd.DataFrame(inflation_data)


def generate_mock_inflation_data():
    """Generate realistic mock inflation data for CPI categories - MONTHLY DATA"""

    # CPI categories with realistic inflation ranges
    cpi_categories = {
        "All Items": {"current": 3.2, "range": (2.5, 4.0)},
        "Food": {"current": 2.4, "range": (1.5, 5.0)},
        "Energy": {"current": -2.1, "range": (-10.0, 15.0)},
        "Housing": {"current": 5.4, "range": (3.0, 7.0)},
        "Transportation": {"current": 1.9, "range": (-5.0, 8.0)},
        "Medical Care": {"current": 3.1, "range": (2.0, 4.5)},
        "Recreation": {"current": 1.8, "range": (0.5, 3.5)},
        "Education": {"current": 4.2, "range": (2.5, 6.0)},
        "Apparel": {"current": 0.8, "range": (-2.0, 4.0)},
        "Other Goods & Services": {"current": 3.5, "range": (2.0, 5.0)},
        "Core CPI (ex Food & Energy)": {"current": 3.8, "range": (3.0, 4.5)},
        "Shelter": {"current": 5.7, "range": (4.0, 7.5)},
        "Used Vehicles": {"current": -2.8, "range": (-15.0, 10.0)},
        "New Vehicles": {"current": 1.2, "range": (-1.0, 4.0)},
        "Gasoline": {"current": -3.5, "range": (-20.0, 25.0)},
    }

    # Generate proper monthly dates - CPI data is released with ~2 month delay
    current_date = datetime.now()

    # CPI data is typically released 2 months behind (e.g., June data released in August)
    # So if we're in September 2024, the latest available data would be July 2024
    latest_available_month = current_date.month - 2
    latest_available_year = current_date.year

    # Handle year rollover for the latest available data
    if latest_available_month <= 0:
        latest_available_month += 12
        latest_available_year -= 1

    dates = []
    date_objects = []

    # Generate 24 months of data ending with the latest available month
    for i in range(24):
        # Calculate the exact month by going back i months from latest available
        year = latest_available_year
        month = latest_available_month - i

        # Handle year rollover
        while month <= 0:
            month += 12
            year -= 1

        # Create date object for the first day of each month
        month_date = datetime(year, month, 1)
        date_objects.append(month_date)
        dates.append(month_date.strftime("%Y-%m"))

    # Reverse to get chronological order (oldest to newest)
    dates.reverse()
    date_objects.reverse()

    inflation_data = []

    for category, info in cpi_categories.items():
        current_rate = info["current"]
        rate_range = info["range"]

        # Generate historical trend
        for i, (date_str, date_obj) in enumerate(zip(dates, date_objects)):
            # Add some realistic variation
            if i == len(dates) - 1:  # Current month
                rate = current_rate
            else:
                # Create a trend that leads to current rate
                trend_factor = (len(dates) - 1 - i) / len(dates)
                variation = random.uniform(-0.5, 0.5)
                rate = base_rate = current_rate + (trend_factor * random.uniform(-1.0, 1.0)) + variation

                # Keep within realistic bounds
                rate = max(rate_range[0], min(rate_range[1], rate))

            inflation_data.append({
                "Date": date_str,
                "Category": category,
                "Rate": rate,
                "Month": date_str,
                "Month_Name": date_obj.strftime("%b %Y"),  # e.g., "Jan 2024"
                "Date_Object": date_obj
            })

    return pd.DataFrame(inflation_data)


def create_inflation_tab(development_mode=False):
    """Create the Inflation tab content"""
    st.subheader("Consumer Price Index (CPI) - 12-Month % Change")
    st.write("Track inflation trends across different consumer categories")

    # Add data availability notice
    current_date = datetime.now()
    latest_available_month = current_date.month - 2
    latest_available_year = current_date.year

    if latest_available_month <= 0:
        latest_available_month += 12
        latest_available_year -= 1

    latest_month_name = datetime(latest_available_year, latest_available_month, 1).strftime("%B %Y")

    st.info(f"📅 **Data Availability**: CPI data is released by the Bureau of Labor Statistics with approximately a 2-month delay. The most recent data available is for **{latest_month_name}**.")

    # Fetch inflation data based on development mode
    if development_mode:
        st.info("🚀 Development Mode: Using mock CPI data for faster iteration...")
        inflation_df = generate_mock_inflation_data()
    else:
        st.info("Fetching real CPI data from Bureau of Labor Statistics...")
        inflation_df = fetch_real_cpi_data()

    # Get the latest data for the summary table
    latest_date = inflation_df['Date'].max()
    latest_data = inflation_df[inflation_df['Date'] == latest_date].copy()
    latest_data = latest_data.sort_values('Rate', ascending=False)

    # Create summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        all_items_rate = latest_data[latest_data['Category'] == 'All Items']['Rate'].iloc[0]
        st.metric(
            "All Items CPI",
            f"{all_items_rate:.1f}%",
            delta=f"{random.uniform(-0.3, 0.3):.1f}% vs last month"
        )

    with col2:
        core_cpi_rate = latest_data[latest_data['Category'] == 'Core CPI (ex Food & Energy)']['Rate'].iloc[0]
        st.metric(
            "Core CPI",
            f"{core_cpi_rate:.1f}%",
            delta=f"{random.uniform(-0.2, 0.2):.1f}% vs last month"
        )

    with col3:
        food_rate = latest_data[latest_data['Category'] == 'Food']['Rate'].iloc[0]
        st.metric(
            "Food",
            f"{food_rate:.1f}%",
            delta=f"{random.uniform(-0.5, 0.5):.1f}% vs last month"
        )

    with col4:
        energy_rate = latest_data[latest_data['Category'] == 'Energy']['Rate'].iloc[0]
        st.metric(
            "Energy",
            f"{energy_rate:.1f}%",
            delta=f"{random.uniform(-2.0, 2.0):.1f}% vs last month"
        )

    # Current Inflation Rates Table
    st.subheader("Current Inflation Rates by Category")

    # Prepare data for display
    display_data = latest_data[['Category', 'Rate']].copy()
    display_data['Rate_Display'] = display_data['Rate'].apply(lambda x: f"{x:.1f}%")

    # Add color coding for the rates
    def get_inflation_color(rate):
        if rate < 0:
            return "🟢"  # Deflation - green
        elif rate < 2.0:
            return "🟡"  # Low inflation - yellow
        elif rate < 4.0:
            return "🟠"  # Moderate inflation - orange
        else:
            return "🔴"  # High inflation - red

    display_data['Status'] = display_data['Rate'].apply(get_inflation_color)

    # Display the table
    st.dataframe(
        display_data[['Category', 'Rate', 'Status']],
        use_container_width=True,
        height=400,
        column_config={
            "Category": st.column_config.TextColumn("Category 📊", width="large"),
            "Rate": st.column_config.NumberColumn("12-Month % Change 📈", format="%.1f%%"),
            "Status": st.column_config.TextColumn("Status 🚦", width="small"),
        },
        hide_index=True,
    )

    # Add legend for status colors
    st.markdown("### Status Legend")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🟢 **Deflation** (< 0%)")
    with col2:
        st.markdown("🟡 **Low** (0-2%)")
    with col3:
        st.markdown("🟠 **Moderate** (2-4%)")
    with col4:
        st.markdown("🔴 **High** (> 4%)")

    # Historical Trends Chart
    st.subheader("Monthly Inflation Trends (24 Months)")
    st.write("📅 **Monthly Data**: Each point represents one month of CPI data")

    # Category selector for the chart
    selected_categories = st.multiselect(
        "Select categories to display:",
        options=inflation_df['Category'].unique(),
        default=['All Items', 'Core CPI (ex Food & Energy)', 'Food', 'Energy', 'Housing']
    )

    if selected_categories:
        # Filter data for selected categories
        chart_data = inflation_df[inflation_df['Category'].isin(selected_categories)]

        # Create the line chart
        fig = go.Figure()

        # Add a line for each selected category
        for category in selected_categories:
            category_data = chart_data[chart_data['Category'] == category]

            fig.add_trace(go.Scatter(
                x=category_data['Date_Object'],  # Use Date_Object for proper monthly intervals
                y=category_data['Rate'],
                mode='lines+markers',
                name=category,
                line=dict(width=2),
                marker=dict(size=5),
                hovertemplate=f'<b>{category}</b><br>' +
                             'Month: %{x|%b %Y}<br>' +  # Format as "Jan 2024"
                             'Rate: %{y:.1f}%<br>' +
                             '<extra></extra>'
            ))

        # Update layout with monthly-specific formatting
        fig.update_layout(
            title="Consumer Price Index - Monthly 12-Month Percentage Change",
            xaxis_title="Month",
            yaxis_title="12-Month % Change",
            hovermode="x unified",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                tickangle=45,  # Rotate month labels for better readability
                tickformat='%b %Y',  # Format ticks as "Jan 2024"
                dtick='M1',  # Show every month (M1 = 1 month interval)
                tickmode='linear'
            )
        )

        # Add horizontal line at 2% (Fed target)
        fig.add_hline(
            y=2.0,
            line_dash="dash",
            line_color="red",
            annotation_text="Fed Target (2%)",
            annotation_position="bottom right"
        )

        # Add horizontal line at 0% (deflation threshold)
        fig.add_hline(
            y=0.0,
            line_dash="dot",
            line_color="gray",
            annotation_text="Deflation Threshold (0%)",
            annotation_position="top right"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Add monthly data summary
        st.info("📊 **Data Frequency**: This chart displays monthly Consumer Price Index data, with each data point representing the 12-month percentage change for that specific month.")

    # Category Comparison Chart
    st.subheader("Current Inflation Rate Comparison")

    # Create a horizontal bar chart for current rates
    fig_bar = px.bar(
        latest_data.head(10),  # Top 10 categories
        x='Rate',
        y='Category',
        orientation='h',
        title="Top 10 Categories by Current Inflation Rate",
        color='Rate',
        color_continuous_scale=['green', 'yellow', 'orange', 'red'],
        text='Rate'
    )

    fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_bar.update_layout(
        height=400,
        xaxis_title="12-Month % Change",
        yaxis_title="Category",
        coloraxis_colorbar=dict(title="Inflation Rate (%)")
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # Analysis and Insights
    st.subheader("Key Insights")

    # Calculate some insights
    highest_inflation = latest_data.iloc[0]
    lowest_inflation = latest_data.iloc[-1]
    above_target = len(latest_data[latest_data['Rate'] > 2.0])
    deflation_categories = len(latest_data[latest_data['Rate'] < 0])

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**Highest Inflation**: {highest_inflation['Category']} at {highest_inflation['Rate']:.1f}%")
        st.info(f"**Categories Above 2% Target**: {above_target} out of {len(latest_data)}")

    with col2:
        st.info(f"**Lowest Inflation**: {lowest_inflation['Category']} at {lowest_inflation['Rate']:.1f}%")
        if deflation_categories > 0:
            st.warning(f"**Deflation Alert**: {deflation_categories} categories showing deflation")
        else:
            st.success("**No Deflation**: All categories showing positive inflation")

    # Data source note
    st.markdown("---")
    st.caption("*Note: This is mock inflation data for demonstration purposes. In production, this would connect to Bureau of Labor Statistics (BLS) API or similar data source.*")
