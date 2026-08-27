# Research node generation

Use this file when generating code for the local research workflow in `scripts/`.

## Strategy CodeControl

Generate Python source with:

- `initialize(context)`
- `handle_data(context, data)`

Rules:

- Keep mutable state in `context`
- Do not read local files from strategy code
- Do not query `tqx_data` inside every bar when the same panel can be cached earlier
- For cross-sectional strategies, keep at least `date` and `symbol`; add `source_date` and `fy_period` when fundamentals affect eligibility
- For time-series strategies, store price history per symbol and compare each symbol with itself only
- If a run fails, first check environment, then data, then strategy logic. Do not guess.

Local mapping:

- `code_control(code)` keeps the source string
- `compile_strategy_code(code)` validates `initialize` and `handle_data`
- `stock_backtest_control(...)` runs the source through the local backtest node
- `backtest_result_control(...)` wraps the backtest result

Strategy source style:

- Use `scripts/tests/hk_ma.py` as the HK strategy style reference
- Keep the code direct and runnable
- Prefer one symbol or a small explicit HK universe

## Factor-analysis CodeControl

Factor analysis is a research dataframe plus a factor column.

Minimum panel:

- `date`
- `symbol`
- `factor`
- `close` or precomputed forward return column

Preferred flow:

1. Build the point-in-time panel from `tqx_data`
2. Compute forward returns with `build_forward_returns`
3. Call `factor_analysis_control(...)`

Rules:

- No future data
- Deduplicate by `(date, symbol)` before analysis
- Drop rows with missing factor or return values
- Treat `IC`, `Rank IC`, `ICIR`, group returns, decay, and confidence as outputs, not source code inputs
- If a factor panel is empty, first check `PARQUET_ROOT_PATH`, market symbol universe, and required columns before changing formula logic.

Factor numerator style:

- Use `scripts/tests/test_factor_anlysis_hk.py` as the HK factor source reference
- Keep the factor expression minimal and explicit
- For the default HK momentum case, the factor source should stay close to the test style

## Default routing

If the user says 回测5日动量的港股因子分析策略，调仓日为5日 default to the local HK factor-analysis flow.
