---
name: skill-tqx-research
description: "Use TQX Qube's Hong Kong and US stock investment research infrastructure, including CLI installation and API-key onboarding, @tqx-ai/cli, @tqx-ai/sdk, factors, factor analysis, strategies, backtesting, panda_backtest market API, tqx_data, time-series strategies, cross-sectional strategies, and Qube simulation or agent decision-support environments. Use when users mention Qube, TQX Agent Quant, tqx research, Research API, factor analysis, strategy backtesting, Hong Kong or US stock strategies, tqx_data, or Qube Python strategy code. Do not use for trading balances, positions, orders, fills, PAPER/LIVE trading accounts, mainland China stocks, futures, or the old QuantFlow workflow."
quantSkills:
  organization: https://github.com/quantskills
  repository: quantskills/skill-skill-tqx-research
  repository_url: https://github.com/quantskills/skill-tqx-research
  project_type: skill
  collection: tqx
  license: GPL-3.0
  category: trader-research
  tags: [tqx, qube, hk-stocks, us-stocks, factor, backtest]
  platforms: [claude-code, codex, openclaw]
  language: zh-en
  status: draft
  validation_level: runnable
  maintainer_type: community
  requires: []
  summary_zh: 港股和美股 TQX Qube 因子、策略、数据和回测研究 Skill
  summary_en: TQX Qube research skill for HK and US factors, strategies, data, and backtests
---

```json qsh-form
{
  "version": 1,
  "task": {
    "placeholder": "例如：分析港股动量因子、生成美股截面策略、检查回测可信度",
    "required": true
  },
  "fields": [
    {
      "key": "market",
      "type": "select",
      "label": "市场",
      "options": [
        { "value": "hk", "label": "港股" },
        { "value": "us", "label": "美股" }
      ]
    },
    {
      "key": "task_type",
      "type": "select",
      "label": "任务类型",
      "options": [
        { "value": "factor", "label": "因子研究" },
        { "value": "strategy", "label": "策略生成" },
        { "value": "backtest", "label": "回测分析" },
        { "value": "data", "label": "数据获取" }
      ]
    },
    {
      "key": "start_date",
      "type": "date",
      "label": "开始日期"
    },
    {
      "key": "end_date",
      "type": "date",
      "label": "结束日期"
    }
  ],
  "prompt_template": "请使用 skill-tqx-research 处理任务：{{task}}；市场：{{market}}；任务类型：{{task_type}}；开始日期：{{start_date}}；结束日期：{{end_date}}。附件：{{attachments}}"
}
```

# TQX Research

Use this skill to perform HK/US Qube research tasks consistently across portable agent platforms such as Claude Code, OpenClaw, and Codex-style skill systems.

## System boundary

Treat Qube as TQX's research system, not its trading system. Qube supports investment research, strategy development, and research-side decision support for a local agent. Do not use Qube commands to query trading balances, positions, orders, or fills, or to place, modify, or cancel orders.

If Qube provides a simulation environment, treat it as research and decision support for a local agent. Do not describe it as a trading account or as executing real trades. Keep it distinct from the trading system's `PAPER` simulated account and `LIVE` real-money account; route those account-based workflows to [`tqx-trading`](../tqx-trading/SKILL.md).

TQX Research has two well-defined layers:

- **Resource management and execution**: Use `@tqx-ai/cli` or `@tqx-ai/sdk` published by `tqx-ts` to access the `/pandaApi` gateway with an API key. Do not use the Python `tqx-cli`, account/password login, session tokens, or `workflow_*`.
- **Strategy runtime and data research**: `panda_backtest` and `tqx_data` remain available in Qube Python strategy source. They are not replacements for the TypeScript Research client; they are domain infrastructure that must be verified when generating, reviewing, and running strategies.

## Version resolution

This Skill is served from the moving `main` branch and must not be treated as a version lock. At the start of a CLI task, resolve the latest standalone release version without requiring Node.js, for example from GitHub Releases metadata or the npm registry through an available HTTP client. Use `npm view @tqx-ai/cli version --json` only when npm is already available. Check the user's installed `tqx --version` when present, and use the resolved version consistently for binary installation, temporary execution, and verification. If an older CLI is already installed, tell the user that the CLI is out of date and should be upgraded before running Research commands; do not silently continue with old command shapes. Do not ask the user to install Node.js merely to install or check the CLI. If the latest version cannot be reached, use only an already verified CLI and report that the latest version could not be checked.

## Read by task

- All CLI operations, authentication, parameters, status and output: read [Commands Reference](references/commands.md).
- Writing Node.js/TypeScript integrations, confirming SDK types, or polling: read [SDK reference](references/sdk.md).
- Generate or modify strategy source code: first read [Strategy Templates](references/strategy_templates.md), then read the corresponding [Hong Kong Stock API](references/stock_hk_api.md) or [US Stock API](references/stock_us_api.md) corresponding to the market.
- Generate time-series strategies: also read [Time-Series Strategies](references/time_series_strategies.md).
- Generate cross-sectional strategies, dynamic stock universes, or fundamental filters: also read [Cross-Sectional Strategies](references/cross_sectional_strategies.md).
- When strategy code calls `tqx_data` directly, read [Quick Reference](references/tqx_data_quick_reference.md), [Market Matrix](references/tqx_data_market_matrix.md), and the complete [Data API](references/tqx_data_usage.md) in that order. The full API reference is the sole authority for fields, parameters, and market restrictions.
- To confirm the CLI's local source inspection boundaries, read [Strategy Source Constraints](references/strategy-source.md).

## How to work

1. Confirm the market is `hk` or `us`, and distinguish between factor definition, factor analysis, strategy definition, strategy backtesting and local source code generation. Resource ID must be a positive integer.
2. When only generating source code, research designs or command drafts, no authentication, no remote resources creation, no analysis or backtesting are performed.
3. `create`, `update`, `run`, `stop`, and `delete` all have remote side effects. Run them only when explicitly requested by the user; deletion requires `--yes`.
4. Before a remote operation, confirm that an API key is available and that the Research gateway's `TQX_BASE_URL` (or build-time default) ends with `/pandaApi`. Never output API keys, persistent credentials, or environment variable values.
5. Keep the `factor_id` / `strategy_id` in the create response and the `analysis_id` / `run_id` in the run response. `SUBMITTED`, `PENDING`, `RUNNING`, `FAILED`, `CANCELLED`, `TIMEOUT` are not completed successfully; only `SUCCESS` of CLI corresponds to server `done`.
6. Use `--json` for machine-readable stdout; error JSON is written to stderr. List commands omit source code by default; use `--includeContent` to request it.

## Research Quality Boundary

- The CLI and SDK validate only client input, transport, and some source constraints. They cannot prove that a strategy is executable, that the data is correct, that it is free of look-ahead bias, or that a backtest is tradable.
- Historical research using `tqx_data` must follow point-in-time visibility, announcement dates, and market-parameter constraints; it is not a Python CLI or an authentication mechanism.
- For analysis or backtest conclusions, report the actual inputs, resource/run IDs, terminal states, service response data, time range, cost assumptions, and unvalidated risks. Do not present backtest results as investment advice.

## Remote file

When the user provides only a remote `SKILL.md`, continue by reading the raw reference files from the same revision. Keep the following paths stable:

- `references/commands.md`
- `references/strategy_templates.md`
- `references/stock_us_api.md`
- `references/stock_hk_api.md`
- `references/tqx_data_usage.md`
- `references/time_series_strategies.md`
- `references/cross_sectional_strategies.md`
- `references/tqx_data_quick_reference.md`
- `references/tqx_data_market_matrix.md`
- `references/sdk.md`
- `references/strategy-source.md`

If a reference required for the task cannot be read, stop and explain what is missing. Do not guess CLI parameters, SDK methods, Python runtime APIs, or data fields.
