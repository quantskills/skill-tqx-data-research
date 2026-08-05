# TQX Research CLI Command Reference

Source: `packages/cli/src/research/command.ts`. The executable command is `tqx`, provided either by the standalone GitHub Release binary or by the `@tqx-ai/cli` npm package; do not use the migrated Python `tqx-cli`. The standalone binary is the preferred user installation path and does not require Node.js. The npm package requires Node.js `>=22.18` and is only a fallback when a Node/npm environment already exists or the binary cannot be used. Resolve the current package version at task start without requiring Node.js; examples pinned to `0.1.14` are illustrative for this repository revision and must not override that runtime check.

## Installation, Gateway and Authentication

Resolve the latest release version with an available HTTP client, not by requiring Node.js. For example:

```powershell
$release = Invoke-RestMethod 'https://api.github.com/repos/tqx-ai/tqx-ts/releases/latest'
$version = $release.tag_name.TrimStart('v')
```

If npm already exists, `npm view @tqx-ai/cli version --json` is also acceptable. Check any existing global CLI next:

```powershell
tqx --version
tqx research --help
```

If the command is missing or its version is older than the resolved version, tell the user that the
installed CLI is out of date and should be upgraded before running Research commands. Install the CLI
globally from the matching GitHub Release standalone binary for the user's OS and architecture, then
verify it. Do not ask the user to install Node.js merely to install or check the CLI. If that binary
cannot be used and a Node/npm environment is available, fall back to the pinned npm package:

```powershell
npm install --global @tqx-ai/cli@<resolved-version>
tqx --version
tqx research --help
```

Use a pinned temporary runner (`npx --yes @tqx-ai/cli@<resolved-version>`, `pnpm dlx @tqx-ai/cli@<resolved-version>`,
or `bunx @tqx-ai/cli@<resolved-version>`) only when that runtime already exists and the task is explicitly isolated or
one-time. Use the same resolved version for every command in the task. The SDK remains a project dependency and is never
installed globally.

Research uses an API key, and the Qube gateway URL must contain `/pandaApi`:

```powershell
$env:TQX_BASE_URL = "https://gateway.example.com/pandaApi"
$env:TQX_API_KEY = "<api-key>"
tqx research factor list --json
```

`TQX_API_KEY` takes precedence over persistent credentials. Use `tqx login --api-key=<api-key>` when you need to save the key; it will verify the key first. The order of credentials is `TQX_API_KEY`, Bun system keychain, `$XDG_CONFIG_HOME/tqx/credentials.json` or `~/.config/tqx/credentials.json`. Do not write keys to source code, command history, makefiles, or output.

`--json` outputs JSON to stdout, error JSON to stderr; `--plain` turns off coloring. Dates accept `YYYYMMDD` or `YYYY-MM-DD` and will be normalized to `YYYY-MM-DD`. `market` accepts case-insensitive `hk` / `us`. The exit code is `2` for usage or validation errors and `1` for API, network and protocol errors.

## Factor Library

```text
tqx research factor create --market=hk|us (--formula=<formula> | --code=<python> | --file=<path>) [--name=<name>] [--description=<text>]
tqx research factor info <factor-id>
tqx research factor update <factor-id> [--market=hk|us] [--formula=<formula> | --code=<python> | --file=<path>] [--name=<name>] [--description=<text>]
tqx research factor run <factor-id> [--name=<name>] [--startDate=<date>] [--endDate=<date>] [--adjustmentCycle=<positive-int>] [--groupNumber=2..20] [--factorDirection=Positive|Negative|1|0] [--pollInterval=<seconds>] [--timeout=<seconds>] [--noWait]
tqx research factor stop <analysis-id> [--pollInterval=<seconds>] [--timeout=<seconds>]
tqx research factor result <analysis-id>
tqx research factor list [--market=all|hk|us] [--offset=<non-negative-int>] [--limit=1..100] [--keyword=<text>] [--includeContent]
tqx research factor delete <factor-id>... --yes
```

The default name of `create` is `TQX Factor`. You must provide one and only one source code input when creating; provide at most one when updating. `--formula` maps to `code_type: formula`, `--code` / `--file` maps to `python`. Python factors must reference at least one `factors["field"]` or `factors['field']`. Formulas starting with a negative sign use `--formula=-close/ref(close,5)`.

`run` defaults to `adjustmentCycle=5`, `groupNumber=5`, `factorDirection=Positive`. `--noWait` returns `SUBMITTED` and `analysis_id`; otherwise poll every 2 seconds, default up to 600 seconds. `stop` polls the cancellation status by default every second, up to 10 seconds; `request_accepted` does not mean that it has been cancelled.

## Strategy Library and Backtests

```text
tqx research strategy create --market=hk|us (--code=<python> | --file=<path>) [--name=<name>] [--description=<text>] [--strictMarketApi] [backtest-options]
tqx research strategy info <strategy-id>
tqx research strategy update <strategy-id> [--market=hk|us] [--code=<python> | --file=<path>] [--name=<name>] [--description=<text>] [--versionSummary=<text>] [--strictMarketApi] [backtest-options]
tqx research strategy run <strategy-id> [backtest-options] [--pollInterval=<seconds>] [--timeout=<seconds>] [--noWait] [--download[=<path>]]
tqx research strategy stop <run-id>
tqx research strategy result <run-id> [--download[=<path>]]
tqx research strategy list [--market=all|hk|us] [--offset=<non-negative-int>] [--limit=1..100] [--keyword=<text>] [--includeContent]
tqx research strategy delete <strategy-id>... --yes
tqx research backtest list [--market=all|hk|us] [--offset=<non-negative-int>] [--limit=1..100] [--keyword=<text>] [--includeContent]
tqx research backtest result <run-id> [--download[=<path>]]
```

`backtest-options`: `--startDate`, `--endDate`, `--startCapital`, `--commissionRate`, `--slippage`, `--frequency=1d|1M`, `--symbols=<symbol1,symbol2,...>`. When creating a strategy, the defaults are `startCapital=10000000`, `commissionRate=1`, `slippage=0`, and `frequency=1d`. Updates and runs retain saved parameters unless explicitly overridden. The CLI rebuilds only supported saved fields and ignores the server's `margin_rate`, `standard_symbol`, and `null` values, so changing the dates does not require deleting and recreating the strategy. The CLI rejects requests whose end date is not later than the start date.

Strategy runs are polled every 2 seconds by default, for up to 600 seconds. A timeout stops local waiting only; it does not cancel the remote run, and the output includes a `stop_command`. `--download` saves the raw result JSON: with no value it writes to the Downloads directory, with a directory it generates a filename there, and with a file path it writes to that file. List commands hide source code by default. `backtest list` also removes large fields and provides `equity_count` and `trade_count`; use `backtest result` for the complete result.

## Local source code check and success status

Strategy source code cannot call `eval`, `exec`, `open`, `__import__`, `compile`, `input`, `globals`, `locals`, `vars`, or `dir` outside strings and comments. `from ... import *` may appear only at module top level. For the current bar, use `data[symbol]` and handle `KeyError`; do not call `data.get(...)`. Hong Kong strategies should import `panda_backtest.api.stock_hk_api`, and US strategies should import `panda_backtest.api.stock_us_api`. A wrong-market import, the mainland `stock_api`, or a missing expected import produces a warning; `--strictMarketApi` turns it into an error.

`done` is mapped to `SUCCESS`; `failed` is `FAILED`, `cancelled` is `CANCELLED`. `PENDING`, `RUNNING`, `SUBMITTED`, `TIMEOUT` and `STOP_REQUESTED` do not complete successfully. Command exit codes are not a substitute for responses, final states, logs, transactions, and result checks.
