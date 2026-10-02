# bots/auditor.py
import json, sqlite3, datetime as dt
from pathlib import Path
import config
from clients import trading, claude

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "team.db"
REPORTS = ROOT / "reports"
KILL = ROOT / "KILL_SWITCH"

def _db():
    DB.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS runs (ts TEXT, payload TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS equity (ts TEXT, equity REAL, spy REAL)")
    return con

def kill_switch_on():
    return KILL.exists()

def trip_kill_switch(reason):
    KILL.write_text(f"{dt.datetime.now().isoformat()} {reason}\n")

def peak_equity(current):
    con = _db()
    row = con.execute("SELECT MAX(equity) FROM equity").fetchone()
    con.close()
    return max(current, row[0] or current)

SUMMARY = """You are the Auditor on a trading team. Write a plain-English
daily report for an owner who is new to investing. Under 250 words.
Sections: Market, Decisions (and why), Rejected by Risk, Performance vs
S&P 500, Problems. Use only numbers present in the JSON; never invent any.
If the team is trailing the S&P 500, say so plainly."""

def record_and_report(run):
    equity = float(trading.get_account().equity)
    spy = run.get("technical", {}).get("SPY", {}).get("price")
    now = dt.datetime.now().isoformat(timespec="seconds")
    con = _db()
    con.execute("INSERT INTO runs VALUES (?, ?)", (now, json.dumps(run, default=str)))
    con.execute("INSERT INTO equity VALUES (?, ?, ?)", (now, equity, spy))
    con.commit()
    first = con.execute("SELECT equity, spy FROM equity WHERE spy IS NOT NULL "
                        "ORDER BY ts LIMIT 1").fetchone()
    con.close()

    perf = {"equity": equity}
    if first and spy:
        perf["team_return_pct"] = round((equity / first[0] - 1) * 100, 2)
        perf["spy_return_pct"] = round((spy / first[1] - 1) * 100, 2)

    errors = [r for r in run.get("results", []) if "error" in r]
    if len(errors) >= 3:
        trip_kill_switch(f"{len(errors)} execution errors in one run")

    msg = claude.messages.create(
        model=config.MODEL_FAST, max_tokens=800, system=SUMMARY,
        messages=[{"role": "user", "content": json.dumps(
            {"run": run, "performance": perf}, default=str)}])
    text = "".join(b.text for b in msg.content if b.type == "text")
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / f"{dt.date.today()}.md").write_text(text)
    print("\n" + text)

