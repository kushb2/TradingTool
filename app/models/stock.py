import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Stock:
    """Data class to hold stock information."""
    ticker: str
    ltp: float = 0.0
    high_52_week: float = 0.0
    low_52_week: float = 0.0
    sma_50_day: float = 0.0
    rsi: float = 0.0
    rsi_series: Optional[Any] = None
    rsi_signal: str = ""
    signal_date: Optional[datetime.date] = None
    volume_spike: float = 0.0
    pe_ratio: Optional[float] = None
    earnings_date: Optional[datetime.date] = None
    history: Optional[Any] = None
    analysis: Optional[Dict[str, Any]] = None
