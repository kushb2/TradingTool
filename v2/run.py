"""
Institutional Footprint Detector v2
Entry point: streamlit run v2/run.py

Detects institutional accumulation patterns in NSE stocks
by analyzing delivery percentage relative to each stock's baseline.
"""
import streamlit as st

# Page config
st.set_page_config(
    page_title="Institutional Footprint Detector",
    page_icon="🐋",
    layout="wide"
)

# Title
st.title("🐋 Institutional Footprint Detector v2")
st.caption("Detect smart money accumulation using relative delivery analysis")

# Stock input
symbol = st.text_input(
    "Enter NSE Stock Symbol",
    placeholder="e.g., NETWEB, UNOMINDA, ETERNAL",
    help="Enter the NSE stock symbol without .NS suffix"
)

if symbol:
    st.info(f"Analyzing: {symbol.upper()}")
    st.write("---")
    st.write("📊 Data and analysis will appear here...")
else:
    st.write("👆 Enter a stock symbol to begin analysis")
