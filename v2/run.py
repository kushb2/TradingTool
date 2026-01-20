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
from v2.data.alphavantage_service import (
    fetch_earnings_calendar,
    fetch_earnings_history,
    fetch_company_overview
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

# Stock input
st.subheader("Select Stocks for Analysis")

# Multiselect dropdown for popular stocks
selected_stocks = st.multiselect(
    "Select from popular stocks:",
    options=popular_stocks
)

# Text input for additional stocks
additional_stocks_str = st.text_input(
    "Or enter comma-separated stock symbols:",
    placeholder="e.g., NETWEB, UNOMINDA, IBM, AAPL",
    help="Enter stock symbols (NSE without .NS suffix, US stocks as-is)"
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
            
            # Create tabs for different data views
            tab_price, tab_earnings = st.tabs(["📊 Price Data", "📅 Earnings"])
            
            # TAB 1: Price Data
            with tab_price:
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
            
            # TAB 2: Earnings Data (Alpha Vantage)
            with tab_earnings:
                st.caption("📌 Earnings data from Alpha Vantage (US stocks only, 25 requests/day limit)")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Next Earnings Date
                    st.markdown("#### 📅 Next Earnings Date")
                    with st.spinner("Fetching earnings calendar..."):
                        calendar_df = fetch_earnings_calendar(symbol, horizon="12month")
                    
                    if calendar_df.empty:
                        st.warning("No upcoming earnings data found. This may be an NSE stock (Alpha Vantage covers US stocks).")
                    else:
                        # Show next earnings date prominently
                        if len(calendar_df) > 0:
                            next_earnings = calendar_df.iloc[0]
                            st.metric(
                                label="Report Date",
                                value=next_earnings.get("reportDate", "N/A")
                            )
                            st.write(f"**Fiscal Quarter:** {next_earnings.get('fiscalDateEnding', 'N/A')}")
                            st.write(f"**EPS Estimate:** {next_earnings.get('estimate', 'N/A')}")
                        
                        # Show full calendar
                        with st.expander("View All Upcoming Earnings", expanded=False):
                            st.dataframe(calendar_df, use_container_width=True)
                            
                            # Download button for earnings calendar
                            csv_calendar = calendar_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Earnings Calendar (CSV)",
                                data=csv_calendar,
                                file_name=f"{symbol}_earnings_calendar.csv",
                                mime="text/csv"
                            )
                
                with col2:
                    # Historical EPS
                    st.markdown("#### 📊 EPS History")
                    with st.spinner("Fetching earnings history..."):
                        earnings_data = fetch_earnings_history(symbol)
                    
                    if not earnings_data or earnings_data.get("quarterly", pd.DataFrame()).empty:
                        st.warning("No earnings history found.")
                    else:
                        quarterly_df = earnings_data.get("quarterly", pd.DataFrame())
                        
                        if not quarterly_df.empty:
                            # Show last 4 quarters
                            recent_quarters = quarterly_df.head(4)
                            
                            # Display key metrics
                            for _, row in recent_quarters.iterrows():
                                fiscal_date = row.get("fiscalDateEnding", "N/A")
                                reported_eps = row.get("reportedEPS", "N/A")
                                estimated_eps = row.get("estimatedEPS", "N/A")
                                surprise_pct = row.get("surprisePercentage", "N/A")
                                
                                # Color code surprise
                                try:
                                    surprise_val = float(surprise_pct)
                                    if surprise_val > 0:
                                        surprise_color = "🟢"
                                    elif surprise_val < 0:
                                        surprise_color = "🔴"
                                    else:
                                        surprise_color = "⚪"
                                except:
                                    surprise_color = "⚪"
                                
                                st.write(f"**{fiscal_date}:** EPS {reported_eps} (Est: {estimated_eps}) {surprise_color} {surprise_pct}%")
                            
                            # Show full history
                            with st.expander("View Full EPS History", expanded=False):
                                st.dataframe(quarterly_df, use_container_width=True)
                                
                                # Download button for EPS history
                                csv_eps = quarterly_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download EPS History (CSV)",
                                    data=csv_eps,
                                    file_name=f"{symbol}_eps_history.csv",
                                    mime="text/csv"
                                )
                
                # Company Overview (optional)
                with st.expander("🏢 Company Overview", expanded=False):
                    with st.spinner("Fetching company overview..."):
                        overview = fetch_company_overview(symbol)
                    
                    if not overview:
                        st.warning("No company overview found.")
                    else:
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.write(f"**Name:** {overview.get('Name', 'N/A')}")
                            st.write(f"**Sector:** {overview.get('Sector', 'N/A')}")
                            st.write(f"**Industry:** {overview.get('Industry', 'N/A')}")
                        
                        with col_b:
                            st.write(f"**Market Cap:** {overview.get('MarketCapitalization', 'N/A')}")
                            st.write(f"**P/E Ratio:** {overview.get('PERatio', 'N/A')}")
                            st.write(f"**EPS:** {overview.get('EPS', 'N/A')}")
                        
                        with col_c:
                            st.write(f"**52W High:** {overview.get('52WeekHigh', 'N/A')}")
                            st.write(f"**52W Low:** {overview.get('52WeekLow', 'N/A')}")
                            st.write(f"**200 DMA:** {overview.get('200DayMovingAverage', 'N/A')}")
            
            st.write("---")
    else:
        st.warning("Please select or enter at least one stock symbol.")
else:
    st.write("👆 Select or enter stock symbols and click 'Analyze Stocks' to begin.")
