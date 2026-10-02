# bots/marketdata.py  -- daily price bars from Alpaca
from datetime import datetime, timedelta, timezone
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed
from clients import data

def get_daily_bars(symbols, days=400):
    req = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=datetime.now(timezone.utc) - timedelta(days=days),
        feed=DataFeed.IEX,  # the free data feed
    )
    return data.get_stock_bars(req).df  # indexed by (symbol, timestamp)
