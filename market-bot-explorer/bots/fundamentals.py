# bots/fundamentals.py
import yfinance as yf

def run(symbols):
    out = {}
    for s in symbols:
        try:
            t = yf.Ticker(s)
            info = t.info
            row = {
                "type": info.get("quoteType"),          # EQUITY or ETF
                "trailing_pe": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "debt_to_equity": info.get("debtToEquity"),
                "profit_margin": info.get("profitMargins"),
            }
            try:
                cal = t.calendar
                dates = cal.get("Earnings Date") if isinstance(cal, dict) else None
                row["next_earnings"] = str(dates[0]) if dates else None
            except Exception:
                row["next_earnings"] = None
            out[s] = row
        except Exception as e:
            out[s] = {"error": str(e)}
    return out

