# main.py
import json, sys, datetime as dt
import config
from clients import trading
from bots import (auditor, macro, scout, technical, news,
                  fundamentals, lead, risk, execution, discovery, breakout)

def main():
    if auditor.kill_switch_on():
        print("KILL_SWITCH file present. Not trading."); return
    if not trading.get_clock().is_open:
        print("Market is closed. Nothing to do."); return
    m = macro.run()
    held = [p.symbol for p in trading.get_all_positions()]
    universe = list(dict.fromkeys(config.WATCHLIST + held + discovery.run()))
    snap = scout.run(universe)
    syms = [s["symbol"] for s in snap]
    tech = technical.run(syms)
    brk = breakout.run(syms)
    nws = news.run(syms)
    fund = fundamentals.run(syms)
    positions = [{"symbol": p.symbol, "qty": p.qty,
                  "avg_entry": p.avg_entry_price,
                  "unrealized_pl_pct": p.unrealized_plpc}
                 for p in trading.get_all_positions()]

    plan = lead.run(m, snap, tech, nws, fund, positions,
                    str(dt.date.today()), brk, universe)
    prices = {s: t["price"] for s, t in tech.items()}
    approved, rejected, halt = risk.run(plan.get("orders", []), m, prices, universe)


    if halt and "drawdown" in halt:
        auditor.trip_kill_switch(halt)

    if approved and config.REQUIRE_HUMAN_APPROVAL:
        print("\nLead's view:", plan.get("market_view"))
        print(json.dumps(approved, indent=2))
        if not sys.stdin.isatty():
            print("No one here to approve; skipping orders."); approved = []
        elif input("Approve these orders? (y/n): ").strip().lower() != "y":
            approved = []

    results = execution.run(approved)
    auditor.record_and_report({
        "macro": m, "scout": snap, "technical": tech, "news": nws,
        "fundamentals": fund, "plan": plan, "approved": approved,
        "rejected": rejected, "halt": halt, "results": results})

if __name__ == "__main__":
    main()


