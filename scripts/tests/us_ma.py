"""US moving-average backtest using only tqx_data and local research nodes."""
from __future__ import annotations

import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env", override=False)

import tqx_data
from scripts.research_nodes import run_backtest


def run() -> dict:
    data = tqx_data.get_us_daily(
        symbol="TSLA.NB", start_date="20240101", end_date="20251231",
        fields=["date", "symbol", "close"],
    )
    if data is None or data.empty:
        return {"ok": False, "reason": "empty_us_daily"}
    data = data.sort_values("date").drop_duplicates(["symbol", "date"], keep="last")
    result = run_backtest(data, short_window=7, long_window=20,
                          initial_cash=1_000_000, commission_rate=0.0003)
    result.update(data_rows=int(len(data)), date_range=[str(data["date"].min()), str(data["date"].max())], symbol="TSLA.NB")
    return result


if __name__ == "__main__":
    output = run()
    assert output.get("ok") is True, output
    for key in ("symbol", "date_range", "data_rows", "total_return", "annualized_return",
                "max_drawdown", "annualized_sharpe", "trade_count", "final_equity"):
        print(f"{key}: {output.get(key)}")
