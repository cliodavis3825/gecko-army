# bots/technical.py
from bots.marketdata import get_daily_bars

def rsi(close, n=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(n).mean()
    loss = (-delta.clip(upper=0)).rolling(n).mean()
    return 100 - 100 / (1 + gain / loss)

def run(symbols):
    df = get_daily_bars(symbols, days=400)
    found = df.index.get_level_values(0)
    out = {}
    for sym in symbols:
        if sym not in found:
            continue
        c = df.loc[sym].close
        if len(c) < 200:
            continue
        price = float(c.iloc[-1])
        sma50 = float(c.rolling(50).mean().iloc[-1])
        sma200 = float(c.rolling(200).mean().iloc[-1])
        r = float(rsi(c).iloc[-1])
        if price > sma50 > sma200 and r < 70:
            signal = "buy"
        elif price < sma50 < sma200 or r > 80:
            signal = "sell"
        else:
            signal = "hold"
        out[sym] = {"price": round(price, 2), "sma50": round(sma50, 2),
                    "sma200": round(sma200, 2), "rsi": round(r, 1),
                    "signal": signal}
    return out

