import pandas as pd
import talib as ta

PATTERN_MAP = {
    'Engulfing': ta.CDLENGULFING,
    'Hammer': ta.CDLHAMMER,
    'ShootingStar': ta.CDLSHOOTINGSTAR,
    'Harami': ta.CDLHARAMI,
}

def detect_patterns(df: pd.DataFrame) -> list:
    """Detects configured patterns on the last candle. Returns list of (name, value).

    value > 0 typically means bullish, <0 bearish depending on the TA-Lib function.
    """
    o = df['open'].values
    h = df['high'].values
    l = df['low'].values
    c = df['close'].values
    found = []
    for name, func in PATTERN_MAP.items():
        try:
            res = func(o, h, l, c)
        except Exception:
            continue
        if len(res) == 0:
            continue
        val = int(res[-1])
        if val != 0:
            found.append((name, val))
    return found

def short_countertrend_move(df: pd.DataFrame, direction: str, window_min: int = 3, window_max: int = 7) -> bool:
    """Check for a short movement (3-7 candles) opposite to pattern direction.

    direction: 'bull' (pattern is bullish → need prior short bearish movement) or 'bear'.
    """
    window = df.tail(window_max)
    if len(window) < window_min:
        return False
    # count closes direction in the last window_min..window_max candles excluding last candle
    prior = window.iloc[:-1]
    if prior.empty:
        return False
    moves = (prior['close'] - prior['open'])
    if direction == 'bull':
        # prior should be negative (downward push)
        return moves.tail(window_min).mean() < 0
    else:
        return moves.tail(window_min).mean() > 0
