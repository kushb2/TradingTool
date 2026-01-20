"""
Institutional Footprint Detector v2
Entry point: streamlit run v2/run.py

Detects institutional accumulation patterns in NSE stocks
by analyzing delivery percentage relative to each stock's baseline.
"""
import streamlit as st

from v2.constants.constants import popular_stocks
from v2.data.price_service import fetch_raw_price_data, fetch_price_data

# Page config
st.set_page_config(
    page_title="Institutional Footprint Detector",
    page_icon="🐋",
    layout="wide"
)

# Title
st.title("🐋 Institutional Footprint Detector v2")
st.caption("Detect smart money accumulation using relative delivery analysis")

# Sidebar options
with st.sidebar:
    st.header("⚙️ Options")
    show_raw_data = st.checkbox("Show Raw Data (Debug)", value=False, 
                                 help="Display unprocessed data from yfinance for debugging")

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
all_stocks = list(set(selected_stocks))
if additional_stocks_str:
    additional_stocks = [s.strip().upper() for s in additional_stocks_str.split(',') if s.strip()]
    all_stocks = list(set(all_stocks + additional_stocks))

# Analysis button
if st.button("Analyze Stocks"):
    if all_stocks:
        st.info(f"Analyzing {len(all_stocks)} stock(s): {', '.join(all_stocks)}")
        st.write("---")
        
        for symbol in all_stocks:
            st.subheader(f"📈 {symbol}")
            
            # Fetch price data
            with st.spinner(f"Fetching price data for {symbol}..."):
                price_df = fetch_price_data(symbol)
            
            if price_df.empty:
                st.error(f"❌ Could not fetch data for {symbol}. Check if the symbol is correct.")
            else:
                st.success(f"✅ Fetched {len(price_df)} days of price data")
                
                # Show raw data if debug mode is enabled
                if show_raw_data:
                    with st.expander(f"🔍 Raw Data - {symbol} (Debug)", expanded=False):
                        raw_df = fetch_raw_price_data(symbol)
                        st.dataframe(raw_df, use_container_width=True)
                
                # Show processed price data
                with st.expander(f"📊 Price Data - {symbol}", expanded=True):
                    st.dataframe(price_df, use_container_width=True)
            
            st.write("---")
    else:
        st.warning("Please select or enter at least one stock symbol.")
else:
    st.write("👆 Select or enter stock symbols and click 'Analyze Stocks' to begin.")
