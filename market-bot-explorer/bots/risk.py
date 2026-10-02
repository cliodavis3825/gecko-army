# bots/risk.py  (explorer version)
import config
from clients import trading
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from bots.auditor import peak_equity

def run(proposals, macro, prices, universe=None):
    acct = trading.get_account()
    equity = float(acct.equity)
    last_equity = float(acct.last_equity)   # equity at yesterday's close
    if equity / last_equity - 1 <= -config.MAX_DAILY_LOSS_PCT:
        return [], [], "daily loss limit hit"
    if equity / peak_equity(equity) - 1 <= -config.MAX_DRAWDOWN_PCT:
        return [], [], "max drawdown limit hit"

    positions = {p.symbol: p for p in trading.get_all_positions()}
    allowed = set(universe or config.WATCHLIST) | set(positions)
    open_orders = {o.symbol for o in trading.get_orders(
        GetOrdersRequest(status=QueryOrderStatus.OPEN))}
    exposure = sum(abs(float(p.market_value)) for p in positions.values())
    size_mult = 0.5 if macro["regime"] == "stressed" else 1.0

    approved, rejected, new_buys = [], [], 0
    def reject(o, why):
        rejected.append({**o, "rejected_because": why})

    for o in proposals:
        sym, side = o.get("symbol"), o.get("side")
        if sym not in allowed:
            reject(o, "not in today's universe"); continue
        if side == "sell":
            if sym in positions:
                approved.append({"symbol": sym, "side": "sell",
                                 "reason": o.get("reason", "")})
            else:
                reject(o, "not held; short selling not allowed")
            continue
        if side != "buy":
            reject(o, "unknown side"); continue
        if float(o.get("confidence", 0)) < config.MIN_CONFIDENCE:
            reject(o, "confidence below minimum"); continue
        if sym in positions or sym in open_orders:
            reject(o, "already held or order pending"); continue
        if new_buys >= config.MAX_NEW_BUYS_PER_DAY:
            reject(o, "daily new-buy limit reached"); continue
        if len(positions) + new_buys >= config.MAX_OPEN_POSITIONS:
            reject(o, "max open positions reached"); continue
        price = prices.get(sym)
        if not price:
            reject(o, "no current price"); continue
        dollars = equity * config.MAX_POSITION_PCT * size_mult
        if exposure + dollars > equity * config.MAX_TOTAL_EXPOSURE_PCT:
            reject(o, "total exposure limit"); continue
        qty = int(dollars // price)
        if qty < 1:
            reject(o, "too small for one whole share"); continue
        approved.append({
            "symbol": sym, "side": "buy", "qty": qty,
            "limit": round(price * 1.002, 2),
            "stop": round(price * (1 - config.STOP_LOSS_PCT), 2),
            "take": round(price * (1 + config.TAKE_PROFIT_PCT), 2),
            "reason": o.get("reason", ""),
        })
        exposure += qty * price
        new_buys += 1
    return approved, rejected, None
