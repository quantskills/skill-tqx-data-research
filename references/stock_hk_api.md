# TQX Hong Kong Stock Strategy API Reference

This document is used to write the strategy code of `tqx research strategy create --market hk`. The source is the current backend
`panda_backtest.api.stock_hk_api`, the generic trading API and `tests/hk_ma.py` which has run validation.

## 1. Interface layering

| Layer | Purpose | Entrance |
|---|---|---|
| Strategy life cycle | Backtesting engine calls user code | `initialize/before_trading/handle_data/after_trading` |
| Current market price | Read current data for each bar | `data[symbol]` |
| Hong Kong stock market history | Low-frequency reading of daily or minute lines | `panda_backtest.api.stock_hk_api` |
| Placing orders and orders | Simulated trading | `panda_backtest.api.api` |
| QUBE CLI | Create, run, query and stop | `tqx research strategy`, `tqx research backtest` |

Do not call internal `run_stock_backtest()` in the strategy code; QUBE backtest running is handed over to `tqx research`.

## 2. Required import and market agreement

```python
from panda_backtest.api.api import *
from panda_backtest.api.stock_hk_api import *
```

- CLI market must be `--market hk`.
- Hong Kong stock codes use 4 digits plus `.HK`, such as `0700.HK`, `0941.HK`, `0005.HK`.
- Do not use 5-digit number formats such as `00941.HK`, and do not import A-share or US stock quotation modules.
- The number of shares per lot of Hong Kong stocks varies depending on the underlying stock. `min_order_amount` must be read and cached at low frequency and cannot be fixed at 100 for the entire market.
- It is recommended to use `--strictMarketApi` when creating or updating.

## 3. `stock_hk_api` officially public function

The module formally registers two functions through `api_list`. Modules do not have `__all__`, do not treat internal helper functions and import names as
Stable API.

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
| `symbol_list` | Must be a non-empty `list` or `tuple`; uses 4-digit `.HK` code |
| `start_date` | Daily line date; minute line can have time, and the boundary includes |
| `end_date` | Same as above, must be no earlier than the start time |
| `fields` | Sequence of field names; do not pass a single string |
| `period` | Can only be lowercase `"1d"` or `"1m"` |

Date support:

- Daily: `YYYYMMDD`, `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYY.MM.DD` strings, and
  `date`、`datetime`、`pandas.Timestamp`。
- Minute line: `YYYYMMDD`, `YYYYMMDDHHMM`, `YYYYMMDDHHMMSS`, `datetime` or
  `pandas.Timestamp`。
- Do not pass `None`, pure `date` objects or space-separated date and time strings for the minute line.

Daily example:

```python
daily = stock_api_quotation(
    symbol_list=["0005.HK", "0700.HK"],
    start_date="20260101",
    end_date="20260131",
    fields=["symbol", "date", "open", "high", "low", "close", "volume", "pre_close"],
    period="1d",
)
```

Minute line example:

```python
minute = stock_api_quotation(
    symbol_list=["0700.HK"],
    start_date="20260105093000",
    end_date="20260105160000",
    fields=["symbol", "date", "time", "close", "volume", "bidprice1", "askprice1"],
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
`pre_close/limit_up/limit_down/trade_status`. The complete column set and dtype depends on the data file.

Minute line conversion: `amount -> turnover`, `minute -> time`, `bid -> bidprice1`, `ask -> askprice1`,
And add `trade_date` and `last = close`. `date/time` is an integer, and the bottom layer always uses `frequency="1m"`.
Time bounds are included, ultimately sorted by `symbol/date/time`.

The Hong Kong stock implementation will ignore fields that do not exist in `fields` and always retain existing `symbol/date`. No data on daily or minute lines,
When the daily line lacks `date`, an empty DataFrame is returned; when the minute raw data is missing `date/minute`, an empty DataFrame is returned.
`KeyError` may still be thrown when `bid/ask/close` is used. The caller must check for `None`, an empty table, and required columns.

### 3.2 `stock_api_pre_close`

```python
def stock_api_pre_close(
    df_stock_code: pandas.DataFrame,
    date: str,
) -> pandas.DataFrame
```

- `df_stock_code` must contain the `symbol` column.
-On success, only the two columns `symbol` and `pre_close` are returned.
- `KeyError` may be thrown when empty input, no market price or missing fields, do not assume that an empty table will be returned stably.

```python
symbols = pd.DataFrame({"symbol": ["0005.HK", "0700.HK"]})
previous = stock_api_pre_close(symbols, "20260105")
```

## 4. Hong Kong stock details and trading units

`min_order_amount` does not belong to `stock_hk_api` and needs to be read through `tqx_data` at low frequency:

```python
import tqx_data

details = tqx_data.get_stock_detail(
    symbol=["0005.HK", "0700.HK"],
    market="hk",
    status=1,
    fields=["symbol", "name", "status", "min_order_amount"],
)
lot_by_symbol = {
    row["symbol"]: int(row["min_order_amount"])
    for _, row in details.dropna(subset=["min_order_amount"]).iterrows()
}
```

Only read and cache low frequency in `initialize` or `before_trading`, do not query on each bar. If the details are missing, skip placing the order.
Don't make up your trading units. `0005.HK=400` and `0700.HK=100` have appeared in the current local sample data. This is not a permanent rule.

## 5. Strategy lifecycle

| Callback | Required | Calling time |
|---|---|---|
| `initialize(context)` | Yes | The strategy starts once, initializing the account, stock pool, parameters and cache |
| `before_trading(context)` | No | Before each trading day, reset the daily status |
| `handle_data(context, data)` | Yes | Each bar; only memory reading, signal calculation and order placement |
| `after_trading(context)` | No | At the end of each trading day, output a low-frequency summary |

Currently `tests/hk_ma.py` only implements `initialize` and `handle_data`. It uses `bar.trade_date` to prevent repetition of the same day
Records close, so its reliable use is for daily strategies; at minute frequency, it records the first bar of the day, not the daily closing price.

```python
symbol = "0700.HK"
try:
    bar = data[symbol]
except KeyError:
    bar = None
account = context.stock_account_dict.get(context.account)
position = None if account is None else account.positions.get(symbol)
```

Commonly used bar fields: `open/high/low/close/last/volume/turnover/vwap/preclose/date/time/trade_date/`
`bidprice1/askprice1`. Commonly used account fields: `cash/total_value/market_value/positions`; position fields:
`quantity/sellable/avg_price/market_value`。

## 6. General stock order API

These functions come from `panda_backtest.api.api`, not `stock_hk_api`:

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

- Positive quantity/amount to buy, negative quantity/amount to sell.
- The buying amount must be rounded down according to the `min_order_amount` of the underlying.
- For selling, use `position.sellable` first; the processing of tail positions is still subject to the matching rules of the target environment.
- The return of an order only represents submission and is not equivalent to a transaction.

```python
lot = context.lot_by_symbol.get(symbol)
if lot and account and bar and bar.close and bar.close > 0:
    raw_qty = int(account.cash * 0.5 // float(bar.close))
    buy_qty = raw_qty // lot * lot
    if buy_qty > 0:
        order_shares(context.account, symbol, buy_qty, style=MarketOrderStyle)

if position and position.sellable > 0:
    order_shares(context.account, symbol, -position.sellable, style=MarketOrderStyle)
```

## 7. Minimum runnable strategy

The existing `tqx_cli/tests/hk_ma.py` is tested with the CLI backtest run, but its buy amount is not rounded to the number of shares per lot; use it as
Life cycle and moving average status examples should not be used directly for real trading unit verification.

```powershell
tqx research strategy create --market hk --file .\tests\hk_ma.py `
  --name "Hong Kong stock moving average strategy" `
  --startDate 20250101 --endDate 20250220 --frequency 1d `
  --strictMarketApi

tqx research strategy run <strategy_id> --timeout 1200
```

This code is a state strategy of holding when the short moving average is higher than the long moving average and clearing when it is lower than the long moving average. It is not a strict cross event detection.

## 8. Data and security checks

- Do not place an order when the market price is empty, necessary fields are missing, price/volume is non-positive, NaN or Inf.
- OHLC, `volume`, and `preclose` may have outliers; protect the denominator before division, and do not directly fill in 0 for invalid market conditions.
- Disable `eval/exec/open/compile/input/globals/locals/vars/dir/__import__`.
- Use `--file` for multiple lines of code; markets, imported modules and code suffixes must be consistent.
- Use `--strictMarketApi` and check for `market=hk` returned by QUBE after creation.
- `TIMEOUT` only stops CLI waiting, not background tasks.

## 9. Confirmed and unconfirmed boundaries

Confirmed by source review: function signatures, parameter validation, field conversion, date filtering, empty-data handling, strategy lifecycle, and the general order-placement signature.

You cannot rely solely on the current source code to promise: all real columns/dtypes, data coverage of all Hong Kong stocks and suspension ranges, the number of shares per lot will remain unchanged forever, fees and
The details are matched and the order must be completed. The above content must be based on the target environment details interface and backtest results.
