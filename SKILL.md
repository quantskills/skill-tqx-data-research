---
name: skill-tqx-research
description: Use tqx_data with local parquet to generate and run Hong Kong and US factor analysis, time-series strategy backtests, and cross-sectional strategy backtests. Use when the prompt asks for factor construction, IC/IR/group/decay analysis, or strategy code generation and validation.
---

Use Python 3.12.

## Setup

- Create or activate a Python 3.12 environment.
- Install dependencies with `python -m pip install -r requirements.txt`.
- If your environment provides a `tqx_data` wheel, install it before running the skill.
- Copy `.env.example` to `.env` and set `PARQUET_ROOT_PATH`.

Read only these references when needed:

- `references/research_rules.md`
- `references/output_contract.md`
- `references/factor_codegen_assistant.md`
- `references/strategy_codegen_assistant.md`

Route by request:

- Factor analysis: market + factor definition + optional period/group/rebalance/direction
- Time-series strategy: market + instrument + entry/exit rule + optional settings
- Cross-sectional strategy: market + universe + filter/rank rule + optional settings

Hard rules:

- Use `tqx_data` plus local parquet only.
- Do not mix factor analysis with strategy backtests.
- Do not use future data.
- Do not hardcode one strategy type.
- If code or data fails, classify environment, data, then logic.
