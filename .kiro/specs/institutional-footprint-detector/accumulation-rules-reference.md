# Smart Money Accumulation Detection Rules

This document captures the detailed rules for identifying institutional accumulation patterns. These rules form the basis of the Institutional Footprint Detector algorithm.

## Key Insight: Relative Delivery Analysis

**The 65% fixed threshold doesn't make sense** because delivery should be **relative to past average or deviation in delivery** for that specific stock. Each stock has its own delivery characteristics based on:
- Free float
- Institutional holding
- Retail participation
- Stock category (momentum vs value)

A stock with typically 15% delivery showing 30% is MORE significant than a stock with typically 50% delivery showing 65%.

## Core Accumulation Detection Rules (Relative Method)

### Rule 1: Relative Delivery Surge

**Statistical Approach:**
1. Calculate 20-day rolling average delivery %
2. Calculate standard deviation of delivery %
3. Alert triggered when:
   - Current delivery > (20-day avg + 1.5 × std deviation)
   - OR Current delivery > 1.5× the 20-day average

### Rule 2: Volume-Price Divergence

- Daily volume > 130% of 20-day average volume
- Delivery > 1.5× rolling 20-day average (relative, not fixed)
- Price change: -3% to +3% (flat to slightly up despite high volume)
- Apply for at least 3 days in a 7-day window

### Rule 3: Price Position Check

- Current price within 5% of 200-day moving average (either above or below)
- OR price between 200-day MA and 50-day MA
- Stock should have corrected at least 15% from recent 52-week high

### Rule 4: Smart Money Footprints (Lower Wick Analysis)

- Compare: (High - Close) vs (Close - Low) for last 5 days
- Calculate lower wick ratio: (Close - Low) / (High - Low)
- If average lower wick ratio > 0.6 = buying pressure at lows
- Calculate: Daily VWAP vs closing price
- If close > VWAP for 60%+ of accumulation days = institutional buying

### Rule 5: Delivery Momentum (Relative)

- Rolling 5-day average delivery % > rolling 20-day average delivery %
- Delivery % trending upward over 2 weeks
- Total delivery quantity in last 5 days > previous 5 days

## Three-Stage Entry System

### Stage 1: Initial Alert
- Day 1: Delivery > 1.5× rolling 20-day average
- Volume > 1.3× rolling 20-day average
- Price change: -3% to +3%

### Stage 2: Confirmation (Critical)
Within next 5 trading days, need at least 2 MORE days with:
- Delivery > 1.2× average
- Sustained interest, not one-off spike

### Stage 3: Entry Trigger
- 3 out of 7 days show elevated delivery (>1.3× avg)
- Price hasn't rallied more than 5% yet
- No major negative news

**IMPORTANT:** Entry only after Stage 2 confirmation (not on first spike day)

## Quantifiable Entry Checklist

Use this exact sequence on any stock:

1. **Calculate baseline delivery** (20-day rolling average)

2. **Is delivery elevated?**
   - Current delivery > 1.5× baseline = Alert
   - Need 3+ such days in 7-day window for confirmation

3. **Is price near 200-day MA?** (within ±5%)

4. **Last 7 days volume analysis:**
   - Count days where volume > 1.3x average
   - Count days where delivery > 1.2× baseline
   - Need minimum 3 such days

5. **Price behavior during high delivery days:**
   - Calculate average price change on those days
   - Should be between -3% to +3%

6. **Lower wick test (last 5 days):**
   - For each day: (Close - Low) / (High - Low)
   - Average should be > 0.6 (buying at dips)

7. **Delivery sustainability check:**
   - Did delivery stay elevated for 3+ days?
   - Or did it collapse back to normal? (pump-and-dump warning)

8. **Institutional confirmation (if available):**
   - Check if FII/DII data shows net buying
   - Mutual fund holding changes quarter-over-quarter

## Exit/Stop Rules

- **Stop loss:** 8% below entry
- **Trailing stop:** Once up 15%, trail stop to breakeven
- **Time stop:** If no 10% move in 45 days, review position
- **Exit signal:** Delivery % drops below baseline average for 3 consecutive days with volume spike

## Warning Signs (Pump-and-Dump Detection)

- Delivery spike on Day 1-2, then collapses back to normal
- Price rises sharply (>5%) with low delivery (<1.0× average)
- High volume but delivery below average = speculation, not accumulation
- One-off spike without follow-through = likely false signal

## Practical Implementation Tips

### Data you'll need:
- Daily OHLC data
- Volume and delivery data (from NSE/BSE)
- 200-day and 50-day moving averages
- Historical delivery percentages

### Screening process:
1. Filter stocks trading near 200-day MA
2. Run volume spike analysis
3. Calculate delivery metrics
4. Verify price behavior pattern
5. Check wick ratios

### Reality check parameters:
- Win rate expectation: 40-50% (like Medallion, focus on risk-reward)
- Target risk-reward: Minimum 1:2
- Position sizing: No more than 5% per trade
- Maximum positions: 5-7 stocks

## Additional Filters to Avoid False Signals

- Avoid stocks with negative quarterly results in last report
- Market cap > ₹1000 crores (avoid manipulation)
- Average daily traded value > ₹10 crores (liquidity)
- Avoid penny stocks trading below ₹50
