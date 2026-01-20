import streamlit as st
import pandas as pd
from app.services.stock_data_service import StockDataService
from app.managers.stock_analysis_manager import StockAnalysisManager
from app.models.stock import Stock
from app.common.constants import DEFAULT_TICKERS, DASHBOARD_COLUMNS, RSI_HISTORY_DAYS
from app.helpers.rsi_helper import get_rsi_description

# 1. Page Configuration
st.set_page_config(page_title="Swing Trading Tool", layout="wide")
st.title("📈 Swing Trading Dashboard")

# 2. Sidebar for User Input
st.sidebar.header("Configuration")
# In the Sidebar section
fetch_fundamentals = st.sidebar.checkbox("Fetch Fundamental Data (PE Ratio)", value=False)
ticker_input = st.sidebar.text_area("Enter Stock Tickers (comma separated)", DEFAULT_TICKERS)

# Convert string input to a clean list
ticker_list = [x.strip() for x in ticker_input.split(',')]

# 3. The "Run" Button
if st.sidebar.button("Analyze Stocks"):
    st.write(f"Analyzing {len(ticker_list)} stocks...")

    # Create a placeholder for the results list
    results = []
    processed_stocks = []

    # Create a progress bar
    progress_bar = st.progress(0)

    stock_data_service = StockDataService()
    stock_analysis_manager = StockAnalysisManager()

    for i, ticker in enumerate(ticker_list):
        # Update progress
        progress_bar.progress((i + 1) / len(ticker_list))

        try:
            stock_data = stock_data_service.fetch_history(ticker)
            if not stock_data:
                st.error(f"Error analyzing {ticker}: No data found")
                continue

            stock = stock_analysis_manager.calculate_metrics(ticker, stock_data)

            if stock.analysis:
                # Add the ticker name to the analysis dict for the table
                row = stock.analysis
                row['Ticker'] = ticker
                row['RSI_Description'] = get_rsi_description(row['RSI'])
                results.append(row)
                processed_stocks.append(stock)
        except Exception as e:
            st.error(f"Error analyzing {ticker}: {e}")

    # 4. Display Results
    if results:
        # Convert list of dicts to a DataFrame for a beautiful interactive table
        df_results = pd.DataFrame(results)

        # Reorder columns to put Ticker first
        final_cols = [c for c in DASHBOARD_COLUMNS if c in df_results.columns]

        st.subheader("Analysis Results")

        # Display the data as an interactive table
        st.dataframe(df_results[final_cols], use_container_width=True)

        st.subheader("🚀 Potential Breakouts (Volume Spikes)")
        for res in results:
            # If Volume is > 1.5x average AND RSI is not overbought yet
            if 'Volume_Spike' in res and 'RSI' in res and res['Volume_Spike'] > 1.5 and res['RSI'] < 70:
                st.write(f"**{res['Ticker']}** is seeing high volume! (Spike: {res['Volume_Spike']}x)")

        # 5. Visual Highlight (Bonus)
        # Show a chart of RSI values to quickly spot oversold stocks
        st.subheader(f"RSI {RSI_HISTORY_DAYS}-Day Trend")
        for stock in processed_stocks:
            with st.expander(f"RSI Trend for {stock.ticker}"):
                if stock.rsi_series is not None and not stock.rsi_series.empty:
                    rsi_history = stock.rsi_series.tail(RSI_HISTORY_DAYS)
                    rsi_df = pd.DataFrame({
                        'Date': rsi_history.index.strftime('%Y-%m-%d'),
                        'RSI': rsi_history.values.round(2)
                    })
                    rsi_df['Description'] = rsi_df['RSI'].apply(get_rsi_description)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("RSI Data")
                        st.dataframe(rsi_df)
                    with col2:
                        st.write("RSI Chart")
                        st.line_chart(rsi_df.set_index('Date')['RSI'])
                else:
                    st.write("Not enough data to calculate RSI trend.")

        # Highlight potential buys
        st.markdown("### 🔔 Potential Signals")
        for res in results:
            if 'RSI' in res:
                rsi_value = res['RSI']
                rsi_description = get_rsi_description(rsi_value)
                if rsi_description == "Oversold":
                    st.success(f"**BUY SIGNAL?** {res['Ticker']} is {rsi_description} (RSI: {rsi_value})")
                elif rsi_description == "Overbought":
                    st.warning(f"**SELL SIGNAL?** {res['Ticker']} is {rsi_description} (RSI: {rsi_value})")
                else:
                    st.info(f"**NEUTRAL**: {res['Ticker']} RSI is {rsi_value}, which is considered neutral.")
        
        st.markdown("---")
        st.subheader("📉 Price vs Moving Average (Visual Analysis)")

        # Create a dropdown to select which stock to visualize
        selected_ticker = st.selectbox("Select a Stock to View Chart:", [s.ticker for s in processed_stocks])

        if selected_ticker:
            selected_stock = next((s for s in processed_stocks if s.ticker == selected_ticker), None)

            if selected_stock and selected_stock.history is not None:
                with st.spinner(f"Generating chart for {selected_ticker}..."):
                    chart_data = selected_stock.history[['Close']].copy()
                    chart_data['50_DMA'] = chart_data['Close'].rolling(window=50).mean()

                    # Streamlit Line Chart
                    st.line_chart(chart_data[['Close', '50_DMA']])

                    # Engineering Note:
                    # If 'Close' line crosses above '50_DMA' line from below,
                    # that is often considered a Bullish (Buy) Signal.
    else:
        st.warning("No data found. Please check ticker symbols.")
else:
    st.info("👈 Enter tickers in the sidebar and click 'Analyze Stocks'")