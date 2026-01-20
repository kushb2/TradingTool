"""
Price Data Service - Fetches OHLC data from yfinance

This service fetches historical price data (Open, High, Low, Close, Volume)
for NSE stocks. We need 60 days of data to calculate 20-day rolling averages
with enough history for the display period.
"""
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from v2.constants.constants import fetch_price_data_days


def _fetch_yfinance_data(symbol: str, days: int) -> pd.DataFrame:
    """
    Private function to fetch raw data from yfinance.
    """
    # Add .NS suffix for NSE stocks if not present
    ticker_symbol = symbol.upper()
    if not ticker_symbol.endswith(".NS"):
        ticker_symbol = f"{ticker_symbol}.NS"
    
    try:
        # Fetch extra days to account for weekends/holidays
        # Rule of thumb: multiply by 1.5 to ensure we get enough trading days
        calendar_days = int(days * 1.5)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=calendar_days)
        
        # Download data from yfinance
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            return pd.DataFrame()
        
        return df
        
    except Exception as e:
        print(f"Error fetching price data for {symbol}: {e}")
        return pd.DataFrame()


def fetch_price_data(symbol: str, days: int = fetch_price_data_days) -> pd.DataFrame:
    """
    Fetch OHLC price data for an NSE stock.
    
    Args:
        symbol: NSE stock symbol (e.g., "RELIANCE", "TCS")
                Will auto-append .NS suffix for yfinance
        days: Number of trading days to fetch (default 60 for baseline calculation)
    
    Returns:
        DataFrame with columns: Date, Open, High, Low, Close, Volume
        Returns empty DataFrame if fetch fails
    
    Example:
        df = fetch_price_data("RELIANCE", days=60)
        # Returns 60 days of OHLC data for Reliance Industries
    """
    df = _fetch_yfinance_data(symbol, days)
    
    if df.empty:
        return pd.DataFrame()
    
    # Reset index to make Date a column
    df = df.reset_index()
    
    # Keep only the columns we need
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    
    # Convert Date to date only (remove time component)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    
    # Sort by date ascending (oldest first)
    df = df.sort_values("Date").reset_index(drop=True)
    
    # Take only the last 'days' rows
    if len(df) > days:
        df = df.tail(days).reset_index(drop=True)
    
    return df


def fetch_raw_price_data(symbol: str, days: int = fetch_price_data_days) -> pd.DataFrame:
    """
    Fetch raw, unprocessed price data for an NSE stock.
    
    Args:
        symbol: NSE stock symbol (e.g., "RELIANCE", "TCS")
        days: Number of trading days to fetch
    
    Returns:
        DataFrame with all available columns from yfinance
        Returns empty DataFrame if fetch fails
    """
    return _fetch_yfinance_data(symbol, days)