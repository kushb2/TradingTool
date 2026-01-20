# Design Document - Institutional Footprint Detector v2

## Overview

Fresh v2 implementation - completely separate from existing code. Simple, testable, easy to pivot.

**Tech Stack:**
- Data: yfinance, nselib, requests (fallback)
- Logic: pandas, numpy, pandas_ta
- UI: streamlit, plotly
- Future: Upstox/Angel One APIs for live data

## File Structure

```
v2/
├── __init__.py
├── data/
│   ├── __init__.py
│   ├── nse_service.py      # Fetch delivery data from NSE
│   └── price_service.py    # Fetch OHLC from yfinance
├── engine/
│   ├── __init__.py
│   ├── metrics.py          # Calculate derived metrics (ratios, MAs)
│   └── detector.py         # 3-phase accumulation detection
├── signals/
│   ├── __init__.py
│   └── recommender.py      # Generate BUY/SELL/HOLD/WATCH
├── ui/
│   ├── __init__.py
│   └── dashboard.py        # Streamlit app
└── run.py                  # Entry point: streamlit run v2/run.py
```

## Components

### 1. Data Layer (`v2/data/`)

**nse_service.py**
- `fetch_delivery_data(symbol, days=60)` → DataFrame with delivery %
- Primary: nselib | Fallback: NSE website scraping
- Returns: Date, Volume, Delivery_Qty, Delivery_Pct

**price_service.py**
- `fetch_price_data(symbol, days=60)` → DataFrame with OHLC
- Source: yfinance
- Returns: Date, Open, High, Low, Close, Volume

### 2. Engine Layer (`v2/engine/`)

**metrics.py**
- `calculate_metrics(price_df, delivery_df)` → DataFrame with all derived columns
- Calculates: Relative_Delivery_Ratio, Volume_Ratio, Wick_Ratio, SMA_50, SMA_200, RSI, Price_Change_Pct

**detector.py**
- `detect_accumulation(metrics_df)` → dict with phase results
- Implements 3-phase algorithm:
  - Phase 1: Alert days
  - Phase 2: Pump & dump filter
  - Phase 3: Confirmation check

### 3. Signals Layer (`v2/signals/`)

**recommender.py**
- `generate_signal(detection_result, metrics_df)` → Signal object
- Returns: signal (BUY/SELL/HOLD/WATCH), confidence (High/Med/Low), explanation, stop_loss

### 4. UI Layer (`v2/ui/`)

**dashboard.py**
- Streamlit app with:
  - Stock input (5-10 symbols)
  - 15-day data table with highlighting
  - Signal badges
  - Price chart with SMA lines
  - Help tooltips

## Data Flow

```
User enters symbol
       ↓
[nse_service] + [price_service] → raw DataFrames
       ↓
[metrics.py] → enriched DataFrame with ratios
       ↓
[detector.py] → phase results (alerts, sustainability, confirmation)
       ↓
[recommender.py] → final signal + explanation
       ↓
[dashboard.py] → display table, chart, signal badge
```

## Key Design Decisions

1. **Separate v2 folder** - No mixing with old code, clean slate
2. **Thin layers** - Each file does one thing
3. **DataFrame-centric** - Pass DataFrames between components, easy to debug
4. **No caching complexity** - Session-level only (Streamlit handles this)
5. **Future-ready** - Easy to swap yfinance/nselib with Upstox/Angel One later

## Testing Approach

Test each component with 1-2 real stocks before moving on:
1. First: nse_service + price_service (can we fetch data?)
2. Then: metrics.py (are calculations correct?)
3. Then: detector.py (does it flag the right days?)
4. Finally: full flow in dashboard

---

*This design is intentionally minimal. Update as we pivot.*
