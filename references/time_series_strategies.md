# Hong Kong and US Stock Time-Series Strategies

The time series strategy generates buy and sell signals based on its own historical data for a single stock, a single index, or multiple independent targets. When generating code
Reuse the life cycle and order structure of `strategy_templates.md` and read the `stock_hk_api.md` of the target market or
`stock_us_api.md`. Read `tqx_data_usage.md` before calling `tqx_data` directly.

## 1. Identify Time-Series Strategies

The following requirements describe a time-series strategy:

- Moving averages, breakouts, reversals, Bollinger Bands, volatility or stop-loss strategies for individual stocks or indices.
- Multiple stocks calculate their own signals, and the targets are not ranked horizontally.
- First select a set of fixed targets based on fundamentals or volume and price conditions, and then independently implement the same or different rules for each target.

If the strategy horizontally filters, scores, sorts, or selects the top N targets on the same position rebalancing day, it is a cross-sectional strategy. Read more
`cross_sectional_strategies.md`. If the underlying set changes from date to date, make it clear that this is a hybrid strategy with a dynamic qualification panel and press
Read `cross_sectional_strategies.md` for the time-point and panel rules for cross-sectional strategies.

## 2. Verified template

| market | example file | target | window | QUBE market |
|---|---|---|---|---|
| Hong Kong stocks | `tqx_cli/tests/hk_ma.py` | `0700.HK` | 5/20 root bar | `hk` |
| US stocks | `tqx_cli/tests/us_ma.py` | `TSLA.NB` | 4/12 root bar | `us` |

Both templates have been verified by Qube backtesting, can be managed through `tqx research`, and can be used as a timing strategy code skeleton. The template implements the state rule: the fast moving average is higher than
Buy when the slow moving average is moving and the position is short, and clear the position when the fast moving average is lower than the slow moving average and there are sellable positions; they are not strictly required to preserve the relationship between the previous moving average.
Top/under events. "1-day fast MA" appears in the comments of the US stock template, and the actual execution parameters are in the code
`context.fast_window = 4` shall prevail.

Window units are always bars. The 5/20 of daily `1d` means 5/20 daily bars; if it is changed to a minute strategy, it cannot be interpreted as
Trading day window, parameters and trigger time must be redefined. The current CLI verified frequencies are `1d` and `1M`.

## 3. Parameters and default values

What is really enforced when creating the CLI is the choice between `--market` and `--code/--file`. Agent first identifies the signal type from the demand, and then supplements the
Deterministic default parameters for the type; missing parameters must not be randomly generated, and the adopted defaults are listed in the reply:

| Parameters | Rules |
|---|---|
| `market` | Must be explicitly specified by the user as `hk` or `us`, which determines the code suffix, API and backtest node |
| Target | Priority is given to user targets; if not specified, Hong Kong stocks default to `0700.HK`, US stocks default to `TSLA.NB`, and clearly stated |
| Entry/Exit | Use signal type corresponding to demand; cannot replace breakout, momentum or reversal demand with moving average |
| Signal parameters | User parameters are used first; if missing, the fixed default corresponding to the signal type below is used, and the unit is bar |
| `frequency` | Default `1d`; `1M` means 1 minute bar, not monthly line |
| Backtest interval | The default task execution date is the latest complete natural quarter, and `--startDate/--endDate` is passed explicitly |
| Position | A maximum of 90% of the funds can be used for a single bid; the default budget for multiple bids is equal, and the total target position does not exceed 90% |
| `start_capital` | CLI default `10,000,000` |
| `commission_rate` | CLI default `1`; this is the backend node parameter value and is not interpreted as 1% by itself |
| `slippage` | CLI default `0` |
| Stop Loss/Take Profit/Maximum Retracement | Not enabled if not specified; random generation of thresholds is prohibited |
| Historical warm-up | At least reach the maximum indicator window; additionally retain the previous valid signal when a strict crossover event is required |
| Hong Kong stock trading unit | No fixed default value; read and cache `min_order_amount` by target |

Agent defaults for time-series signal types:

| Requirement type | Default rule when no value is specified |
|---|---|
| Moving average | Hong Kong stock fast/slow window `5/20`, US stock `4/12`; buy above the fast line and clear positions below |
| Breakout | Buy when the high of 20 bar breaks out, exit when the low of 20 bar falls below |
| Momentum | 20 bar return is greater than 0 to buy, less than or equal to 0 to exit |
| Mean reversion | 20 bar mean and standard deviation, z-score less than `-2` buy, return to 0 to exit |
| RSI | 14 bar RSI, buy if less than 30, exit if more than 70 |

These are deterministic defaults for the Skill, not the TQX backend defaults. Target, signal type, window, threshold and exit rules given by the user
Always take priority. When the target is not specified, a template target can be used, but it cannot be written as randomly selecting "any stock" every time.

## 4. Generation process

1. Confirm the market `hk/us`, underlying, frequency and backtest range.
2. Confirm the rules for entry, position addition, position reduction, exit, stop loss, take profit and maximum position.
3. Copy the import, accounts, lifecycle, bar check, position read and `order_shares` structures from the corresponding market template.
4. Replace stock codes, windows, signals and risk controls with user needs; all variable states are saved in `context`.
5. Write multiple lines of code into a UTF-8 `.py` file and use `--file` and `--strictMarketApi` of `tqx research strategy create` to create the QUBE strategy.
6. Only run when explicitly requested by the user; check the successful final status, error log, transaction, position and profit results.

When the user does not specify a backtest date, the most recent complete natural quarter before the task execution date is used by default. For example, the task execution date is on
`2026-07-25`, the default range is `20260401` to `20260630`. The agent must explicitly pass the calculated date in the create command,
You cannot reuse the historical example dates in this article, nor can you rely on the CLI's default interval of 180 days. The timing strategy is judged bar by signal and is not automatically applied.
The default value of cross-section strategy "position adjustment every 5 trading days".

## 5. Single bid and multi bid

The single-target strategy stores `context.symbol` in `initialize`. For multi-symbol time-series strategies,
`context.stock_universe` and save independent history and status for each stock:

```python
context.stock_universe = ["AAPL.NB", "MSFT.NB"]
context.close_history = {
    symbol: [] for symbol in context.stock_universe
}
```

Read `data[symbol]` in `handle_data` one by one, and use `try/except` to handle that the target does not exist; each stock independently calculates signals, checks positions and places orders. prohibit all
Stocks share a price history list, and do not sort them horizontally by income; once compared horizontally, it becomes a cross-sectional strategy.

## 6. Use TQX data pre-screening

The time series strategy can use the fundamental and volume and price data of `tqx_data` to narrow the scope of the target before running independent rules:

- Fundamentals: revenue growth, profitability, cash flow, assets and liabilities, and company events.
- Volume and price: price, volume, turnover, volatility, trend and liquidity.
- Reference data: stock status, trading calendar and index composition.

When pre-screening you must observe:

1. Check the real function, parameters, fields, date limits and market values ​​from `tqx_data_usage.md`.
2. Static pre-screening is bound to the data section date, and only the data that has been disclosed before the starting point of the backtest is used.
3. If the hard condition field is missing, the denominator is not positive, `NaN` or an infinite value, the stock will be eliminated without falling back to the unfiltered full set.
4. To get only the latest financial report per share as of the cross-section date, you can use `get_financial_statement(..., is_latest=True,
   date=<cross-section date>)`; `is_latest=False` must be used when calculating year-on-year, trend or dynamic qualifications that require multiple period financial reports, press
   `(symbol, fy_period)` selects the latest disclosure version before the deadline. Historical strategies must not omit `date`.
5. The query is generated offline, `initialize` or low-frequency `before_trading` and cached, prohibiting repeated querying in each bar.
6. Currently `tqx research strategy create` does not upload independent local DataFrame, and the strategy cannot use `open()` to read the user's local path. small screening
   Results are written into policy code; large or dynamic data is constructed using documented interfaces accessible at computing nodes.
7. If fundamental conditions determine whether a stock continues to implement the timing rules, and the one-year backtest spans the new financial disclosure period, the qualifications must also be dynamic
   renew. Only the data announced at that time can be used on each signal day or reservation qualification update day; the backtest starting point list cannot be used to cover the whole year.
8. If the qualifying symbols are different for each date, generate the `(date, symbol)` qualification panel and press
   Time point rules reading of `cross_sectional_strategies.md`.

Data pre-screening only determines which targets run the rules, and does not change the definition of "each target is calculated independently" of the time series signal.

## 7. Life cycle and data security

- `initialize(context)`: Set account, target, parameters, history cache and status.
- `before_trading(context)`: Reset daily temporary status; do not clear cross-day price history.
- `handle_data(context, data)`: Read the current bar, update the history, calculate the signal and place an order.
- `after_trading(context)`: Record account, order intention and diagnostic log.

The code must check bar, price, account, cash, position, `sellable` and history length. The price must be a finite positive number, and all ratios must be
Protect the denominator. The length of the history cache is limited to avoid unlimited growth with backtesting. Currently bar must use `data[symbol]` and handle
`KeyError`; Don't rely on unacknowledged `bar.close_array`.

The buying quantity of Hong Kong stocks is processed according to the trading unit of each stock in `stock_hk_api.md`; the order for US stocks is processed as an integer number of shares. sell for use
`position.sellable`, order submission does not mean the transaction is completed, and the transaction record must be checked eventually.

## 8. Create and run

Hong Kong stocks:

```powershell
tqx research strategy create --market hk --file ./tests/hk_ma.py `
  --name "Hong Kong stock moving average timing strategy" `
  --startDate 20250101 --endDate 20250220 --frequency 1d `
  --strictMarketApi
```

US stocks:

```powershell
tqx research strategy create --market us --file ./tests/us_ma.py `
  --name "US stock moving average timing strategy" `
  --startDate 20250101 --endDate 20250220 --frequency 1d `
  --strictMarketApi
```

Save `strategy_id` after successful creation. Only executed when explicitly requested by the user:

```powershell
tqx research strategy run <strategy_id> --timeout 1200
```

A successful remote backtest must meet the status `SUCCESS` and progress 100%, and check the log corresponding to `run_id`.
Transactions, positions and profits.
