#TQX Hong Kong and US stock strategy reference templates

This file is a reference template for Agent to quickly generate strategies for Hong Kong and US stocks. It comes from the already run `tqx_cli/tests/hk_ma.py` and
`tqx_cli/tests/us_ma.py`. After the customer puts forward strategic requirements, the Agent should select the corresponding market template and reuse its life cycle, data reading,
The account holding and order framework only replaces the stock pool, strategy parameters, signals, positions and risk control. Do not re-guess the back-end interface from a blank perspective.
Before generating or modifying a strategy, first determine whether it is a time series strategy or a cross-sectional strategy, and read the `stock_hk_api.md` or
`stock_us_api.md`. Time-series strategies must also read `time_series_strategies.md`; cross-sectional strategies and dynamic universes must also read
`cross_sectional_strategies.md`; reads `tqx_data_usage.md` when calling `tqx_data` directly.

Quick selection:

| User requirements | Start template | Simultaneous reading |
|---|---|---|
| Hong Kong stock time series strategy, `.HK` target | `tqx_cli/tests/hk_ma.py` | `stock_hk_api.md`, `time_series_strategies.md` |
| US stock time series strategy, `.NB` target | `tqx_cli/tests/us_ma.py` | `stock_us_api.md`, `time_series_strategies.md` |
| Hong Kong stock cross-sectional strategies | `tqx_cli/tests/hsi_cs_st.py` | `stock_hk_api.md`, `cross_sectional_strategies.md` |
| U.S. stock cross-sectional strategies | `tqx_cli/tests/nasdq100_cs_st.py` | `stock_us_api.md`, `cross_sectional_strategies.md` |

Moving average logic is just an example and can be replaced by momentum, breakout, reversal or other signals; the corresponding market introduction, strategy callback signature,
Defensive data checking, account position reading and secure order placement.

The time-series strategy evaluates rules independently for each target. A cross-sectional strategy first builds a stock universe, then filters, scores, or ranks it on each rebalancing day. Unless the user specifies otherwise, it rebalances every 5 trading days, and the backtest defaults to the most recent complete calendar quarter before the task date. A dynamic universe must be represented in strategy code as a panel containing at least `date` and `symbol`; it cannot rely on local files inaccessible to the compute node.
The agent must convert the default quarter to explicit `--startDate/--endDate` values and must not substitute the historical test dates below.
The maximum number of stocks you can hold is the number of stocks you pass; if it is less than `top_n`, you must still use all qualified stocks, and you cannot skip position adjustment or make up with unqualified stocks.
All default parameters must be determined and reproducible. Random selection of stocks, indicator windows, stop losses, take profits or positions is prohibited. First select the moving average according to user needs,
Breakthrough, momentum, mean reversion, RSI or other signals; only when the signal type is not specified at all, Hong Kong stocks reuse the `0700.HK` 5/20 template,
US stocks reuse the `TSLA.NB` 4/12 template. See `time_series_strategies.md` for the default values ​​of each signal type. When no risk control threshold is specified
Additional stop-loss/take-profit rules are disabled unless requested. If a cross-sectional strategy lacks an initial universe or ranking factor, ask first.
Cannot be filled randomly.
When it comes to financial report screening, only use `get_financial_statement(..., is_latest=True, date=<section date>)` for a single period snapshot; year-on-year,
Trends, historical panels, and dynamic universes based on multi-period financial reports must use `is_latest=False`, then deduplicate by `(symbol, fy_period)` to retain
The latest disclosed version before the deadline. `date` cannot be omitted in any historical backtest. Specific implementation of reading the financial quarter of `tqx_data_usage.md`
Report section.

If fundamental conditions determine position qualification and the backtest is one year or spans the new financial report disclosure period, the template must be transformed into a dynamic fundamental panel: each position adjustment day
Eligibility will be recalculated using only data announced on that day and previously. First filter the announcement date according to the position adjustment date, and then process the restatement of the same financial period; backtesting cannot be used permanently.
The qualified list of the starting point cannot query the interface repeatedly in each bar. The strategy log should output the position adjustment date, financial period, maximum announcement date,
`eligible_count` and the target stock.

## 1. QUBE Strategy Contract

| Market | CLI | QUBE Strategy `market` | Example underlying |
|---|---|---|---|
| Hong Kong stocks | `--market hk` | `hk` | `0700.HK` |
| US stocks | `--market us` | `us` | `AAPL.NB` |

`tqx research strategy create` saves the Python source code to Strategy `code` and saves the default backtest parameters to
`params.backtest`：`period_start`、`period_end`、`init_balance`、`commission_rate`、
`slippage`, `frequency` and optional `symbols`. `1M` means 1 minute bar, not monthly line.

`tqx research strategy run` calls QUBE `POST /strategies/{strategy_id}/run-backtest` and returns the integer `run_id`;
Do not call `start()`, `get_backtest_id()` or `run_stock_backtest()` yourself in the strategy code.

## 2. Reliable structure shared by both templates

1. Import the general trading API and the corresponding market API at the same time.
2. `initialize(context)` sets the account, target, parameters and all mutable states.
3. `handle_data(context, data)` defensively checks account, bar, price and history length.
4. Historical prices are saved in `context` and do not rely on unconfirmed `bar.close_array`.
5. Read accounts and positions through `context.stock_account_dict`.
6. `order_shares` is a positive number to buy and a negative number to sell; use `position.sellable` to sell.
7. The current template implements the status judgment of "hold if the short moving average is higher than the long moving average", and is not a strict judgment of upper/lower crossing events.

## 3. Hong Kong stock daily moving average template

This template corresponds to `tqx_cli/tests/hk_ma.py`, is used for QUBE `market=hk`, and can be used as a single-label daily line compatible skeleton.
The original run-through template does not actively round up by `min_order_amount`. The current backend will normalize the order quantity again, so the requested quantity is the same as
Actual order quantities may vary. When generating a new Hong Kong stock strategy, even if you still use `0700.HK`, you must press `stock_hk_api.md`
Read and cache the `min_order_amount` of each target, and then round the buying amount; do not regard the unrounded part below as a best practice.

```python
from panda_backtest.api.api import *
from panda_backtest.api.stock_hk_api import *
import tqx_data


def initialize(context):
    context.account = "15032863"
    context.symbol = "0700.HK"

    context.short_window = 5
    context.long_window = 20
    context.max_position_ratio = 0.9

    context.closes = []
    context.last_date = None


def _update_closes(context, bar):
    trade_date = getattr(bar, "trade_date", None)
    if trade_date is not None:
        if context.last_date == trade_date:
            return
        context.last_date = trade_date

    context.closes.append(float(bar.close))
    max_len = max(context.short_window, context.long_window)
    if len(context.closes) > max_len:
        context.closes = context.closes[-max_len:]


def _calc_ma(series, window):
    if len(series) < window:
        return None
    return sum(series[-window:]) / window


def _get_position(account, symbol):
    if account is None:
        return None
    return account.positions.get(symbol)


def _position_size_by_cash(account, price, max_ratio):
    if account is None or price is None or price <= 0:
        return 0
    cash_to_use = account.cash * max_ratio
    qty = int(cash_to_use // price)
    return max(qty, 0)


def handle_data(context, data):
    symbol = context.symbol

    try:
        bar = data[symbol]
    except Exception:
        return

    if bar is None or bar.close is None or bar.close <= 0:
        return

    _update_closes(context, bar)
    if len(context.closes) < context.long_window:
        return

    short_ma = _calc_ma(context.closes, context.short_window)
    long_ma = _calc_ma(context.closes, context.long_window)
    if short_ma is None or long_ma is None:
        return

    account = context.stock_account_dict.get(context.account)
    position = _get_position(account, symbol)
    quantity = position.quantity if position else 0

    if short_ma > long_ma:
        if quantity == 0:
            price = float(bar.close)
            buy_qty = _position_size_by_cash(
                account, price, context.max_position_ratio
            )
            if buy_qty > 0:
                order_shares(
                    context.account,
                    symbol,
                    buy_qty,
                    style=MarketOrderStyle,
                )
    elif short_ma < long_ma and position and position.sellable > 0:
        order_shares(
            context.account,
            symbol,
            -position.sellable,
            style=MarketOrderStyle,
        )
```

run:

```powershell
tqx research strategy create --market hk --file .\tests\hk_ma.py `
  --name "Hong Kong stock moving average strategy" `
  --startDate 20250101 --endDate 20250220 --frequency 1d `
  --strictMarketApi

tqx research strategy run <strategy_id> --timeout 1200
```

## 4. US stock daily moving average template

This template corresponds to `tqx_cli/tests/us_ma.py`, for QUBE `market=us`. The window unit is bar: the daily line is the trading day,
The minute frequency becomes minutes, so do not directly switch this template to the minute strategy.

```python
from panda_backtest.api.api import *
from panda_backtest.api.stock_us_api import *
import tqx_data


def initialize(context):
    context.account = "15032863"
    context.stock_universe = ["TSLA.NB"]

    context.fast_window = 4
    context.slow_window = 12
    context.max_position_ratio = 0.9

    context.today_trades = []
    context.close_history = {
        symbol: [] for symbol in context.stock_universe
    }


def before_trading(context):
    context.today_trades = []
    account = context.stock_account_dict.get(context.account)
    if account is not None:
        print(
            f"[US before_trading] date={context.now}, "
            f"total_value={account.total_value:.2f}, cash={account.cash:.2f}"
        )


def _compute_ma(series, window):
    if series is None or len(series) < window:
        return None
    window_vals = series[-window:]
    window_vals = [
        value for value in window_vals
        if value is not None and value > 0
    ]
    if len(window_vals) < window:
        return None
    return sum(window_vals) / float(window)


def handle_data(context, data):
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    for symbol in context.stock_universe:
        try:
            bar = data[symbol]
        except (KeyError, TypeError, AttributeError):
            continue
        if bar is None:
            continue

        close_val = getattr(bar, "close", None)
        if close_val is None:
            continue
        close_price = float(close_val)
        if close_price <= 0:
            continue

        history = context.close_history.setdefault(symbol, [])
        history.append(close_price)
        max_len = max(context.fast_window, context.slow_window) * 5
        if len(history) > max_len:
            history[:] = history[-max_len:]
        if len(history) < context.slow_window:
            continue

        curr_fast = _compute_ma(history, context.fast_window)
        curr_slow = _compute_ma(history, context.slow_window)
        if curr_fast is None or curr_slow is None:
            continue

        position = account.positions.get(symbol)
        quantity = 0 if position is None else position.quantity
        sellable = 0 if position is None else position.sellable

        should_buy = curr_fast > curr_slow and quantity == 0
        should_sell = (
            curr_fast < curr_slow and quantity > 0 and sellable > 0
        )

        if should_buy:
            cash = account.cash
            if cash <= 0:
                continue
            max_invest_cash = cash * context.max_position_ratio
            buy_qty = int(max_invest_cash // close_price)
            if buy_qty <= 0:
                continue

            order_shares(
                context.account,
                symbol,
                buy_qty,
                style=MarketOrderStyle,
            )
            context.today_trades.append({
                "symbol": symbol,
                "side": "BUY",
                "qty": buy_qty,
                "price": close_price,
                "fast_ma": curr_fast,
                "slow_ma": curr_slow,
            })
        elif should_sell:
            order_shares(
                context.account,
                symbol,
                -sellable,
                style=MarketOrderStyle,
            )
            context.today_trades.append({
                "symbol": symbol,
                "side": "SELL",
                "qty": sellable,
                "price": close_price,
                "fast_ma": curr_fast,
                "slow_ma": curr_slow,
            })


def after_trading(context):
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    print(
        f"[US after_trading] date={context.now}, "
        f"total_value={account.total_value:.2f}, cash={account.cash:.2f}"
    )
    if context.today_trades:
        print("Today's MA order submissions:")
        for trade in context.today_trades:
            print(
                f"  {trade['symbol']} {trade['side']} "
                f"{trade['qty']} @ {trade['price']:.2f} "
                f"(fast={trade['fast_ma']:.2f}, "
                f"slow={trade['slow_ma']:.2f})"
            )
    else:
        print("No orders submitted today.")
```

run:

```powershell
tqx research strategy create --market us --file .\tests\us_ma.py `
  --name "US stock moving average strategy" `
  --startDate 20250101 --endDate 20250220 --frequency 1d `
  --strictMarketApi

tqx research strategy run <strategy_id> --timeout 1200
```

## 5. Checklist when modifying templates

- Markets, nodes, API imports and stock suffixes are consistent.
- Preserve the signatures of `initialize(context)` and `handle_data(context, data)`.
- Put mutable state in `context`, do not use module-level mutable global variables.
- Get bar, account, price, check for non-existence and null values ​​before opening a position.
- Protect zero denominator before division, reject NaN, Inf and non-positive prices.
- Check cash and quantity before buying; Hong Kong stocks are rounded according to the underlying trading unit.
- Use `sellable` for selling; order submission does not equal transaction.
- An empty cross-sectional universe is liquidated by default; sell non-target positions first, then skip buying when the target is empty, and do not `return` early.
- Do not query historical market prices, details or trading calendar frequently in `handle_data`.
- Disable dangerous built-in functions; use `--strictMarketApi`.
- After modification, create the QUBE strategy first, then run and check the final state, error log, transaction and income results.
