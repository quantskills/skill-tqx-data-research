from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env", override=False)

from scripts.research_nodes import run_factor_analysis


SYMBOLS = [
    "AAPL.NB", "MSFT.NB", "NVDA.NB", "AMZN.NB", "GOOGL.NB",
    "META.NB", "TSLA.NB", "AVGO.NB", "COST.NB", "NFLX.NB",
    "AMD.NB", "QCOM.NB", "AMAT.NB", "CSCO.NB", "PEP.NB",
    "ADBE.NB", "INTU.NB", "TXN.NB", "CMCSA.NB", "TMUS.NB",
    "AMGN.NB", "ISRG.NB", "BKNG.NB", "SBUX.NB", "MU.NB",
    "LRCX.NB", "KLAC.NB", "PANW.NB", "ADP.NB", "GILD.NB",
]


def run() -> dict:
    import tqx_data

    data = tqx_data.get_us_daily(
        symbol=SYMBOLS,
        start_date="20250601",
        end_date="20260131",
        fields=["date", "symbol", "close"],
        market="nb",
    )
    required = {"date", "symbol", "close"}
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise RuntimeError("empty US daily panel")
    if not required.issubset(data.columns):
        raise RuntimeError(f"missing columns: {sorted(required - set(data.columns))}")

    frame = data.copy()
    frame["date"] = frame["date"].astype(str).str.replace("-", "", regex=False)
    frame["symbol"] = frame["symbol"].astype(str)
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    frame = frame.dropna(subset=["date", "symbol", "close"])
    frame = frame.sort_values(["symbol", "date"]).drop_duplicates(["symbol", "date"])
    grouped = frame.groupby("symbol")["close"]
    frame["factor"] = -(grouped.pct_change(5))
    for horizon in (1, 3, 5, 10, 20):
        frame[f"fwd_return_{horizon}d"] = grouped.shift(-horizon) / frame["close"] - 1

    market_dates = sorted(frame.loc[frame["date"].between("20250701", "20251231"), "date"].unique())
    rebalance_dates = set(market_dates[::5])
    panel = frame[frame["date"].isin(rebalance_dates)].dropna(
        subset=["factor", "fwd_return_5d"]
    )
    result = run_factor_analysis(
        panel,
        factor_col="factor",
        return_col="fwd_return_5d",
        group_count=5,
        decay_lags=(1, 3, 5, 10, 20),
        higher_is_better=True,
    )
    if not result.get("ok"):
        raise RuntimeError(str(result))
    return {
        "market": "US/NASDAQ",
        "period": ["20250701", "20251231"],
        "requested_symbols": len(SYMBOLS),
        "available_symbols": int(panel["symbol"].nunique()),
        "rebalance_days": len(rebalance_dates),
        "panel_rows": len(panel),
        **{key: result[key] for key in (
            "ic", "rank_ic", "icir", "group_return_summary", "decay", "confidence"
        )},
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
