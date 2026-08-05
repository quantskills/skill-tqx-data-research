# Cross-sectional strategy for Hong Kong stocks and US stocks

On each rebalancing day, a cross-sectional strategy filters, scores, or ranks a set of instruments and then selects the target holdings. This document explains the stock universe, data, and rebalancing process;
The life cycle, market and order API are still based on `strategy_templates.md`, `stock_hk_api.md` and `stock_us_api.md`.
Read `tqx_data_usage.md` before calling `tqx_data` directly.

## 1. Identify cross-section strategies

The strategy must start with an initial stock universe. If each stock generates signals independently from its own history and stocks are not compared on the same date, it is a time-series strategy; read `time_series_strategies.md` instead.

The initial stock universe can come from:

- Index constituents such as NASDAQ-100, Hang Seng Index or Hang Seng Technology Index.
- Hong Kong stocks or US stocks all market stocks.
- Fixed stock list provided by users.
- A basket of stocks based on fundamentals, industry, market capitalization, liquidity or volume and price rules.

### 1.1 Parameters and default values

The CLI only requires `--market` and one of `--code` or `--file`, but a cross-sectional strategy needs more than a market. The initial universe and ranking factors determine what is compared and how instruments are selected, so there is no safe random default; ask when the research specification is incomplete. For a demonstration requested by the user, you may use a verified sample universe and factor, clearly stating that it is not general investment advice.

| Parameters | Rules |
|---|---|
| `market` | Must be explicitly specified by the user as `hk` or `us` |
| Initial stock universe | Actual research must clearly define index constituents, the full market, a user-provided list, or deterministic screening rules; random stock lists are prohibited |
| Universe type | A fixed list whose eligibility does not change over time may be static; fundamentals, index membership, or time-varying eligibility require a dynamic panel |
| Hard filter conditions | No additional hard filtering by default if not specified by the user; random addition of fundamentals or liquidity thresholds is prohibited |
| Ranking factors | Actual research must be clear; random selection of momentum, ROE or valuation factors is prohibited |
| `top_n` | Default `5`, indicating the maximum number of positions; hold all qualified stocks when there are insufficient qualified stocks |
| Position adjustment period | Default is once every 5 trading days |
| Weight method | Default is equal weight, the total target position does not exceed 90% |
| `frequency` | Default daily line `1d`; `1M` means 1 minute, not monthly line |
| Backtest interval | The most recent complete natural quarter before the default task execution date, and the date is explicitly passed in |
| Exit rules | By default, sell all sellable positions outside the new target set; an empty universe means liquidate by default, while positions that cannot be sold are retained and the reasons recorded |
| Backtest node parameters | `start_capital=10,000,000`, `commission_rate=1`, `slippage=0` |

The dynamic universe must contain at least `date` and `symbol`. If it also performs fundamental screening, retain `source_date`, `fy_period`, the factor values, and `eligible` so that the absence of look-ahead bias can be verified.

## 2. Stock-universe construction

### 2.1 Static universe

The static universe remains unchanged throughout the backtest. First determine the data cutoff date, and use only information disclosed before that date to avoid look-ahead bias.
Write the screening results into the stock list of strategy codes, and then use volume and price signals to sort and adjust positions.

Use a static universe only when the user explicitly requests a frozen universe, fundamentals do not affect later eligibility, or the backtest is known not to cross a new disclosure period. If hard fundamental conditions such as revenue growth, gross margin, or cash flow determine eligibility, do not use a start-date static list for a one-year backtest.

Example that has been run in production environment:

| Market | Sample File | Financial-report cutoff | Hard-condition filter results |
|---|---|---|---|
| US stocks | `tqx_cli/tests/nasdq100_cs_st.py` | `2025-01-01` | `NVDA.NB`, `AVGO.NB` |
| Hong Kong stocks | `tqx_cli/tests/hsi_cs_st.py` | `2025-01-01` | `1810.HK`, `3690.HK` |

The hard conditions are that revenue growth is greater than 20% year-on-year, gross profit margin is greater than 20%, and operating cash flow is greater than 0. The above list is only for the candidate scope and financial reporting caliber.
The results are valid only for that candidate universe, reporting basis, and cross-section date. Re-screen whenever the date or candidate universe changes; do not treat the sample list as a permanent conclusion.

### 2.2 Dynamic universe

The dynamic universe changes over time. First generate panel data with at least the `date` and `symbol` columns:

```text
date      symbol
20250102  NVDA.NB
20250102  AVGO.NB
20250109  NVDA.NB
20250109  META.NB
```

When generating a panel you must:

1. Use the trading day format `YYYYMMDD`, the Hong Kong stock code `.HK`, and the US stock code `.NB`.
2. Deduplicate and sort `(date, symbol)`, and delete empty codes, invalid dates and codes that do not belong to the target market.
3. For each date, only the fundamental data published before that day and the volume and price data visible before that day are used.
4. Preserve dates with no qualifying symbols; do not fall back to the unfiltered universe when a date's universe is empty.
5. Small panels can be stored as constants in the strategy and converted to a DataFrame in `initialize`. Build large panels once, in `initialize` or low-frequency `before_trading`, using the documented `tqx_data` interface, then cache them in `context`.
6. `tqx research strategy create` does not accept a separate local DataFrame. Before creating a Qube strategy, put panel construction or loading logic in the strategy source. Do not use the backend-prohibited `open()` to read local files, and do not assume that a local path exists in the remote compute environment.
7. It is forbidden to repeatedly execute large-scale `tqx_data` queries in each bar and each target loop of `handle_data`.

When fundamentals determine eligibility and the backtest spans a new financial-report disclosure period, a dynamic universe is mandatory. A one-year backtest must rebuild the cross-section on each rebalancing day. A financial factor may remain unchanged when there is no new announcement; after an announcement, use the new value starting on the next rebalancing date. The panel should retain at least:

```text
date      symbol   fy_period  source_date  revenue_growth  gross_margin  operating_cf  eligible
20250102  3690.HK  FY2024Q3  20241129     0.2268          0.3867        40284393000   true
20250702  3690.HK  FY2025Q1  20250527     0.1812          0.3745        10131128000   false
```

`source_date` is the actual financial announcement date, and each row must satisfy `source_date <= date`. A stock can move from eligible to ineligible, so screening only on the backtest start date is incorrect.

On a rebalancing day, prefer the row matching the current `date`. If the business rules allow the most recent available panel, choose only the maximum date satisfying `panel.date <= context.now`; never read a future date.

## 3. Use TQX data filtering

First obtain candidate stocks from the full market, index constituents, or a user list. Combine the following data to form the final universe:

- Fundamentals: financial statements, operating metrics, company metrics, events and consensus expectations.
- Volume and price: daily line, minute line, trading volume, turnover, yield, volatility and liquidity indicators.
- Reference data: stock status, trading calendar and index component changes.

All function names, fields, market parameters, date ranges and frequencies must be verified from `tqx_data_usage.md`. Special attention:

- The US stock market parameter of `get_financial_statement` is `market="nb"`, and the Hong Kong stock market parameter is `market="hk"`.
- Financial report year-on-year filtering uses `date=<position adjustment date>` and `is_latest=False`. Press `(symbol, fy_period)` first to retain the announcement date before the deadline
  For the latest version, find the latest financial period currently available for each stock and compare it with the same financial period of the previous year. You only need the latest single-period indicator on the rebalancing date.
  Use `is_latest=True`, but you must still pass `date=<position adjustment date>`.
- `is_latest=True` Only retains one row for each stock, only suitable for the latest single-period snapshot; cannot calculate year-on-year or build multi-period panels. Historical backtesting
  It is forbidden to omit `date`, otherwise the data disclosed after the position adjustment date will be read.
- One year dynamic fundamental strategy uses `is_latest=False`. You can pass `date=<position date>` separately for each position adjustment day, or you can prefetch it all at once.
  `date=<end date of backtest>` and then construct the cross-section in the memory one by one according to the position adjustment day; the prefetch method must first perform `date <= position adjustment day` filtering, and then filter
  `(symbol, fy_period)` Deduplication cannot be done globally first.
- `fy_period` is the company's fiscal year, which is not equivalent to the calendar year in which the announcement is made. Query quarterly upper bounds to cover company fiscal years that may be marked early, and always
  Use `date` to control visibility; year-on-year queries also cover the same fiscal period of the previous year, while complying with the interface limit of up to 5 calendar years.
- Commonly available fields in financial reports include reported revenue/total business revenue, reported gross profit/gross profit, and operating cash flow; actual data may only be filled in
  A set of compatible fields that must be checked for null values ​​before calculation.
- Revenue growth uses the latest disclosed financial period to compare with the same financial period of the previous year; gross profit margin is gross profit/revenue; operating cash flow must be greater than 0.
- The denominator must be positive, and `NaN`, positive and negative infinity and illegal values ​​are deleted after calculation. Stocks missing hard condition fields will be eliminated directly.

## 4. Position adjustment process

When the user does not specify the frequency of position adjustment, the default position adjustment is once every 5 trading days. According to user requirements when users specify weeks, months, quarters or specific dates.

Each position adjustment is performed in the following order:

1. Read the static or dynamic universe corresponding to the rebalancing day.
2. Apply fundamentals, trading status, and liquidity hard conditions.
3. Calculate cross-section scores in targets that pass hard conditions, such as momentum, multi-factor scores, or user rules.
4. Sort and select up to the top N, and calculate equal weights, market capitalization weighting, or user-specified weights.
5. First sell sellable positions outside the target universe, then adjust the target positions.
6. Check bar, price, cash, position and order quantity; Hong Kong stocks are rounded according to the trading unit of each stock.
7. After running, check the final status, logs, transactions, positions and profits. Do not just look at the command exit code.

`top_n` is the maximum position quantity, not the minimum opening quantity. If only 1 to `top_n - 1` stocks pass the hard conditions, all qualified stocks will be
Stocks are used as targets and positions are adjusted as usual, holding only less than the target number of stocks; they are not allowed to be skipped due to insufficient quantity, nor are they made up with unqualified stocks.
If the universe is empty after screening, the default target set is empty and all sellable positions are sold; record any positions that are suspended, unsellable, or affected by failed orders. Override this liquidation behavior only when the user explicitly requests that an empty universe be held, and never silently fall back to the original universe.

```python
ranked = sorted(scores, key=scores.get, reverse=True)
targets = ranked[: context.top_n] # Allow results to be less than top_n
```

It is forbidden to write `if len(ranked) < context.top_n: return`.

An empty target set must still enter the selling phase. Do not write `if not targets: return` before portfolio rebalancing. First sell every sellable position not in `targets`, then skip buying when `targets` is empty; this ensures that an empty universe is liquidated by default.

## 5. Default parameters

The default rules uniformly use the parameter list of 1.1 and are explicitly listed in the reply. Strategy type based on "Independent Signal" or "Horizontal Comparison/Top N"
Classify the strategy accordingly; ask first if uncertain. Never invent the initial universe or ranking factors. Pass the calculated backtest dates explicitly in
`--startDate` and `--endDate` cannot follow the document example date, nor can they rely on the server-side default range that is not explicitly stated.

For example, if the task execution date is `2026-07-25`, the default latest complete quarter is `20260401` to `20260630`. in documentation
`20250101~20250220` is only used for recurrence history verification and is not the default interval for dateless requests.

## 6. Generation and verification

1. Identify `hk/us`, time-series or cross-sectional structure, the initial universe, and the signal rules.
2. Read `tqx_data_usage.md` when you need to access data directly, then generate a static universe or `(date, symbol)` panel.
3. Read the corresponding market API and `strategy_templates.md`, and reuse the verified life cycle and order structure.
4. Write the multi-line strategy to a UTF-8 `.py` file; use `--file` and `--strictMarketApi` of `tqx research strategy create` when creating it.
5. Perform remote QUBE operations only if the user explicitly asks to create or run them.
6. A successful backtest must meet the following requirements: the final state is `SUCCESS`, and the logs, transactions, positions and income results must be checked. The log output is at least
   Adjustment date, `eligible_count`, actual target quantity and `target_symbols`; when there is zero transaction, the specific reason must be stated.
