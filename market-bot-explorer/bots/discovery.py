# bots/discovery.py
import config
from clients import KEY, SECRET, trading
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.requests import MostActivesRequest, MarketMoversRequest
from alpaca.trading.enums import AssetExchange
from bots.marketdata import get_daily_bars

screener = ScreenerClient(KEY, SECRET)

def run():
    found = []
    try:
        movers = screener.get_market_movers(MarketMoversRequest(top=config.DISCOVERY_TOP))
        found += [m.symbol for m in movers.gainers]
    except Exception as e:
        print("movers error:", e)
    try:
        actives = screener.get_most_actives(MostActivesRequest(top=config.DISCOVERY_TOP))
        found += [a.symbol for a in actives.most_actives]
    except Exception as e:
        print("most-actives error:", e)
    found = [s for s in dict.fromkeys(found) if s not in config.WATCHLIST]
    if not found:
        return []

    df = get_daily_bars(found, days=40)
    have = df.index.get_level_values(0)
    keep = []
    for sym in found:
        if sym not in have or float(df.loc[sym].close.iloc[-1]) < config.MIN_PRICE:
            continue
        try:
            a = trading.get_asset(sym)
            if not a.tradable or a.exchange == AssetExchange.OTC:
                continue
        except Exception:
            continue
        keep.append(sym)
        if len(keep) >= config.MAX_DISCOVERED:
            break
    return keep
