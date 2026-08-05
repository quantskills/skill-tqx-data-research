# TQX Data HK/US Parameter Matrix

| Data category | Hong Kong | United States | Note |
|---|---|---|---|
| Symbol | `0700.HK` | `TSLA.NB` | Suffix must match the interface |
| Daily bars | `get_hk_daily` | `get_us_daily` | Verify dates, adjustment, and missing values |
| Minute bars | `get_hk_min` | `get_us_min` | Verify timezone, DST, and sessions |
| Generic minute data | `market="hk"` | Use the interface's documented `market="nb"` where required | Do not normalize every API to `us` |
| Trading calendar | `market="hk"` | Verify the method documentation | Do not assume calendar days are trading days |
| Factors | `type="hk"` | Verify the method documentation | Factor type must match symbols |
| Financials/events | Verify each method | Verify each method | Filter by announcement time |
| Index members | `market="hk"` | Verify each method | Historical backtests need historical membership |

## Point-in-Time Constraints

```text
announcement_date <= rebalance_date
source_date <= decision_time
```
