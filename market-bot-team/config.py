# config.py
WATCHLIST = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA",
             "AMZN", "GOOGL", "JPM", "XOM", "UNH"]

# Risk limits (fractions of account equity)
MAX_POSITION_PCT = 0.05        # max 5% of account per new position
MAX_TOTAL_EXPOSURE_PCT = 0.60  # max 60% invested; rest stays cash
MAX_OPEN_POSITIONS = 8
MAX_NEW_BUYS_PER_DAY = 3
MAX_DAILY_LOSS_PCT = 0.02      # stop for the day after a 2% drop
MAX_DRAWDOWN_PCT = 0.10        # trip kill switch at 10% below peak
STOP_LOSS_PCT = 0.05           # auto-sell 5% below entry
TAKE_PROFIT_PCT = 0.10         # auto-sell 10% above entry
MIN_CONFIDENCE = 0.6           # Lead must be at least this sure

REQUIRE_HUMAN_APPROVAL = True  # you approve every order
PAPER = True                   # never change without Section 7 criteria

MODEL_SMART = "claude-sonnet-5-5"
MODEL_FAST = "claude-haiku-4-5-20251001"



