"""
Institutional Footprint Detector v2
Entry point: streamlit run v2/run.py

Detects institutional accumulation patterns in NSE stocks
by analyzing delivery percentage relative to each stock's baseline.
"""
import streamlit as st
import pandas as pd

from v2.constants.constants import popular_stocks
from v2.data.price_service import fetch_raw_price_data, fetch_price_data
from v2.data.earnings_service import (
    fetch_next_earnings_date as fetch_next_earnings_date_from_nse,
    fetch_earnings_history,
    fetch_company_info,
    fetch_earnings_with_performance,
    fetch_all_earnings_summary
)

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

# Stock input section
st.subheader("Select Stocks for Analysis")

# Multiselect dropdown for popular stocks
selected_stocks = st.multiselect(
    "Select from popular stocks:",
    options=popular_stocks
)

# Text input for additional stocks
additional_stocks_str = st.text_input(
    "Or enter comma-separated stock symbols:",
    placeholder="e.g., NETWEB, UNOMINDA, TCS, RELIANCE",
    help="Enter NSE stock symbols without .NS suffix"
)

# Combine and process stocks
all_stocks = list(set(selected_stocks))
if additional_stocks_str:
    additional_stocks = [s.strip().upper() for s in additional_stocks_str.split(',') if s.strip()]
    all_stocks = list(set(all_stocks + additional_stocks))

st.write("---")

# Main tabs - separate views for different analysis
main_tab_analysis, main_tab_earnings = st.tabs(["📊 Stock Analysis", "📅 Earnings Calendar"])

# ============================================
# TAB 1: Stock Analysis (Price Data)
# ============================================
with main_tab_analysis:
    if st.button("🔍 Analyze Stocks", key="analyze_btn"):
        if all_stocks:
            st.info(f"Analyzing {len(all_stocks)} stock(s): {', '.join(all_stocks)}")
            st.write("---")
            
            for symbol in all_stocks:
                st.subheader(f"📈 {symbol}")
                
                with st.spinner(f"Fetching price data for {symbol}..."):
                    price_df = fetch_price_data(symbol)
                
                if price_df.empty:
                    st.error(f"❌ Could not fetch price data for {symbol}. Check if the symbol is correct.")
                else:
                    st.success(f"✅ Fetched {len(price_df)} days of price data")
                    
                    # Show raw data if debug mode is enabled
                    if show_raw_data:
                        with st.expander(f"🔍 Raw Data (Debug)", expanded=False):
                            raw_df = fetch_raw_price_data(symbol)
                            st.dataframe(raw_df, use_container_width=True)
                    
                    # Show processed price data
                    st.dataframe(price_df, use_container_width=True)
                
                st.write("---")
        else:
            st.warning("Please select or enter at least one stock symbol.")
    else:
        st.write("👆 Select stocks above and click 'Analyze Stocks' to begin.")

# ============================================
# TAB 2: Earnings Calendar (Card Style UI)
# ============================================
with main_tab_earnings:
    st.caption("📌 Earnings data with stock performance vs NIFTY 50")
    
    if st.button("📅 Fetch Earnings Data", key="earnings_btn"):
        if all_stocks:
            st.info(f"Fetching earnings for {len(all_stocks)} stock(s)...")
            
            progress_bar = st.progress(0)
            
            # Fetch all earnings data
            all_earnings = []
            for idx, symbol in enumerate(all_stocks):
                progress_bar.progress((idx + 1) / len(all_stocks))
                data = fetch_earnings_with_performance(symbol, num_quarters=3)
                all_earnings.append(data)
            
            progress_bar.empty()
            
            # Display each stock as a card
            for data in all_earnings:
                symbol = data["symbol"]
                ticker = data.get("ticker", symbol)
                
                # Card container
                with st.container():
                    # Header row
                    col_title, col_badge = st.columns([3, 1])
                    with col_title:
                        st.markdown(f"### {symbol}")
                    with col_badge:
                        st.caption(f"NSE: {symbol}")
                    
                    # Next earnings and relative performance
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Directly fetch the next earnings date using the NSE-specific function
                        # This bypasses the date returned by fetch_earnings_with_performance
                        # to ensure we are displaying the most direct NSE result
                        next_date = fetch_next_earnings_date_from_nse(symbol)
                        if next_date:
                            date_str = next_date.strftime("%Y-%m-%d")
                            st.markdown(f"**Next Quarterly Earning Date (NSE):** `{date_str}`")
                        else:
                            st.markdown("**Next Quarterly Earning Date (NSE):** `N/A`")
                    
                    with col2:
                        rel_perf = data.get("relative_performance")
                        if rel_perf is not None:
                            color = "green" if rel_perf >= 0 else "red"
                            arrow = "↓" if rel_perf >= 0 else "↑"
                            st.markdown(f"**Performance vs. NIFTY 50 (last month):** "
                                       f"<span style='color:{color}'>{rel_perf:+.1f}% {arrow}</span>", 
                                       unsafe_allow_html=True)
                        else:
                            st.markdown("**Performance vs. NIFTY 50 (last month):** `N/A`")
                    
                    # Earnings History Table
                    st.markdown("#### Earnings History")
                    
                    history = data.get("history", [])
                    if history:
                        # Create table header
                        header_cols = st.columns([2, 3, 3])
                        with header_cols[0]:
                            st.markdown("**EARNING DATE**")
                        with header_cols[1]:
                            st.markdown("**STOCK PERFORMANCE (1 WEEK)**")
                        with header_cols[2]:
                            st.markdown("**NIFTY 50 PERFORMANCE**")
                        
                        # Table rows
                        for entry in history:
                            row_cols = st.columns([2, 3, 3])
                            
                            with row_cols[0]:
                                st.write(entry.get("date", "N/A"))
                            
                            with row_cols[1]:
                                stock_perf = entry.get("stock_performance")
                                if stock_perf is not None:
                                    color = "green" if stock_perf >= 0 else "red"
                                    arrow = "↓" if stock_perf >= 0 else "↑"
                                    st.markdown(f"<span style='color:{color}'>{stock_perf:+.1f}% {arrow}</span>", 
                                               unsafe_allow_html=True)
                                else:
                                    st.write("N/A")
                            
                            with row_cols[2]:
                                nifty_perf = entry.get("nifty_performance")
                                if nifty_perf is not None:
                                    color = "green" if nifty_perf >= 0 else "red"
                                    arrow = "↓" if nifty_perf >= 0 else "↑"
                                    st.markdown(f"<span style='color:{color}'>{nifty_perf:+.1f}% {arrow}</span>", 
                                               unsafe_allow_html=True)
                                else:
                                    st.write("N/A")
                    else:
                        st.write("No earnings history available")
                    
                    st.write("---")
            
            # Download summary
            summary_data = []
            for data in all_earnings:
                row = {
                    "Symbol": data["symbol"],
                    "Next Earnings": data.get("next_earnings"),
                    "Relative Perf vs NIFTY": data.get("relative_performance")
                }
                for i, h in enumerate(data.get("history", [])[:3]):
                    row[f"Q{i+1} Date"] = h.get("date")
                    row[f"Q{i+1} Stock Perf"] = h.get("stock_performance")
                    row[f"Q{i+1} NIFTY Perf"] = h.get("nifty_performance")
                summary_data.append(row)
            
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Earnings Summary (CSV)",
                    data=csv,
                    file_name="earnings_summary.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Please select or enter at least one stock symbol above.")
    else:
        st.write("👆 Select stocks above and click 'Fetch Earnings Data' to view earnings calendar.")
