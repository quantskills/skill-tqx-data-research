from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env", override=True)

from scripts.research_nodes import backtest_result_control, code_control, run_code_backtest


STRATEGY = """
def initialize(context):
    context.symbols = ["AAPL.NB"]
    context.period = 14
    context.oversold = 30.0
    context.overbought = 70.0
    context.in_position = False

def handle_data(context, data):
    symbol = context.symbols[0]
    history = data.history(symbol, "close", context.period + 1).tolist()
    if len(history) < context.period + 1:
        return

    changes = [history[i] - history[i - 1] for i in range(1, len(history))]
    gains = [max(change, 0.0) for change in changes]
    losses = [max(-change, 0.0) for change in changes]
    avg_gain = sum(gains) / context.period
    avg_loss = sum(losses) / context.period
    rsi = 100.0 if avg_loss == 0 else 100.0 - 100.0 / (1.0 + avg_gain / avg_loss)

    if rsi < context.oversold and not context.in_position:
        context.order_target_percent(symbol, 0.9, reason="RSI oversold")
        context.in_position = True
    elif rsi > context.overbought and context.in_position:
        context.order_target_percent(symbol, 0.0, reason="RSI overbought")
        context.in_position = False
"""


def run() -> dict:
    import tqx_data

    df = tqx_data.get_us_daily(
        symbol=["AAPL.NB"],
        start_date="20251001",
        end_date="20251231",
        fields=["date", "symbol", "close"],
    )
    if not isinstance(df, pd.DataFrame) or df.empty:
        return {"ok": False, "reason": "empty_input"}
    required = {"date", "symbol", "close"}
    if not required.issubset(df.columns):
        return {"ok": False, "reason": f"missing_columns:{sorted(required - set(df.columns))}"}
    df = df.copy()
    df["date"] = df["date"].astype(str).str.replace("-", "", regex=False)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["date", "symbol", "close"])
    df = df.sort_values(["symbol", "date"]).drop_duplicates(["symbol", "date"])
    if df.empty or not df["date"].is_monotonic_increasing:
        return {"ok": False, "reason": "invalid_date_order"}

    result = run_code_backtest(code_control(STRATEGY), df, commission_rate=0.0003)
    return backtest_result_control(result)


if __name__ == "__main__":
    output = run()
    assert output["status"] == "ok", output
    print(json.dumps(output["metrics"], ensure_ascii=False))
