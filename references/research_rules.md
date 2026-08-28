# Local research rules

## Default routing

- `??5?????????????????5?` -> factor analysis
- MA / RSI / breakout / momentum / entry-exit -> time-series strategy
- top N / screening / ranking / universe selection -> cross-sectional strategy

## Defaults

- Factor analysis: use a local HK universe if the universe is missing.
- Time-series strategy: use one symbol unless the user asks for more.
- Cross-sectional strategy: use the requested universe; if missing, derive a local HK/US universe from parquet.
- If dates are missing, use the smallest workable period and say what you assumed.

## Execution order

- Factor analysis: panel -> factor -> forward returns -> `factor_analysis_control(...)`
- Strategy backtest: code -> `code_control(...)` -> `stock_backtest_control(...)` -> `backtest_result_control(...)`

## Failure order

1. Environment
2. Data
3. Logic

Return the exact missing path, column, market, or rule; do not invent results.
