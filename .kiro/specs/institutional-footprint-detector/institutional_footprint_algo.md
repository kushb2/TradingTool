# Institutional Footprint Engine Algorithm

**Version:** 2.1 (Relative Delivery Update)  
**Context:** Institutional Accumulation Detection for Indian Equities (NSE)  
**Role:** Core Logic Engine  
**Approved by:** Chief Investment Officer

---

## 1. System Philosophy

### 1.1 Objective
Identify "Smart Money" accumulation by detecting statistical anomalies in delivery percentages relative to a stock's own baseline, rather than arbitrary fixed thresholds.

### 1.2 Core Principle: "The Remora Strategy"
We do not predict market moves; we detect when the 'Whales' (Institutions) have already committed capital and hitch a ride on their wake.

### 1.3 Risk Profile
High selectivity. **Better to miss a trade than to enter a false signal (Pump & Dump).**

### 1.4 Key Philosophical Tenets
- **Relative > Absolute:** A delivery spike of 35% in a stock that averages 15% is more significant than 65% in a stock that averages 60%.
- **Price Stealth:** True accumulation happens quietly. High volume + High delivery + Flat Price = Accumulation. High Price Jump + Low Delivery = Speculation.
- **Validation:** A single spike is a "Watch" signal. A cluster of spikes is a "Buy" signal.

---

## 2. Data Ingestion & Pre-Processing Requirements

### 2.1 Required Data Window
- **Fetch Range:** Current Date minus **60 Days (Minimum)**
- **Reason:** We need a 20-day rolling window to establish the baseline. To have a valid baseline for the data displayed 15 days ago, we need data preceding that.
- **Note:** The standard "Last 15 Days" fetch is insufficient for calculation (though fine for display).

### 2.2 Raw Input Variables (Per Stock)
- Date
- Open, High, Low, Close (OHLC)
- Volume (Total Traded Quantity)
- Delivery_Quantity (or Delivery %)
- VWAP (Optional, if available from data source)

### 2.3 Derived Metric Calculation (Vectorized)
Before applying rules, compute the following columns for the entire dataframe:

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Delivery_Pct** | `(Delivery_Quantity / Volume) * 100` | Base delivery percentage |
| **Baseline_Delivery_Avg** | Rolling 20-day Mean of Delivery_Pct | Historical average |
| **Baseline_Delivery_StdDev** | Rolling 20-day Standard Deviation of Delivery_Pct | Volatility measure |
| **Relative_Delivery_Ratio** | `Delivery_Pct / Baseline_Delivery_Avg` | **Key Signal** (Target: > 1.5x) |
| **Volume_Ratio** | `Volume / Rolling_20_Day_Avg_Volume` | Volume anomaly detector |
| **Price_Change_Pct** | `(Close - Prev_Close) / Prev_Close * 100` | Price movement |
| **Wick_Ratio** | `(Close - Low) / (High - Low)` | Buying pressure indicator |
| **SMA_50** | 50-day Simple Moving Average | Short-term trend |
| **SMA_200** | 200-day Simple Moving Average | Long-term support |

**Note:** Handle division by zero for Wick_Ratio when High == Low.

---

## 3. The Core Algorithm: "Relative Footprint" Detector

The detection logic operates in a **State Machine** format. It evaluates the most recent **7-day window** for specific sequences.

### Phase 1: The Alert Trigger (Day T)
A stock enters the **"Watchlist"** state if any single day in the last 7 days meets these criteria:

#### Criterion A (Statistical Anomaly)
```
Delivery_Pct > (Baseline_Delivery_Avg + 1.5 * Baseline_Delivery_StdDev)
  OR
Relative_Delivery_Ratio > 1.5 (150% of normal)
```

#### Criterion B (Volume Support)
```
Volume_Ratio > 1.3
```

#### Criterion C (Price Stealth)
```
Price_Change_Pct is between -3.0% and +3.0%
```
**Logic:** Institutions buy without moving the price up initially.

---

### Phase 2: The Sustainability Test (Pump & Dump Filter)
If an Alert (Phase 1) is detected on Day T, analyze T+1 and T+2:

#### FAIL Condition (Pump & Dump)
```
IF Relative_Delivery_Ratio drops below 1.0 
   (Back to average or lower) on T+1 OR T+2
THEN Mark as SIGNAL_REJECTED_SPECULATION
```

#### PASS Condition
```
Relative_Delivery_Ratio remains > 1.0 
(Above average) for next 2 days
```

---

### Phase 3: The Confirmation Pattern (The Entry Key)
To generate a **BUY** signal, the following "Cluster Validity" check must pass within a rolling 7-day window:

#### Frequency Check
- **Count:** Days where `Relative_Delivery_Ratio > 1.2`
- **Requirement:** Count >= 3 (The initial spike + 2 follow-up days)

#### Wick Validation
- **Calculate:** Average Wick_Ratio for the accumulation days
- **Requirement:** Avg > 0.6 (Evidence of buying at intraday lows)

#### Price Trend Validation
- **Total Price change** over the 7-day window < 5%
- **Rationale:** We want to catch it before the breakout

---

## 4. Contextual Filters (The "Quality" Gates)

Even if the algorithmic pattern matches, the stock is rejected if it fails these solvency and structural checks. **Execute these FIRST. If FAIL, return SIGNAL_IGNORE.**

### 4.1 Liquidity & Manipulation Gates
| Gate | Requirement | Purpose |
|------|-------------|---------|
| **Market Cap Check** | > ₹1,000 Crores | Avoid micro-caps |
| **Liquidity Check** | `Close * Rolling_Avg_Volume > ₹10 Crores` (Daily Value) | Ensure tradability |
| **Penny Stock Filter** | `Close > ₹50` | Avoid manipulation-prone stocks |

### 4.2 Location Gates (Trend Alignment)

#### The 200 DMA Rule
```
Current_Price must be within ±5% of SMA_200
  OR
Current_Price is > SMA_200 AND < SMA_50 (Pullback to support)
```

#### Overextension Check
```
RSI (14) must be < 70 (Not overbought)
```

---

## 5. Scoring & Signal Generation Logic

The Recommendation Engine will output one of **four states** based on the logic below.

### Output Logic (Pseudo-Code)

```python
IF (Manipulation_Gates == FAIL):
    RETURN "IGNORE" 
    Reason: "Low Quality - Failed structural filters"

IF (Pattern_Detected == TRUE):
    
    IF (Pump_Dump_Check == FAIL):
        RETURN "WATCH - CAUTION"
        Reason: "Delivery Spike detected but not sustained. Possible speculation."
        
    IF (Frequency_Count >= 3) AND (Location_Gate == PASS):
        SCORE = Calculate_Confidence_Score() # See Section 6
        RETURN "BUY"
        Reason: "Confirmed Institutional Accumulation (Stage 3). Risk/Reward Optimal."
        
    IF (Frequency_Count < 3) AND (Frequency_Count >= 1):
        RETURN "WATCH"
        Reason: "Accumulation started (Stage 1). Awaiting confirmation."

ELSE:
    IF (Held_Position == TRUE) AND (Delivery_Trend < Baseline FOR 3 DAYS) AND (Volume > 1.5x):
        RETURN "SELL"
        Reason: "Distribution Detected (High Volume, Low Delivery)."
    
    RETURN "HOLD/NEUTRAL"
```

### Signal Definitions

#### Output 1: BUY (Stage 3 Entry)
**Conditions:**
- Count(ACCUMULATION_DAY) >= 3 within the 7-day window
- Price Trend: Total price move in window < 5%
- Wick Test: Avg_Wick_Ratio > 0.6
- Trend Gate: Passed Phase 1 Trend Gate

**Output Payload:**
- Signal: "BUY"
- Stop_Loss: 8% below Entry OR Recent Swing Low
- Confidence: Score (0-100)

#### Output 2: WATCH (Stage 1 or 2 Alert)
**Conditions:**
- Count(ACCUMULATION_DAY) is 1 or 2
- Trend Gate: Passed
- Pump-and-Dump Guard: Not triggered

**Output Payload:**
- Signal: "WATCH"
- Reason: "Accumulation detected (Stage 1/2). Awaiting confirmation (3rd spike)."

#### Output 3: SELL (Distribution Detected)
**Conditions:**
- User holds the stock (if portfolio connected) OR General Analysis
- Volume > 1.3x Avg
- Delivery < 1.0x Baseline (Low quality volume)
- Sequence: Occurs for 3 consecutive days

**Output Payload:**
- Signal: "SELL"
- Reason: "Distribution Pattern: High volume with low delivery."

#### Output 4: AVOID / SPECULATION
**Conditions:**
- Price_Change_Pct > 5% (Sharp Rally)
- Relative_Delivery_Ratio < 1.0 (Low Delivery)

**Output Payload:**
- Signal: "AVOID"
- Reason: "Retail Speculation / Pump. No institutional footprint."

---

## 6. Confidence Scoring Model (0-100)

When a **BUY** signal is generated, attach a confidence score to help position sizing.

| Metric | Weight | Condition for Max Points |
|--------|--------|--------------------------|
| **Delivery Magnitude** | 30% | Spike day is > 2.0x Baseline (200% of normal) |
| **Consistency** | 30% | 4+ days of elevated delivery in 7-day window |
| **Price Stability** | 20% | Price stayed within 2% range during accumulation |
| **Wick Support** | 10% | Avg Lower Wick Ratio > 0.7 |
| **Trend Location** | 10% | Exactly at 200 DMA (Support) |

### Scoring Algorithm

```python
Base_Score = 0

# 1. Magnitude of Interest (Max 30 pts)
if Max(Relative_Delivery_Ratio) > 2.0: 
    Base_Score += 30
elif Max(Relative_Delivery_Ratio) > 1.75: 
    Base_Score += 20
else: 
    Base_Score += 10

# 2. Consistency (Max 30 pts)
Spike_Count = Count(ACCUMULATION_DAY)
if Spike_Count >= 4: 
    Base_Score += 30
elif Spike_Count == 3: 
    Base_Score += 20

# 3. Price Control (Max 20 pts)
Window_Price_Range = Max(High) - Min(Low) in Window
if Window_Price_Range < (Close * 0.05): 
    Base_Score += 20

# 4. Wick Support (Max 10 pts)
if Avg_Wick_Ratio > 0.7:
    Base_Score += 10

# 5. Technical Support (Max 10 pts)
if Abs(Close - SMA_200) < (Close * 0.02): 
    Base_Score += 10  # Very close to 200DMA
```

---

## 7. Execution Parameters (Trade Management)

This data must be presented alongside the signal.

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Entry Zone** | Current Market Price (CMP) | Execute at market |
| **Stop Loss (Hard)** | Entry_Price * 0.92 | 8% Risk |
| **Stop Loss (Structural)** | Lowest Low of 7-day accumulation window | Alternative stop |
| **Target 1** | Entry_Price * 1.15 | 15% Gain |
| **Action at Target 1** | Move Stop Loss to Breakeven | Lock in profits |

### Exit Triggers
- Price Close < Stop Loss
- **OR** Relative_Delivery_Ratio < 0.8 for 3 consecutive days while Price drops

---

## 8. Implementation Notes for Developers

### 8.1 Handle N/A Data
- If stock is new (IPO < 60 days), return `INSUFFICIENT_DATA`
- Do not try to guess the 20-day baseline

### 8.2 Handling IPOs/New Listings
```
IF len(dataframe) < 50:
    SMA_200 = Null
    Baseline_Delivery = Calculate on available data (e.g., 5 days) 
                        but flag reliability as LOW
    Suppress "Trend Gate" failures
    Show warning: "Insufficient History for MA Check"
```

### 8.3 Data Fallback Strategy
**Primary:** Use `nselib` as primary data source

**ERROR HANDLER:** If nselib returns None or raises Timeout:
1. Trigger fallback scraper for NSE Website equity-delivery endpoint
2. If both fail, return `DATA_UNAVAILABLE` status to UI
3. **Do not compute signals on partial data**

**Web Scraping Fallback:** nselib often times out. Ensure the NSE_Data_Service has a robust retry mechanism (exponential backoff) or falls back to HTML parsing of the NSE website if the API fails.

### 8.4 Caching Policy
Because we are fetching 60 days of data to calculate rolling averages, **Cache this aggressively**.

**Cache Strategy:**
- Cache the processed dataframe (with rolling metrics) for 24 hours (or until market close next day)
- Key = `Stock_Symbol + Date`
- Do not re-fetch for every UI refresh

### 8.5 UI Visualization Logic
**In the 15-day history table:**
- Do **NOT** color code based on fixed 60% or 70%
- Color code based on `Relative_Delivery_Ratio` (e.g., Green if > 1.5x)
- When rendering the "Last 15 Days" table, do not verify the "Accumulation" column using simple logic
- Use the `ACCUMULATION_DAY` boolean calculated in Phase 2A
- This ensures the visual table matches the Signal Engine

---

## 9. Glossary

| Term | Definition |
|------|------------|
| **Delivery Percentage** | Percentage of traded volume that resulted in actual delivery (not intraday speculation) |
| **Relative Delivery Ratio** | Current delivery % divided by historical 20-day average |
| **Accumulation Day** | A day meeting all Phase 1 criteria (anomalous delivery + volume + price stealth) |
| **Wick Ratio** | Measures where price closed relative to the day's range; high ratio = buying at lows |
| **SMA_200** | 200-day Simple Moving Average - key institutional support level |
| **Pump & Dump** | Artificial price inflation followed by rapid selling |

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | Current | Relative Delivery Update - moved from fixed thresholds to statistical baseline |
| 2.0 | - | Introduced Relative Delivery Logic |
| 1.x | - | Legacy fixed threshold system |

---

**End of Algorithm Specification**
