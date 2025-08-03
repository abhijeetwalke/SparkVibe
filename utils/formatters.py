"""
Formatting utilities for SparkVibe Finance application
"""

import pandas as pd
from .constants import DECIMAL_PRECISION


def format_currency(value):
    """Format currency values in billions"""
    if pd.isna(value) or value == "N/A":
        return "N/A"

    if isinstance(value, str):
        return value

    # Always show market cap in billions for large values
    if value >= 1e9:
        return f"${value/1e9:.{DECIMAL_PRECISION}f}B"
    elif value >= 1e6:
        return f"${value/1e6:.{DECIMAL_PRECISION}f}M"
    else:
        return f"${value:,.{DECIMAL_PRECISION}f}"


def format_volume(volume):
    """Format volume in millions"""
    if pd.isna(volume) or volume == "N/A":
        return "N/A"

    # Always show volume in millions
    return f"{volume/1e6:.{DECIMAL_PRECISION}f}M"
