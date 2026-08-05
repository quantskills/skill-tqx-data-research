# TQX Data Quick Reference

Production assumes the interfaces documented in `tqx_data_usage.md` are available. Before calling one, read its full section and verify parameters, fields, dates, and market limits.

## Route by Research Task

| Research need | Preferred interface |
|---|---|
| HK/US daily bars | `get_hk_daily` / `get_us_daily` |
| HK/US minute bars | `get_hk_min` / `get_us_min` |
| Generic minute, tick, real-time | `get_min_data` / `get_tick_data` / `get_live_market_data` |
| Technical indicators | `calculate_indicators` |
| Stock details, calendars, index members | `get_stock_detail` / `get_trading_calendar` / `get_index_component` |
| Factors, financials, filings | `get_factor` / `get_financial_statement` / `get_filing_announcement` |
| Company and event data | `get_company_*` / `get_event_*` |
| Consensus and FX | `get_consensus_*` / `get_currency` |

## Function Index

### Market and indicators

`get_hk_daily`, `get_us_daily`, `get_hk_min`, `get_us_min`, `get_min_data`, `get_tick_data`, `get_live_market_data`, `calculate_indicators`

### Company, calendars, and indexes

`get_stock_detail`, `get_trading_calendar`, `get_index_component`

### Factors, financials, and events

`get_factor`, `get_financial_statement`, `get_filing_announcement`, `get_event_devidend`, `get_event_capital_market`, `get_event_corporate_actions`, `get_event_fina_disclosure`, `get_event_investor_relation_activities`

### Company fundamentals and holdings

`get_company_concentration`, `get_company_top_concentration`, `get_company_investor`, `get_company_insider_transaction`, `get_company_shareholder_report`, `get_company_oper_metrics`, `get_company_current`, `get_company_imed`, `get_company_price_vol`

### Consensus and FX

`get_consensus_nonperiod`, `get_consensus_recommend`, `get_currency`

## Minimum Return Validation

Check that the result is non-empty, required fields exist, dates are sorted and not duplicated, numeric values contain no unhandled NaN/Inf, prices and volumes are positive, and financial/event data satisfies `source_date <= rebalance_date`.
