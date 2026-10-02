# bots/macro.py
import yfinance as yf
from bots.marketdata import get_daily_bars

def run():
    spy = get_daily_bars(["SPY"]).loc["SPY"].close
    above_200 = bool(spy.iloc[-1] > spy.rolling(200).mean().iloc[-1])
    try:
        vix = float(yf.Ticker("^VIX").history(period="5d")["Close"].iloc[-1])
    except Exception:
        vix = None
    if (vix is not None and vix > 30) or not above_200:
        regime = "stressed"
    elif vix is not None and vix < 15:
        regime = "calm"
    else:
        regime = "normal"
    return {"regime": regime, "vix": vix, "spy_above_200dma": above_200}



