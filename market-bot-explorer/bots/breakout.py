# bots/breakout.py
from bots.marketdata import get_daily_bars

def run(symbols):
    df = get_daily_bars(symbols, days=400)
    have = df.index.get_level_values(0)
    out = {}
    for sym in symbols:
        if sym not in have:
            continue
        d = df.loc[sym]
        if len(d) < 60:
            continue
        close = float(d.close.iloc[-1])
        high_20 = float(d.high.iloc[-21:-1].max())
        high_52w = float(d.high.iloc[-253:-1].max())
        avg_vol = float(d.volume.iloc[-21:-1].mean())
        vol_ratio = float(d.volume.iloc[-1]) / avg_vol if avg_vol > 0 else 0.0
        rng = float(d.high.iloc[-1] - d.low.iloc[-1])
        pos = (close - float(d.low.iloc[-1])) / rng if rng > 0 else 0.5
        out[sym] = {
            "breakout_20d": close > high_20,
            "new_52w_high": close > high_52w,
            "pct_above_20d_high": round((close / high_20 - 1) * 100, 2),
            "volume_ratio": round(vol_ratio, 2),
            "close_in_day_range": round(pos, 2),   # 1.0 = closing at the high
        }
    return out
