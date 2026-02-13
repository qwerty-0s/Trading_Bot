from datetime import time
import pytz

MSK = pytz.timezone('Europe/Moscow')

def in_clearing_exclusion(now=None) -> bool:
    """Exclude generating alerts during clearing windows: 14:00-14:05, 18:50-19:05 MSK"""
    from datetime import datetime
    now = now or datetime.now(MSK)
    t = now.time()
    ranges = [(time(14,0), time(14,5)), (time(18,50), time(19,5))]
    for a,b in ranges:
        if a <= t <= b:
            return True
    return False
