# Error handling

Use this when factor analysis or strategy backtest code fails.

## Order of diagnosis

1. Environment
   - `.env` loaded
   - `PARQUET_ROOT_PATH` visible
   - `tqx_data` import works
   - local path exists and is readable
2. Data
   - frame is not empty
   - required columns exist
   - `(date, symbol)` has no duplicates
   - no NaN or Inf in critical columns
   - market universe is not empty
3. Logic
   - no future leakage
   - rebalance cycle matches the prompt
   - market matches the symbol suffix
   - code path matches the task: factor code vs strategy code

## Fix order

- Fix environment first
- Fix data second
- Fix logic last

## Return rule

If the run still fails after the above checks, return the exact broken layer and the exact missing field or path. Do not invent results.

## Shared-node rule

If the failure comes from shared research nodes, patch `scripts/research_nodes.py` first. Do not only patch the generated test script.

