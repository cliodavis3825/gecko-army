# clients.py
import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
import anthropic
import config

load_dotenv()
KEY = os.environ["ALPACA_API_KEY"]
SECRET = os.environ["ALPACA_SECRET_KEY"]

trading = TradingClient(KEY, SECRET, paper=config.PAPER)
data = StockHistoricalDataClient(KEY, SECRET)
claude = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY automatically
