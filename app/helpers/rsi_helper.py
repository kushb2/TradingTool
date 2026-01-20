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
