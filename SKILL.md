---
name: tqx-data-research
description: 使用 tqx_data 和本地 parquet 做港股、美股因子分析与策略回测，优先快速取数并输出可执行的研究代码。
---

# tqx research

## 目标

- 港股和美股投研
- 因子分析
- 策略回测
- 先快取数，再计算，再出结论；数据可用时必须直接运行分析，不因未指定次要参数而停摆

## 必须遵守

- 只做研究和回测，不做 CLI 封装，不做实时交易。
- 必须先安装 Python 3.12 对应的 `tqx_data` wheel；wheel 未安装或版本不符时，先报告安装错误，不得探测 Parquet。
- 不写账号、密码、token、私有路径到技能文件。
- `tqx_data` wheel 是本地 Parquet 的唯一读取适配器：必须先安装并成功导入 wheel，再加载 `.env`，最后调用 `tqx_data.get_hk_daily` 或 `get_us_daily`；不要用 pandas 自行猜目录结构。
- 只取完成任务所需字段，禁止无意义全量拉取。
- 数据不足时要明确说明，不允许伪造结果。
- 禁止先扫描全库或逐股票串行取数；优先一次面板查询、必要字段、限定日期和明确股票池。
- 取数后立即检查行数、日期、标的数和必需列；非空即可进入计算，不重复探测同一接口。
- 数据优先级固定为：用户明确提供的数据文件 -> 已有可复用面板 -> `tqx_data` SDK 读取 `.env` 指向的本地 Parquet。`tests/` 是代码目录，不等于数据源。

## 标准流程

1. 检查 Python 3.12 和 `tqx_data` wheel；通过后读取 `.env`，复用同一进程和 DataFrame。
2. 加载技能根目录 `.env`，确认 `PARQUET_ROOT_PATH` 非空；不要扫描磁盘或改写该变量。
3. 调用 `tqx_data.get_hk_daily` 或 `get_us_daily`，一次传入日期、股票池和最小字段；禁止绕过 SDK 直接读取未知 Parquet 表。
4. 根据用户需求新建唯一命名的代码到 `scripts/tests/`；复用 `scripts/research_nodes.py` 的入口并实际运行。旧示例只供理解，不复制其中的外部框架导入、账号或硬编码参数。
5. 执行 `run_factor_analysis` 或 `run_backtest`，输出指标、样本和数据来源。

## 取数原则

- 本地 parquet 必须通过已安装的 `tqx_data` wheel 访问。
- 能只取少量字段就不要取全表。
- 能缩小日期区间就不要拉长区间。
- 能先确认股票池就不要盲目遍历。
- 相同 `(market, symbols, start, end, fields)` 查询在本次任务中缓存；禁止为检查重复取数。
- 远程接口失败时指数退避最多 2 次；本地文件失败直接报告路径和权限，不循环等待。

## 输出要求

- 因子分析：IC、Rank IC、ICIR、分组收益、衰减、样本量、结论
- 策略回测：总收益、年化收益、最大回撤、Sharpe、交易次数、最终净值、结论

## 代码生成约束

- 因子分析复用 `factor_analysis_workflow`（内部调用 `run_factor_analysis`）。
- 常规均线策略复用 `run_backtest`；自定义时序/截面策略代码复用 `run_code_backtest`。
- 截面策略和时序策略都支持。
- 默认优先本地 parquet、wheel 和 tests。
- 遇到失败先检查字段、日期、市场、股票池和样本量。

## 按需读取参考文件

- 因子任务：读取 `references/factor_codegen_assistant.md`、`research_rules.md`、`output_contract.md`。
- 回测任务：读取 `references/strategy_codegen_assistant.md`、`research_rules.md`、`output_contract.md`。
- 用户参数不完整时读取 `references/prompt_template.md`；来源争议时读取 `source_boundary.md`。
- 只读取当前任务相关文件；生成代码写入 `scripts/tests/` 并实际执行。
- 失败必须返回阶段、原始异常、已检查项和下一步修复；数据为空不输出伪造指标。
