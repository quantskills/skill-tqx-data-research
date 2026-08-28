# skill-tqx-research

[简体中文](README.md) | **English**

> A Hong Kong and U.S. equity factor-analysis and strategy-backtesting Skill powered by `tqx_data` or local parquet data. It does not wrap a CLI.

## What It Does

- Factor analysis: coverage, quantile portfolios, IC, Rank IC, IR, and decay.
- Time-series backtests: moving average, RSI, breakout, momentum, and custom entry/exit rules.
- Cross-sectional backtests: universe filters, ranking, rebalancing, and portfolio performance.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python scripts/check_tqx_data_api.py
```

Set `PARQUET_ROOT_PATH` in `.env`. When using the SDK, install the matching `tqx_data` wheel and initialize authentication as required by that package.

## Data and Output

Input is a panel containing `date`, `symbol`, and market/factor columns. Each run should report the data range, sample count, signal rules, costs, returns, drawdown, and failure reasons.

## Boundaries

- Use only `tqx_data` and local parquet data; do not mix unapproved market sources.
- Keep factor analysis separate from strategy backtests, and use only information available at each decision time.
- See `references/` for contracts and `scripts/` for executable nodes.

## 🐼 PandaAI / QUANTSKILLS Community

<div align="center">
  <img src="https://raw.githubusercontent.com/quantskills/.github/main/profile/assets/pandaai-community-qr.jpg" alt="PandaAI community QR code" width="220">
  <br>
  <sub>Scan to join the PandaAI community for QUANTSKILLS Skills, agent workflows, and quantitative research practice.</sub>
</div>
