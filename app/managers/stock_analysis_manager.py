from app.models.stock import Stock
import pandas as pd

class StockAnalysisManager:
    """Manager for analyzing stock data."""

    def calculate_metrics(self, ticker: str, stock_data: dict) -> Stock:
        """
        Calculates various metrics for a stock.
        """
        history = stock_data.get("history")
        if history is None or history.empty:
            return Stock(ticker=ticker)

        high_52 = history['High'].max()
        low_52 = history['Low'].min()
        sma_50 = history['Close'].rolling(window=50).mean().iloc[-1]
        ltp = history['Close'].iloc[-1]
        rsi_val = self._calculate_rsi(history['Close'])

        current_vol = history['Volume'].iloc[-1]
        avg_vol_20 = history['Volume'].rolling(window=20).mean().iloc[-1]
        vol_spike = current_vol / avg_vol_20 if avg_vol_20 > 0 else 0

        info = stock_data.get("info", {})
        pe_ratio = info.get('trailingPE')

        calendar = stock_data.get("calendar")
        earnings_date = None
        if calendar is not None and 'Earnings Date' in calendar:
            earnings_date = calendar['Earnings Date'][0]

        analysis = {
            "LTP": round(ltp, 2),
            "52_Week_High": round(high_52, 2),
            "52_Week_Low": round(low_52, 2),
            "50_Day_MA": round(sma_50, 2),
            "RSI": round(rsi_val, 2),
            "Volume_Spike": round(vol_spike, 2),
            "PE_Ratio": pe_ratio,
            "Earnings_Date": earnings_date
        }

        return Stock(
            ticker=ticker,
            ltp=round(ltp, 2),
            high_52_week=round(high_52, 2),
            low_52_week=round(low_52, 2),
            sma_50_day=round(sma_50, 2),
            rsi=round(rsi_val, 2),
            volume_spike=round(vol_spike, 2),
            pe_ratio=pe_ratio,
            earnings_date=earnings_date,
            history=history,
            analysis=analysis
        )

    def _calculate_rsi(self, series: pd.Series, period: int = 14) -> float:
        """
        Calculates the Relative Strength Index (RSI).
        """
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
