from app.models.stock import Stock
import pandas as pd

class StockAnalysisManager:
    """Manager for analyzing stock data."""

    def calculate_metrics(self, ticker: str, stock_data: dict) -> Stock:
        """
        Calculates various metrics for a stock.
        """
        history = stock_data.get("history")
        if history is None or history.empty or len(history) < 2:
            return Stock(ticker=ticker)

        high_52 = history['High'].max()
        low_52 = history['Low'].min()
        sma_50 = history['Close'].rolling(window=50).mean().iloc[-1]
        ltp = history['Close'].iloc[-1]
        signal_date = history.index[-1].date()

        # 1. Calculate Full RSI Series
        rsi_series = self._calculate_rsi_series(history['Close'])
        if rsi_series is None or len(rsi_series) < 2:
            return Stock(ticker=ticker, history=history, analysis={"LTP": round(ltp, 2)})

        # 2. Get the last values to see the "Story"
        rsi_now = rsi_series.iloc[-1]
        rsi_prev = rsi_series.iloc[-2]

        # 3. Get the "Smart Description"
        rsi_signal = self._get_smart_rsi_signal(rsi_now, rsi_prev)

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
            "RSI": round(rsi_now, 2),
            "RSI_Signal": rsi_signal,
            "Signal_Date": signal_date,
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
            rsi=round(rsi_now, 2),
            rsi_series=rsi_series,
            rsi_signal=rsi_signal,
            signal_date=signal_date,
            volume_spike=round(vol_spike, 2),
            pe_ratio=pe_ratio,
            earnings_date=earnings_date,
            history=history,
            analysis=analysis
        )

    def _calculate_rsi_series(self, series: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculates the Relative Strength Index (RSI) series.
        """
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _get_smart_rsi_signal(self, current: float, previous: float) -> str:
        """
        Generates a smart signal based on RSI momentum.
        """
        # CASE 1: OVERSOLD (Buying Opportunities)
        if current <= 30:
            if current > previous:
                return "Oversold (Bouncing) ⚠️"  # Value is low, but rising
            return "Oversold (Falling) 🛑"      # Catching a falling knife

        # CASE 2: OVERBOUGHT (Selling Opportunities)
        elif current >= 70:
            if current < previous:
                return "Overbought (Cooling) 🔻" # Momentum losing steam
            return "Overbought (Strong) 🔥"      # Super strong trend, don't sell yet!

        # CASE 3: NEUTRAL ZONES (30 to 70)
        else:
            # Check for crossovers
            if previous <= 30 and current > 30:
                return "Bullish Reversal 🟢"     # Ideally the best BUY signal
            elif previous >= 70 and current < 70:
                return "Bearish Reversal 🔴"     # Ideally the best SELL signal
            
            # General Trend
            if current > previous:
                return "Neutral (Rising) ↗️"
            else:
                return "Neutral (Falling) ↘️"
