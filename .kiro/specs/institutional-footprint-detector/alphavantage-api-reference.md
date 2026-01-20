# Alpha Vantage API Reference

**Base URL:** `https://www.alphavantage.co/query`  
**API Key:** Store in environment variable `ALPHAVANTAGE_API_KEY`

## Relevant APIs for Our Use Case

### 1. Earnings Calendar (Primary - Next Earnings Date)

Returns upcoming earnings dates for a company.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={SYMBOL}&horizon={HORIZON}&apikey={API_KEY}
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| function | Yes | `EARNINGS_CALENDAR` |
| symbol | No | Stock symbol (e.g., `IBM`). If omitted, returns all companies |
| horizon | No | `3month` (default), `6month`, or `12month` |
| apikey | Yes | Your API key |

**Response Format:** CSV

**Example:**
```
https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol=IBM&horizon=12month&apikey=demo
```

**Response Fields:**
- symbol
- name
- reportDate
- fiscalDateEnding
- estimate
- currency

---

### 2. Earnings History (Historical EPS Data)

Returns annual and quarterly earnings (EPS) with analyst estimates and surprise metrics.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=EARNINGS&symbol={SYMBOL}&apikey={API_KEY}
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| function | Yes | `EARNINGS` |
| symbol | Yes | Stock symbol (e.g., `IBM`) |
| apikey | Yes | Your API key |

**Response Format:** JSON

**Example:**
```
https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo
```

**Response Structure:**
```json
{
  "symbol": "IBM",
  "annualEarnings": [
    {
      "fiscalDateEnding": "2023-12-31",
      "reportedEPS": "9.62"
    }
  ],
  "quarterlyEarnings": [
    {
      "fiscalDateEnding": "2023-12-31",
      "reportedDate": "2024-01-24",
      "reportedEPS": "3.87",
      "estimatedEPS": "3.78",
      "surprise": "0.09",
      "surprisePercentage": "2.3810"
    }
  ]
}
```

---

### 3. Earnings Estimates (Analyst Forecasts)

Returns EPS and revenue estimates with analyst count and revision history.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol={SYMBOL}&apikey={API_KEY}
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| function | Yes | `EARNINGS_ESTIMATES` |
| symbol | Yes | Stock symbol (e.g., `IBM`) |
| apikey | Yes | Your API key |

**Response Format:** JSON

---

### 4. Earnings Call Transcript

Returns earnings call transcript with LLM-based sentiment signals.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={SYMBOL}&quarter={QUARTER}&apikey={API_KEY}
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| function | Yes | `EARNINGS_CALL_TRANSCRIPT` |
| symbol | Yes | Stock symbol (e.g., `IBM`) |
| quarter | Yes | Fiscal quarter in `YYYYQM` format (e.g., `2024Q1`) |
| apikey | Yes | Your API key |

**Note:** Covers 15+ years of history since 2010Q1.

---

### 5. Company Overview (Fundamentals)

Returns company info, financial ratios, and key metrics.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=OVERVIEW&symbol={SYMBOL}&apikey={API_KEY}
```

**Response includes:**
- Company description
- Sector, Industry
- Market Cap
- P/E Ratio, PEG Ratio
- Book Value, Dividend Yield
- EPS, Revenue TTM
- 52 Week High/Low
- 50 DMA, 200 DMA

---

### 6. Income Statement

Returns annual and quarterly income statements.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={SYMBOL}&apikey={API_KEY}
```

---

### 7. Dividends

Returns historical and future (declared) dividend distributions.

**Endpoint:**
```
GET https://www.alphavantage.co/query?function=DIVIDENDS&symbol={SYMBOL}&apikey={API_KEY}
```

---

## API Limits (Free Tier)

- **Rate Limit:** 25 requests per day
- **Premium:** Unlimited requests with paid plans

## Implementation Notes

1. **NSE Stocks:** Alpha Vantage primarily covers US stocks. For NSE stocks, we may need to:
   - Use BSE/NSE symbol with `.BSE` or `.NSE` suffix (check if supported)
   - Fall back to other sources for Indian stocks

2. **CSV Parsing:** EARNINGS_CALENDAR returns CSV, not JSON. Use pandas `read_csv()` with `StringIO`.

3. **Caching:** Given the 25/day limit, cache responses aggressively.

4. **Error Handling:** API returns JSON with error message if symbol not found or rate limited.

---

## Quick Reference - Our Use Cases

| Use Case | API Function | Format |
|----------|--------------|--------|
| Next earnings date | `EARNINGS_CALENDAR` | CSV |
| Historical EPS + surprise | `EARNINGS` | JSON |
| Analyst estimates | `EARNINGS_ESTIMATES` | JSON |
| Earnings call transcript | `EARNINGS_CALL_TRANSCRIPT` | JSON |
| Company fundamentals | `OVERVIEW` | JSON |
