---
name: skill-tqx-research
description: 使用 tqx_data 和本地 parquet 做港股和美股因子分析与策略回测。用于因子构建、IC/IR/分组/衰减分析，以及策略代码生成或验证。
---

## 安装

- 使用 Python 3.12。
- 执行 `python -m pip install -r requirements.txt`。
- 如果有 `tqx_data` 的 whl，先安装它。
- 复制 `.env.example` 为 `.env`，并设置 `PARQUET_ROOT_PATH`。

## 参考文件

按需读取：

- `references/research_rules.md`
- `references/output_contract.md`
- `references/factor_codegen_assistant.md`
- `references/strategy_codegen_assistant.md`

## 入口分类

- 因子分析：市场 + 因子定义 + 可选周期/分组/调仓/方向
- 时序回测：市场 + 标的 + 开平仓规则 + 可选参数
- 截面回测：市场 + 股票池 + 过滤/排序规则 + 可选参数

## 硬规则

- 只用 `tqx_data` + 本地 parquet。
- 不要把因子分析和策略回测混在一起。
- 不要使用未来数据。
- 如果代码或数据失败，先判断环境，再判断数据，最后判断逻辑。
