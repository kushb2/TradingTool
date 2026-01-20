import yfinance as yf

class StockDataService:
    """Service to fetch stock data using yfinance."""

    def fetch_history(self, ticker: str, period: str = "1y") -> dict:
        """
        Fetches historical data for a given ticker.
        """
        yf_object = yf.Ticker(ticker)
        data = yf_object.history(period=period, auto_adjust=True)
        if data.empty:
            return {}
        
        return {
            "history": data,
            "info": yf_object.info,
            "calendar": yf_object.calendar
        }
