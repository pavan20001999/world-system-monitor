"""Fetch daily market readings for the World System Monitor.

Runs in GitHub Actions (see .github/workflows/update-live-data.yml) and writes
data/live.json, which index.html reads on load to refresh the market tiles.
"""
import json
import datetime as dt
from pathlib import Path

import yfinance as yf

TICKERS = {
    "nifty":  ("Nifty 50",       "^NSEI"),
    "sensex": ("Sensex",         "^BSESN"),
    "spx":    ("S&P 500",        "^GSPC"),
    "nasdaq": ("Nasdaq",         "^IXIC"),
    "dow":    ("Dow Jones",      "^DJI"),
    "brent":  ("Brent crude",    "BZ=F"),
    "wti":    ("WTI crude",      "CL=F"),
    "us10y":  ("US 10-yr yield", "^TNX"),
    "sox":    ("SOX semis",      "^SOX"),
}


def quote(symbol):
    hist = yf.Ticker(symbol).history(period="1mo", auto_adjust=False)["Close"].dropna()
    if len(hist) < 2:
        return None
    last, prev = float(hist.iloc[-1]), float(hist.iloc[-2])
    wk_base = float(hist.iloc[-6]) if len(hist) >= 6 else float(hist.iloc[0])
    return {
        "last": round(last, 2),
        "chg_pct": round((last / prev - 1) * 100, 2),
        "wk_pct": round((last / wk_base - 1) * 100, 2),
        "date": hist.index[-1].strftime("%Y-%m-%d"),
    }


def main():
    out = {"updated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "quotes": {}}
    for key, (label, symbol) in TICKERS.items():
        try:
            q = quote(symbol)
        except Exception as exc:  # one bad ticker must not sink the run
            print(f"skip {symbol}: {exc}")
            q = None
        if q:
            out["quotes"][key] = {"label": label, "symbol": symbol, **q}
    if not out["quotes"]:
        raise SystemExit("no quotes fetched; keeping previous data/live.json")
    path = Path(__file__).resolve().parent.parent / "data" / "live.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {len(out['quotes'])} quotes to {path}")


if __name__ == "__main__":
    main()
