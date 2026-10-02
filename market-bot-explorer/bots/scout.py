# bots/scout.py
from bots.marketdata import get_daily_bars

def run(watchlist):
    df = get_daily_bars(watchlist, days=60)
    found = df.index.get_level_values(0)
    out = []
    for sym in watchlist:
        if sym not in found:
            continue
        d = df.loc[sym]
        if len(d) < 22:
            continue
        change = d.close.iloc[-1] / d.close.iloc[-2] - 1
        avg_vol = float(d.volume.iloc[-21:-1].mean())
        vol_ratio = float(d.volume.iloc[-1]) / avg_vol if avg_vol > 0 else 0.0
        out.append({
            "symbol": sym,
            "price": round(float(d.close.iloc[-1]), 2),
            "change_pct": round(float(change) * 100, 2),
            "volume_ratio": round(float(vol_ratio), 2),
            "notable": abs(change) > 0.02 or vol_ratio > 1.5,
        })
    return out

