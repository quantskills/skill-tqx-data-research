# TQX US Stock Strategy API Reference

This document is used to write the strategy code of `tqx research strategy create --market us`. The source is the current backend
`panda_backtest.api.stock_us_api`, the generic trading API and `tests/us_ma.py` which has run validation.

## 1. Interface layering

Don't confuse the following four layers:

| Layer | Purpose | Entrance |
|---|---|---|
| Strategy life cycle | Backtesting engine calls user code | `initialize/before_trading/handle_data/after_trading` |
| Current market price | Read current data for each bar | `data[symbol]` |
| US stock market history | Low-frequency reading of daily or minute lines | `panda_backtest.api.stock_us_api` |
| Placing orders and orders | Simulated trading | `panda_backtest.api.api` |
| QUBE CLI | Create, run, query and stop | `tqx research strategy`, `tqx research backtest` |

Do not call internal `run_stock_backtest()` in the strategy code; QUBE backtest running is handed over to `tqx research`.

## 2. Required import and market agreement

```python
from panda_backtest.api.api import *
from panda_backtest.api.stock_us_api import *
```

- CLI markets must be `--market us`.
- The current US stock data codes use `.NB`, such as `AAPL.NB`, `TSLA.NB`, `NVDA.NB`.
- Do not import A-share `panda_backtest.api.stock_api` or Hong Kong stock `stock_hk_api`.
- It is recommended to use `--strictMarketApi` when creating or updating, so that incorrect or missing market imports will fail directly.

## 3. `stock_us_api` officially public function

The module formally registers two functions through `api_list`. The module does not have `__all__`, `import *` technically also exposes some internal names,
But do not rely on informal interfaces such as `append_to_api_list`, `get_us_daily`, `get_us_min`, `pd`, etc.

### 3.1 `stock_api_quotation`

```python
def stock_api_quotation(
    symbol_list: Optional[List[str]] = None,
    start_date: Optional[object] = None,
    end_date: Optional[object] = None,
    fields: Optional[Iterable[str]] = None,
    period: Optional[str] = None,
) -> pandas.DataFrame
```

| Parameters | Rules |
|---|---|
| `symbol_list` | Must be a non-empty `list` or `tuple`; use `.NB` code |
| `start_date` | The daily line uses date; the minute line can have time, and the boundary includes |
| `end_date` | Same as above, must be no earlier than the start time |
| `fields` | Sequence of field names; do not pass a single string |
| `period` | Can only be lowercase `"1d"` or `"1m"` |

Date support:

- Daily: `YYYYMMDD`, `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYY.MM.DD` strings, and
  `date`、`datetime`、`pandas.Timestamp`。
- Minute line: `YYYYMMDD`, `YYYYMMDDHHMM`, `YYYYMMDDHHMMSS`, `datetime` or
  `pandas.Timestamp`。
- Do not pass `None`, plain `date` objects or `YYYY-MM-DD HH:MM:SS` strings separated by spaces for the minute line.

Daily example:

```python
daily = stock_api_quotation(
    symbol_list=["AAPL.NB", "TSLA.NB"],
    start_date="20260101",
    end_date="20260131",
    fields=["symbol", "date", "open", "high", "low", "close", "volume", "pre_close"],
    period="1d",
)
```

Minute line example:

```python
minute = stock_api_quotation(
    symbol_list=["AAPL.NB"],
    start_date="20260105093000",
    end_date="20260105160000",
    fields=["symbol", "date", "time", "close", "volume"],
    period="1m",
)
```

Daily field conversion:

| Underlying fields | API return fields |
|---|---|
| `amount` | `turnover` |
| `pre_close` | `preclose`, and add compatible alias `pre_close` |
| `uplimit` | `limit_up` |
| `lolimit` | `limit_down` |
| `date` | Convert to string and add string `trade_date` |

Commonly used daily fields are `symbol/date/trade_date/open/high/low/close/volume/turnover/vwap/preclose/`
`pre_close/limit_up/limit_down/trade_status`. The complete column set and dtype depend on the current data file and should not be hard-coded.

The minute line will `amount -> turnover`, `us_date -> date/trade_date`, `us_minute -> time`, and increase
`last = close`. `date/time` is an integer and `trade_date` is a string. The underlying fixed use is `frequency="1m"` and
`market="nb"`。

`symbol`, `date` are retained when `fields` is specified. The implementation of U.S. stocks will throw `KeyError` when encountering unknown fields; empty data will be returned every minute.
Empty DataFrame, daily empty data may also throw `KeyError` due to missing `date`, the caller must capture and check the result.

### 3.2 `stock_api_pre_close`

```python
def stock_api_pre_close(
    df_stock_code: pandas.DataFrame,
    date: str,
) -> pandas.DataFrame
```

- `df_stock_code` must contain the `symbol` column.
- `date` uses date line date format.
-On success, only the two columns `symbol` and `pre_close` are returned.
- `ValueError`/`KeyError` may be thrown when empty input, missing `symbol`, no market price or missing leading field.

```python
symbols = pd.DataFrame({"symbol": ["AAPL.NB", "TSLA.NB"]})
previous = stock_api_pre_close(symbols, "20260105")
```

## 4. Strategy lifecycle

| Callback | Required | Calling time |
|---|---|---|
| `initialize(context)` | Yes | The strategy starts once, initializing the account, stock pool, parameters and cache |
| `before_trading(context)` | No | Before each trading day, reset the daily status |
| `handle_data(context, data)` | Yes | Each bar; only memory reading, signal calculation and order placement |
| `after_trading(context)` | No | At the end of each trading day, output a low-frequency summary |

In minute backtest, `context.hms` is used according to the US stock market trading hours. Do not call stock details, trading calendar or
`stock_api_quotation`; Historical data should be loaded and cached at low frequency during initialization or before trading.

### Current bar, account and position

```python
symbol = "TSLA.NB"
try:
    bar = data[symbol]
except KeyError:
    bar = None
account = context.stock_account_dict.get(context.account)
position = None if account is None else account.positions.get(symbol)
```

Commonly used bar fields: `open/high/low/close/last/volume/turnover/vwap/preclose/date/time/trade_date`.
Commonly used account fields: `cash/total_value/market_value/positions`. Commonly used position fields:
`quantity/sellable/avg_price/market_value`。

## 5. General stock order API

These functions are from `panda_backtest.api.api`, not `stock_us_api`:

```python
order_shares(account_id, id_or_ins, quantity, style=None, retry_num=0,
             risk_control_client=None, remark=None)
order_values(account_id, id_or_ins, amount, style=None, retry_num=0,
             risk_control_client=None, remark=None)
cancel_order(account_id, order_id)
target_stock_group_order(account, symbol_dict, price_type=0)
sub_stock(symbol_list)
get_today_order(account_id, order_id)
get_today_work_order(account_id)
```

- `order_shares`: `quantity > 0` for buying, `quantity < 0` for selling; the current U.S. stock backend is verified based on integer shares and a minimum of 1 share.
- `order_values`: `amount > 0` for buying, `amount < 0` for selling.
- Use `position.sellable` first for selling, do not assume that all `quantity` is sellable.
- Calling the order function only means submitting the order and cannot be directly regarded as a transaction; the transaction is subject to the order and backtest results.

```python
if account and bar and bar.close and bar.close > 0:
    buy_qty = int(account.cash * 0.5 // float(bar.close))
    if buy_qty > 0:
        order_shares(context.account, "TSLA.NB", buy_qty, style=MarketOrderStyle)

if position and position.sellable > 0:
    order_shares(context.account, "TSLA.NB", -position.sellable, style=MarketOrderStyle)
```

## 6. Minimum runnable strategy

It is preferred to use the verified file `tqx_cli/tests/us_ma.py` directly:

```powershell
tqx research strategy create --market us --file .\tests\us_ma.py `
  --name "US stock moving average strategy" `
  --startDate 20250101 --endDate 20250220 --frequency 1d `
  --strictMarketApi

tqx research strategy run <strategy_id> --timeout 1200
```

This example is a 4/12 bar moving average state strategy, not a strict cross event detection; `today_trades` records the order intention,
It is not a transaction confirmation. The window unit changes with frequency, the daily line is the trading day, and the minute line is the minute.

## 7. Data and security checks

- Do not place an order when the market price is empty, fields are missing, price/volume is non-positive, NaN or Inf.
- OHLC, `volume`, and `preclose` may have outliers; protect the denominator before division, and do not directly fill in 0 for invalid market conditions.
- Disable `eval/exec/open/compile/input/globals/locals/vars/dir/__import__`.
- Use `--file` for multi-line code to avoid PowerShell parameters damaging source code quotes.
- The market, imported modules, and code suffixes must be consistent and use `--strictMarketApi`.
- `TIMEOUT` only stops CLI waiting; retain the returned `run_id`, use `tqx research strategy result <run_id>` query or
  `tqx research strategy stop <run_id>` Cancel the background task.

## 8. Confirmed and unconfirmed boundaries

Confirmed by source review: function signatures, parameter validation, field conversion, sorting, date filtering, strategy lifecycle, and the general order signature.

The current source code alone cannot promise: all real data columns and dtypes, all historical interval coverage, precise time zone semantics of `us_datetime`,
Non-`.NB` suffix compatibility, orders must be completed. The above content must be based on the actual data of the target environment and the backtest results.
