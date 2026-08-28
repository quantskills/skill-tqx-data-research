# Output contract

## Factor analysis

Return:

- `IC`
- `Rank IC`
- `ICIR`
- grouped return summary
- decay
- confidence

If data is missing, return the exact missing market, universe, column, date range, or parquet path.

## Strategy backtest

Return:

- total return
- annual return
- max drawdown
- Sharpe
- trade count
- final equity

If a run fails, return the exact missing environment, data, or logic item. Do not invent metrics.
