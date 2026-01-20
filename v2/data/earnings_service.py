"""
Earnings Service - Fetches earnings data using yfinance and yahoo_fin

This service provides earnings calendar and historical earnings data
for both NSE (Indian) and US stocks without API limits.

Sources:
- yfinance: ticker.calendar, ticker.get_earnings_dates()
- yahoo_fin: stock_info.get_next_earnings_date()
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Try importing yahoo_fin (optional, provides cleaner next earnings date)
try:
    from yahoo_fin import stock_info as si
    YAHOO_FIN_AVAILABLE = True
except ImportError:
    YAHOO_FIN_AVAILABLE = False
    print("yahoo_fin not installed. Using yfinance only. Install with: pip install yahoo_fin")

# NIFTY 50 symbol for relative performance
NIFTY_SYMBOL = "^NSEI"


def _get_ticker_symbol(symbol: str) -> str:
    """
    Convert symbol to yfinance format.
    NSE stocks need .NS suffix, US stocks use as-is.
    """
    symbol = symbol.upper().strip()
    # If already has suffix, return as-is
    if symbol.endswith(".NS") or symbol.endswith(".BSE"):
        return symbol
    # Common US stocks - don't add suffix
    us_stocks = ["AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "IBM", "NFLX"]
    if symbol in us_stocks:
        return symbol
    # Assume NSE stock, add .NS suffix
    return f"{symbol}.NS"


def fetch_next_earnings_date(symbol: str) -> Optional[datetime]:
    """
    Fetch the next earnings date for a stock.
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS", "AAPL")
    
    Returns:
        datetime of next earnings, or None if not available
    """
    ticker_symbol = _get_ticker_symbol(symbol)
    
    # Method 1: Try yahoo_fin first (cleaner API)
    if YAHOO_FIN_AVAILABLE:
        try:
            date = si.get_next_earnings_date(ticker_symbol)
            if date:
                return date
        except Exception as e:
            print(f"yahoo_fin failed for {symbol}: {e}")
    
    # Method 2: Fall back to yfinance calendar
    try:
        ticker = yf.Ticker(ticker_symbol)
        calendar = ticker.calendar
        
        if calendar is not None and not calendar.empty:
            # calendar is a DataFrame with earnings date info
            if "Earnings Date" in calendar.index:
                earnings_dates = calendar.loc["Earnings Date"]
                if isinstance(earnings_dates, pd.Series) and len(earnings_dates) > 0:
                    return pd.to_datetime(earnings_dates.iloc[0])
                elif isinstance(earnings_dates, (str, datetime)):
                    return pd.to_datetime(earnings_dates)
    except Exception as e:
        print(f"yfinance calendar failed for {symbol}: {e}")
    
    return None


def fetch_earnings_history(symbol: str, limit: int = 12) -> pd.DataFrame:
    """
    Fetch historical earnings dates and EPS data.
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS", "AAPL")
        limit: Number of past earnings to fetch (default 12 = 3 years quarterly)
    
    Returns:
        DataFrame with columns: Date, EPS, Surprise (if available)
        Returns empty DataFrame if fetch fails
    """
    ticker_symbol = _get_ticker_symbol(symbol)
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        earnings_df = ticker.get_earnings_dates(limit=limit)
        
        if earnings_df is None or earnings_df.empty:
            return pd.DataFrame()
        
        # Reset index to make date a column
        earnings_df = earnings_df.reset_index()
        
        # Rename columns for clarity
        column_mapping = {
            "Earnings Date": "Date",
            "EPS Estimate": "EPS_Estimate",
            "Reported EPS": "EPS_Reported",
            "Surprise(%)": "Surprise_Pct"
        }
        earnings_df = earnings_df.rename(columns=column_mapping)
        
        return earnings_df
        
    except Exception as e:
        print(f"Error fetching earnings history for {symbol}: {e}")
        return pd.DataFrame()


def fetch_earnings_calendar(symbol: str) -> Dict[str, Any]:
    """
    Fetch full earnings calendar info from yfinance.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        Dictionary with calendar info (earnings date, revenue estimate, etc.)
    """
    ticker_symbol = _get_ticker_symbol(symbol)
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        calendar = ticker.calendar
        
        if calendar is None or calendar.empty:
            return {}
        
        # Convert to dict
        result = {}
        for idx in calendar.index:
            values = calendar.loc[idx]
            if isinstance(values, pd.Series):
                result[idx] = values.tolist()
            else:
                result[idx] = values
        
        return result
        
    except Exception as e:
        print(f"Error fetching calendar for {symbol}: {e}")
        return {}


def fetch_company_info(symbol: str) -> Dict[str, Any]:
    """
    Fetch company info and key metrics.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        Dictionary with company info
    """
    ticker_symbol = _get_ticker_symbol(symbol)
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        if not info:
            return {}
        
        # Extract relevant fields
        return {
            "name": info.get("longName", info.get("shortName", "N/A")),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", info.get("forwardPE", "N/A")),
            "eps": info.get("trailingEps", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "50_dma": info.get("fiftyDayAverage", "N/A"),
            "200_dma": info.get("twoHundredDayAverage", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "beta": info.get("beta", "N/A")
        }
        
    except Exception as e:
        print(f"Error fetching company info for {symbol}: {e}")
        return {}



def _get_price_change(symbol: str, start_date: datetime, days: int = 7) -> Optional[float]:
    """
    Calculate price change % over a period starting from a date.
    
    Args:
        symbol: Stock symbol with suffix (e.g., "RELIANCE.NS")
        start_date: Start date for calculation
        days: Number of days to measure (default 7 = 1 week)
    
    Returns:
        Percentage change or None if data unavailable
    """
    try:
        end_date = start_date + timedelta(days=days + 5)  # Extra buffer for weekends
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=end_date)
        
        if hist.empty or len(hist) < 2:
            return None
        
        # Get price on earnings date and after 'days' trading days
        start_price = hist['Close'].iloc[0]
        end_idx = min(days, len(hist) - 1)
        end_price = hist['Close'].iloc[end_idx]
        
        return ((end_price - start_price) / start_price) * 100
        
    except Exception as e:
        print(f"Error calculating price change: {e}")
        return None


def fetch_earnings_with_performance(symbol: str, num_quarters: int = 3) -> Dict[str, Any]:
    """
    Fetch earnings dates with stock and NIFTY performance after each earnings.
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS", "NETWEB")
        num_quarters: Number of past quarters to fetch (default 3)
    
    Returns:
        Dictionary with:
        - symbol: Stock symbol
        - next_earnings: Next earnings date
        - relative_performance: Stock vs NIFTY 50 (last month)
        - history: List of past earnings with performance data
    """
    ticker_symbol = _get_ticker_symbol(symbol)
    
    result = {
        "symbol": symbol,
        "ticker": ticker_symbol,
        "next_earnings": None,
        "relative_performance": None,
        "history": []
    }
    
    # 1. Get next earnings date
    result["next_earnings"] = fetch_next_earnings_date(symbol)
    
    # 2. Get earnings history
    earnings_df = fetch_earnings_history(symbol, limit=num_quarters * 2)  # Fetch extra to filter
    
    if earnings_df.empty:
        return result
    
    # 3. Calculate performance for each past earnings date
    history = []
    count = 0
    
    for _, row in earnings_df.iterrows():
        if count >= num_quarters:
            break
            
        earnings_date = row.get("Date")
        if pd.isna(earnings_date):
            continue
            
        # Convert to datetime if needed
        if isinstance(earnings_date, str):
            try:
                earnings_date = pd.to_datetime(earnings_date)
            except:
                continue
        
        # Get current time in the same timezone as earnings_date for correct comparison
        now_aware = pd.Timestamp.now(tz=earnings_date.tz)

        # Skip future dates
        if earnings_date > now_aware:
            continue
        
        # Calculate stock performance (1 week after earnings)
        stock_perf = _get_price_change(ticker_symbol, earnings_date, days=7)
        
        # Calculate NIFTY performance (same period)
        nifty_perf = _get_price_change(NIFTY_SYMBOL, earnings_date, days=7)
        
        history.append({
            "date": earnings_date.strftime("%Y-%m-%d") if hasattr(earnings_date, 'strftime') else str(earnings_date),
            "stock_performance": round(stock_perf, 1) if stock_perf is not None else None,
            "nifty_performance": round(nifty_perf, 1) if nifty_perf is not None else None,
            "eps_reported": row.get("EPS_Reported"),
            "eps_estimate": row.get("EPS_Estimate"),
            "surprise_pct": row.get("Surprise_Pct")
        })
        
        count += 1
    
    result["history"] = history
    
    # 4. Calculate relative performance vs NIFTY (last month)
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        stock_month_perf = _get_price_change(ticker_symbol, start_date, days=30)
        nifty_month_perf = _get_price_change(NIFTY_SYMBOL, start_date, days=30)
        
        if stock_month_perf is not None and nifty_month_perf is not None:
            result["relative_performance"] = round(stock_month_perf - nifty_month_perf, 1)
    except Exception as e:
        print(f"Error calculating relative performance: {e}")
    
    return result


def fetch_all_earnings_summary(symbols: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch earnings summary for multiple stocks.
    
    Args:
        symbols: List of stock symbols
    
    Returns:
        List of earnings data dictionaries
    """
    results = []
    for symbol in symbols:
        data = fetch_earnings_with_performance(symbol, num_quarters=3)
        results.append(data)
    return results
