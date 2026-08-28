# Factor code generation assistant

Use this path when the user wants factor analysis code or local validation code.

## Flow

1. Load parquet from `.env`
2. Build a `(date, symbol)` panel
3. Compute the factor column explicitly
4. Build forward returns with `build_forward_returns`
5. Call `factor_analysis_control(...)`
6. Return the outputs in `references/output_contract.md`

## Rules

- No future data.
- No empty-universe silence.
- Keep the factor expression minimal and explicit.
- Return `IC`, `Rank IC`, `ICIR`, grouped returns, decay, and confidence.

## Style

- HK factor numerator style: `scripts/tests/test_factor_anlysis_hk.py`
- HK 5-day momentum validation: `scripts/tests/hk_factor_analysis_5d.py`
- US factor numerator style: `scripts/tests/test_factor_anlysis_us.py`
