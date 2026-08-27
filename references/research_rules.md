# Local research rules

This skill is local-first. Use `tqx_data` SDK (whl) plus local parquet data, and `scripts/research_nodes.py` for execution. Load `PARQUET_ROOT_PATH` from `.env`.

## Default interpretation

If the user says:

- “回测5日动量的港股因子分析策略”
- “调仓日为5日”

Treat it as:

- Hong Kong factor analysis
- factor = 5-day momentum
- rebalance cycle = 5 trading days
- output = factor-analysis result, not PnL backtest

This request should return factor-analysis results directly when local parquet is available; do not redirect it away from the local research flow.

## Data priority

1. Local parquet via `PARQUET_ROOT_PATH`
2. Local `tqx_data` SDK (whl)
3. Synthetic fallback only for validation

## Stock universe

If the user does not specify a universe, use the locally available HK sample universe from parquet data. Do not stop just because no explicit stock pool was given.

## Output

Return:

- `IC`
- `Rank IC`
- `ICIR`
- group return summary
- decay
- confidence

If data is unavailable, report the exact missing input and stop.

## Error handling

When a run fails, classify it first:

1. Environment: `.env` missing, `PARQUET_ROOT_PATH` wrong, `tqx_data` import failed, path not visible
2. Data: empty frame, missing market rows, missing columns, duplicate `(date, symbol)`, NaN/Inf
3. Logic: future leakage, wrong rebalance cycle, wrong market, wrong code path, bad position sizing

Fix in this order:

- Environment first
- Data second
- Logic last

If the failure is in shared research nodes, patch `scripts/research_nodes.py` first. Do not only patch a single test script.

If the failure is in generated code, regenerate the code from the matching assistant reference and rerun the local test script.

## Code-control example

For the request 回测5日动量的港股因子分析策略，调仓日为5日 use the example script in `scripts/tests/hk_factor_analysis_5d.py` as the template for generated code and local validation.

## Code generation split

- Factor-analysis code generation: read `references/factor_codegen_assistant.md`
- Strategy-backtest code generation: read `references/strategy_codegen_assistant.md`
