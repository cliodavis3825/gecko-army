# bots/execution.py
from clients import trading
from alpaca.trading.requests import (LimitOrderRequest, TakeProfitRequest,
                                     StopLossRequest, GetOrdersRequest)
from alpaca.trading.enums import (OrderSide, TimeInForce, OrderClass,
                                  QueryOrderStatus)

def run(orders):
    results = []
    for o in orders:
        try:
            if o["side"] == "sell":
                pending = trading.get_orders(GetOrdersRequest(
                    status=QueryOrderStatus.OPEN, symbols=[o["symbol"]]))
                for p in pending:
                    trading.cancel_order_by_id(p.id)
                res = trading.close_position(o["symbol"])
            else:
                req = LimitOrderRequest(
                    symbol=o["symbol"], qty=o["qty"], side=OrderSide.BUY,
                    time_in_force=TimeInForce.GTC, limit_price=o["limit"],
                    order_class=OrderClass.BRACKET,
                    take_profit=TakeProfitRequest(limit_price=o["take"]),
                    stop_loss=StopLossRequest(stop_price=o["stop"]),
                )
                res = trading.submit_order(req)
            results.append({"symbol": o["symbol"], "side": o["side"],
                            "status": str(res.status), "order_id": str(res.id)})
        except Exception as e:
            results.append({"symbol": o["symbol"], "side": o["side"],
                            "error": str(e)})
    return results













