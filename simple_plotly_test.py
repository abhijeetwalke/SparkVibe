import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page title
st.set_page_config(page_title="Simple Plotly Test", layout="wide")

st.title("Simple Plotly Chart Test")

# Create some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a simple Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sine Wave'))
fig.update_layout(title="Simple Sine Wave", xaxis_title="X", yaxis_title="Y")

# Display the figure
st.plotly_chart(fig, use_container_width=True)

st.write("If you can see the chart above, Plotly is working correctly!")
