# 因子代码生成助手

当用户要做因子分析时使用。

## 输入

- 市场：港股或美股
- 股票池：单只股票、指数成分股或自定义 universe
- 因子定义
- 前向收益定义
- 回测区间

## 输出

- 可执行的因子代码
- 因子样本面板
- IC、Rank IC、ICIR、分组收益、衰减结果

## 规则

- 新代码写入 `scripts/tests/<market>_<factor>_<date>.py`，从 `scripts.research_nodes` 导入公共节点。
- 加载技能根目录 `.env`；通过 `tqx_data` wheel 调用 `get_hk_daily` 或 `get_us_daily`，至少取 `date,symbol,close` 及因子所需字段。
- 面板按 `symbol,date` 升序去重；因子在每只股票内计算，禁止使用未来数据。
- 生成 `factor` 和 `fwd_return_1d/3d/5d/10d/20d`；主预测周期与用户调仓周期一致。
- 调用 `factor_analysis_workflow(df, factor_col="factor", horizon=<周期>)`，打印结果而不是只保存代码。
- 截面 IC 每个日期至少 5 只有效股票；不足时返回样本诊断，不把单股票时序相关性称为 IC。
- 先用小股票池验证代码，再用目标股票池正式运行；正式结果必须披露市场、股票池、日期、样本量和数据来源。
