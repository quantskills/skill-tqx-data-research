# Strategy backtest code generation assistant

Use this path when the user wants strategy backtest code, entry/exit logic, or local backtest validation.

## Goal

Generate runnable strategy code for the local backtest node.

## Required flow

1. Write Python source with `initialize(context)` and `handle_data(context, data)`
2. Keep mutable state in `context`
3. Route through `code_control(code)` and `stock_backtest_control(...)`
4. Wrap the result with `backtest_result_control(...)`

## Rules

- Do not read local files from strategy code
- Do not query `tqx_data` on every bar if the panel can be cached outside the loop
- Keep one symbol or a small explicit HK universe unless the user asks for broad cross-section
- Preserve point-in-time behavior

## Style

- Strategy source style should stay close to `scripts/tests/hk_ma.py`
- Prefer direct, runnable code over framework-heavy abstractions

