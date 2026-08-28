# 策略代码生成助手

当用户要做策略回测时使用。

## 输入

- 市场：港股或美股
- 股票池
- 策略规则
- 调仓频率
- 回测区间

## 输出

- 可执行的策略代码
- 交易信号
- 回测结果
- 总收益、年化收益、最大回撤、Sharpe、交易次数、最终净值

## 规则

- 新代码写入 `scripts/tests/<market>_<strategy>_<date>.py`，从 `scripts.research_nodes` 导入公共节点；不要导入外部回测框架。
- 加载技能根目录 `.env`；通过 `tqx_data` wheel 调用 `get_hk_daily` 或 `get_us_daily`，只取策略所需日线字段。
- 数据按 `symbol,date` 升序去重。时点 `t` 收盘后形成的信号最早在 `t+1` 生效，禁止当日信号吃到当日收益。
- 单标的均线任务调用 `run_backtest(df, short_window=..., long_window=...)`；其他时序或截面代码定义 `initialize(context)` 和 `handle_data(context,data)` 后调用 `run_code_backtest`。
- 用户未给均线参数时使用 5/20 日；未给区间时使用可用数据最近 2 年；未给资金时使用 1,000,000；这些默认值必须在结果中披露。
- 正式运行必须打印数据行数、日期范围、标的数、成本假设和结果；无交易时解释信号覆盖，而不是把风险指标写成 0。
