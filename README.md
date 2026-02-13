# Morris MOEX Volume Hunter

Python bot skeleton to detect Morris patterns on MOEX futures using RVOL + S/R filters.

Quick start

1. Create virtual env and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Implement `fetch_ohlcv` in `src/morris_moex/scanner.py` to connect to your data provider.

3. Set Telegram credentials in `run.py` and run:

```bash
python run.py
```

Notes
- Clearing exclusion windows: 14:00-14:05 and 18:50-19:05 MSK (no alerts).
- RVOL threshold is 1.5× average of last 20 candles.
- Pattern detection uses TA-Lib functions: Engulfing, Hammer, ShootingStar, Harami.
- Levels: daily High/Low and extrema of last 300 candles.
# Trading_Bot