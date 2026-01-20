# Requirements Document

## Introduction

This is a personal tool for detecting institutional footprint in NSE stocks. Built for analyzing 5-10 fundamentally sound stocks at a time. The goal is to identify when institutional investors ("smart money") are accumulating shares by analyzing delivery percentage patterns relative to each stock's own baseline.

**Core Philosophy:**
- Simple over complex - if I don't understand it, we don't build it
- Test each feature with 1-2 real stocks before moving forward
- No need for liquidity/quality filters - I pick fundamental stocks
- Relative thresholds (vs stock's own average) over fixed percentages

**Reference:** Full algorithm details in `institutional_footprint_algo.md` (kept for reference, not all features needed)

## Glossary

- **Delivery_Percentage**: Percentage of traded shares that result in actual delivery (ownership transfer) vs intraday trading
- **Relative_Delivery_Ratio**: Today's delivery % divided by 20-day average delivery % (e.g., 1.5 means 50% above normal)
- **Accumulation_Day**: A day where delivery is significantly above baseline with volume support and stable price
- **Wick_Ratio**: (Close - Low) / (High - Low) - measures if buyers stepped in at lower prices
- **SMA_200**: 200-day Simple Moving Average - long-term trend indicator
- **Pump_and_Dump**: Artificial price spike followed by crash - we want to avoid these

## Requirements

### Requirement 1: NSE Delivery Data Integration

**User Story:** As a trader, I want to fetch delivery percentage data from NSE, so that I can identify institutional buying patterns.

#### Acceptance Criteria

1. WHEN a user requests analysis for an NSE stock, THE NSE_Data_Service SHALL fetch daily delivery data for the last **60 trading days** (needed for 20-day rolling baseline calculations)
2. WHEN the nselib API returns valid data, THE NSE_Data_Service SHALL parse and return: Date, OHLC, Volume, Delivery Quantity, and Delivery Percentage
3. IF nselib fails, THEN THE NSE_Data_Service SHALL attempt NSE website scraping as fallback
4. IF both sources fail, THEN THE system SHALL display "Data Unavailable" and NOT compute signals on partial data
5. WHEN delivery data is fetched, THE NSE_Data_Service SHALL cache data for the session to avoid repeated API calls

### Requirement 2: Derived Metrics Calculation

**User Story:** As a trader, I want the system to calculate relative metrics, so that I can compare today's activity against the stock's own baseline.

#### Acceptance Criteria

1. WHEN processing stock data, THE system SHALL calculate these derived metrics:
   - **Baseline_Delivery_Avg**: Rolling 20-day mean of Delivery_Pct
   - **Relative_Delivery_Ratio**: Delivery_Pct / Baseline_Delivery_Avg
   - **Volume_Ratio**: Volume / Rolling 20-day Avg Volume
   - **Price_Change_Pct**: (Close - Prev_Close) / Prev_Close × 100
   - **Wick_Ratio**: (Close - Low) / (High - Low) - handle division by zero when High == Low
   - **SMA_50** and **SMA_200**: Simple Moving Averages
2. WHEN there is insufficient data (stock < 60 days old), THE system SHALL display "Insufficient History" warning

### Requirement 3: Last 15 Days Data Display

**User Story:** As a trader, I want to see the last 15 days of data with relative metrics, so that I can visually spot accumulation patterns.

#### Acceptance Criteria

1. WHEN a stock is selected, THE Dashboard SHALL display a table with last 15 days showing: Date, LTP, Daily Change %, Volume, Volume_Ratio, Delivery %, and **Relative_Delivery_Ratio**
2. WHEN displaying the table, THE Dashboard SHALL highlight rows where **Relative_Delivery_Ratio > 1.5** (not fixed 70%)
3. WHEN displaying the table, THE Dashboard SHALL show an "Accumulation Day" marker for days meeting Phase 1 criteria
4. WHEN delivery data is unavailable, THE Dashboard SHALL display "N/A"

### Requirement 4: Institutional Activity Detection (3-Phase Algorithm)

**User Story:** As a trader, I want the system to detect accumulation using relative thresholds, so that I catch institutional activity specific to each stock's behavior.

#### Acceptance Criteria

**Phase 1 - Alert Trigger:**
1. WHEN analyzing the last 7 days, THE system SHALL flag an "Alert Day" if ANY day meets ALL of:
   - Relative_Delivery_Ratio > 1.5 (50% above baseline)
   - Volume_Ratio > 1.3 (30% above average volume)
   - Price_Change_Pct between -3% and +3% (price stealth)

**Phase 2 - Sustainability Test (Pump & Dump Filter):**
2. WHEN an Alert Day is detected on Day T, THE system SHALL check T+1 and T+2:
   - IF Relative_Delivery_Ratio drops below 1.0 on T+1 OR T+2, THEN mark as "Pump & Dump Warning"
   - IF Relative_Delivery_Ratio stays above 1.0 for both days, THEN pass sustainability test

**Phase 3 - Confirmation:**
3. WHEN checking for BUY signal, THE system SHALL require within a 7-day window:
   - At least 3 days with Relative_Delivery_Ratio > 1.2
   - Average Wick_Ratio > 0.6 (buying at dips)
   - Total price change < 5% (catching it before breakout)

### Requirement 5: Recommendation Engine

**User Story:** As a trader, I want clear BUY/SELL/HOLD/WATCH signals with simple explanations, so that I can make decisions quickly.

#### Acceptance Criteria

1. THE Recommendation_Engine SHALL generate one of 4 signals: **BUY, SELL, HOLD, WATCH**

2. **BUY Signal** requires ALL of:
   - Phase 3 confirmation passed (3+ elevated delivery days)
   - Price within 5% of SMA_200 OR between SMA_200 and SMA_50
   - Average Wick_Ratio > 0.6
   - RSI < 70 (not overbought)

3. **WATCH Signal** when:
   - Phase 1 Alert triggered but Phase 2/3 not yet confirmed
   - Display: "Accumulation started. Awaiting confirmation."

4. **WATCH - CAUTION Signal** when:
   - Pump & Dump filter triggered
   - Display: "Delivery spike not sustained. Possible speculation."

5. **SELL Signal** when:
   - Relative_Delivery_Ratio < 1.0 for 3 consecutive days
   - Volume_Ratio > 1.3 (high volume distribution)
   - Display: "Distribution detected - institutions may be exiting"

6. **HOLD Signal** when:
   - None of the above conditions met

7. WHEN generating any signal, THE system SHALL show:
   - Signal badge (large, color-coded)
   - Confidence: High / Medium / Low
   - Key metrics: Relative_Delivery_Ratio, Volume_Ratio, Wick_Ratio
   - Simple one-line explanation

8. WHEN BUY signal generated, THE system SHALL suggest:
   - Stop Loss: 8% below entry price
   - Exit trigger: "Exit if delivery drops below average for 3 days with volume spike"

### Requirement 6: Raw Data Visibility

**User Story:** As a learning trader, I want to see all raw data behind each recommendation, so that I can understand and validate the analysis.

#### Acceptance Criteria

1. WHEN displaying a recommendation, THE Dashboard SHALL show all input data: delivery %, volume ratios, price changes, RSI for the analysis period
2. WHEN displaying data, THE Dashboard SHALL include tooltips explaining each metric in simple terms
3. WHEN a user expands detailed view, THE Dashboard SHALL show day-by-day classification (Accumulation Day / Normal / Distribution)

### Requirement 7: Dashboard Integration

**User Story:** As a trader, I want all features in one unified dashboard, so that I have a complete view.

#### Acceptance Criteria

1. WHEN the dashboard loads, THE Dashboard SHALL maintain existing functionality (52-week high/low, 50-day MA, RSI, volume spike, earnings date)
2. WHEN displaying results table, THE Dashboard SHALL add columns: SMA_200, Latest Relative_Delivery_Ratio, Institutional Signal
3. WHEN a stock is selected, THE Dashboard SHALL show "Institutional Footprint" section with 15-day table and recommendation
4. WHEN displaying charts, THE Dashboard SHALL add SMA_200 line to price chart

### Requirement 8: Simple & Clear UI

**User Story:** As a user, I want a clean interface that shows me what matters without overwhelming details.

#### Acceptance Criteria

1. THE Dashboard SHALL use color coding:
   - Green: BUY / Accumulation signals
   - Red: SELL / Distribution signals  
   - Yellow/Orange: WATCH signals
   - Gray: HOLD / Neutral
2. THE Dashboard SHALL highlight rows where Relative_Delivery_Ratio > 1.5 (green background)
3. THE Dashboard SHALL use large, clear signal badges that are immediately visible
4. THE Dashboard SHALL provide hover tooltips for all trading terms

### Requirement 9: Code Documentation

**User Story:** As the developer/user, I want code comments explaining trading concepts, so that I can understand and maintain the tool.

#### Acceptance Criteria

1. WHEN writing code, THE Developer SHALL include inline comments explaining trading concepts in simple terms
2. WHEN defining functions, THE Developer SHALL include docstrings explaining business purpose
3. WHEN using thresholds, THE Code SHALL include comments explaining why (e.g., "1.5× because 50% above normal is statistically significant")

### Requirement 10: Educational Help Section

**User Story:** As a learning trader, I want explanations of all metrics, so that I can build my knowledge.

#### Acceptance Criteria

1. THE Dashboard SHALL include a "Help & Learn" section in sidebar
2. THE Help section SHALL explain: RSI, Delivery %, Relative Delivery Ratio, Volume Spike, Moving Averages, Accumulation, Distribution, Wick Ratio
3. WHEN a user hovers over any metric, THE Dashboard SHALL show a quick tooltip with explanation
