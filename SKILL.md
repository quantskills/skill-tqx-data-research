---
name: skill-tqx-research
description: Use tqx_data for Hong Kong and US factor analysis and backtest strategy code generation. Use when the task is market-data research, factor construction, IC/IR/group/decay analysis, strategy signals, or local backtest examples.
---

Use `tqx_data` SDK (whl) with local parquet as the data source, and the local scripts in `scripts/` as the only implementation surface. Put all executable logic in `scripts/`.
Before any run, copy `.env.example` to `.env` and set `PARQUET_ROOT_PATH`.

If the user asks for 回测5日动量的港股因子分析策略，调仓日为5日，给我返回因子分析结果, treat it as local HK factor analysis and return factor-analysis results directly.

Read these references when needed:

- `references/factor_codegen_assistant.md`
- `references/strategy_codegen_assistant.md`
- `references/error_handling.md`
- `references/research_rules.md`
- `references/research_node_generation.md`
- `references/tqx_data_usage.md`

Canonical functions:

- `run_code_backtest`
- `load_daily_data`
- `build_forward_returns`
- `run_factor_analysis`
- `run_backtest`
- `factor_analysis_control`
- `stock_backtest_control`
- `backtest_result_control`
- `factor_analysis_chart_control`

Validation rules:

- Prefer small local DataFrame checks before any real data run.
- Reject empty input, missing required columns, bad date order, duplicate rows, NaN/Inf, and point-in-time leakage.
- If code or data fails, first classify the failure as environment, data, or logic, then follow `references/error_handling.md`.

Style rules:

- Strategy code should follow `scripts/tests/hk_ma.py`
- Factor numerator code should follow `scripts/tests/test_factor_anlysis_hk.py`
- Local HK 5-day momentum validation should follow `scripts/tests/hk_factor_analysis_5d.py`
- When generating code, separate factor-analysis code generation from strategy-backtest code generation.
