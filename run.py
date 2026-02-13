"""Runner for Morris MOEX Volume Hunter (minimal example)."""
import asyncio
from datetime import datetime
import pytz
from morris_moex.scanner import RestScanner
from morris_moex.level_detector import daily_high_low, extrema_levels, touches_level
from morris_moex.pattern_engine import detect_patterns, short_countertrend_move
from morris_moex.visualizer import plot_signal
from morris_moex.telegram_manager import TelegramManager
from morris_moex.utils import in_clearing_exclusion, MSK

TIMEFRAMES = ['5m', '10m', '15m']

# in-memory dedup store: mapping signal_id -> last_candle_iso
last_sent: dict = {}

async def analyze_once(ticker: str, scanner: RestScanner, tg: TelegramManager):
    now = datetime.now(MSK)
    if in_clearing_exclusion(now):
        return
    for tf in TIMEFRAMES:
        try:
            df = scanner.fetch_ohlcv(ticker, tf, limit=400)
        except NotImplementedError:
            print('fetch_ohlcv not implemented for provider')
            continue
        if df is None or df.empty:
            continue
        avg_vol = scanner.avg_volume(df, 20)
        last_vol = float(df['volume'].iloc[-1])
        rvol = last_vol / (avg_vol + 1e-9)
        if rvol < 1.5:
            continue
        patterns = detect_patterns(df)
        if not patterns:
            continue
        dh = daily_high_low(df)
        ex = extrema_levels(df, lookback=300)
        levels = {'day_high': dh['high'], 'day_low': dh['low'], 'ext_max': ex['max'], 'ext_min': ex['min']}
        # check level proximity
        last_close = float(df['close'].iloc[-1])
        last_candle_ts = df.index[-1]
        for name, val in patterns:
            direction = 'bull' if val > 0 else 'bear'
            support_hit = touches_level(last_close, dh['low']) or touches_level(last_close, ex['min'])
            resistance_hit = touches_level(last_close, dh['high']) or touches_level(last_close, ex['max'])
            ok = False
            if direction == 'bull' and support_hit:
                ok = short_countertrend_move(df, 'bull')
            if direction == 'bear' and resistance_hit:
                ok = short_countertrend_move(df, 'bear')
            if not ok:
                continue

            signal_id = f"{ticker}:{tf}:{name}"
            last_iso = str(last_candle_ts.isoformat())
            # deduplicate: if we've already sent alert for this signal for same candle, skip
            if last_sent.get(signal_id) == last_iso:
                continue

            img = plot_signal(df.tail(200), levels, abnormal_idx=len(df.tail(200)) - 1)
            title = f"🚨 VOL-SIGNAL: {ticker} {tf}"
            pattern_desc = (
                f"Паттерн: {name} ({'bull' if val>0 else 'bear'})\n"
                f"Объём: {rvol:.2f}x среднего (RVOL)\n"
                f"Уровень: {'Отскок от локального минимума дня' if direction=='bull' else 'Отскок от локального максимума дня'}"
            )
            await tg.send_alert(title, pattern_desc, png_bytes=img)
            last_sent[signal_id] = last_iso

async def main():
    scanner = RestScanner()
    tg = TelegramManager(token='YOUR_TELEGRAM_TOKEN', chat_id='YOUR_CHAT_ID')
    tickers = ['Si-6.26']
    while True:
        for t in tickers:
            try:
                await analyze_once(t, scanner, tg)
            except Exception as e:
                print('Error during analyze:', e)
        await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())
