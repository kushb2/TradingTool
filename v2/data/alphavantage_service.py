"""
Alpha Vantage Service - Fetches earnings data and company fundamentals

This service provides access to Alpha Vantage APIs for:
- Earnings calendar (next earnings date)
- Earnings history (historical EPS with analyst estimates and surprise)
- Company overview (fundamentals)

API Limits (Free Tier): 25 requests/day
Documentation: https://www.alphavantage.co/documentation/
"""
import requests
import pandas as pd
from io import StringIO
from typing import Optional, Dict, Any

from v2.config import ALPHAVANTAGE_API_KEY, ALPHAVANTAGE_BASE_URL


def _make_request(params: Dict[str, str]) -> Optional[Any]:
    """
    Make a request to Alpha Vantage API.
    
    Args:
        params: Dictionary of query parameters (function, symbol, etc.)
    
    Returns:
        JSON response or None if request fails
    """
    params["apikey"] = ALPHAVANTAGE_API_KEY
    
    try:
        response = requests.get(ALPHAVANTAGE_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        
        # Check for API error messages
        if response.headers.get("Content-Type", "").startswith("application/json"):
            data = response.json()
            if "Error Message" in data:
                print(f"Alpha Vantage API Error: {data['Error Message']}")
                return None
            if "Note" in data:
                # Rate limit warning
                print(f"Alpha Vantage API Note: {data['Note']}")
                return None
            return data
        else:
            # CSV response (for EARNINGS_CALENDAR)
            return response.text
            
    except requests.exceptions.RequestException as e:
        print(f"Alpha Vantage request failed: {e}")
        return None


def fetch_earnings_calendar(symbol: str, horizon: str = "3month") -> pd.DataFrame:
    """
    Fetch upcoming earnings dates for a company.
    
    Args:
        symbol: Stock symbol (e.g., "IBM", "AAPL")
        horizon: Time horizon - "3month", "6month", or "12month"
    
    Returns:
        DataFrame with columns: symbol, name, reportDate, fiscalDateEnding, estimate, currency
        Returns empty DataFrame if fetch fails
    
    Example:
        df = fetch_earnings_calendar("IBM", horizon="12month")
        # Returns upcoming earnings dates for IBM in next 12 months
    """
    params = {
        "function": "EARNINGS_CALENDAR",
        "symbol": symbol.upper(),
        "horizon": horizon
    }
    
    response = _make_request(params)
    
    if response is None or not isinstance(response, str):
        return pd.DataFrame()
    
    try:
        # Parse CSV response
        df = pd.read_csv(StringIO(response))
        return df
    except Exception as e:
        print(f"Error parsing earnings calendar: {e}")
        return pd.DataFrame()


def fetch_earnings_history(symbol: str) -> Dict[str, Any]:
    """
    Fetch historical earnings (EPS) data with analyst estimates and surprise metrics.
    
    Args:
        symbol: Stock symbol (e.g., "IBM", "AAPL")
    
    Returns:
        Dictionary with:
        - "symbol": Stock symbol
        - "annual": DataFrame of annual earnings
        - "quarterly": DataFrame of quarterly earnings with estimates and surprise
        Returns empty dict if fetch fails
    
    Example:
        data = fetch_earnings_history("IBM")
        # data["quarterly"] contains EPS, estimates, and surprise %
    """
    params = {
        "function": "EARNINGS",
        "symbol": symbol.upper()
    }
    
    response = _make_request(params)
    
    if response is None or not isinstance(response, dict):
        return {}
    
    result = {"symbol": response.get("symbol", symbol)}
    
    # Parse annual earnings
    annual = response.get("annualEarnings", [])
    if annual:
        result["annual"] = pd.DataFrame(annual)
    else:
        result["annual"] = pd.DataFrame()
    
    # Parse quarterly earnings (includes estimates and surprise)
    quarterly = response.get("quarterlyEarnings", [])
    if quarterly:
        result["quarterly"] = pd.DataFrame(quarterly)
    else:
        result["quarterly"] = pd.DataFrame()
    
    return result


def fetch_company_overview(symbol: str) -> Dict[str, Any]:
    """
    Fetch company fundamentals and key metrics.
    
    Args:
        symbol: Stock symbol (e.g., "IBM", "AAPL")
    
    Returns:
        Dictionary with company info including:
        - Name, Description, Sector, Industry
        - MarketCapitalization, PERatio, PEGRatio
        - BookValue, DividendYield, EPS
        - 52WeekHigh, 52WeekLow
        - 50DayMovingAverage, 200DayMovingAverage
        Returns empty dict if fetch fails
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol.upper()
    }
    
    response = _make_request(params)
    
    if response is None or not isinstance(response, dict):
        return {}
    
    return response


def fetch_earnings_estimates(symbol: str) -> Dict[str, Any]:
    """
    Fetch analyst EPS and revenue estimates.
    
    Args:
        symbol: Stock symbol (e.g., "IBM", "AAPL")
    
    Returns:
        Dictionary with analyst estimates and revision history
        Returns empty dict if fetch fails
    """
    params = {
        "function": "EARNINGS_ESTIMATES",
        "symbol": symbol.upper()
    }
    
    response = _make_request(params)
    
    if response is None or not isinstance(response, dict):
        return {}
    
    return response
