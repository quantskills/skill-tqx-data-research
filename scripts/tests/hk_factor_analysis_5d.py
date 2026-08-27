from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env", override=False)

from scripts.research_nodes import build_hk_momentum_factor_panel, factor_analysis_workflow


def _pick_symbols() -> list[str]:
    return [
        "0700.HK",
        "1810.HK",
        "2269.HK",
        "2318.HK",
        "2628.HK",
        "3690.HK",
        "9618.HK",
        "9988.HK",
        "9999.HK",
    ]


def run() -> dict:
    start_date = "20250101"
    end_date = "20250331"
    symbols = _pick_symbols()
    panel = build_hk_momentum_factor_panel(
        start_date=start_date,
        end_date=end_date,
        symbols=symbols,
        horizon=5,
    )
    if panel.empty:
        return {"ok": False, "reason": "empty_factor_panel"}
    return factor_analysis_workflow(
        df_factor=panel,
        factor_col="factor",
        price_col="close",
        horizon=5,
        group_count=5,
        decay_lags=(1, 3, 5),
        higher_is_better=True,
    )


def main() -> None:
    result = run()
    assert result.get("status") == "ok", result
    analysis = result["analysis"]
    assert analysis.get("ok") is True, analysis
    print("status:", result["status"])
    print("ic:", analysis["ic"])
    print("rank_ic:", analysis["rank_ic"])
    print("icir:", analysis["icir"])
    print("group_return_summary:", analysis["group_return_summary"])
    print("decay:", analysis["decay"])
    print("confidence:", analysis["confidence"])


if __name__ == "__main__":
    main()
