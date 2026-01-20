"""
Institutional Footprint Detector v2
Entry point: streamlit run v2/run.py

Detects institutional accumulation patterns in NSE stocks
by analyzing delivery percentage relative to each stock's baseline.
"""
import streamlit as st

from v2.constants.constants import popular_stocks

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
st.subheader("Select Stocks for Analysis")

# Multiselect dropdown for popular stocks
selected_stocks = st.multiselect(
    "Select from popular stocks:",
    options=popular_stocks
)

# Text input for additional stocks
additional_stocks_str = st.text_input(
    "Or enter comma-separated NSE stock symbols:",
    placeholder="e.g., NETWEB, UNOMINDA, ETERNAL",
    help="Enter NSE stock symbols without .NS suffix"
)

# Combine and process stocks
all_stocks = set(selected_stocks)
if additional_stocks_str:
    additional_stocks = [s.strip().upper() for s in additional_stocks_str.split(',')]
    all_stocks.update(additional_stocks)

# Analysis button
if st.button("Analyze Stocks"):
    if all_stocks:
        st.info("Analyzing the following stocks:")
        
        # Create a numbered list of stocks
        numbered_list = "\n".join([f"{i+1}. {stock}" for i, stock in enumerate(all_stocks)])
        st.markdown(numbered_list)
        
        st.write("---")
        st.write("📊 Data and analysis will appear here...")
    else:
        st.warning("Please select or enter at least one stock symbol.")

else:
    st.write("👆 Select or enter stock symbols and click 'Analyze Stocks' to begin.")