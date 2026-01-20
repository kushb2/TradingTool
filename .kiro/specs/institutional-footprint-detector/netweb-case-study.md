# Netweb Technologies Case Study - Smart Money Analysis

This document captures the analysis of Netweb Technologies stock to illustrate how the institutional footprint detection algorithm should work.

## Stock Overview (Jan 14, 2026)

- **Price:** ₹3,187.60 (down 2.6%)
- **Recent trend:** Declining from ₹3,397 (Jan 8) - about 6% correction

## Initial Analysis (Fixed 65% Threshold - FLAWED)

### Rule-by-Rule Check:

#### ❌ Rule 1: Volume-Price Divergence
- Delivery percentages: 21.4%, 17.5%, 12.1%, 13.4%, 15.1%, 12.0%
- **FAILS:** All delivery % are well below 65% threshold
- This indicates speculative trading, not institutional accumulation
- Low delivery = traders buying and selling same day (not holding)

#### ⚠️ Rule 2: Price Position
- Stock down 6% in last week - minor correction
- Would need to see if it's near 200-day MA

#### ❌ Rule 3: Smart Money Footprints
- Price declining on most days (9 out of 10 days are red/down)
- This suggests selling pressure, not accumulation

#### ❌ Rule 4: Delivery Momentum
- Recent 5-day avg delivery: (21.4+17.5+12.1+13.4+15.1)/5 = 15.9%
- Previous 5-day avg: (12.0+11.9+9.1+36.3+31.9)/5 = 20.2%
- **DECLINING delivery** - getting worse, not better!

### Critical Observations:

🚨 **Red Flags:**
- Very low delivery % (12-21%) = Day trading activity, not investing
- Declining delivery trend = Interest is fading
- Consistent price decline with this pattern = Distribution, not accumulation
- Jan 5 huge volume spike (9.1% delivery) but price jumped 8.3% = likely news-driven speculation
- Jan 2 (36.3% delivery) was better, but still below 65% threshold

### What This Pattern Actually Shows:
- This looks like **distribution/selling** by informed players
- Retail speculation (low delivery %)
- Price weakness = sellers in control
- **NOT a smart money accumulation pattern**

**Verdict: DO NOT ENTER ❌**

---

## January 2nd Deep Dive

### Day's Performance:
- **Price:** ₹3,024.10 (down 1.7%)
- **Delivery:** 36.3%
- **Volume:** Significantly higher (wider bar)

### Rule-by-Rule Check for Jan 2:

#### ⚠️ Rule 1: Volume-Price Divergence (Partial Pass)
- ✅ Volume appears elevated
- ❌ Delivery 36.3% - still below 65% threshold
- ✅ Price behavior: -1.7% (within acceptable range of -2% to +3%)

**Verdict:** Good volume, acceptable price action, BUT delivery too low

### What Jan 2 Shows:

**Positive Signs:**
- Higher delivery than surrounding days (36.3% vs typical 12-20%)
- Large volume with contained price decline
- Someone WAS taking delivery despite negative sentiment
- Could indicate early accumulation attempt

**Why It's Still Not Enough:**
- ❌ 36.3% delivery is BORDERLINE at best
- Ideal: 65%+ (genuine institutional buying)
- 36.3% means: For every ₹100 traded, only ₹36 was actual investing
- Remaining ₹64 was intraday speculation

### Comparative Analysis:

| Date | Delivery % | Price Change | Pattern |
|------|------------|--------------|---------|
| Jan 1 | 31.9% | -1.1% | Moderate activity |
| Jan 2 | 36.3% | -1.7% | Spike in delivery |
| Jan 5 | 9.1% | +8.3% | Speculation rally |
| Jan 6-14 | 11-21% | Mixed | Back to trading |

### What happened after Jan 2?
- Price went from ₹3,024 → ₹3,397 (+12.3%) by Jan 8
- Then crashed to ₹3,187 (-6.2%) by Jan 14
- **Classic pump and dump pattern with low delivery**

---

## KEY INSIGHT: Relative Delivery Analysis

### The Problem with Fixed 65% Threshold
The 65% threshold doesn't make sense because delivery should be **relative to past average or deviation in delivery** for that specific stock.

### Revised Smart Money Detection (Relative Delivery Analysis)

#### Statistical Approach:
1. Calculate 20-day average delivery %
2. Calculate standard deviation of delivery %
3. Alert triggered when:
   - Current delivery > (20-day avg + 1.5 × std deviation)
   - OR Current delivery > 1.5× the 20-day average

### For Netweb Technologies:

**Calculation from visible data:**
- Recent delivery %: 36.3%, 31.9%, 9.1%, 11.9%, 12.0%, 15.1%, 13.4%, 12.1%, 17.5%, 21.4%
- **Average: ~18%**
- Jan 2 (36.3%): That's **2× the average** ✅
- Jan 1 (31.9%): That's **1.77× the average** ✅

### Netweb Jan 2 Re-Analysis with Relative Method:

#### ✅ Rule 1A: Delivery Spike Detected
- Jan 1-2 delivery: 31.9% and 36.3%
- Baseline average: ~18%
- **Spike confirmed: 75-100% above normal**

#### ❌ Rule 1B: Sustained Elevation?
- Need to check if delivery stayed elevated for 3+ days in a 10-day window
- Jan 1: 31.9% ✅
- Jan 2: 36.3% ✅
- Jan 5: 9.1% ❌ (collapsed)
- **FAILED: Only 2 days, then it crashed**

#### ✅ Rule 2: Volume Context
- Jan 2 had massive traded quantity
- With elevated delivery = genuine interest
- **Confirmed: Big players were active**

#### ✅ Rule 3: Price Behavior During Spike
- Jan 1: -1.1% with 31.9% delivery
- Jan 2: -1.7% with 36.3% delivery
- **Perfect: Price flat/down while delivery surges = accumulation pattern**

### The Pattern Score for Jan 2:

| Criteria | Check | Score |
|----------|-------|-------|
| Delivery > 1.5× avg | ✅ Yes (2×) | 10/10 |
| Sustained 3+ days | ❌ No (only 2 days) | 3/10 |
| Volume elevated | ✅ Yes | 9/10 |
| Price flat/down | ✅ Yes (-1.7%) | 10/10 |
| Follow-through | ❌ Delivery crashed after | 2/10 |

**Overall Score: 34/50 = 68% - BORDERLINE SIGNAL**

---

## Revised Entry Rules (Relative Method)

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

### For Netweb on Jan 2:
- ✅ Stage 1 triggered
- ❌ Stage 2 FAILED (delivery collapsed to 9.1%, 11.9%)
- ❌ **No entry should have been taken**

---

## What Good Accumulation Looks Like

| Date | Delivery | Avg | Multiple | Pattern |
|------|----------|-----|----------|---------|
| Day 1 | 35% | 18% | 1.94× | ✅ Alert |
| Day 2 | 32% | 18% | 1.78× | ✅ Confirm |
| Day 3 | 22% | 18% | 1.22× | ✅ Sustained |
| Day 4 | 28% | 18% | 1.56× | ✅ Still active |
| Day 5 | 25% | 18% | 1.39× | ✅ Pattern holds |

**That's 5/5 days showing elevated delivery = strong signal**

---

## Revised Complete Framework

1. **Step 1:** Calculate baseline (20-day rolling average delivery)
2. **Step 2:** Identify spikes (>1.5× average)
3. **Step 3:** Confirm pattern (3+ elevated days in 7-day window)
4. **Step 4:** Check price behavior (should be flat or down during accumulation)
5. **Step 5:** Verify volume surge (big volumes on high delivery days)
6. **Step 6:** Monitor follow-through (delivery stays elevated, not one-off)

**Entry:** Only after Stage 2 confirmation (not on first spike day)
**Stop Loss:** Below the low of the accumulation zone

---

## Why Relative Analysis is Better

Each stock has its own delivery characteristics based on:
- Free float
- Institutional holding
- Retail participation
- Stock category (momentum vs value)

The 65% arbitrary rule doesn't account for these differences. A stock with typically 15% delivery showing 30% is MORE significant than a stock with typically 50% delivery showing 65%.
