import datetime
from typing import Optional, Dict, Any
import pandas as pd


class Stock:
    """Data class to hold stock information."""
    def __init__(self, ticker: str, ltp: float = 0.0, high_52_week: float = 0.0, low_52_week: float = 0.0,
                 sma_50_day: float = 0.0, rsi: float = 0.0, rsi_series: Optional[Any] = None,
                 rsi_signal: str = "", signal_date: Optional[datetime.date] = None, volume_spike: float = 0.0,
                 pe_ratio: Optional[float] = None, earnings_date: Optional[datetime.date] = None,
                 history: Optional[Any] = None, analysis: Optional[Dict[str, Any]] = None):
        self.ticker = ticker
        self.ltp = ltp
        self.high_52_week = high_52_week
        self.low_52_week = low_52_week
        self.sma_50_day = sma_50_day
        self.rsi = rsi
        self.rsi_series = rsi_series
        self.rsi_signal = rsi_signal
        self.signal_date = signal_date
        self.volume_spike = volume_spike
        self.pe_ratio = pe_ratio
        self.earnings_date = earnings_date
        self.history = history
        self.analysis = analysis

    def get_last_10_days_stats(self):
        """
        Returns a DataFrame of the last 10 days with:
        - Min, Max, LTP (Close)
        - Volume
        - Volume Change (Spike)
        """
        if self.history is None or self.history.empty:
            return None

        # 1. Slice the last 10 records
        last_10 = self.history.tail(10).copy()

        # 2. Calculate daily metric: Price Change %
        last_10['Change_%'] = last_10['Close'].pct_change() * 100

        # 3. Calculate Volume Context
        # We need the 20-day average volume to know if today's volume is "High" or "Low"
        # We take the rolling mean from the FULL data, then slice the last 10
        full_avg_vol = self.history['Volume'].rolling(window=20).mean()
        last_10['Avg_Vol_20'] = full_avg_vol.tail(10)

        # Calculate Spike Factor (e.g., 2.0x means double the normal volume)
        last_10['Vol_Spike'] = last_10['Volume'] / last_10['Avg_Vol_20']

        # 4. Clean up columns for display
        # We format the date index to look nice
        last_10.index = last_10.index.date

        display_df = last_10[['Low', 'High', 'Close', 'Volume', 'Vol_Spike', 'Change_%']]

        # Rename for clarity
        display_df.columns = ['Min', 'Max', 'LTP', 'Volume', 'Vol_Spike (x)', 'Change %']

        # Sort so today is at the top
        return display_df.sort_index(ascending=False)



