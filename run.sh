#!/bin/bash

# SparkVibe Finance - Streamlit Application Runner
# This script runs the SparkVibe stock monitoring application

echo "🎺 Starting SparkVibe Finance Application..."
echo "================================================"

# Navigate to the SparkVibe directory
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "❌ Error: Streamlit is not installed"
    echo "Installing required packages..."
    echo "Run: pip install streamlit yfinance pandas numpy plotly"
    exit 1
fi

# Display system information
echo "✅ Python 3: $(python3 --version)"
echo "✅ Streamlit: $(python3 -c "import streamlit; print(streamlit.__version__)")"
echo "✅ Working Directory: $(pwd)"
echo ""

# Run the Streamlit application
echo "🚀 Launching SparkVibe Finance..."
echo "📊 The application will open in your default web browser"
echo "🌐 Local URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo "================================================"

# Start the Streamlit app
streamlit run main_app.py

echo ""
echo "👋 SparkVibe Finance application has been stopped"
