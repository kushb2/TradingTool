# Implementation Tasks

- [x] 1. Project Setup & Runnable Baseline
  - [x] 1.1 Create v2/ folder structure with all __init__.py files
  - [x] 1.2 Create v2/run.py with basic Streamlit app (title, text input for symbol)
  - [x] 1.3 Create requirements_v2.txt with all dependencies
  - [x] 1.4 TEST: Run `streamlit run v2/run.py` - should show empty dashboard with input field

- [x] 2. Price Data Service (yfinance)
  - [x] 2.1 Create v2/data/price_service.py with `fetch_price_data(symbol, days=60)`
  - [x] 2.2 Update dashboard to call price_service and display raw DataFrame
  - [x] 2.3 TEST: Enter "RELIANCE.NS" - should show 60 days of OHLC data in table

- [-] 2A. Alpha Vantage Earnings Integration
  - [x] 2A.1 Create v2/data/alphavantage_service.py with API key config
  - [x] 2A.2 Implement `fetch_earnings_calendar(symbol)` - get next earnings date
  - [x] 2A.3 Implement `fetch_earnings_history(symbol)` - get historical EPS with surprise data
  - [x] 2A.4 Add "Earnings" tab in dashboard showing: next earnings date, recent EPS history, analyst estimates
  - [x] 2A.5 Add download button for earnings report data (CSV export)
  - [ ] 2A.6 TEST: Enter "IBM" - should show next earnings date and historical EPS

- [ ] 3. NSE Delivery Data Service
  - [ ] 3.1 Create v2/data/nse_service.py with `fetch_delivery_data(symbol, days=60)`
  - [ ] 3.2 Implement nselib as primary source
  - [ ] 3.3 Add fallback to NSE website scraping if nselib fails
  - [ ] 3.4 Update dashboard to show delivery data alongside price data
  - [ ] 3.5 TEST: Enter "RELIANCE" - should show delivery % for last 60 days

- [ ] 4. Derived Metrics Calculation
  - [ ] 4.1 Create v2/engine/metrics.py with `calculate_metrics(price_df, delivery_df)`
  - [ ] 4.2 Implement: Relative_Delivery_Ratio, Volume_Ratio, Price_Change_Pct
  - [ ] 4.3 Implement: Wick_Ratio (handle division by zero)
  - [ ] 4.4 Implement: SMA_50, SMA_200, RSI using pandas_ta
  - [ ] 4.5 Update dashboard to show enriched DataFrame with all metrics
  - [ ] 4.6 TEST: Verify Relative_Delivery_Ratio = Delivery_Pct / 20-day avg for a stock

- [ ] 5. 15-Day Display Table
  - [ ] 5.1 Create formatted 15-day table in dashboard (Date, LTP, Change%, Volume, Vol_Ratio, Delivery%, Rel_Delivery_Ratio)
  - [ ] 5.2 Add row highlighting where Relative_Delivery_Ratio > 1.5 (green background)
  - [ ] 5.3 Add tooltips explaining each column header
  - [ ] 5.4 Add color gradient for trend visualization: green shades for up/high values, red shades for down/low (darker = stronger move)
  - [ ] 5.5 Add Daily Change % column (today vs yesterday) with color coding
  - [ ] 5.6 Add Change vs Average % column (today vs 20-day avg) with color coding
  - [ ] 5.7 TEST: Visually verify highlighting and color gradients show trends at a glance

- [ ] 6. Phase 1 - Alert Detection
  - [ ] 6.1 Create v2/engine/detector.py with `detect_phase1_alerts(metrics_df)`
  - [ ] 6.2 Implement Phase 1 criteria: Rel_Delivery > 1.5 AND Vol_Ratio > 1.3 AND Price_Change between -3% to +3%
  - [ ] 6.3 Add "Alert Day" marker column to 15-day table
  - [ ] 6.4 TEST: Verify alert days are correctly flagged for a known accumulation stock

- [ ] 7. Phase 2 - Pump & Dump Filter
  - [ ] 7.1 Add `detect_phase2_sustainability(metrics_df, alert_days)` to detector.py
  - [ ] 7.2 Implement: Check T+1 and T+2 after each alert - fail if Rel_Delivery drops below 1.0
  - [ ] 7.3 Add "Pump & Dump Warning" indicator to dashboard when filter triggers
  - [ ] 7.4 TEST: Find a stock with unsustained spike, verify warning appears

- [ ] 8. Phase 3 - Confirmation Check
  - [ ] 8.1 Add `detect_phase3_confirmation(metrics_df)` to detector.py
  - [ ] 8.2 Implement: Count days with Rel_Delivery > 1.2 in 7-day window (need >= 3)
  - [ ] 8.3 Implement: Average Wick_Ratio > 0.6 check
  - [ ] 8.4 Implement: Total price change < 5% in window check
  - [ ] 8.5 TEST: Verify confirmation triggers correctly for accumulation pattern

- [ ] 9. Signal Generation
  - [ ] 9.1 Create v2/signals/recommender.py with `generate_signal(detection_result, metrics_df)`
  - [ ] 9.2 Implement BUY signal logic (Phase 3 passed + price near SMA_200 + Wick > 0.6 + RSI < 70)
  - [ ] 9.3 Implement WATCH signal logic (Phase 1 triggered, awaiting confirmation)
  - [ ] 9.4 Implement WATCH-CAUTION signal logic (Pump & Dump warning)
  - [ ] 9.5 Implement SELL signal logic (Rel_Delivery < 1.0 for 3 days + Vol_Ratio > 1.3)
  - [ ] 9.6 Implement HOLD signal logic (default)
  - [ ] 9.7 Add confidence level (High/Med/Low) based on strength of signals
  - [ ] 9.8 TEST: Verify correct signal generated for different stock scenarios

- [ ] 10. Signal Display & UI Polish
  - [ ] 10.1 Add large color-coded signal badge to dashboard (Green=BUY, Red=SELL, Yellow=WATCH, Gray=HOLD)
  - [ ] 10.2 Add one-line explanation below signal
  - [ ] 10.3 Add stop loss suggestion (8% below entry) for BUY signals
  - [ ] 10.4 Add key metrics summary (Rel_Delivery, Vol_Ratio, Wick_Ratio, RSI)
  - [ ] 10.5 TEST: Verify signal badge displays correctly with proper colors

- [ ] 11. Price Chart with Moving Averages
  - [ ] 11.1 Create Plotly candlestick chart with price data
  - [ ] 11.2 Add SMA_50 line (blue)
  - [ ] 11.3 Add SMA_200 line (red)
  - [ ] 11.4 Add hover tooltips showing OHLC values
  - [ ] 11.5 TEST: Verify chart renders with both MA lines visible

- [ ] 12. Multi-Stock Support
  - [ ] 12.1 Update input to accept comma-separated symbols (max 10)
  - [ ] 12.2 Create summary table showing all stocks with their signals
  - [ ] 12.3 Allow clicking a stock to see detailed view
  - [ ] 12.4 TEST: Enter 3-5 stocks, verify summary table and drill-down works

- [ ] 13. Help Section
  - [ ] 13.1 Add "Help & Learn" expandable section in sidebar
  - [ ] 13.2 Add explanations for: RSI, Delivery %, Relative Delivery Ratio, Volume Ratio, Wick Ratio, SMA, Accumulation, Distribution
  - [ ] 13.3 Ensure all column headers have hover tooltips
  - [ ] 13.4 TEST: Verify help section is accessible and tooltips work

- [ ] 14. Error Handling & Edge Cases
  - [ ] 14.1 Handle nselib timeout/failure - show "Data Unavailable" message
  - [ ] 14.2 Handle insufficient history (< 60 days) - show warning
  - [ ] 14.3 Handle invalid symbol input - show error message
  - [ ] 14.4 Handle division by zero in Wick_Ratio calculation
  - [ ] 14.5 TEST: Enter invalid symbol, verify graceful error message
