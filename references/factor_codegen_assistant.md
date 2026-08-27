# Factor code generation assistant

Use this path when the user wants factor analysis code, factor numerator code, or local validation code for HK/US research.

## Goal

Generate point-in-time factor research code that can be run locally against `tqx_data` + parquet.

## Required flow

1. Load local parquet from `.env`
2. Build a `(date, symbol)` panel
3. Compute the factor column explicitly
4. Build forward returns with `build_forward_returns`
5. Call `factor_analysis_control(...)` or `factor_analysis_workflow(...)`

## Rules

- No future data
- No empty-universe silence: if no explicit universe is given, derive a local HK universe
- Keep the factor expression minimal and explicit
- Treat `IC`, `Rank IC`, `ICIR`, grouped returns, decay, and confidence as outputs

## Style

- Factor numerator style should stay close to `scripts/tests/test_factor_anlysis_hk.py`
- Local HK 5-day momentum validation should stay close to `scripts/tests/hk_factor_analysis_5d.py`
- Return actual analysis results when parquet is available

