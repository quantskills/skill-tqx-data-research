# Qube Strategy Source Constraints

The TypeScript CLI uploads Python source as opaque text. Its source checks supplement the documented Qube runtime: read `strategy_templates.md` and the market-specific API reference before generating source, and read the `tqx_data` references before using data APIs.

## Confirm before generation

Before writing source that will be uploaded or run, read the task-routed Qube reference and obtain any missing contract from the user or an authoritative runtime document:

- a known-good Qube strategy or factor;
- the required market API and field definitions;
- the source API contract for the requested strategy type.

Without that material, draft a research specification or explain the missing contract instead of fabricating executable Python.

## CLI-verifiable rules

- Factor definitions accept a formula or Python source. Python factor source must reference at least one `factors["field"]` or `factors['field']` expression.
- Strategy definitions accept only Python source.
- For Hong Kong strategies, the CLI expects `panda_backtest.api.stock_hk_api`; for US strategies, it expects `panda_backtest.api.stock_us_api`.
- The CLI warns about the mainland `panda_backtest.api.stock_api`, the wrong market import, or a missing expected import. Pass `--strictMarketApi` to reject those warnings.
- The CLI rejects calls to `eval`, `exec`, `open`, `__import__`, `compile`, `input`, `globals`, `locals`, `vars`, and `dir` when they occur outside strings and comments.
- Star imports (`from ... import *`) must be at module top level. The CLI rejects nested star imports.
- Current-bar data must use `data[symbol]` with `KeyError` handling. The CLI rejects `data.get(...)`.

The checks above are not a compiler, sandbox guarantee, data validation, or evidence that code will execute successfully on Qube.
