# Strategy backtest code generation assistant

Use this path when the user wants strategy backtest code or local backtest validation.

## Flow

1. Write Python source with `initialize(context)` and `handle_data(context, data)`
2. Keep mutable state in `context`
3. Route through `code_control(code)` and `stock_backtest_control(...)`
4. Wrap with `backtest_result_control(...)`
5. Return the outputs in `references/output_contract.md`

## Routes

- Time-series: one symbol or a small explicit universe; compare each symbol with itself only.
- Cross-sectional: rank or filter a universe on each rebalance date; use point-in-time eligibility.

## Rules

- Do not read local files from strategy code.
- Do not query `tqx_data` on every bar if the panel can be cached outside the loop.
- Preserve point-in-time behavior.
- Do not hardcode one strategy type.
- Keep the generated code direct and runnable.

## Style

- Time-series style: `scripts/tests/hk_ma.py`
- Cross-sectional style: `scripts/tests/hsi_cs_st.py`
- US time-series style: `scripts/tests/us_ma.py` / `scripts/tests/us_rsi.py`
