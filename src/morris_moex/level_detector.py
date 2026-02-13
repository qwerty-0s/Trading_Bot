import pandas as pd

def daily_high_low(df: pd.DataFrame) -> dict:
    """Return daily High/Low for the last 24 hours window in the df (assumes chronological index)."""
    last_24h = df.last('24H')
    return {"high": float(last_24h['high'].max()), "low": float(last_24h['low'].min())}

def extrema_levels(df: pd.DataFrame, lookback: int = 300) -> dict:
    """Return extrema (max/min) over last `lookback` candles."""
    window = df.tail(lookback)
    return {"max": float(window['high'].max()), "min": float(window['low'].min())}

def touches_level(price: float, level: float, pct: float = 0.002) -> bool:
    """Check if price is within pct (e.g., 0.002 = 0.2%) of level."""
    if level == 0:
        return False
    return abs(price - level) / level <= pct
