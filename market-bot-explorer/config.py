# config.py
WATCHLIST = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA",
             "AMZN", "GOOGL", "JPM", "XOM", "UNH"]

# Risk limits (fractions of account equity)
MAX_POSITION_PCT = 0.08
MAX_TOTAL_EXPOSURE_PCT = 0.80
MAX_OPEN_POSITIONS = 12
MAX_NEW_BUYS_PER_DAY = 5
STOP_LOSS_PCT = 0.07           # breakouts need room to wiggle
TAKE_PROFIT_PCT = 0.15
MIN_CONFIDENCE = 0.55
MAX_DAILY_LOSS_PCT = 0.02      # stop for the day after a 2% drop
MAX_DRAWDOWN_PCT = 0.10        # trip kill switch at 10% below peak
REQUIRE_HUMAN_APPROVAL = True  # you approve every order
PAPER = True                   # never change without Section 7 criteria

MODEL_SMART = "claude-sonnet-5-5"
MODEL_FAST = "claude-haiku-4-5-20251001"

DISCOVERY_TOP = 20     # how many movers/most-actives to pull
MAX_DISCOVERED = 10    # cap on new names added per run
MIN_PRICE = 5.00       # skip shares under $5 (see E7)

