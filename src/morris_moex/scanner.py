import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz

class RestScanner:
    """Simple REST scanner for OHLCV. Replace `fetch_ohlcv` with provider specifics."""

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def fetch_ohlcv(self, ticker: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        """Fetch OHLCV for ticker/timeframe. This is a stub — wire to your data provider.

        Returned DataFrame must have index as pd.DatetimeIndex and columns: ['open','high','low','close','volume']
        """
        raise NotImplementedError("Please implement fetch_ohlcv for your data provider")

    @staticmethod
    def avg_volume(df: pd.DataFrame, window: int = 20) -> float:
        """Compute a robust average volume over `window` candles.

        Uses clipping at 5th/95th percentiles and returns the median of clipped values
        to reduce sensitivity to single extreme spikes.
        """
        s = df['volume'].tail(window).astype(float)
        if s.empty:
            return 0.0
        low = s.quantile(0.05)
        high = s.quantile(0.95)
        clipped = s.clip(lower=low, upper=high)
        # prefer median for robustness
        return float(clipped.median())
