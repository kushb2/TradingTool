def get_rsi_description(rsi: float) -> str:
    """
    Returns a qualitative description of the RSI value.
    """
    if rsi >= 70:
        return "Overbought"
    elif rsi <= 30:
        return "Oversold"
    else:
        return "Neutral"

def get_smart_rsi_daily_signal(current: float, previous: float) -> str:
    """
    Generates a smart signal based on RSI momentum for daily trend.
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
