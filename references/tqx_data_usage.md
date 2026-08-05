> **说明（本仓库）**：本文档为 TQX TypeScript 工作区内 **港美股数据接口（tqx）** 的**唯一权威说明**，路径固定为 **`skills/tqx-research/references/tqx_data_usage.md`**。提示词、Agent 设计与运维说明**仅引用本路径**，**不**依赖其它仓库中的同名或类似文档。
>
> **维护**：接口说明由本仓库审阅与修订；变更时直接更新本文件并更新下方日期。
>
> **修订日期**：2026-04-21
>
> --- 


# 获取港美股数据的接口文档（tqx）

## 简介：

香港股票：

\- 代码格式：股票代码 + \`.HK\`后缀（如：0001.HK、0700.HK）

美国股票：

\- NASDAQ BASIC代码格式：股票代码 + \`.NB\`后缀（如：AAPL.NB、0013.NB）

## 一、行情数据

### 1. 获取港股日线数据

#### 1.1. 方法名：get_hk_daily

#### 1.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702"，与结束日期间不超过5年 | 必填 |
| end_date | str | 结束日期,eg:"20250702"，与开始日期间不超过5年 | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |

#### 1.3. 响应参数

| 字段         | 类型   | 描述                  |
|:-------------|:-------|:----------------------|
| date         | str    | 交易日                |
| symbol       | str    | 股票代码              |
| open         | str    | 开盘价                |
| high         | double | 最高价                |
| low          | double | 最低价                |
| close        | double | 理论收市价            |
| volume       | double | 成交量                |
| pre_close    | double | 前一日收盘价          |
| name         | str    | 股票名称              |
| trade_status | int    | 交易状态代码          |
| alt_close    | double | 调整收市价（同close） |
| acvol_uns    | double | 成交股数（同volume）  |
| bid          | double | 买盘价                |
| ask          | double | 卖盘价                |
| vwap         | double | 成交量加权平均价      |
| vwap_vol     | double | 计算VWAP的成交量      |
| opn_aucvol   | double | 开市竞价时段成交量    |
| opn_auc      | double | 开市竞价时段价格      |
| lmt_refpr2   | double | 限价参考价            |
| lolimit      | double | 价格下限              |
| uplimit      | double | 价格上限              |
| lolimit_2    | double | 二级价格下限          |
| uplimit_2    | double | 二级价格上限          |
| navalue      | double | 资产净值              |
| num_moves    | double | 成交笔数              |
| uplimit_3    | double | 三级价格上限          |
| lolimit_3    | double | 三级价格下限          |
| cls_aucvol   | double | 收市竞价时段成交量    |

#### 1.4. 使用示例

##### 1.4.1. 获取一定日期内所有港股的日线数据

```python
import tqx_data
result = tqx_data.get_hk_daily(
    symbol=[],
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
```

**响应示例**

```text
symbol date alt_close ... volume vwap vwap_vol
0 0001.HK 20250102 41.05 ... 4164402.0 40.9803 4158500.0
1 0001.HK 20250103 41.15 ... 2627730.0 41.1130 2612000.0
2 0001.HK 20250106 41.30 ... 3892729.0 41.2474 3670000.0
3 0001.HK 20250107 41.05 ... 4598793.0 41.0616 4507000.0
4 0001.HK 20250108 40.55 ... 5808409.0 40.6327 5409500.0
... ... ... ... ... ... ... ...
55259 9999.HK 20250122 154.80 ... 5641743.0 154.4849 5464600.0
55260 9999.HK 20250123 156.60 ... 6658593.0 157.1597 5601500.0
55261 9999.HK 20250124 158.40 ... 6535204.0 158.1166 5624400.0
55262 9999.HK 20250127 158.30 ... 4516011.0 158.6012 3997700.0
55263 9999.HK 20250128 161.00 ... 3836508.0 160.9322 3628800.0
```

##### 1.4.2. 获取一定日期内部分港股的日线数据并限制返回字段

```python
import tqx_data
result = tqx_data.get_hk_daily(
    symbol=["0001.HK","0002.HK","0003.HK"],
    start_date="20250101",
    end_date="20250110",
    fields=["vwap","bid","ask"]
)
print(result)
```

**响应示例**

```text
symbol date ask bid vwap
0 0001.HK 20250110 40.35 40.30 40.2948
1 0001.HK 20250109 40.55 40.50 40.5320
2 0001.HK 20250108 40.60 40.55 40.6327
3 0001.HK 20250107 41.05 41.00 41.0616
4 0001.HK 20250106 41.30 41.15 41.2474
5 0001.HK 20250103 41.15 41.10 41.1130
6 0001.HK 20250102 41.10 40.95 40.9803
7 0002.HK 20250110 63.70 63.65 63.7027
8 0002.HK 20250109 63.35 63.30 63.4421
9 0002.HK 20250108 63.50 63.45 63.5171
10 0002.HK 20250107 63.75 63.70 63.5882
11 0002.HK 20250106 64.25 64.20 64.2346
12 0002.HK 20250103 64.20 64.15 64.1212
13 0002.HK 20250102 64.20 64.15 64.2394
14 0003.HK 20250110 5.99 5.98 5.9910
15 0003.HK 20250109 5.98 5.97 5.9978
16 0003.HK 20250108 6.04 6.03 6.0329
17 0003.HK 20250107 6.07 6.05 6.0565
18 0003.HK 20250106 6.12 6.11 6.1256
19 0003.HK 20250103 6.13 6.10 6.1247
20 0003.HK 20250102 6.11 6.10 6.1050
```

### 2. 获取美股日线数据

#### 2.1. 方法名：get_us_daily

#### 2.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702"，与结束日期间不超过5年 | 必填 |
| end_date | str | 结束日期,eg:"20250702"，与开始日期间不超过5年 | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |

#### 2.3. 响应参数

| 字段         | 类型   | 描述             |
|:-------------|:-------|:-----------------|
| date         | str    | 交易日           |
| symbol       | str    | 股票代码         |
| open         | str    | 开盘价           |
| high         | double | 最高价           |
| low          | double | 最低价           |
| close        | double | 理论收市价       |
| volume       | double | 成交量           |
| pre_close    | double | 前一日收盘价     |
| name         | str    | 股票名称         |
| trade_status | int    | 交易状态代码     |
| blkcount     | double | 大宗交易笔数     |
| blkvolum     | double | 大宗交易量数     |
| bid          | double | 买盘价           |
| ask          | double | 卖盘价           |
| vwap         | double | 成交量加权平均价 |
| num_moves    | double | 成交笔数         |
| amount       | double | 成交额           |

#### 2.4. 使用示例

##### 2.4.1. 获取一定日期内所有美股的日线数据

```python
import tqx_data
result = tqx_data.get_us_daily(
    symbol=[],
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
```

**响应示例**

```text
symbol date amount ... trade_status volume vwap
0 A.NB 20260102 114271300.0 ... 0.0 1650714.0 136.8875
1 A.NB 20260105 246968868.0 ... 0.0 2981500.0 141.2442
2 A.NB 20260106 208702238.0 ... 0.0 2627715.0 147.0739
3 A.NB 20260107 169312459.0 ... 0.0 2279107.0 147.1272
4 A.NB 20260108 142722373.0 ... 0.0 1728989.0 146.5342
... ... ... ... ... ... ... ...
128770 ZYME.NB 20260126 20283763.0 ... 0.0 1017764.0 22.9013
128771 ZYME.NB 20260127 8745284.0 ... 0.0 472354.0 23.1272
128772 ZYME.NB 20260128 10779410.0 ... 0.0 652771.0 22.4135
128773 ZYME.NB 20260129 9794904.0 ... 0.0 625269.0 22.4472
128774 ZYME.NB 20260130 8614917.0 ... 0.0 560163.0 22.5178
```

##### 2.4.2. 获取一定日期内部分美股的日线数据并限制返回字段

```python
import tqx_data
result = tqx_data.get_hk_daily(
    symbol=["A.NB", "AAPL.NB"],
    start_date="20250101",
    end_date="20250131",
    fields=["volume", "close", "pre_close"]
)
print(result)
```

**响应示例**

```text
symbol date volume close pre_close
0 A.NB 20250102 953587.0 133.43 134.34
1 A.NB 20250103 1246919.0 135.69 133.43
2 A.NB 20250106 1047034.0 136.43 135.69
3 A.NB 20250107 1056693.0 137.41 136.43
4 A.NB 20250108 1684573.0 137.00 137.41
5 A.NB 20250110 1369875.0 137.47 137.00
6 A.NB 20250113 1561959.0 141.95 137.47
7 A.NB 20250114 2445434.0 143.43 141.95
8 A.NB 20250115 2328643.0 142.23 143.43
9 A.NB 20250116 1661474.0 144.72 142.23
10 A.NB 20250117 3210310.0 147.36 144.72
11 A.NB 20250121 2759636.0 152.57 147.36
12 A.NB 20250122 1730996.0 152.60 152.57
13 A.NB 20250123 1332235.0 152.45 152.60
14 A.NB 20250124 1844887.0 151.44 152.45
15 A.NB 20250127 2229590.0 150.96 151.44
16 A.NB 20250128 1791623.0 150.34 150.96
17 A.NB 20250129 1583243.0 147.09 150.34
18 A.NB 20250130 1496057.0 151.38 147.09
19 A.NB 20250131 1886605.0 151.52 151.38
20 AAPL.NB 20250102 55740731.0 243.85 250.42
21 AAPL.NB 20250103 40244114.0 243.36 243.85
22 AAPL.NB 20250106 45045571.0 245.00 243.36
23 AAPL.NB 20250107 40855960.0 242.21 245.00
24 AAPL.NB 20250108 37628940.0 242.70 242.21
25 AAPL.NB 20250110 61710856.0 236.85 242.70
26 AAPL.NB 20250113 49630725.0 234.40 236.85
27 AAPL.NB 20250114 39435294.0 233.28 234.40
28 AAPL.NB 20250115 39831969.0 237.87 233.28
29 AAPL.NB 20250116 71759052.0 228.26 237.87
30 AAPL.NB 20250117 68488301.0 229.98 228.26
31 AAPL.NB 20250121 98070429.0 222.64 229.98
32 AAPL.NB 20250122 64126500.0 223.83 222.64
33 AAPL.NB 20250123 60234760.0 223.66 223.83
34 AAPL.NB 20250124 54697907.0 222.78 223.66
35 AAPL.NB 20250127 94863418.0 229.86 222.78
36 AAPL.NB 20250128 75707569.0 238.26 229.86
37 AAPL.NB 20250129 45486100.0 239.36 238.26
38 AAPL.NB 20250130 55658279.0 237.59 239.36
39 AAPL.NB 20250131 101075128.0 236.00 237.59
```

### 3. 获取港股分钟线数据

#### 3.1. 方法名：get_hk_min

#### 3.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码, 当symbol为空时，开始与结束日期不能超过1个月 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段,如果不传,默认为 "open","high", "low","close","volume"和"amount" | 非必填 |
| time_zone | Optional\[tuple\] | 时间段过滤,格式为("HH:MM", "HH:MM")，例如("10:00", "23:00") | 非必填 |
| frequency | Optional\[str\] | 频率, 支持 "1m", "5m", "10m", "60m",默认为"1m" | 非必填 |

#### 3.3. 响应参数

| 字段       | 类型   | 描述                 |
|:-----------|:-------|:---------------------|
| date       | str    | 日期                 |
| datetime   | str    | 日期和时间           |
| minute     | str    | 时间（精确至分钟）   |
| symbol     | str    | 股票代码             |
| open       | double | 分钟开盘价           |
| high       | double | 分钟最高价           |
| low        | double | 分钟最低价           |
| close      | double | 分钟收盘价           |
| volume     | double | 分钟成交量           |
| amount     | double | 分钟成交金额         |
| num_trades | double | 分钟成交笔数         |
| high_yld   | double | 分钟最高收益率       |
| low_yld    | double | 分钟最低收益率       |
| open_yld   | double | 分钟开盘收益率       |
| yield      | double | 分钟收盘收益率       |
| vwap       | double | 分钟成交量加权平均价 |
| bid_high   | double | 买盘最高报价         |
| bid_low    | double | 买盘最低报价         |
| open_bid   | double | 开盘买盘价           |
| bid        | double | 收盘买盘价           |
| bid_nummov | double | 买盘变动次数         |
| ask_high   | double | 卖盘最高报价         |
| ask_low    | double | 卖盘最低报价         |
| open_ask   | double | 开盘卖盘价           |
| ask        | double | 收盘卖盘价           |
| ask_nummov | double | 卖盘变动次数         |
| mid_high   | double | 中间价最高值         |
| mid_low    | double | 中间价最低值         |
| mid_open   | double | 开盘中间价           |
| mid_price  | double | 收盘中间价           |

#### 3.4. 使用示例

##### 3.4.1. 获取单支股票的1分钟线数据并使用fields

```python
import tqx_data
result = tqx_data.get_hk_min(
    symbol="0700.HK",
    start_date="20260101",
    end_date="20260131",
    fields=["symbol", "date", "num_trades", "amount", "volume"],
    frequency="1m",
    time_zone=("10:00", "11:00")
)
print(result)
```

**响应示例**

```text
symbol date num_trades ... volume datetime minute
0 0700.HK 20260102 415.0 ... 109000.0 2026-01-02 10:00:00 100000
1 0700.HK 20260102 89.0 ... 26900.0 2026-01-02 10:01:00 100100
2 0700.HK 20260102 61.0 ... 17200.0 2026-01-02 10:02:00 100200
3 0700.HK 20260102 250.0 ... 97900.0 2026-01-02 10:03:00 100300
4 0700.HK 20260102 266.0 ... 182600.0 2026-01-02 10:04:00 100400
... ... ... ... ... ... ... ...
1276 0700.HK 20260130 37.0 ... 12700.0 2026-01-30 10:56:00 105600
1277 0700.HK 20260130 32.0 ... 6900.0 2026-01-30 10:57:00 105700
1278 0700.HK 20260130 96.0 ... 29800.0 2026-01-30 10:58:00 105800
1279 0700.HK 20260130 43.0 ... 10300.0 2026-01-30 10:59:00 105900
1280 0700.HK 20260130 140.0 ... 62900.0 2026-01-30 11:00:00 110000
```

##### 3.4.2. 获取多支股票的10分钟线数据

```python
import tqx_data
result = tqx_data.get_hk_min(
    symbol=["0700.HK","0003.HK"],
    start_date="20260101",
    end_date="20260131",
    fields=[],
    frequency="10m",
    time_zone=("10:00", "11:00")
)
print(result)
```

**响应示例**

```text
symbol date datetime ... close volume amount
0 0003.HK 20260102 2026-01-02 10:00:00 ... 7.07 305000.0 2156350.0
1 0003.HK 20260102 2026-01-02 10:10:00 ... 7.09 333000.0 2360970.0
2 0003.HK 20260102 2026-01-02 10:20:00 ... 7.09 463000.0 3282670.0
3 0003.HK 20260102 2026-01-02 10:30:00 ... 7.09 324000.0 2297160.0
4 0003.HK 20260102 2026-01-02 10:40:00 ... 7.09 368000.0 2609120.0
.. ... ... ... ... ... ... ...
289 0700.HK 20260130 2026-01-30 10:20:00 ... 613.00 392600.0 240663800.0
290 0700.HK 20260130 2026-01-30 10:30:00 ... 612.50 797000.0 488162500.0
291 0700.HK 20260130 2026-01-30 10:40:00 ... 613.50 397200.0 243682200.0
292 0700.HK 20260130 2026-01-30 10:50:00 ... 614.00 333900.0 205014600.0
293 0700.HK 20260130 2026-01-30 11:00:00 ... 614.50 296100.0 181953450.0
```

### 4. 获取美股分钟线数

#### 4.1. 方法名：get_us_min

#### 4.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702"此为美国纽约日期） | 必填 |
| end_date | str | 结束日期,eg:"20250702"（此为美国纽约日期） | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码, 当symbol为空时，开始与结束日期不能超过1个月 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段,如果不传,默认为 "open","high", "low","close","volume"和"amount" | 非必填 |
| time_zone | Optional\[tuple\] | 时间段过滤,格式为("HH:MM", "HH:MM")，例如("10:00", "23:00") | 非必填 |
| frequency | Optional\[str\] | 频率, 支持 "1m", "5m", "10m", "60m",默认为"1m" | 非必填 |

#### 4.3. 响应参数

| 字段        | 类型   | 描述                       |
|:------------|:-------|:---------------------------|
| us_date     | str    | 美国纽约日期               |
| us_datetime | str    | 美国纽约日期和时间         |
| us_minute   | str    | 美国纽约时间（精确至分钟） |
| cn_date     | str    | 中国日期                   |
| cn_datetime | str    | 中国日期和时间             |
| cn_minute   | str    | 中国时间（精确至分钟）     |
| symbol      | str    | 股票代码                   |
| open        | double | 分钟开盘价                 |
| high        | double | 分钟最高价                 |
| low         | double | 分钟最低价                 |
| close       | double | 分钟收盘价                 |
| volume      | double | 分钟成交量                 |
| amount      | double | 分钟成交金额               |
| num_trades  | double | 分钟成交笔数               |
| high_yld    | double | 分钟最高收益率             |
| low_yld     | double | 分钟最低收益率             |
| open_yld    | double | 分钟开盘收益率             |
| yield       | double | 分钟收盘收益率             |
| vwap        | double | 分钟成交量加权平均价       |
| bid_high    | double | 买盘最高报价               |
| bid_low     | double | 买盘最低报价               |
| open_bid    | double | 开盘买盘价                 |
| bid         | double | 收盘买盘价                 |
| bid_nummov  | double | 买盘变动次数               |
| ask_high    | double | 卖盘最高报价               |
| ask_low     | double | 卖盘最低报价               |
| open_ask    | double | 开盘卖盘价                 |
| ask         | double | 收盘卖盘价                 |
| ask_nummov  | double | 卖盘变动次数               |

#### 4.4. 使用示例

##### 4.4.1. 获取单支股票的1分钟线数据并使用fields

```python
import tqx_data
result = tqx_data.get_us_min(
    symbol="AAPL.NB",
    start_date="20260101",
    end_date="20260131",
    fields=["symbol", "date", "num_trades", "amount", "volume"],
    frequency="1m",
    time_zone=("10:00", "11:00")
)
print(result)
```

**响应示例**

```text
symbol us_date num_trades ... volume us_datetime us_minute
0 AAPL.NB 20260102 557.0 ... 96820.0 2026-01-02 10:00:00 100000
1 AAPL.NB 20260102 417.0 ... 80610.0 2026-01-02 10:01:00 100100
2 AAPL.NB 20260102 458.0 ... 88307.0 2026-01-02 10:02:00 100200
3 AAPL.NB 20260102 429.0 ... 84335.0 2026-01-02 10:03:00 100300
4 AAPL.NB 20260102 517.0 ... 93921.0 2026-01-02 10:04:00 100400
... ... ... ... ... ... ... ...
1215 AAPL.NB 20260130 327.0 ... 72088.0 2026-01-30 10:56:00 105600
1216 AAPL.NB 20260130 265.0 ... 62458.0 2026-01-30 10:57:00 105700
1217 AAPL.NB 20260130 507.0 ... 88342.0 2026-01-30 10:58:00 105800
1218 AAPL.NB 20260130 287.0 ... 51118.0 2026-01-30 10:59:00 105900
1219 AAPL.NB 20260130 504.0 ... 100017.0 2026-01-30 11:00:00 110000
```

##### 4.4.2. 获取多支股票的10分钟线数据

```python
import tqx_data
result = tqx_data.get_us_min(
    symbol=["AAPL.NB", "TSLE.NB"],
    start_date="20260101",
    end_date="20260131",
    fields=[],
    frequency="10m",
    time_zone=("10:00", "11:00")
)
print(result)
```

**响应示例**

```text
symbol us_date ... us_datetime us_minute
0 AAPL.NB 20260102 ... 2026-01-02 10:00:00 100000
1 AAPL.NB 20260102 ... 2026-01-02 10:10:00 101000
2 AAPL.NB 20260102 ... 2026-01-02 10:20:00 102000
3 AAPL.NB 20260102 ... 2026-01-02 10:30:00 103000
4 AAPL.NB 20260102 ... 2026-01-02 10:40:00 104000
.. ... ... ... ... ...
275 TSLA.NB 20260130 ... 2026-01-30 10:20:00 102000
276 TSLA.NB 20260130 ... 2026-01-30 10:30:00 103000
277 TSLA.NB 20260130 ... 2026-01-30 10:40:00 104000
278 TSLA.NB 20260130 ... 2026-01-30 10:50:00 105000
279 TSLA.NB 20260130 ... 2026-01-30 11:00:00 110000
```

5\. **获取港美股实时分钟线数据**

#### 5.1. 方法名：get_min_data

#### 5.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| count | int | 返回的分钟线条数(默认返回500条) | 非必填 |
| market | Optional\[str\] | 市场，默认为‘hk’, 可选‘hk’，‘nb’ | 非必填 |
| frequency | Optional\[str\] | 频率, 支持 "1m", "5m", "10m", "60m",默认为"1m" | 非必填 |

#### 5.3. 响应参数

| 字段   | 类型   | 描述         |
|:-------|:-------|:-------------|
| date   | str    | 日期和时间   |
| symbol | str    | 股票代码     |
| open   | double | 分钟开盘价   |
| high   | double | 分钟最高价   |
| low    | double | 分钟最低价   |
| close  | double | 分钟收盘价   |
| volume | double | 分钟成交量   |
| amount | double | 分钟成交金额 |

#### 5.4. 使用示例

##### 5.4.1. 获取2只股票的实时分钟线数据

```python
import tqx_data
result = tqx_data.get_min_data(
    symbol=["0700.HK","AAPL.NB"],
    count=500,
)
print(result)
```

**响应示例**

```text
symbol date open ... close volume amount
0 0700.HK 2026-03-17 13:10:00 561.00 ... 561.0000 14500.0 8.134500e+06
1 0700.HK 2026-03-17 13:11:00 561.00 ... 558.0000 82500.0 4.603500e+07
2 0700.HK 2026-03-17 13:12:00 558.00 ... 559.0000 39100.0 2.185690e+07
3 0700.HK 2026-03-17 13:13:00 559.50 ... 559.0000 20600.0 1.151540e+07
4 0700.HK 2026-03-17 13:14:00 559.00 ... 559.0000 9400.0 5.254600e+06
.. ... ... ... ... ... ... ...
995 AAPL.NB 2026-03-18 23:13:00 252.81 ... 252.7700 20841.0 5.267796e+06
996 AAPL.NB 2026-03-18 23:14:00 252.76 ... 252.5200 25664.0 6.482680e+06
997 AAPL.NB 2026-03-18 23:15:00 252.77 ... 252.4700 16429.0 4.148977e+06
998 AAPL.NB 2026-03-18 23:16:00 252.52 ... 252.3900 20952.0 5.289706e+06
999 AAPL.NB 2026-03-18 23:17:00 252.38 ... 252.5082 16155.0 4.078721e+06
```

##### 5.4.2. 获取全港股的实时分钟线数据

```python
import tqx_data
result = tqx_data.get_min_data(
    symbol=[],
    count=500,
    market="hk",
)
print(result)
```

**响应示例**

```text
symbol date open ... close volume amount
0 0856.HK 2026-03-17 13:10:00 8.250 ... 8.250 0.0 0.0
1 0856.HK 2026-03-17 13:11:00 8.240 ... 8.230 38000.0 312740.0
2 0856.HK 2026-03-17 13:12:00 8.220 ... 8.240 76000.0 626240.0
3 0856.HK 2026-03-17 13:13:00 8.230 ... 8.230 8000.0 65840.0
4 0856.HK 2026-03-17 13:14:00 8.230 ... 8.230 0.0 0.0
... ... ... ... ... ... ... ...
1365648 0855.HK 2026-03-18 15:55:00 5.335 ... 5.335 0.0 0.0
1365649 0855.HK 2026-03-18 15:56:00 5.340 ... 5.340 2000.0 10680.0
1365650 0855.HK 2026-03-18 15:57:00 5.340 ... 5.340 6000.0 32040.0
1365651 0855.HK 2026-03-18 15:58:00 5.340 ... 5.340 0.0 0.0
1365652 0855.HK 2026-03-18 15:59:00 5.340 ... 5.340 2000.0 10680.0
```

##### 5.4.3. 获取全美股的实时分钟线数据

```python
import tqx_data
result = tqx_data.get_min_data(
    symbol=[],
    count=500,
    market="nb",
)
print(result)
```

**响应示例**

```text
symbol date open ... close volume amount
0 BDTX.NB 2026-03-17 21:31:00 2.1900 ... 2.2100 3008.0 6647.68
1 BDTX.NB 2026-03-17 21:32:00 2.1931 ... 2.2050 2790.0 6151.95
2 BDTX.NB 2026-03-17 21:33:00 2.2050 ... 2.1622 950.0 2054.09
3 BDTX.NB 2026-03-17 21:34:00 2.1747 ... 2.2200 5590.0 12409.80
4 BDTX.NB 2026-03-17 21:35:00 2.2200 ... 2.2300 800.0 1784.00
... ... ... ... ... ... ... ...
3241075 WDH.NB 2026-03-18 23:20:00 1.7200 ... 1.7100 0.0 0.00
3241076 WDH.NB 2026-03-18 23:21:00 1.7200 ... 1.7100 0.0 0.00
3241077 WDH.NB 2026-03-18 23:22:00 1.7200 ... 1.7100 0.0 0.00
3241078 WDH.NB 2026-03-18 23:23:00 1.7200 ... 1.7100 0.0 0.00
3241079 WDH.NB 2026-03-18 23:24:00 1.7200 ... 1.7100 0.0 0.00
```

##### 5.4.4. 获取全港股的实时10分钟线数据

```python
import tqx_data
result = tqx_data.get_min_data(
    symbol=[],
    count=500,
    market="hk",
    frequency="10m",
)
print(result)
```

**响应示例**

```text
symbol date amount ... low open volume
0 0001.HK 2026-03-23 13:30:00 16617500.0 ... 57.70 57.9 287500.0
1 0001.HK 2026-03-23 13:40:00 6336000.0 ... 57.60 57.8 110000.0
2 0001.HK 2026-03-23 13:50:00 15596050.0 ... 57.50 57.6 271000.0
3 0001.HK 2026-03-23 14:00:00 18556350.0 ... 57.40 57.5 323000.0
4 0001.HK 2026-03-23 14:10:00 15868800.0 ... 57.45 57.5 275500.0
... ... ... ... ... ... ... ...
1356075 9999.HK 2026-04-16 13:30:00 13094930.0 ... 185.60 186.0 70500.0
1356076 9999.HK 2026-04-16 13:40:00 11862670.0 ... 185.40 185.7 63900.0
1356077 9999.HK 2026-04-16 13:50:00 17880440.0 ... 185.70 185.9 96200.0
1356078 9999.HK 2026-04-16 14:00:00 16669740.0 ... 185.70 186.0 89700.0
1356079 9999.HK 2026-04-16 14:10:00 24277210.0 ... 185.90 186.0 130500.0
```

##### 5.4.5. 获取全美股的实时5分钟线数据

```python
import tqx_data
result = tqx_data.get_min_data(
    symbol=[],
    count=500,
    market="nb",
    frequency="5m"
)
print(result)
```

**响应示例**

```text
symbol date open ... close volume amount
0 A.NB 2026-04-08 01:20:00 113.850 ... 113.9300 1200.0 1.367160e+05
1 A.NB 2026-04-08 01:25:00 113.955 ... 114.0200 1962.0 2.237072e+05
2 A.NB 2026-04-08 01:30:00 114.040 ... 114.0625 2655.0 3.028359e+05
3 A.NB 2026-04-08 01:35:00 114.200 ... 114.3600 2940.0 3.362184e+05
4 A.NB 2026-04-08 01:40:00 114.360 ... 114.2700 6615.0 7.558960e+05
... ... ... ... ... ... ... ...
3229329 ZYME.NB 2026-04-16 03:35:00 27.820 ... 27.8400 966.0 2.689344e+04
3229330 ZYME.NB 2026-04-16 03:40:00 27.820 ... 27.8500 4555.0 1.268568e+05
3229331 ZYME.NB 2026-04-16 03:45:00 27.850 ... 27.8900 4377.0 1.220745e+05
3229332 ZYME.NB 2026-04-16 03:50:00 27.890 ... 27.7400 10878.0 3.017557e+05
3229333 ZYME.NB 2026-04-16 03:55:00 27.730 ... 27.7500 70975.0 1.969556e+06
```

**6.获取港美股最新tick数据**

#### 6.1. 方法名：get_tick_data

#### 6.2. 入参

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 |
| market | Optional\[str\] | 市场，默认为‘hk’, 可选‘hk’，‘nb’ |

#### 6.3. 响应参数

| 字段         | 类型   | 描述           |
|:-------------|:-------|:---------------|
| date         | str    | 日期和时间     |
| symbol       | str    | 股票代码       |
| last_price   | double | 最新价         |
| price_change | double | 价格变化       |
| percentage   | double | 价格百分比变化 |

#### 6.4. 使用示例

##### 6.4.1. 获取1只股票的最新tick数据

```python
import tqx_data
result = tqx_data.get_tick_data(
    symbol=["0700.HK"],
    market="hk",
)
print(result)
```

**响应示例**

```text
symbol last_price date
0 0700.HK 516.0 2026-03-24 15:59:59.000
```

##### 6.4.2. 获取全港股的最新tick数据

```python
import tqx_data
result = tqx_data.get_tick_data(
    market="hk",
)
print(result)
```

**响应示例**

```text
symbol date last_price
0 0001.HK 2026-03-24 15:59:56.000 58.850
1 0002.HK 2026-03-24 15:59:55.000 72.350
2 0003.HK 2026-03-24 15:59:54.000 7.130
3 0004.HK 2026-03-24 15:59:51.000 23.040
4 0005.HK 2026-03-24 15:59:57.000 123.500
... ... ... ...
2731 9993.HK 2026-03-24 15:59:48.000 1.370
2732 9995.HK 2026-03-24 15:59:55.000 91.400
2733 9996.HK 2026-03-24 15:59:18.000 5.600
2734 9998.HK 2026-03-24 15:58:54.000 0.475
2735 9999.HK 2026-03-24 15:59:53.000 177.300
```

##### 6.4.3. 获取全美股的最新tick数据

```python
import tqx_data
result = tqx_data.get_tick_data(
    market="nb",
)
print(result)
```

**响应示例**

```text
symbol date last_price
0 A.NB 2026-03-25 03:59:49.344 114.1400
1 AA.NB 2026-03-25 03:59:51.123 56.6900
2 AACBR.NB 2026-03-25 02:24:16.798 0.3250
3 AACBU.NB 2026-03-24 03:59:00 10.5300
4 AACG.NB 2026-03-25 03:59:29.319 1.0100
... ... ... ...
6470 ZWZZT.NB 2026-03-25 03:59:00 10.0100
6471 ZXIET.NB 2026-03-25 03:59:00 100.0000
6472 ZXZZT.NB 2026-03-25 03:59:00 12.1000
6473 ZYBT.NB 2026-03-25 03:59:48.032 0.8404
6474 ZYME.NB 2026-03-25 03:59:50.931 23.6150
```

**7.指标计算接口**

#### 7.1. 方法名：calculate_indicators

#### 7.2. 入参


| 字段 | 类型 | 描述 |
|:---|:---|:---|
| market_data | Dict[str, List[Dict]] | 按股票代码分组的实时行情数据字典 |
| indicator_params | Dict[str, Dict] | 指标参数字典,，格式：{"rsi": {"period": 7, "limit": 30}, "macd": {"period": 26, "limit": 30}} - period: 周期参数（MACD的period表示慢线周期，必需） - limit: 最多返回的个数限制（可选，默认等于period） 支持的指标：rsi, macd, atr, ema, boll |


#### 7.3 响应参数

| 字段           | 类型   | 描述              |
|:---------------|:-------|:------------------|
| symbol         | str    | 股票代码          |
| rsi\_{period}  | Double | RSI 指标结果列表  |
| macd\_{period} | Double | MACD 指标结果列表 |
| atr\_{period}  | Double | ATR 指标结果列表  |
| ema\_{period}  | Double | EMA 指标结果列表  |
| boll\_{period} | Double | BOLL 指标结果列表 |

#### 7.4 使用示例

```python
import tqx_data
market_data = tqx_data.get_live_market_data(
    symbols=["0005.HK"],
    count=60,
)
result = tqx_data.calculate_indicators(
    market_data = market_data,
    indicator_params={
        "rsi": {"period": 7, "limit": 5},
        "macd": {"period": 26, "limit": 5},
    },
)
print(result)
```

**响应示例**

```json
{'0005.HK': {'rsi_7': [
51.38758258818659,
51.38758258818659,
51.38758258818659,
59.3371266618274,
59.3371266618274
], 'macd_26': [
0.07868518510328215,
0.0743897749055975,
0.07015702290236447,
0.07528413372823195,
0.07831080401081181
]
}
}
```

## 二、市场参考数据

### 1. 获取股票的详细信息

#### 1.1. 方法名：get_stock_detail

#### 1.2. 入参

| **字段** | **类型** | **描述** | **是否必填** |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | Optional\[str\] | 市场，支持hk,us，默认hk | 非必填 |
| status | Optional\[int\] | 是否在市，1 -在市，0 -退市，-1 -未知 | 非必填 |

#### 1.3. 响应参数

##### 1.3.1. hk相应参数

| 字段                    | 类型 | 描述             |
|:------------------------|:-----|:-----------------|
| symbol                  | str  | 股票代码         |
| name                    | str  | 股票名称         |
| cn_name                 | str  | 中文名           |
| local_name              | str  | 本地组织名称     |
| status                  | int  | 股票状态         |
| isin_code               | str  | 国际证券识别编码 |
| abbrev_symbol           | str  | 股票的名称缩写   |
| min_order_amount        | str  | 一手对应多少股   |
| trading_code            | str  | 交易代码         |
| asset_state             | str  | 交易状态         |
| rcs_asset_category_name | str  | 资产类别名称     |
| business_sector         | str  | 业务领域名称     |
| economic_sector         | str  | 经济领域名称     |
| industry_group          | str  | 行业组名称       |
| incorp_date             | str  | 公司成立日期     |
| office_address          | str  | 公司总部地址     |
| office_city             | str  | 总部城市         |
| office_country          | str  | 总部所在国家     |
| office_region           | str  | 总部所在地区     |
| postal_code             | str  | 总部邮政编码     |
| website                 | str  | 公司网站         |
| listed_date             | str  | 上市日期         |

##### 1.3.2. us相应参数

| 字段                    | 类型 | 描述             |
|:------------------------|:-----|:-----------------|
| symbol                  | str  | 股票代码         |
| original_symbol         | str  | 原始股票代码     |
| name                    | str  | 股票名称         |
| listed_date             | str  | 上市日期         |
| local_name              | str  | 本地组织名称     |
| exchange_name           | str  | 交易所名称       |
| status                  | int  | 股票状态         |
| isin_code               | str  | 国际证券识别编码 |
| abbrev_symbol           | str  | 股票的名称缩写   |
| min_order_amount        | str  | 一手对应多少股   |
| trading_code            | str  | 交易代码         |
| asset_state             | str  | 交易状态         |
| rcs_asset_category_name | str  | 资产类别名称     |
| business_sector         | str  | 业务领域名称     |
| economic_sector         | str  | 经济领域名称     |
| industry_group          | str  | 行业组名称       |
| incorp_date             | str  | 公司成立日期     |
| office_address          | str  | 公司总部地址     |
| office_city             | str  | 总部城市         |
| office_country          | str  | 总部所在国家     |
| office_region           | str  | 总部所在地区     |
| postal_code             | str  | 总部邮政编码     |
| website                 | str  | 公司网站         |

#### 1.4. 使用示例

##### 1.4.1. 港股

```python
import tqx_data
result = tqx_data.get_stock_detail(
    symbol=["0001.HK","0002.HK","0003.HK"],
    market="hk",
    fields=[""],
    status=None
)
print(result)
```

**响应示例**

```text
symbol abbrev_symbol ... status trading_code
0 0001.HK CKHUH ... 1 0001
1 0002.HK CLPHL ... 1 0002
2 0003.HK HKCNG ... 1 0003|864603
```

##### 1.4.2. 美股

```python
import tqx_data
result = tqx_data.get_stock_detail(
    symbol=["0013.NB", "005490.NB", "ZYXIQ.NB"],
    market="us",
    fields=[""],
    status=None
)
print(result)
```

**响应示例**

```text
symbol abbrev_symbol ... status trading_code
0 0013.NB None ... 1 None
1 005490.NB POSCO ... 1 893094
2 ZYXIQ.NB ZYXIQ ... 0 None
```

##### 1.4.3. 获取全部港股股票代码

```python
import tqx_data
result = tqx_data.get_stock_detail(
    symbol="",
    fields=["symbol"],
    market="hk",
    status=None
)
print(result)
```

**响应示例**

```text
symbol
0 0001.HK
1 0002.HK
2 0003.HK
3 0004.HK
4 0005.HK
... ...
3224 SPFH.HK
3225 SUFH.HK
3226 TEXH.HK
3227 TTFH.HK
3228 UNTX.HK
```

##### 1.4.4. 获取全部美股股票代码

```python
import tqx_data
result = tqx_data.get_stock_detail(
    symbol="",
    fields=["symbol"],
    market="us",
    status=None
)
print(result)
```

**响应示例**

```text
symbol
0 0013.NB
1 005490.NB
2 015760.NB
3 017670.NB
4 030200.NB
... ...
7792 ZXZZT.NB
7793 ZYBT.NB
7794 ZYME.NB
7795 ZYRX.NB
7796 ZYXIQ.NB
```

### 2. 获取交易日历

#### 2.1. 方法名：get_trading_calendar

#### 2.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | Optional\[str\] | 开始日期，格式为 YYYYMMDD | 非必填 |
| end_date | Optional\[str\] | 结束日期，格式为 YYYYMMDD | 非必填 |
| market | Optional\[str\] | 交易所代码，默认为 "hk"，目前支持"hk"和"us" | 非必填 |
| is_trading_day | Optional\[int\] | 是否为交易日，1=交易日，0=非交易日，None=全部 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 需要返回的字段列表 | 非必填 |

#### 2.3. 响应参数

| 字段            | 类型 | 描述                                     |
|:----------------|:-----|:-----------------------------------------|
| nature_date     | int  | 日期，格式为YYYYMMDD                     |
| exchange        | str  | 交易所代码                               |
| is_trade        | int  | 是否为交易日，1表示交易日，0表示非交易日 |
| pretrade_date   | str  | 当前日期前一个交易日                     |
| next_trade_date | str  | 当前日期后一个交易日                     |

#### 2.4. 使用示例

##### 2.4.1. 获取一段时间内港股交易日历

```python
import tqx_data
result = tqx_data.get_trading_calendar(
    start_date="20250101",
    end_date="20250115",
    market="hk",
    is_trading_day=None,
    fields=[]
)
print(result)
```

**响应示例**

```text
nature_date exchange is_trade next_trade_date pretrade_date
0 20250101 HK 0 20250102 20241230
1 20250102 HK 1 20250103 20241231
2 20250103 HK 1 20250106 20250102
3 20250104 HK 0 20250106 20250102
4 20250105 HK 0 20250106 20250102
5 20250106 HK 1 20250107 20250103
6 20250107 HK 1 20250108 20250106
7 20250108 HK 1 20250109 20250107
8 20250109 HK 1 20250110 20250108
9 20250110 HK 1 20250113 20250109
10 20250111 HK 0 20250113 20250109
11 20250112 HK 0 20250113 20250109
12 20250113 HK 1 20250114 20250110
13 20250114 HK 1 20250115 20250113
14 20250115 HK 1 20250116 20250114
```

##### 2.4.2. 获取一段时间内美股非交易日且使用fields

```python
import tqx_data
result = tqx_data.get_trading_calendar(
    start_date="20241215",
    end_date="20250110",
    market="us",
    is_trading_day=0,
    fields=["nature_date", "is_trade", "next_trade_date", "pretrade_date"]
)
print(result)
```

**响应示例**

```text
nature_date is_trade next_trade_date pretrade_date
0 20241215 0 20241216 20241212
1 20241221 0 20241223 20241219
2 20241222 0 20241223 20241219
3 20241225 0 20241226 20241223
4 20241228 0 20241230 20241226
5 20241229 0 20241230 20241226
6 20250101 0 20250102 20241230
7 20250104 0 20250106 20250102
8 20250105 0 20250106 20250102
9 20250109 0 20250110 20250108
```

##### 2.4.3. 获取一段时间内港股交易日

```python
import tqx_data
result = tqx_data.get_trading_calendar(
    start_date="20250101",
    end_date="20250120",
    market="hk",
    is_trading_day=1,
    fields=[]
)
print(result)
```

**响应示例**

```text
nature_date exchange is_trade next_trade_date pretrade_date
0 20250102 HK 1 20250103 20241231
1 20250103 HK 1 20250106 20250102
2 20250106 HK 1 20250107 20250103
3 20250107 HK 1 20250108 20250106
4 20250108 HK 1 20250109 20250107
5 20250109 HK 1 20250110 20250108
6 20250110 HK 1 20250113 20250109
7 20250113 HK 1 20250114 20250110
8 20250114 HK 1 20250115 20250113
9 20250115 HK 1 20250116 20250114
10 20250116 HK 1 20250117 20250115
11 20250117 HK 1 20250120 20250116
12 20250120 HK 1 20250121 20250117
```

### 3. 获取股票分红相关的事件

#### 3.1. 方法名：get_event_devidend

#### 3.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 3.3. 响应参数

| 字段         | 类型 | 描述                             |
|:-------------|:-----|:---------------------------------|
| publish_date | str  | 事件公告发布日期（日期筛选依据） |
| symbol       | str  | 股票代码                         |
| excute_date  | str  | 事件执行日期                     |
| event_type   | str  | 事件类型                         |
| number       | str  | 每股金额                         |
| currency     | str  | 交易币种                         |
| event        | str  | 事件                             |

#### 3.4. 使用示例

##### 3.4.1. 获取一定时间内某个港股分红相关的事件

```python
import tqx_data
result = tqx_data.get_event_devidend(
    market='hk',
    symbol="9999.HK",
    fields=[],
    start_date="20250101",
    end_date="20260501",
)
print(result)
```

**响应示例**

```text
symbol publish_date ... currency event
0 9999.HK 20250305 ... USD 9999.HK Final Cash Dividend of gross USD 0.244...
1 9999.HK 20250529 ... USD 9999.HK Interim Cash Dividend of gross USD 0.1...
2 9999.HK 20250827 ... USD 9999.HK Interim Cash Dividend of gross USD 0.1...
3 9999.HK 20251204 ... USD 9999.HK Interim Cash Dividend of gross USD 0.1...
4 9999.HK 20260313 ... USD 9999.HK Final Cash Dividend of gross USD 0.232...
```

##### 3.4.2. 获取一定时间内全部美股分红相关的事件

```python
import tqx_data
result = tqx_data.get_event_devidend(
    market='us',
    symbol="",
    fields=[],
    start_date="20250101",
    end_date="20260401",
)
print(result)
```

**响应示例**

```text
symbol publish_date ... currency event
0 A.NB 20250401 ... USD A.NB Interim Cash Dividend of gross USD 0.248 ...
1 A.NB 20250701 ... USD A.NB Interim Cash Dividend of gross USD 0.248 ...
2 A.NB 20250930 ... USD A.NB Final Cash Dividend of gross USD 0.248 pa...
3 A.NB 20260106 ... USD A.NB Interim Cash Dividend of gross USD 0.255 ...
4 A.NB 20260331 ... USD A.NB Interim Cash Dividend of gross USD 0.255 ...
... ... ... ... ... ...
14433 ZWS.NB 20250220 ... USD ZWS.NB Interim Cash Dividend of gross USD 0.09...
14434 ZWS.NB 20250520 ... USD ZWS.NB Interim Cash Dividend of gross USD 0.09...
14435 ZWS.NB 20250820 ... USD ZWS.NB Interim Cash Dividend of gross USD 0.09...
14436 ZWS.NB 20251120 ... USD ZWS.NB Final Cash Dividend of gross USD 0.11 p...
14437 ZWS.NB 20260220 ... USD ZWS.NB Interim Cash Dividend of gross USD 0.11...
```

### 4. 获取市场活动相关的事件

#### 4.1. 方法名：get_event_capital_market

#### 4.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 4.3. 响应参数

| 字段           | 类型 | 描述                                       |
|:---------------|:-----|:-------------------------------------------|
| info_date      | str  | 公告日期（日期筛选依据）                   |
| symbol         | str  | 股票代码                                   |
| start_date     | str  | 事件执行日期                               |
| end_date       | str  | 事件完成日期                               |
| is_estimated   | int  | 事件是否被预计（0表示否，1表示是）         |
| fiscal_quarter | str  | 财年季度（若事件不涉及财年季度则此列为空） |
| event          | str  | 事件                                       |

#### 4.4. 使用示例

##### 4.4.1. 获取一定时间内全部港股市场活动相关的事件

```python
import tqx_data
result = tqx_data.get_event_capital_market(
    market='hk',
    symbol="",
    fields=[],
    start_date="20250101",
    end_date="20260401",
)
print(result)
```

**响应示例**

```text
symbol start_date ... event_type fiscal_quarter
0 0020.HK 20260329 ... IpoLockupExpirations None
1 0092.HK 20260203 ... SecondaryPricings None
2 0139.HK 20260122 ... SecondaryFilings None
3 0167.HK 20260213 ... SecondaryFilings None
4 0167.HK 20260312 ... SecondaryPricings None
.. ... ... ... ... ...
278 9887.HK 20260121 ... IpoLockupExpirations None
279 9958.HK 20260204 ... SecondaryPricings None
280 9973.HK 20260324 ... IpoLockupExpirations None
281 9980.HK 20260203 ... SecondaryPricings None
282 9981.HK 20260213 ... SecondaryPricings None
```

### 5. 获取公司会议相关的事件

#### 5.1. 方法名：get_event_corporate_actions

#### 5.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 5.3. 响应参数

| 字段           | 类型 | 描述                                       |
|:---------------|:-----|:-------------------------------------------|
| info_date      | str  | 公告日期（日期筛选依据）                   |
| symbol         | str  | 股票代码                                   |
| start_date     | str  | 事件执行日期                               |
| end_date       | str  | 事件完成日期                               |
| is_estimated   | int  | 事件是否被预计（0表示否，1表示是）         |
| fiscal_quarter | str  | 财年季度（若事件不涉及财年季度则此列为空） |
| event          | str  | 事件                                       |

#### 5.4. 使用示例

##### 5.4.1. 获取一定时间内全部港股公司会议相关的事件

```python
import tqx_data
result = tqx_data.get_event_corporate_actions(
    market='hk',
    symbol="",
    fields=[],
    start_date="20250101",
    end_date="20260401",
)
print(result)
```

**响应示例**

```text
symbol start_date ... event_type fiscal_quarter
0 0001.HK 20250522 ... ShareholderAndAnnualMeetings None
1 0002.HK 20250509 ... ShareholderAndAnnualMeetings None
2 0002.HK 20220506 ... ShareholderAndAnnualMeetings None
3 0003.HK 20250604 ... ShareholderAndAnnualMeetings None
4 0004.HK 20250513 ... ShareholderAndAnnualMeetings None
... ... ... ... ... ...
5198 9997.HK 20250523 ... ShareholderAndAnnualMeetings None
5199 9997.HK 20251110 ... ShareholderAndAnnualMeetings None
5200 9997.HK 20251110 ... ExtraordinaryShareholdersMeeting None
5201 9998.HK 20251218 ... ShareholderAndAnnualMeetings None
5202 9999.HK 20250625 ... ShareholderAndAnnualMeetings None
```

### 6. 获取财务披露相关的事件

#### 6.1. 方法名：get_event_fina_disclosure

#### 6.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 6.3. 响应参数

| 字段           | 类型 | 描述                                       |
|:---------------|:-----|:-------------------------------------------|
| info_date      | str  | 公告日期（日期筛选依据）                   |
| symbol         | str  | 股票代码                                   |
| start_date     | str  | 事件执行日期                               |
| end_date       | str  | 事件完成日期                               |
| is_estimated   | int  | 事件是否被预计（0表示否，1表示是）         |
| fiscal_quarter | str  | 财年季度（若事件不涉及财年季度则此列为空） |
| event          | str  | 事件                                       |

#### 6.4. 使用示例

##### 6.4.1. 获取一定时间内全部港股财务批量相关的事件

```python
import tqx_data
result = tqx_data.get_event_fina_disclosure(
    market='hk',
    symbol="",
    fields=[],
    start_date="20250101",
    end_date="20260401",
)
print(result)
```

**响应示例**

```text
symbol start_date ... event_type fiscal_quarter
0 0001.HK 20250320 ... EarningsReleases 2024q4
1 0001.HK 20250814 ... EarningsReleases 2025q2
2 0001.HK 20250814 ... EarningsPresentation 2025q2
3 0001.HK 20250320 ... EarningsPresentation 2024q4
4 0001.HK 20260319 ... EarningsReleases 2025q4
... ... ... ... ... ...
9247 9999.HK 20050803 ... EarningsCallsAndPresentations None
9248 9999.HK 20051108 ... EarningsCallsAndPresentations None
9249 9999.HK 20031029 ... EarningsCallsAndPresentations None
9250 9999.HK 20260211 ... EarningsReleases 2025q4
9251 9999.HK 20260211 ... EarningsCallsAndPresentations 2025q4
```

### 7. 获取投资者关系活动相关的事件

#### 7.1. 方法名：get_event_investor_relation_activities

#### 7.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 7.3. 响应参数

| 字段           | 类型 | 描述                                       |
|:---------------|:-----|:-------------------------------------------|
| info_date      | str  | 公告日期（日期筛选依据）                   |
| symbol         | str  | 股票代码                                   |
| start_date     | str  | 事件执行日期                               |
| end_date       | str  | 事件完成日期                               |
| is_estimated   | int  | 事件是否被预计（0表示否，1表示是）         |
| fiscal_quarter | str  | 财年季度（若事件不涉及财年季度则此列为空） |
| event          | str  | 事件                                       |

#### 7.4. 使用示例

##### 7.4.1. 获取一定时间内全部港股财务批量相关的事件

```python
import tqx_data
result = tqx_data.get_event_investor_relation_activities(
    market='hk',
    symbol="",
    fields=[],
    start_date="20250101",
    end_date="20260401",
)
print(result)
```

**响应示例**

```text
symbol start_date ... event_type fiscal_quarter
0 0002.HK 20250225 ... CorporateInvestorRoadshow None
1 0002.HK 20250227 ... CorporateInvestorRoadshow None
2 0002.HK 20250303 ... CorporateInvestorRoadshow None
3 0002.HK 20250114 ... ConferencePresentations None
4 0002.HK 20250326 ... ConferencePresentations None
.. ... ... ... ... ...
741 9987.HK 20251126 ... ConferencePresentations None
742 9987.HK 20251127 ... ConferencePresentations None
743 9987.HK 20251117 ... CorporateAnalystMeetings None
744 9987.HK 20251113 ... ConferencePresentations None
745 9988.HK 20250917 ... ConferencePresentations None
```

### 8. 获取公司投资者集中度

#### 8.1. 方法名：get_company_concentration

#### 8.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 8.3. 响应参数

| 字段                       | 类型   | 描述                     |
|:---------------------------|:-------|:-------------------------|
| symbol                     | str    | 股票代码                 |
| currency                   | str    | 交易币种                 |
| total_investors            | int    | 总投资者数               |
| investor_outstanding_ratio | double | 投资者持有占总流通股比例 |
| total_sharehold            | double | 总持股                   |
| total_holdings_value       | double | 总持股市值               |

#### 8.4. 使用示例

##### 8.4.1. 获取全部港股公司投资者集中度数据

```python
import tqx_data
result = tqx_data.get_company_concentration(
    market='hk',
    symbol="",
    fields=[],
)
print(result)
```

**响应示例**

```text
symbol currency ... total_sharehold total_holdings_value
0 0001.HK HKD ... 2.042810e+09 1.294356e+10
1 0002.HK HKD ... 1.026492e+09 9.308294e+09
2 0003.HK HKD ... 9.963026e+09 8.726823e+09
3 0004.HK HKD ... 2.243385e+09 6.330515e+09
4 0005.HK USD ... 8.827207e+09 1.567821e+11
... ... ... ... ... ...
2707 9995.HK CNY ... 7.764612e+07 7.876332e+08
2708 9996.HK CNY ... 3.606810e+08 2.498107e+08
2709 9997.HK CNY ... 2.440423e+08 2.016341e+08
2710 9998.HK SGD ... 6.000000e+08 1.467572e+07
2711 9999.HK CNY ... 2.200467e+09 4.651509e+10
```

### 9. 获取公司前20投资者集中度

#### 9.1. 方法名：get_company_top_concentration

#### 9.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 9.3. 响应参数

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | str | 股票代码 |
| currency | str | 交易币种 |
| top_investors_num | int | 前n个投资者数（对于此接口通常为20，不足20个投资者的会返回小于20） |
| investor_outstanding_ratio | double | 投资者持有占总流通股比例 |
| sharehold | double | 前n个投资者总持股 |
| holdings_value | double | 前n个投资者总持股市值 |

#### 9.4. 使用示例

##### 9.4.1. 获取全部港股公司投资者集中度数据

```python
import tqx_data
result = tqx_data.get_company_top_concentration(
    market='hk',
    symbol="",
    fields=[],
)
print(result)
```

**响应示例**

```text
symbol currency ... sharehold holdings_value
0 0001.HK HKD ... 1.726426e+09 1.058605e+10
1 0002.HK HKD ... 9.395121e+08 8.506187e+09
2 0003.HK HKD ... 9.405393e+09 8.208555e+09
3 0004.HK HKD ... 2.212428e+09 6.234463e+09
4 0005.HK USD ... 6.809123e+09 1.225648e+11
... ... ... ... ... ...
2707 9995.HK CNY ... 7.010446e+07 7.125567e+08
2708 9996.HK CNY ... 3.605222e+08 2.496836e+08
2709 9997.HK CNY ... 2.433189e+08 2.009243e+08
2710 9998.HK SGD ... 6.000000e+08 1.467572e+07
2711 9999.HK CNY ... 1.847153e+09 3.801278e+10
```

### 10. 获取公司投资者排行

#### 10.1. 方法名：get_company_investor

#### 10.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |
| max_rank | Optional\[int\] | 最大返回排名（小于等于20的正整数），默认为空返回前20名 | 非必填 |

#### 10.3. 响应参数

| 字段                       | 类型   | 描述                       |
|:---------------------------|:-------|:---------------------------|
| symbol                     | str    | 股票代码                   |
| investor_name              | str    | 投资者名称                 |
| investor_type              | str    | 投资者类型                 |
| investor_outstanding_ratio | double | 投资者持有占总流通股比例   |
| sharehold                  | double | 投资者持股                 |
| sharehold_change           | double | 投资者持股较上一次报告变化 |
| info_date                  | str    | 此次报告日期               |
| turnover_rating            | str    | 换手率评级                 |
| currency                   | str    | 交易币种                   |
| rank                       | int    | 排行                       |

#### 10.4. 使用示例

##### 10.4.1. 获取全部港股公司前10投资者数据

```python
import tqx_data
result = tqx_data.get_company_investor(
    market='hk',
    symbol="",
    fields=[],
    max_rank=10
)
print(result)
```

**响应示例**

```text
symbol investor_name ... rank currency
0 0001.HK Li (Ka Shing) ... 1 HKD
1 0001.HK BlackRock Institutional Trust Company, N.A. ... 2 HKD
2 0001.HK The Vanguard Group, Inc. ... 3 HKD
3 0001.HK Norges Bank Investment Management (NBIM) ... 4 HKD
4 0001.HK Hang Seng Investment Management Ltd. ... 5 HKD
... ... ... ... ... ...
18252 9999.HK CSOP Asset Management Limited ... 6 CNY
18253 9999.HK China Asset Management Co., Ltd. ... 7 CNY
18254 9999.HK BlackRock Advisors (UK) Limited ... 8 CNY
18255 9999.HK Hang Seng Investment Management Ltd. ... 9 CNY
18256 9999.HK Norges Bank Investment Management (NBIM) ... 10 CNY
```

### 11. 获取公司内部人交易活动

#### 11.1. 方法名：get_company_insider_transaction

#### 11.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702"（此接口查询消息日期） | 必填 |
| end_date | str | 结束日期,eg:"20250702"（此接口查询消息日期） | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 11.3. 响应参数

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | str | 股票代码 |
| investor_name | str | 投资者名称 |
| investor_type | str | 投资者类型 |
| info_date | str | 消息日期（日期筛选依据） |
| insider_role | str | 内部人身份 |
| is_main_role | int | 是否为主要人物（若某次内部交易涉及多个内部人，则此字段为1的为主要人物） |
| insider_active_date | str | 成为内部人日期 |
| insider_inactive_date | str | 不再视为内部人日期 |
| transaction_date | str | 交易发生日期 |
| transaction_type | str | 交易类型 |
| acquisition_type | str | 处置行为类型 |
| adjusted_trade_shares | double | 调整后交易股数 |
| reported_trade_shares | double | 申报交易股数 |
| trade_outstanding_ratio | double | 交易股数占总流通股比例 |
| transaction_price | double | 交易价格 |
| filing_currency_price | double | 申报时货币的价格 |
| filing_type | str | 申报文件类型 |
| transaction_holding_type | str | 交易持有方式 |
| adjusted_sharehold | double | 调整后持有股数 |
| reported_sharehold | double | 申报持有股数 |
| adjusted_indirect_sharehold | double | 调整后间接持有股数 |
| reported_indirect_sharehold | double | 申报间接持有股数 |
| currency | str | 交易币种 |

#### 11.4. 使用示例

##### 11.4.1. 获取一定时间内某港股公司内部人交易活动

```python
import tqx_data
result = tqx_data.get_company_insider_transaction(
    market='hk',
    symbol="0004.HK",
    fields=[],
    start_date="20250101",
    end_date="20251231",
)
print(result)
```

**响应示例**

```text
symbol investor_name info_date ... adjusted_indirect_sharehold reported_indirect_sharehold currency
0 0004.HK Fang (Kang Vincent) 20250425 ... NaN NaN HKD
1 0004.HK Fang (Kang Vincent) 20250428 ... NaN NaN HKD
2 0004.HK Fang (Kang Vincent) 20250429 ... NaN NaN HKD
3 0004.HK Fang (Kang Vincent) 20250430 ... NaN NaN HKD
4 0004.HK Fang (Kang Vincent) 20250502 ... NaN NaN HKD
5 0004.HK Fang (Kang Vincent) 20250506 ... NaN NaN HKD
```

### 12. 获取公司股东持股报告

#### 12.1. 方法名：get_company_shareholder_report

#### 12.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702"（此接口查询持股报告日期） | 必填 |
| end_date | str | 结束日期,eg:"20250702"（此接口查询持股报告日期） | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 12.3. 响应参数

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | str | 股票代码 |
| investor_name | str | 投资者名称 |
| investor_category | str | 投资者大类 |
| investor_type | str | 投资者详细类别 |
| investment_activeness_orientation | str | 投资活动倾向 |
| turnover_rating | str | 换手率评级 |
| turnover_ratio | double | 换手率比例（相对于投资者总资产的交易活动量） |
| total_equity_assets | double | 总权益资产 |
| sharehold | double | 持有股数 |
| outstanding_ratio | double | 持股占总流通股比例 |
| hold_portfolio_ratio | double | 持仓占投资者投资组合比例 |
| sharehold_value | double | 持仓市值 |
| holding_date | str | 持股报告日期（日期筛选依据） |
| filing_type | str | 申报类型 |
| sharehold_change | double | 较上一次报告持股变动数量 |
| sharehold_value_change | double | 持仓市值变动 |
| outstanding_ratio_change | double | 占总流通股比例变动 |
| sharehold_change_ratio | double | 持股数变动百分比 |
| prev_sharehold | double | 上期持股数量 |
| prev_outstanding_ratio | double | 上期占总流通股比例 |
| prev_sharehold_value | double | 上期持仓市值 |
| prev_holding_date | str | 上期持股报告日期 |
| prev_filing_type | str | 上期申报类型 |
| currency | str | 交易币种 |

#### 12.4. 使用示例

##### 12.4.1. 获取一定时间内某港股公司股东持股报告

```python
import tqx_data
result = tqx_data.get_company_shareholder_report(
    market='hk',
    symbol="8510.HK",
    fields=[],
    start_date="20250101",
    end_date="20251231",
)
print(result)
```

**响应示例**

```text
symbol currency investor_name ... prev_sharehold_value prev_holding_date prev_filing_type
0 8510.HK HKD Chuk (Stanley) ... 457944.91 20241231 Hong Kong Insider
1 8510.HK HKD Chuan (Hng Bok) ... 328943.66 20241231 Shareholder Report
2 8510.HK HKD Lau (Wing Kee) ... 228433.10 20241231 Shareholder Report NaN HKD
```

### 13. 获取港美股指数成分股信息

#### 13.1. 方法名：get_index_component

#### 13.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| stock_symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| index_symbol | Optional\[Union\[str, List\[str\]\]\] | 指数代码 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

支持的指数列表:

|            |                                     |
|:-----------|:------------------------------------|
| 指数代码   | 名称                                |
| HSCC       | 恒生CC指数                          |
| HSCE       | 恒生国企指数                        |
| HSCEEWI    | 恒生国企等权重指数                  |
| HSCI       | 恒生综合指数                        |
| HSCIE      | 恒生能源指数                        |
| HSCIM      | 恒生原材料指数                      |
| HSEWI      | 恒生等权重指数                      |
| HSHFI      | 恒生港股通中国金融业精选指数        |
| HSI        | 恒生指数                            |
| HSLI       | 恒生综合大型股指数                  |
| HSMI       | 恒生综合中型股指数                  |
| HSNC       | 恒生工商指数                        |
| HSNF       | 恒生金融业指数                      |
| HSNP       | 恒生地产指数                        |
| HSNU       | 恒生公用事业指数                    |
| HSSI       | 恒生综合小型股指数                  |
| HSC50      | 恒生中国50指数                      |
| HSCAHAI    | 恒生港股通中国AH股(A股)指数         |
| HSCAHHI    | 恒生港股通中国AH股(H股)指数         |
| HSCAHI     | 恒生港股通中国AH股(A+H股)指数       |
| HSCAHPI    | 恒生港股通中国AH股溢价指数          |
| HSCIC      | 恒生综合企业指数                    |
| HSCIF      | 恒生金融业指数                      |
| HSCIIG     | 恒生工业制品指数                    |
| HSCIIT     | 恒生资讯科技指数                    |
| HSCIPC     | 恒生地产建筑指数                    |
| HSCIT      | 恒生综合电讯业指数                  |
| HSCIU      | 恒生公用事业指数                    |
| HSFM25     | 恒生中国(香港上市)30指数            |
| HSH35      | 恒生香港35指数                      |
| HSM100     | 恒生中国(香港上市)100指数           |
| HSREIT     | 恒生房地产投资信托基金指数          |
| HSCASUS    | 恒生(中国A股)企业可持续发展指数     |
| HSCASUSB   | 恒生(中国A股)企业可持续发展基准指数 |
| HSCEIDPI   | 恒生国企股息点数指数                |
| HSFCCI     | 恒生外国公司综合指数                |
| HSIDPI     | 恒生指数股息点数指数                |
| HSMHSUS    | 恒生(内地与香港)企业可持续发展指数  |
| HSSUS      | 恒生企业可持续发展指数              |
| HSSUSB     | 恒生企业可持续发展基准指数          |
| HSCAHSI    | 恒生港股通中国AH股精明指数          |
| HSCAT100   | 恒生中国A股顶尖100指数              |
| HSHBI      | 恒生高贝塔系数指数                  |
| HSHDYI     | 恒生高股息率指数                    |
| HSHYLV     | 恒生港股通高股息低波幅指数          |
| HSLVI      | 恒生低波幅指数                      |
| HSMBI      | 恒生内地银行指数                    |
| HSMPI      | 恒生内地物业指数                    |
| HSCGSI     | 恒生消费指数                        |
| HSCICS     | 恒生综合行业指数（主要消费）        |
| HSHCI      | 恒生医疗保健指数                    |
| HSIII      | 恒生互联网及资讯科技指数            |
| HSMOGI     | 恒生内地石油及天然气指数            |
| HKCSCMC    | 中证主要消费指数                    |
| HKCSHKDIV  | 中证红利指数                        |
| HKCSHKLC   | 中证消费指数                        |
| HKCSHKLRE  | 中证地产指数                        |
| HKCSHKMCS  | 中证中盘指数                        |
| HKCSHKME   | 中证企业指数（ME）                  |
| HKCSHKPE   | 中证企业指数（PE）                  |
| HKCSHKSE   | 中证企业指数（SE）                  |
| HKCSIHK100 | 中证香港100指数                     |
| HKSSE180   | 上证180指数                         |
| HKSSE180GV | 上证公司治理指数                    |
| HKSSE380   | 上证380指数                         |
| HKSSECEQT  | 上证商品指数                        |
| HKSSEDIV   | 上证红利指数                        |
| HKSSEITOP  | 上证行业龙头指数                    |
| HKSSEMCAP  | 上证中盘指数                        |
| HSCICD     | 恒生综合行业指数（非必需性消费）    |
| HKCES100   | 中华交易服务港股通精选100指数       |
| HKCES120   | 中华120指数                         |
| HKCES280   | 中华中国280指数                     |
| HKCES300   | 中华港股通300指数                   |
| HKCESA80   | 中华A股80指数                       |
| HKCESG10   | 中华G10指数                         |
| HKCESHKM   | 中华香港主板指数                    |
| HKCSRHK50  | 中证基本面指数                      |
| HKSSEMEGA  | 上证超大盘指数                      |
| HSCIH      | 恒生医疗保健行业指数                |
| SPHKGEM    | 标普香港创业板指数                  |
| SPHKL      | 标普香港大盘股指数                  |
| NDX        | 纳斯达克100指数                     |
| IXIC       | 纳斯达克综合指数                    |
| NBI        | 纳斯达克生物技术指数                |

#### 13.3. 响应参数

| 字段         | 类型 | 描述           |
|:-------------|:-----|:---------------|
| index_symbol | str  | 指数代码       |
| stock_symbol | str  | 股票代码       |
| added_date   | str  | 纳入成分股日期 |
| deleted_date | str  | 剔除成分股日期 |

#### 13.4. 使用示例

##### 13.4.1. 获取全部港股指数成分股信息

```python
import tqx_data
result = tqx_data.get_index_component(
    market='hk',
    stock_symbol="",
    index_symbol="",
)
print(result)
```

**响应示例**

```text
index_symbol stock_symbol added_date deleted_date
0 HKCES100 0001.HK 20210118 None
1 HKCES100 0002.HK 20210118 None
2 HKCES100 0003.HK 20210118 None
3 HKCES100 0004.HK 20210118 None
4 HKCES100 0005.HK 20210118 None
... ... ... ... ...
6653 SPHKL 9888.HK 20210312 None
6654 SPHKL 9961.HK 20210408 None
6655 SPHKL 9988.HK 20210118 None
6656 SPHKL 9992.HK 20210118 None
6657 SPHKL 9999.HK 20210118 None
```

### 14. 获取公司标准化营运指标

#### 14.1. 方法名：get_company_oper_metrics

#### 14.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_year | str | 开始财年,eg:"2025" | 必填 |
| end_year | str | 结束财年,eg:"2025" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 14.3. 响应参数

| 字段                      | 类型   | 描述                  |
|:--------------------------|:-------|:----------------------|
| symbol                    | str    | 股票代码              |
| is_final                  | int    | 是否是最终报告        |
| financial_year            | str    | 财年                  |
| financial_period_end_date | str    | 财报截止日期          |
| report_type               | str    | 报告类型（原始/重述） |
| data_type                 | str    | 数据类型              |
| consol_basis              | str    | 数据合并基础          |
| report_source             | str    | 报告来源              |
| item_name                 | str    | 指标名称              |
| is_pershare_item          | str    | 是否为每股指标        |
| is_percent_item           | str    | 是否为百分比指标      |
| item_unit                 | str    | 指标单位缩放          |
| item_currency             | str    | 指标货币单位          |
| item_num                  | double | 指标值                |

#### 14.4. 使用示例

##### 14.4.1. 获取一定财年内全部港股公司标准化营运指标

```python
import tqx_data
result = tqx_data.get_company_oper_metrics(
    market='hk',
    symbol=[""],
    fields=[""],
    start_year="2023",
    end_year="2025",
)
print(result)
```

**响应示例**

```text
symbol is_final financial_year ... item_unit item_currency item_num
0 0004.HK 1 2023 ... Units HKD 142989.000000
1 0004.HK 1 2023 ... No scaling HKD 0.000047
2 0004.HK 1 2023 ... Units HKD 142989.000000
3 0004.HK 1 2023 ... No scaling HKD 0.000047
4 0004.HK 1 2024 ... Units HKD 136832.000000
... ... ... ... ... ... ... ...
3273 9993.HK 1 2023 ... Units CNY 23952.919000
3274 9993.HK 1 2024 ... Units CNY 14833.422000
3275 9993.HK 1 2024 ... Units CNY 14833.422000
3276 9993.HK 0 2025 ... Units CNY 7914.030000
3277 9993.HK 0 2025 ... Units CNY 7914.030000
```

### 15. 获取公司最新市场财务统计指标

#### 15.1. 方法名：get_company_current

#### 15.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 15.3. 响应参数

备注：数据每日刷新，对于每个symbol的每个字段会尽可能返回已知的最新日期的数据

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | str | 股票代码 |
| date | str | 数据日期 |
| period_end_date | str | 财报截止日期 |
| curr_ebitda_to_ev_ratio | double | EBITDA占企业价值比重 |
| curr_ebitda_to_ev_ratio_ttm | double | EBITDA占企业价值比重（TTM） |
| curr_ev_to_ebitda | double | 企业价值/EBITDA |
| curr_ev_to_ebitda_ttm | double | 企业价值/EBITDA（TTM） |
| curr_ev_to_fcf | double | 企业价值/自由现金流 |
| curr_ev_to_fcf_ttm | double | 企业价值/自由现金流（TTM） |
| curr_ev_to_fcf | double | 企业价值/自由现金流 |
| curr_ev_to_fcf_ttm | double | 企业价值/自由现金流（TTM） |
| curr_ev_to_ocf | double | 企业价值/经营现金流 |
| curr_ev_to_ocf_ttm | double | 企业价值/经营现金流（TTM） |
| curr_ev_to_rev | double | 企业价值/营业收入 |
| curr_ev_to_rev_ttm | double | 企业价值/营业收入（TTM） |
| curr_fcf_to_ev_ratio | double | 自由现金流占企业价值比重 |
| curr_fcf_to_ev_ratio_ttm | double | 自由现金流占企业价值比重（TTM） |
| curr_rev_to_ev_ratio | double | 营业收入占企业价值比重 |
| curr_rev_to_ev_ratio_ttm | double | 营业收入占企业价值比重（TTM） |
| curr_ev_to_fcf | double | 企业价值/自由现金流 |
| curr_ev_to_fcf_ttm | double | 企业价值/自由现金流（TTM） |
| curr_ev_to_ebit | double | 企业价值/息税前利润 |
| curr_ev_to_ebit_ttm | double | 企业价值/息税前利润（TTM） |
| curr_price_to_fcf_pershr | double | 股价/每股自由现金流 |
| curr_price_to_fcf_pershr_ttm | double | 股价/每股自由现金流（TTM） |
| curr_price_to_fcf_pershr_issue | double | 股价/每股自由现金流（发行特定） |
| curr_price_to_fcf_pershr_issue_ttm | double | 股价/每股自由现金流（发行特定，TTM） |
| curr_fcf_to_ev_ratio | double | 自由现金流占企业价值比重 |
| curr_fcf_to_ev_ratio_ttm | double | 自由现金流占企业价值比重（TTM） |
| curr_div_yld_issue_ratio | double | 股息率-普通股净额（发行特定） |
| curr_div_yld_gross_issue_ratio | double | 股息率-普通股毛额（发行特定） |
| curr_div_yld_issue_ratio_ann | double | 股息率-普通股净额（年化，发行特定） |
| curr_div_yld_gross_issue_ratio_ann | double | 股息率-普通股毛额（年化，发行特定） |
| curr_div_yld_issue_ratio_ttm | double | 股息率-普通股净额（TTM，发行特定） |
| curr_div_yld_gross_issue_ratio_ttm | double | 股息率-普通股毛额（TTM，发行特定） |
| curr_cash_to_mcap_ratio | double | 现金及短期投资占市值比重 |
| curr_price_to_cf_pershr | double | 股价/每股现金流 |
| curr_price_to_cf_pershr_ttm | double | 股价/每股现金流（TTM） |
| curr_price_to_cf_pershr_ann | double | 股价/每股现金流（年化） |
| curr_price_to_cf_pershr_issue | double | 股价/每股现金流（发行特定） |
| curr_price_to_cf_pershr_issue_ttm | double | 股价/每股现金流（发行特定，TTM） |
| curr_price_to_fcf_pershr_issue | double | 股价/每股自由现金流（发行特定） |
| curr_price_to_fcf_pershr_issue_ttm | double | 股价/每股自由现金流（发行特定，TTM） |
| curr_price_to_ocf_pershr | double | 股价/每股经营现金流 |
| curr_price_to_ocf_pershr_ttm | double | 股价/每股经营现金流（TTM） |
| curr_price_to_ocf_pershr_issue | double | 股价/每股经营现金流（发行特定） |
| curr_price_to_ocf_pershr_issue_ttm | double | 股价/每股经营现金流（发行特定，TTM） |
| curr_price_to_rev_pershr | double | 股价/每股营业收入 |
| curr_price_to_rev_pershr_ann | double | 股价/每股营业收入（年化） |
| curr_price_to_rev_pershr_ttm | double | 股价/每股营业收入（TTM） |
| curr_price_to_rev_pershr_issue | double | 股价/每股营业收入（发行特定） |
| curr_price_to_rev_pershr_issue_ttm | double | 股价/每股营业收入（发行特定，TTM） |
| curr_price_to_fcf_pershr_issue | double | 股价/每股自由现金流（发行特定） |
| curr_price_to_fcf_pershr_issue_ttm | double | 股价/每股自由现金流（发行特定，TTM） |
| curr_price_to_dps_issue | double | 股价/每股股息-普通股净额（发行特定） |
| curr_price_to_dps_gross_issue | double | 股价/每股股息-普通股毛额（发行特定） |
| curr_price_to_dps_issue_ttm | double | 股价/每股股息-普通股净额（TTM，发行特定） |
| curr_price_to_dps_gross_issue_ttm | double | 股价/每股股息-普通股毛额（TTM，发行特定） |
| curr_pe_dil_excl_issue | double | 市盈率-稀释扣非（发行特定） |
| curr_pe_dil_excl_issue_ttm | double | 市盈率-稀释扣非（TTM，发行特定） |
| curr_pe_dil_excl | double | 市盈率-稀释扣非 |
| curr_pe_dil_excl_ttm | double | 市盈率-稀释扣非（TTM） |
| curr_pe_dil_norm_issue | double | 市盈率-稀释扣非标准化（发行特定） |
| curr_pe_dil_norm_issue_ttm | double | 市盈率-稀释扣非标准化（TTM，发行特定） |
| curr_pe_dil_norm | double | 市盈率-稀释扣非标准化 |
| curr_pe_dil_norm_ttm | double | 市盈率-稀释扣非标准化（TTM） |
| curr_pe_dil_incl_issue | double | 市盈率-稀释含非常项目（发行特定） |
| curr_pe_dil_incl_issue_ttm | double | 市盈率-稀释含非常项目（TTM，发行特定） |
| curr_pe_dil_incl | double | 市盈率-稀释含非常项目 |
| curr_pe_dil_incl_ttm | double | 市盈率-稀释含非常项目（TTM） |
| curr_price_to_ebitda_pershr_issue | double | 股价/每股EBITDA（发行特定） |
| curr_price_to_ebitda_pershr_issue_ttm | double | 股价/每股EBITDA（TTM，发行特定） |
| curr_price_to_ebitda_pershr | double | 股价/每股EBITDA |
| curr_price_to_ebitda_pershr_ttm | double | 股价/每股EBITDA（TTM） |
| curr_pe_basic_excl_issue | double | 市盈率-基本扣非（发行特定） |
| curr_pe_basic_excl_issue_ttm | double | 市盈率-基本扣非（TTM，发行特定） |
| curr_pe_basic_excl | double | 市盈率-基本扣非 |
| curr_pe_basic_excl_ttm | double | 市盈率-基本扣非（TTM） |
| curr_pe_basic_incl_issue | double | 市盈率-基本含非常项目（发行特定） |
| curr_pe_basic_incl_issue_ttm | double | 市盈率-基本含非常项目（TTM，发行特定） |
| curr_pe_basic_incl | double | 市盈率-基本含非常项目 |
| curr_pe_basic_incl_ttm | double | 市盈率-基本含非常项目（TTM） |
| curr_earn_yld_basic_excl_issue_ratio | double | 每股基本收益（扣非）占股价比重（发行特定） |
| curr_earn_yld_basic_excl_issue_ratio_ttm | double | 每股基本收益（扣非）占股价比重（TTM，发行特定） |
| curr_earn_yld_basic_excl_ratio | double | 每股基本收益（扣非）占股价比重 |
| curr_earn_yld_basic_excl_ratio_ttm | double | 每股基本收益（扣非）占股价比重（TTM） |
| curr_earn_yld_basic_incl_issue_ratio | double | 每股基本收益（含非常）占股价比重（发行特定） |
| curr_earn_yld_basic_incl_issue_ratio_ttm | double | 每股基本收益（含非常）占股价比重（TTM，发行特定） |
| curr_earn_yld_basic_incl_ratio | double | 每股基本收益（含非常）占股价比重 |
| curr_earn_yld_basic_incl_ratio_ttm | double | 每股基本收益（含非常）占股价比重（TTM） |
| curr_earn_yld_dil_excl_issue_ratio | double | 每股稀释收益（扣非）占股价比重（发行特定） |
| curr_earn_yld_dil_excl_issue_ratio_ttm | double | 每股稀释收益（扣非）占股价比重（TTM，发行特定） |
| curr_earn_yld_dil_excl_ratio | double | 每股稀释收益（扣非）占股价比重 |
| curr_earn_yld_dil_excl_ratio_ttm | double | 每股稀释收益（扣非）占股价比重（TTM） |
| curr_earn_yld_dil_incl_issue_ratio | double | 每股稀释收益（含非常）占股价比重（发行特定） |
| curr_earn_yld_dil_incl_issue_ratio_ttm | double | 每股稀释收益（含非常）占股价比重（TTM，发行特定） |
| curr_earn_yld_dil_incl_ratio | double | 每股稀释收益（含非常）占股价比重 |
| curr_earn_yld_dil_incl_ratio_ttm | double | 每股稀释收益（含非常）占股价比重（TTM） |
| curr_rel_pe_dil_excl_issue_ratio | double | 相对市盈率分位数（发行特定） |
| curr_rel_pe_dil_excl_ratio | double | 相对市盈率分位数 |
| curr_peg | double | 市盈率相对盈利增长比率 |
| curr_peg_issue | double | 市盈率相对盈利增长比率（发行特定） |
| curr_peg_ttm | double | 市盈率相对盈利增长比率（TTM） |
| curr_peg_issue_ttm | double | 市盈率相对盈利增长比率（TTM，发行特定） |
| curr_pegy_issue | double | 市盈率相对盈利增长及股息比率（发行特定） |
| curr_pegy_issue_ttm | double | 市盈率相对盈利增长及股息比率（TTM，发行特定） |
| curr_pe_dil_excl_ttm_incl_neg | double | 市盈率-稀释扣非（TTM，含负值） |
| curr_pe_dil_excl_issue_ttm_incl_neg | double | 市盈率-稀释扣非（TTM，发行特定，含负值） |
| curr_sales_per_emp_ann | double | 人均销售额（年化） |
| curr_sales_per_emp_currency_ann | str | 人均销售额-货币单位（年化） |
| curr_sales_per_emp_ttm | double | 人均销售额（TTM） |
| curr_sales_per_emp_currency_ttm | str | 人均销售额-货币单位（TTM） |
| curr_net_inc_per_emp_ann | double | 人均税后净利润（年化） |
| curr_net_inc_per_emp_currency_ann | str | 人均税后净利润-货币单位（年化） |
| curr_net_inc_per_emp_ttm | double | 人均税后净利润（TTM） |
| curr_net_inc_per_emp_currency_ttm | str | 人均税后净利润-货币单位（TTM） |
| curr_ev | double | 企业价值 |
| curr_ev_currency | str | 企业价值-货币单位 |
| curr_pb | double | 市净率 |
| curr_pb_issue | double | 市净率（发行特定） |
| curr_ptb | double | 市净率-有形 |
| curr_ptb_issue | double | 市净率-有形（发行特定） |
| curr_ev_excl_lt_inv | double | 企业价值（扣除长期投资） |
| curr_ev_excl_lt_inv_currency | str | 企业价值-货币单位（扣除长期投资） |
| curr_cash_to_mcap_ratio_lfy | double | 现金及短期投资占市值比重（上一财年） |
| curr_pb_lfy | double | 市净率（上一财年） |
| curr_pb_issue_lfy | double | 市净率（上一财年，发行特定） |
| curr_ptb_lfy | double | 市净率-有形（上一财年） |
| curr_ptb_issue_lfy | double | 市净率-有形（上一财年，发行特定） |
| curr_ev_out | double | 企业价值（基于流通股本） |
| curr_ev_out_currency | str | 企业价值-货币单位（基于流通股本） |
| curr_net_debt_to_ev_ratio | double | 净债务占企业价值比重 |
| curr_price_to_fcf_pershr | double | 股价/每股自由现金流 |
| curr_price_to_fcf_pershr_ttm | double | 股价/每股自由现金流（TTM） |
| curr_price_to_fcf_pershr | double | 股价/每股自由现金流 |
| curr_price_to_fcf_pershr_ttm | double | 股价/每股自由现金流（TTM） |
| curr_high_to_pe_dil_excl_ttm | double | 52周最高价/每股收益（TTM） |
| curr_high_to_pe_dil_excl_issue_ttm | double | 52周最高价/每股收益（TTM，发行特定） |
| curr_low_to_pe_dil_excl_ttm | double | 52周最低价/每股收益（TTM） |
| curr_low_to_pe_dil_excl_issue_ttm | double | 52周最低价/每股收益（TTM，发行特定） |
| curr_earn_yld_dil_excl_issue_to_high_ratio_ttm | double | 每股收益占52周最高价比重（发行特定，TTM） |
| curr_earn_yld_dil_excl_to_high_ratio_ttm | double | 每股收益占52周最高价比重（TTM） |
| curr_earn_yld_dil_excl_issue_to_low_ratio_ttm | double | 每股收益占52周最低价比重（发行特定，TTM） |
| curr_earn_yld_dil_excl_to_low_ratio_ttm | double | 每股收益占52周最低价比重（TTM） |
| curr_high_to_pb | double | 52周最高价/每股账面价值 |
| curr_high_to_pb_issue | double | 52周最高价/每股账面价值（发行特定） |
| curr_low_to_pb | double | 52周最低价/每股账面价值 |
| curr_low_to_pb_issue | double | 52周最低价/每股账面价值（发行特定） |

#### 15.4. 使用示例

##### 15.4.1. 获取全部港股公司最新的部分市场财务统计指标

```python
import tqx_data
result = tqx_data.get_company_current(
    market='hk',
    symbol=[""],
    fields=["curr_price_to_dps_issue_ttm","curr_div_yld_gross_issue_ratio","curr_fcf_to_ev_ratio_ttm"]
)
print(result)
```

**响应示例**

```text
symbol date curr_price_to_dps_issue_ttm curr_div_yld_gross_issue_ratio curr_fcf_to_ev_ratio_ttm
0 0001.HK 20251231 NaN NaN NaN
1 0001.HK 20260422 NaN NaN 7.405582
2 0002.HK 20251231 NaN NaN NaN
3 0002.HK 20260421 26.089543 4.185285 NaN
4 0002.HK 20260422 NaN NaN 2.373637
... ... ... ... ... ...
5651 9998.HK 20260422 NaN NaN NaN
5652 9999.HK 20251231 NaN NaN NaN
5653 9999.HK 20260416 NaN NaN 12.294160
5654 9999.HK 20260421 NaN NaN NaN
5655 9999.HK 20260422 37.359101 2.677018 NaN
```

### 16. 获取公司最新行业中位统计数据

#### 16.1. 方法名：get_company_imed

#### 16.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 16.3. 响应参数

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | str | 股票代码 |
| date | str | 日期 |
| industry_name | str | 行业名称 |
| imed_rec_turnover_ttm | double | 应收账款周转率TTM |
| imed_asset_turnover_ttm | double | 总资产周转率TTM |
| imed_net_trade_cycle_days_ttm | double | 平均净营业周期(天)TTM |
| imed_gross_div_yield_ttm | double | 当前股息率(毛利)TTM |
| imed_net_div_yield_ttm | double | 当前股息率(净利)TTM |
| imed_price_to_fcf_per_shr_ttm | double | 股价/每股自由现金流TTM |
| imed_gross_div_yield_ttm | double | 股息率(毛利)TTM |
| imed_retention_ratio_ttm | double | 盈利留存率TTM |
| imed_fa_turnover_ttm | double | 固定资产周转率TTM |
| imed_inv_turnover_ttm | double | 存货周转率TTM |
| imed_inv_ratio_ttm | double | 投资比率TTM |
| imed_net_debt_to_ebitda_ttm | double | 净债务/EBITDA TTM |
| imed_pretax_roa_ratio_ttm | double | 税前总资产收益率TTM |
| imed_pretax_roe_ratio_ttm | double | 税前净资产收益率TTM |
| imed_pe_excl_exord_ttm | double | 市盈率(不含非常项目)TTM |
| imed_price_to_fcf_net_div_ttm | double | 股价/每股FCF(扣股息)TTM |
| imed_price_to_cfo_per_shr_ttm | double | 股价/每股经营现金流TTM |
| imed_price_to_rev_per_shr_ttm | double | 股价/每股总收入TTM |
| imed_loan_loss_prov_to_loans_ratio_ttm | double | 贷款损失准备/净贷款TTM |
| imed_reinv_ratio_ttm | double | 再投资率TTM |
| imed_roe_avg_common_ttm | double | 平均普通股ROE TTM |
| imed_roic_ratio_ttm | double | 投入资本回报率TTM |
| imed_sales_per_emp_ttm | double | 人均销售额TTM |
| imed_sales_per_emp_ccy_ttm | str | 人均销售额-货币单位TTM |
| imed_wcap_to_rev_pct_chg_ttm | double | 营运资本/收入(环比变化)TTM |
| imed_pe_ttm | double | 当前市盈率TTM |
| imed_pb_ttm | double | 当前市净率TTM |
| imed_pcfo_ttm | double | 当前股价/经营现金流TTM |
| imed_ps_ttm | double | 当前市销率TTM |
| imed_core_tier1_ratio_fye_mid | double | 核心一级资本充足率 |
| imed_combined_ratio_insur_fye_mid | double | 综合比率-保险 |
| imed_curr_ratio_fye_mid | double | 流动比率 |
| imed_deposits_pct_chg_fye_mid | double | 存款环比变化 |
| imed_ebitda_margin_ratio_fye_mid | double | EBITDA利润率 |
| imed_efficiency_ratio_fye_mid | double | 效率比率 |
| imed_expense_ratio_insur_fye_mid | double | 费用率-保险 |
| imed_fee_rev_ratio_fye_mid | double | 手续费收入占比 |
| imed_gross_margin_ratio_fye_mid | double | 毛利率 |
| imed_net_income_margin_excl_exord_fye_mid | double | 普通股净利润率(不含非常) |
| imed_tax_rate_ratio_fye_mid | double | 所得税率 |
| imed_insur_reserves_pct_chg_fye_mid | double | 保险准备金环比变化 |
| imed_int_coverage_ratio_fye_mid | double | 利息覆盖率 |
| imed_net_loans_pct_chg_fye_mid | double | 净贷款环比变化 |
| imed_nonperf_loans_to_gross_loans_ratio_fye_mid | double | 不良及减值贷款/总贷款 |
| imed_loans_to_deposits_ratio_fye_mid | double | 存贷比 |
| imed_loss_ratio_insur_fye_mid | double | 损失率-保险 |
| imed_lt_debt_to_tot_cap_ratio_fye_mid | double | 长期债务/总资本 |
| imed_cfo_abs_fye_mid | double | 经营活动现金流净额(绝对) |
| imed_cfo_ccy_fye_mid | str | 经营活动现金流-货币单位 |
| imed_nim_ratio_fye_mid | double | 净息差 |
| imed_net_margin_ratio_fye_mid | double | 净利润率 |
| imed_net_premiums_earned_diff_fye_mid | double | 已赚净保费(环比变化) |
| imed_net_premiums_earned_diff_ccy_fye_mid | str | 已赚净保费-货币单位 |
| imed_nonint_inc_to_op_inc_ratio_fye_mid | double | 非利息收入/营业收入 |
| imed_op_lev_fye_mid | double | 经营杠杆 |
| imed_op_margin_ratio_fye_mid | double | 营业利润率 |
| imed_op_ratio_insur_fye_mid | double | 经营比率-保险 |
| imed_pb_fye_mid | double | 市净率(财年中期) |
| imed_prov_doubtful_to_rec_ratio_fye_mid | double | 坏账准备/应收款项 |
| imed_quick_ratio_fye_mid | double | 速动比率 |
| imed_foreclosed_assets_to_loans_ratio_fye_mid | double | 法拍房地产/总贷款 |
| imed_securities_to_earn_assets_ratio_fye_mid | double | 证券/盈利资产 |
| imed_tax_complement_fye_mid | double | 税务互补率 |
| imed_assets_to_equity_ratio_fye_mid | double | 总资产/总权益 |
| imed_debt_to_equity_ratio_fye_mid | double | 总债务/普通股权益 |
| imed_rec_turnover_fye | double | 应收账款周转率(财年) |
| imed_asset_turnover_fye | double | 总资产周转率(财年) |
| imed_net_trade_cycle_days_fye | double | 平均净营业周期(财年) |
| imed_core_tier1_ratio_fye | double | 核心一级资本充足率(财年) |
| imed_combined_ratio_insur_fye | double | 综合比率-保险(财年) |
| imed_curr_ratio_fye | double | 流动比率(财年) |
| imed_deposits_pct_chg_fye | double | 存款环比变化(财年) |
| imed_gross_div_yield_fye | double | 股息率(毛利-财年) |
| imed_retention_ratio_fye | double | 盈利留存率(财年) |
| imed_ebitda_margin_ratio_fye | double | EBITDA利润率(财年) |
| imed_efficiency_ratio_fye | double | 效率比率(财年) |
| imed_expense_ratio_insur_fye | double | 费用率-保险(财年) |
| imed_fee_rev_ratio_fye | double | 手续费收入占比(财年) |
| imed_fa_turnover_fye | double | 固定资产周转率(财年) |
| imed_gross_margin_ratio_fye | double | 毛利率(财年) |
| imed_net_income_margin_excl_exord_fye | double | 普通股净利润率(不含非常-财年) |
| imed_tax_rate_ratio_fye | double | 所得税率(财年) |
| imed_insur_reserves_pct_chg_fye | double | 保险准备金环比变化(财年) |
| imed_int_coverage_ratio_fye | double | 利息覆盖率(财年) |
| imed_inv_turnover_fye | double | 存货周转率(财年) |
| imed_inv_ratio_fye | double | 投资比率(财年) |
| imed_net_loans_pct_chg_fye | double | 净贷款环比变化(财年) |
| imed_nonperf_loans_to_gross_loans_ratio_fye | double | 不良贷款率(财年) |
| imed_loans_to_deposits_ratio_fye | double | 存贷比(财年) |
| imed_loss_ratio_insur_fye | double | 损失率-保险(财年) |
| imed_lt_debt_to_tot_cap_ratio_fye | double | 长期债务/总资本(财年) |
| imed_cfo_abs_fye | double | 经营现金流净额(财年) |
| imed_cfo_ccy_fye | str | 经营现金流-货币单位(财年) |
| imed_net_debt_to_ebitda_fye | double | 净债务/EBITDA(财年) |
| imed_nim_ratio_fye | double | 净息差(财年) |
| imed_net_margin_ratio_fye | double | 净利润率(财年) |
| imed_net_premiums_earned_diff_fye | double | 已赚净保费（环比变化），行业中位数 - 最近财年 |
| imed_net_premiums_earned_diff_ccy_fye | str | 已赚净保费（环比变化）- 货币单位，行业中位数 - 最近财年 |
| imed_nonint_inc_to_op_inc_ratio_fye | double | 非利息收入 / 营业收入，行业中位数 - 最近财年 |
| imed_op_lev_fye | double | 经营杠杆，行业中位数 - 最近财年 |
| imed_op_margin_ratio_fye | double | 营业利润率（%），行业中位数 - 最近财年 |
| imed_op_ratio_insur_fye | double | 经营比率 - 保险（%），行业中位数 - 最近财年 |
| imed_pretax_roa_ratio_fye | double | 税前总资产收益率（%），行业中位数 - 最近财年 |
| imed_pretax_roe_ratio_fye | double | 税前净资产收益率（%），行业中位数 - 最近财年 |
| imed_pb_fye | double | 股价 / 每股净资产，行业中位数 - 最近财年 |
| imed_pe_excl_exord_fye | double | 股价 / 稀释每股收益（不含非常项目），行业中位数 - 最近财年 |
| imed_price_to_fcf_net_div_fye | double | 股价 / 每股自由现金流（扣除股息），行业中位数 - 最近财年 |
| imed_price_to_cfo_per_shr_fye | double | 股价 / 每股经营活动现金流，行业中位数 - 最近财年 |
| imed_price_to_rev_per_shr_fye | double | 股价 / 每股总收入，行业中位数 - 最近财年 |
| imed_prov_doubtful_to_rec_ratio_fye | double | 坏账准备 / 应收款项净额（%），行业中位数 - 最近财年 |
| imed_loan_loss_prov_to_loans_ratio_fye | double | 贷款损失准备 / 净贷款总额（%），行业中位数 - 最近财年 |
| imed_quick_ratio_fye | double | 速动比率，行业中位数 - 最近财年 |
| imed_foreclosed_assets_to_loans_ratio_fye | double | 法拍房地产 / 总贷款总额（%），行业中位数 - 最近财年 |
| imed_reinv_ratio_fye | double | 再投资率（%），行业中位数 - 最近财年 |
| imed_roe_avg_common_fye | double | 平均普通股回报率（%），行业中位数 - 最近财年 |
| imed_roic_ratio_fye | double | 投入资本回报率（%），行业中位数 - 最近财年 |
| imed_sales_per_emp_fye | double | 人均销售额，行业中位数 - 最近财年 |
| imed_sales_per_emp_ccy_fye | str | 人均销售额 - 货币单位，行业中位数 - 最近财年 |
| imed_securities_to_earn_assets_ratio_fye | double | 证券占平均盈利资产比例（%），行业中位数 - 最近财年 |
| imed_tax_complement_fye | double | 税务互补率，行业中位数 - 最近财年 |
| imed_assets_to_equity_ratio_fye | double | 总资产 / 总权益，行业中位数 - 最近财年 |
| imed_debt_to_equity_ratio_fye | double | 总债务 / 普通股权益，行业中位数 - 最近财年 |
| imed_wcap_to_rev_pct_chg_fye | double | 营运资本占总收入百分比（环比变化），行业中位数 - 最近财年 |
| imed_rec_turnover_prev_fye | double | 应收账款周转率，行业中位数 - 上一财年 |
| imed_asset_turnover_prev_fye | double | 总资产周转率，行业中位数 - 上一财年 |
| imed_net_trade_cycle_days_prev_fye | double | 平均净营业周期（天），行业中位数 - 上一财年 |
| imed_core_tier1_ratio_prev_fye | double | 核心一级资本充足率（%），行业中位数 - 上一财年 |
| imed_combined_ratio_insur_prev_fye | double | 综合比率 - 保险（%），行业中位数 - 上一财年 |
| imed_curr_ratio_prev_fye | double | 流动比率，行业中位数 - 上一财年 |
| imed_deposits_pct_chg_prev_fye | double | 存款总额（环比%变化），行业中位数 - 上一财年 |
| imed_gross_div_yield_prev_fye | double | 股息率（普通股-毛率-%），行业中位数 - 上一财年 |
| imed_retention_ratio_prev_fye | double | 盈利留存率，行业中位数 - 上一财年 |
| imed_ebitda_margin_ratio_prev_fye | double | EBITDA 利润率（%），行业中位数 - 上一财年 |
| imed_efficiency_ratio_prev_fye | double | 效率比率（%），行业中位数 - 上一财年 |
| imed_expense_ratio_insur_prev_fye | double | 费用率 - 保险（%），行业中位数 - 上一财年 |
| imed_fee_rev_ratio_prev_fye | double | 手续费收入占比（%），行业中位数 - 上一财年 |
| imed_fa_turnover_prev_fye | double | 固定资产周转率，行业中位数 - 上一财年 |
| imed_gross_margin_ratio_prev_fye | double | 毛利率（%），行业中位数 - 上一财年 |
| imed_net_income_margin_excl_exord_prev_fye | double | 普通股可分配净利润率（不含非常项目，%），行业中位数 - 上一财年 |
| imed_tax_rate_ratio_prev_fye | double | 所得税率（%），行业中位数 - 上一财年 |
| imed_insur_reserves_pct_chg_prev_fye | double | 保险准备金总额（环比%变化），行业中位数 - 上一财年 |
| imed_int_coverage_ratio_prev_fye | double | 利息覆盖率，行业中位数 - 上一财年 |
| imed_inv_turnover_prev_fye | double | 存货周转率，行业中位数 - 上一财年 |
| imed_inv_ratio_prev_fye | double | 投资比率（%），行业中位数 - 上一财年 |
| imed_net_loans_pct_chg_prev_fye | double | 净贷款总额（环比%变化），行业中位数 - 上一财年 |
| imed_nonperf_loans_to_gross_loans_ratio_prev_fye | double | 不良及减值贷款 / 总贷款总额（%），行业中位数 - 上一财年 |
| imed_loans_to_deposits_ratio_prev_fye | double | 存贷比（期末），行业中位数 - 上一财年 |
| imed_loss_ratio_insur_prev_fye | double | 损失率 - 保险（%），行业中位数 - 上一财年 |
| imed_lt_debt_to_tot_cap_ratio_prev_fye | double | 长期债务占总资本比例（%），行业中位数 - 上一财年 |
| imed_cfo_abs_prev_fye | double | 经营活动现金流净额，行业中位数 - 上一财年 |
| imed_cfo_ccy_prev_fye | str | 经营活动现金流净额 - 货币单位，行业中位数 - 上一财年 |
| imed_net_debt_to_ebitda_prev_fye | double | 净债务 / EBITDA，行业中位数 - 上一财年 |
| imed_nim_ratio_prev_fye | double | 净息差（%），行业中位数 - 上一财年 |
| imed_net_margin_ratio_prev_fye | double | 净利润率（%），行业中位数 - 上一财年 |
| imed_net_premiums_earned_diff_prev_fye | double | 已赚净保费（环比变化），行业中位数 - 上一财年 |
| imed_net_premiums_earned_diff_ccy_prev_fye | str | 已赚净保费（环比变化）- 货币单位，行业中位数 - 上一财年 |
| imed_nonint_inc_to_op_inc_ratio_prev_fye | double | 非利息收入 / 营业收入，行业中位数 - 上一财年 |
| imed_op_lev_prev_fye | double | 经营杠杆，行业中位数 - 上一财年 |
| imed_op_margin_ratio_prev_fye | double | 营业利润率（%），行业中位数 - 上一财年 |
| imed_op_ratio_insur_prev_fye | double | 经营比率 - 保险（%），行业中位数 - 上一财年 |
| imed_pretax_roa_ratio_prev_fye | double | 税前总资产收益率（%），行业中位数 - 上一财年 |
| imed_pretax_roe_ratio_prev_fye | double | 税前净资产收益率（%），行业中位数 - 上一财年 |
| imed_pb_prev_fye | double | 股价 / 每股净资产，行业中位数 - 上一财年 |
| imed_pe_excl_exord_prev_fye | double | 股价 / 稀释每股收益（不含非常项目），行业中位数 - 上一财年 |
| imed_price_to_fcf_net_div_prev_fye | double | 股价 / 每股自由现金流（扣除股息），行业中位数 - 上一财年 |
| imed_price_to_cfo_per_shr_prev_fye | double | 股价 / 每股经营活动现金流，行业中位数 - 上一财年 |
| imed_price_to_rev_per_shr_prev_fye | double | 股价 / 每股总收入，行业中位数 - 上一财年 |
| imed_prov_doubtful_to_rec_ratio_prev_fye | double | 坏账准备 / 应收款项净额（%），行业中位数 - 上一财年 |
| imed_loan_loss_prov_to_loans_ratio_prev_fye | double | 贷款损失准备 / 净贷款总额（%），行业中位数 - 上一财年 |
| imed_quick_ratio_prev_fye | double | 速动比率，行业中位数 - 上一财年 |
| imed_foreclosed_assets_to_loans_ratio_prev_fye | double | 法拍房地产 / 总贷款总额（%），行业中位数 - 上一财年 |
| imed_reinv_ratio_prev_fye | double | 再投资率（%），行业中位数 - 上一财年 |
| imed_roe_avg_common_prev_fye | double | 平均普通股回报率（%），行业中位数 - 上一财年 |
| imed_roic_ratio_prev_fye | double | 投入资本回报率（%），行业中位数 - 上一财年 |
| imed_sales_per_emp_prev_fye | double | 人均销售额，行业中位数 - 上一财年 |
| imed_sales_per_emp_ccy_prev_fye | str | 人均销售额 - 货币单位，行业中位数 - 上一财年 |
| imed_securities_to_earn_assets_ratio_prev_fye | double | 证券占平均盈利资产比例（%），行业中位数 - 上一财年 |
| imed_tax_complement_prev_fye | double | 税务互补率，行业中位数 - 上一财年 |
| imed_assets_to_equity_ratio_prev_fye | double | 总资产 / 总权益，行业中位数 - 上一财年 |
| imed_debt_to_equity_ratio_prev_fye | double | 总债务 / 普通股权益，行业中位数 - 上一财年 |
| imed_wcap_to_rev_pct_chg_prev_fye | double | 营运资本占总收入百分比（环比变化），行业中位数 - 上一财年 |
| imed_dps_yield_cur_fye | double | 每股股息率（%），行业中位数 - 当前财年 |
| imed_fwd_ev_to_ebit_cur_fye | double | 前瞻企业价值 / EBIT，行业中位数 - 当前财年 |
| imed_fwd_ev_to_ebitda_cur_fye | double | 前瞻企业价值 / EBITDA，行业中位数 - 当前财年 |
| imed_fwd_ev_to_cfo_cur_fye | double | 前瞻企业价值 / 经营现金流，行业中位数 - 当前财年 |
| imed_fwd_ev_to_sales_cur_fye | double | 前瞻企业价值 / 销售额，行业中位数 - 当前财年 |
| imed_fwd_net_debt_to_ebitda_cur_fye | double | 前瞻净债务 / EBITDA，行业中位数 - 当前财年 |
| imed_fwd_pe_cur_fye | double | 前瞻市盈率（P/E），行业中位数 - 当前财年 |
| imed_fwd_peg_cur_fye | double | 前瞻市盈率相对盈利增长（P/E/G），行业中位数 - 当前财年 |
| imed_fwd_pb_cur_fye | double | 前瞻股价 / 每股净资产，行业中位数 - 当前财年 |
| imed_fwd_pcfo_cur_fye | double | 前瞻股价 / 每股现金流，行业中位数 - 当前财年 |
| imed_fwd_ps_cur_fye | double | 前瞻股价 / 每股销售额，行业中位数 - 当前财年 |
| imed_fwd_total_debt_to_ebitda_cur_fye | double | 前瞻总债务 / EBITDA，行业中位数 - 当前财年 |
| imed_dps_yield_ntm | double | 每股股息率（%），行业中位数 - 未来十二个月 |
| imed_fwd_ev_to_ebit_ntm | double | 前瞻企业价值 / EBIT，行业中位数 - 未来十二个月 |
| imed_fwd_ev_to_ebitda_ntm | double | 前瞻企业价值 / EBITDA，行业中位数 - 未来十二个月 |
| imed_fwd_ev_to_cfo_ntm | double | 前瞻企业价值 / 经营现金流，行业中位数 - 未来十二个月 |
| imed_fwd_ev_to_sales_ntm | double | 前瞻企业价值 / 销售额，行业中位数 - 未来十二个月 |
| imed_fwd_net_debt_to_ebitda_ntm | double | 前瞻净债务 / EBITDA，行业中位数 - 未来十二个月 |
| imed_fwd_pe_ntm | double | 前瞻市盈率（P/E），行业中位数 - 未来十二个月 |
| imed_fwd_peg_ntm | double | 前瞻市盈率相对盈利增长（P/E/G），行业中位数 - 未来十二个月 |
| imed_fwd_pcfo_ntm | double | 前瞻股价 / 每股现金流，行业中位数 - 未来十二个月 |
| imed_fwd_ps_ntm | double | 前瞻股价 / 每股销售额，行业中位数 - 未来十二个月 |
| imed_fwd_total_debt_to_ebitda_ntm | double | 前瞻总债务 / EBITDA，行业中位数 - 未来十二个月 |

#### 16.4. 使用示例

##### 16.4.1. 获取全部港股公司最新的部分行业中位统计数据

```python
import tqx_data
result = tqx_data.get_company_imed(
    market='hk',
    symbol=[""],
    fields=["imed_net_trade_cycle_days_ttm","imed_pretax_roa_ratio_ttm"]
)
print(result)
```

**响应示例**

```text
symbol date imed_net_trade_cycle_days_ttm imed_pretax_roa_ratio_ttm
0 0002.HK 20240920 46.081797 NaN
1 0002.HK 20260331 NaN NaN
2 0002.HK 20260421 NaN 1.716472
3 0018.HK 20240920 23.065888 NaN
4 0018.HK 20260421 NaN 4.118784
.. ... ... ... ...
531 9938.HK 20260421 NaN 5.000255
532 9977.HK 20240920 67.514588 NaN
533 9977.HK 20260421 NaN 4.453275
534 9991.HK 20240920 35.499386 NaN
535 9991.HK 20260421 NaN 5.831199
```

### 17. 获取公司最新价量指标数据

#### 17.1. 方法名：get_company_price_vol

#### 17.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 17.3. 响应参数

| 字段                   | 类型   | 描述                            |
|:-----------------------|:-------|:--------------------------------|
| symbol                 | str    | 股票代码                        |
| pv_beta_5y             | double | 5年贝塔值（股价波动相对于市场） |
| pv_return_mtd          | double | 本月至今涨跌幅（%）             |
| pv_market_cap          | double | 市值（数值）                    |
| pv_market_cap_currency | str    | 市值（货币单位）                |
| pv_market_cap_date     | str    | 市值（计算日期）                |
| pv_high_52w            | double | 52周最高价                      |
| pv_high_52w_date       | str    | 52周最高价发生日期              |
| pv_low_52w             | double | 52周最低价                      |
| pv_low_52w_date        | str    | 52周最低价发生日期              |
| pv_rel_return_4w       | double | 相对基准4周涨跌幅（%）          |
| pv_return_13w          | double | 13周涨跌幅（%）                 |
| pv_rel_return_13w      | double | 相对基准13周涨跌幅（%）         |
| pv_return_1d           | double | 1日涨跌幅（%）                  |
| pv_return_26w          | double | 26周涨跌幅（%）                 |
| pv_rel_return_26w      | double | 相对基准26周涨跌幅（%）         |
| pv_return_52w          | double | 52周涨跌幅（%）                 |
| pv_rel_return_52w      | double | 相对基准52周涨跌幅（%）         |
| pv_return_5d           | double | 5日涨跌幅（%）                  |
| pv_return_ytd          | double | 年初至今涨跌幅（%）             |
| pv_rel_return_ytd      | double | 相对基准年初至今涨跌幅（%）     |
| pv_avg_vol_10d         | double | 10日平均成交量                  |
| pv_avg_monthly_vol_13w | double | 13周平均月成交量                |
| pv_close               | double | 最新收盘价                      |
| pv_close_date          | str    | 最新收盘价日期                  |
| pv_close_currency      | str    | 收盘价货币单位                  |
| pv_avg_vol_90d         | double | 90日平均成交量                  |
| pv_avg_val_3m          | double | 3个月平均日成交金额             |

#### 17.4. 使用示例

##### 17.4.1. 获取一定时间内某港股公司股东持股报告

```python
import tqx_data
result = tqx_data.get_company_price_vol(
    market='hk',
    symbol=[""],
    fields=["pv_beta_5y","pv_rel_return_26w"]
)
print(result)
```

**响应示例**

```text
symbol pv_beta_5y pv_rel_return_26w
0 0001.HK 0.592207 25.364034
1 0002.HK 0.244215 12.544505
2 0003.HK 0.434090 -0.222832
3 0004.HK 0.451330 11.580112
4 0005.HK 1.355217 23.942310
... ... ... ...
2850 9995.HK 1.052884 21.851235
2851 9996.HK 1.294652 14.637149
2852 9997.HK 0.681334 12.775834
2853 9998.HK 0.748572 -16.618340
2854 9999.HK 0.883445 -23.775904
```

### 18. 获取非周期性指标一致预期

#### 18.1. 方法名：get_consensus_nonperiod

#### 18.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 18.3. 响应参数

注：对于除symbol，currency，indicator外的参数默认是最新日期的预测，且有历史维度衍生字段，衍生后缀有week，1month~12month对每个字段构成共十三个衍生字段，表示对应字段在一周，一个月~十二个月前的预测值

例：mean_week表示一周前的预测均值，std_6month表示6个月前的预测标准差

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| symbol | str | 股票代码 |
| currency | str | 货币单位 |
| indicator | str | 指标名:LTGROWTH为未来3~5年长期增长，TP为未来1年目标价 |
| mean | double | 预测均值 |
| median | double | 预测中位数 |
| high | double | 预测最高值 |
| low | double | 预测最低值 |
| std | double | 预测标准差 |
| estimates_num | double | 预测数 |
| included_estimates_num | double | 纳入统计的预测数 |

#### 18.4. 使用示例

##### 18.4.1. 获取全部港股非周期性指标的部分一致预期

```python
import tqx_data
result = tqx_data.get_consensus_nonperiod(
    market='hk',
    symbol=[""],
    fields=["indicator","mean","std_6month","high_week"]
)
print(result)
```

**响应示例**

```text
symbol indicator mean std_6month high_week
0 0001.HK LTGROWTH 4.60000 NaN 4.60
1 0001.HK TP 69.43333 1.50000 78.00
2 0002.HK LTGROWTH 2.70000 0.00000 2.70
3 0002.HK TP 77.02000 4.06262 86.64
4 0003.HK LTGROWTH 6.38000 0.00000 7.30
.. ... ... ... ... ...
972 9996.HK TP 9.43200 0.55741 10.66
973 9997.HK LTGROWTH NaN 0.00000 NaN
974 9997.HK TP NaN 0.00000 NaN
975 9999.HK LTGROWTH 4.80000 0.00000 4.80
976 9999.HK TP 235.88571 46.77894 289.00
```

### 19. 获取买卖建议一致预期

#### 19.1. 方法名：get_consensus_recommend

#### 19.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 返回字段 | 非必填 |
| market | str | 市场，支持"hk" ,"us"，默认为"hk" | 必填 |

#### 19.3. 响应参数

注1：对于除symbol，currency外的参数默认是最新日期的预测，且有历史维度衍生字段，衍生后缀有week，1month~12month对每个字段构成共十三个衍生字段，表示对应字段在一周，一个月~十二个月前的预测值

例：mean_week表示一周前的预期均值，low_6month表示6个月前的预期最低值  
注2：强卖，卖，持仓，买，强买依次记为5，4，3，2，1评分

| 字段                | 类型   | 描述       |
|:--------------------|:-------|:-----------|
| symbol              | str    | 股票代码   |
| currency            | str    | 货币单位   |
| mean                | double | 预期均值   |
| median              | double | 预期中位数 |
| high                | double | 预期最高值 |
| low                 | double | 预期最低值 |
| strong_buy_num      | double | 强买建议数 |
| buy_num             | double | 买入建议数 |
| hold                | double | 持仓建议数 |
| sell_num            | double | 卖出建议数 |
| strong_sell_num     | double | 强卖建议数 |
| no_opinion_num      | double | 无意见数   |
| recommendations_num | double | 推荐总数   |

#### 19.4. 使用示例

##### 19.4.1. 获取全部港股买卖建议的部分一致预期

```python
import tqx_data
result = tqx_data.get_consensus_recommend(
    market='hk',
    symbol=[""],
    fields=["strong_buy_num","buy_num_week"]
)
print(result)
```

**响应示例**

```text
symbol strong_buy_num buy_num_week
0 0001.HK 2.0 5.0
1 0002.HK 1.0 2.0
2 0003.HK 1.0 2.0
3 0004.HK 0.0 2.0
4 0005.HK 3.0 6.0
.. ... ... ...
816 9992.HK 12.0 14.0
817 9995.HK 6.0 6.0
818 9996.HK 1.0 3.0
819 9997.HK NaN NaN
820 9999.HK 7.0 12.0
```

**三. 财务与市场因子**

**1.获取港美股回测因子**

#### 1.1. 方法名：get_factor

#### 1.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | str | 开始日期,eg:"20250702" | 必填 |
| end_date | str | 结束日期,eg:"20250702" | 必填 |
| symbol | Optional\[Union\[str, List\[str\]\]\] | 股票代码 | 非必填 |
| factors | Union\[str, List\[str\]\] | 因子列表 | 必填 |
| type | Optional\[str\] | 产品类型，支持"hk" ,"nb"，默认为"hk" | 非必填 |

#### 1.3. 响应参数

基础因子类:

| 字段      | 类型   | 描述       |
|:----------|:-------|:-----------|
| date      | str    | 日期       |
| symbol    | str    | 股票代码   |
| open      | double | 开盘价     |
| close     | double | 收盘价     |
| high      | double | 最高价     |
| low       | double | 最低价     |
| volume    | double | 成交量     |
| amount    | double | 成交额     |
| pre_close | double | 前日收盘价 |

#### 1.4. 使用示例

##### 1.4.1. 获取单支港股的部分回测因子

```python
import tqx_data
result = tqx_data.get_factor(
    symbol="0700.HK",
    start_date="20260101",
    end_date="20260131",
    type="hk",
    factors=["symbol", "date", "close"],
)
print(result)
```

**响应示例**

```text
symbol date close
0 0700.HK 20260130 678.9326
1 0700.HK 20260129 696.8582
2 0700.HK 20260128 695.7379
3 0700.HK 20260127 680.0530
4 0700.HK 20260126 671.6503
5 0700.HK 20260123 666.6088
6 0700.HK 20260122 669.4096
7 0700.HK 20260121 675.0114
8 0700.HK 20260120 673.3309
9 0700.HK 20260119 683.4140
10 0700.HK 20260116 691.8166
11 0700.HK 20260115 696.8582
12 0700.HK 20260114 709.1821
13 0700.HK 20260113 703.0202
14 0700.HK 20260112 697.9786
15 0700.HK 20260109 684.5344
16 0700.HK 20260108 690.1361
17 0700.HK 20260107 699.6591
18 0700.HK 20260106 708.6219
19 0700.HK 20260105 699.6591
20 0700.HK 20260102 697.9786
```

##### 1.4.2. 获取单支美股的部分回测因子

```python
import tqx_data
result = tqx_data.get_factor(
    symbol="AAPL.NB",
    start_date="20260101",
    end_date="20260131",
    type="nb",
    factors=["symbol", "date", "volume"],
)
print(result)
```

**响应示例**

```text
symbol date volume
0 AAPL.NB 20260130 92443408.0
1 AAPL.NB 20260129 67253009.0
2 AAPL.NB 20260128 41287971.0
3 AAPL.NB 20260127 49648271.0
4 AAPL.NB 20260126 55969234.0
5 AAPL.NB 20260123 41688982.0
6 AAPL.NB 20260122 39708340.0
7 AAPL.NB 20260121 54641725.0
8 AAPL.NB 20260120 80267517.0
9 AAPL.NB 20260116 72142773.0
10 AAPL.NB 20260115 39388564.0
11 AAPL.NB 20260114 40019421.0
12 AAPL.NB 20260113 45730847.0
13 AAPL.NB 20260112 45263767.0
14 AAPL.NB 20260109 39996967.0
15 AAPL.NB 20260108 50419337.0
16 AAPL.NB 20260107 48309804.0
17 AAPL.NB 20260106 52352090.0
18 AAPL.NB 20260105 45647190.0
19 AAPL.NB 20260102 37838054.0
```

### 2. 获取财务季度报告

#### 2.1. 方法名：get_financial_statement

#### 2.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| symbol | Optional\[Union\[str, list\]\] | 股票代码；港股 `.HK`、美股 `.NB`。`None`、空字符串或空列表都会查询全市场 | 非必填 |
| start_quarter | str | 起始财期，格式为 `YYYYqN`，大小写均可 | 必填 |
| end_quarter | str | 结束财期，格式为 `YYYYqN`，大小写均可；与起始财期合计最多覆盖 5 个自然年 | 必填 |
| date | Optional\[str\] | 公告日期上限，格式为 `YYYYMMDD` 或 `YYYY-MM-DD`，返回该日及之前的数据 | 非必填；历史研究和回测必须填写 |
| is_latest | Optional\[bool\] | `True`：每个 `symbol` 只保留公告日期最大的一行；`False`：返回范围内全部财期和披露记录。默认为 `True` | 非必填 |
| market | str | `hk` 或 `nb`，大小写均可；函数默认 `hk`，但策略代码必须显式传入 | 非必填 |
| fields | Optional\[Union\[str, list\]\] | 返回字段；推荐明确传列表。接口会自动补充 `symbol`、`fy_period`、`date` | 非必填 |
| interim_type | str | 报表口径，可选 `cumulative`（累计，默认）或 `single`（单季） | 非必填 |

#### 2.2.1. `is_latest` 选择规则（生产环境实测）

`is_latest` 的粒度是**每只股票**，不是“每只股票的每个财期”：

- `is_latest=True`：适合查询“截至某日，每只股票最新披露的一份财报”的单期快照。即使季度范围包含
  多个财期，最终通常每只股票只有一行。
- `is_latest=False`：适合收入同比、环比、多期趋势、历史截面、动态券池和回测。返回数据后仍要按
  `(symbol, fy_period)` 选择公告日期最新的版本，不能直接使用可能存在重复披露的全部行。
- 历史研究和回测两种模式都必须传 `date=<截面日或调仓日>`。省略 `date` 会使用当前数据集中最新披露，
  可能把回测日期之后的财报带入策略，造成未来数据泄漏。

2026-07-25 在生产算力节点用 `date="20250101"`、`2023q1~2024q4` 做过港美股对照验证：

| 市场与标的 | `is_latest=False` | `is_latest=True` | 截止日前最新财期 |
|---|---:|---:|---|
| 美股 `NVDA.NB`、`AVGO.NB` | 16 行，每股 8 行 | 2 行，每股 1 行 | `FY2024Q4` |
| 港股 `1810.HK`、`3690.HK` | 14 行，每股 7 行 | 2 行，每股 1 行 | `FY2024Q3` |

同一测试省略 `date` 后，美股返回了公告日期为 `20260225/20260609` 的记录，港股返回了
`20260526/20260601` 的记录。若策略回测时间是 2025 年，这些记录在当时不可见，因此禁止用于历史决策。

#### 2.2.2. 全参数生产测试经验

2026-07-25 在生产算力节点逐项验证了全部参数，使用经验如下：

| 参数 | 实测结果 | 使用规则 |
|---|---|---|
| `start_quarter`、`end_quarter` | 必填；`2024q1` 和 `2024Q1` 均可；超过 5 个自然年报错。生产版本对结束早于开始曾返回空表 | 调用前自行校验格式、跨度及 `start <= end`，不能依赖后端一定报错 |
| `market` | `hk`、`nb` 及大写形式成功；`us` 报错 | 美股必须用 `nb`，港股用 `hk`，始终显式传入 |
| `symbol` | 字符串和列表成功；`None`、`""`、`[]` 都变成全市场，本次美股样本返回 5095 只 | 策略查询候选池时禁止传空值；全市场查询必须是明确意图并限制字段和财期 |
| `fields` | 字符串和列表均成功；缺少三列时接口自动补充；`None` 或 `[]` 返回约 1363 列；不存在的字段被静默忽略 | 推荐非空列表；返回后必须检查每个请求字段确实存在，不能只检查调用成功 |
| `date` | `20250101` 与 `2025-01-01` 结果一致；`2025/01/01` 报错；`None` 不限制公告日 | 历史策略必须传入，且断言返回的最大公告日期不晚于决策日 |
| `is_latest` | `True` 两只股票返回 2 行；`False` 返回 8 行 | 单份最新公告用 `True`；同比和动态多期面板用 `False` |
| `interim_type` | `cumulative` 返回数据；`single` 是合法值，但本次美股样本区间返回空表；其他值报错 | 默认并优先使用 `cumulative`；使用 `single` 前必须验证目标市场、股票和财期确有数据 |

`fields` 的静默忽略尤其危险。例如请求 `fields=["not_a_real_field"]` 没有报错，只返回了自动补充的
`symbol`、`fy_period`、`date`。因此 Agent 必须在计算前执行 `required_fields <= set(df.columns)` 检查。

#### 2.2.3. 一年回测的动态时点规则

财报大致按季度披露，但不同公司公告日期不同。若基本面决定股票资格，一年回测必须在每个调仓日重新
计算 point-in-time 财务因子；不能把回测起点的合格券池固定使用一年。生产测试得到：

| 截面日 | `3690.HK` 最新可见财期 | 收入同比 | 毛利率 | 经营现金流 | 是否通过三项硬条件 |
|---|---|---:|---:|---:|---|
| `20250101` | `FY2024Q3` | 22.68% | 38.67% | 40,284,393,000 | 是 |
| `20250701` | `FY2025Q1` | 18.12% | 37.45% | 10,131,128,000 | 否 |
| `20251001` | `FY2025Q2` | 14.71% | 35.22% | 14,348,525,000 | 否 |
| `20260101` | `FY2025Q3` | 9.95% | 32.13% | -7,243,689,000 | 否 |

这不是未来数据问题，而是静态券池使用了已经过期的基本面。正确动态流程是：

1. 取得整个回测所需的多期财报，使用 `is_latest=False`，并以回测结束日作为接口最大 `date`。
2. 对每个调仓日先筛选 `announcement date <= rebalance date`。
3. 在该可见子集中按 `(symbol, fy_period)` 保留公告日期最新的版本。
4. 按公司财期选择当时可见的最新财期，匹配上年同财期并计算因子。
5. 形成包含 `date`、`symbol`、`fy_period`、`source_date`、各因子和 `eligible` 的面板。
6. 交易时只读取 `panel.date <= context.now` 的最近截面；有新公告就在下一调仓日更新，没有则沿用旧值。

顺序不能改成“先对回测结束日全部数据去重，再按调仓日过滤”，否则后续重述版本可能覆盖早期当时可见的
版本。每个截面必须验证 `max(source_date) <= rebalance_date`。

#### 2.3. 响应参数

##### 2.3.1. 响应参数

| 字段      | 类型   | 描述                             |
|:----------|:-------|:---------------------------------|
| symbol    | str    | 股票代码                         |
| fields    | double | 需要返回的财务字段(见数据库设计) |
| fy_period | str    | 财务年时间段                     |

以下为财务相关字段

现金流量表(cfs)

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| cfs_cash_receipts_business | Double | 现金收入 - 业务活动 - 现金流量 |
| cfs_cash_receipts_sales | Double | 现金收入 - 商品和服务销售 - 现金流量 |
| cfs_cash_receipts_other_customers | Double | 现金收入 - 其他 - 客户 - 现金流量 |
| cfs_premiums_received | Double | 收到的保费 - 现金流量 |
| cfs_reinsurance_recovered | Double | 再保险收回 - 现金流量 |
| cfs_fees_received | Double | 收到的费用 - 现金流量 |
| cfs_inv_income_received | Double | 投资收入 - 收到 - 现金流量 |
| cfs_cash_receipts_other | Double | 现金收入 - 其他 - 现金流量 |
| cfs_cash_receipts_banking_inv | Double | 现金收入 - 银行及投资相关活动 - CF |
| cfs_cash_payments_business | Double | 现金支付 - 业务活动 - 现金流量 |
| cfs_cash_payments_suppliers | Double | 现金支付 - 商品和服务供应商 - 现金流量 |
| cfs_reinsurance_paid | Double | 支付再保险 - 现金流 |
| cfs_claims_paid | Double | 已支付的索赔 - 现金流量 |
| cfs_cash_payments_int_banking_liab | Double | 现金支付 - 银行相关负债支付的利息 - CF |
| cfs_cash_payments_employees | Double | 现金支付 - 员工 - 现金流量 |
| cfs_fees_paid | Double | 支付的费用 - 现金流量 |
| cfs_cash_payments_other | Double | 现金支付 - 其他 - 现金流量 |
| cfs_income_taxes_paid_reimbursed | Double | 所得税 - 已付/（已报销） - 现金流量 |
| cfs_interest_paid_cash_direct | Double | 支付利息 - 现金（现金流量 - 直接） |
| cfs_int_div_received_cash_direct | Double | 利息和股息 - 已收 - 总计 - 现金流量 - 直接 |
| cfs_cash_receipts_payments_net | Double | 现金收入/（付款）-净额-现金流量 |
| cfs_cash_receipts_payments_associates | Double | 现金收入/（付款） - 联营公司 - 现金流量 |
| cfs_profit_loss_starting | Double | 利润/（亏损） - 起始线 - 现金流量 |
| cfs_non_cash_adj | Double | 非现金项目和调节调整 - 现金流量 |
| cfs_extraordinary_after_tax_reconcile | Double | 税后非常项目 - 现金流量 - 调节 |
| cfs_minority_interest_reconcile | Double | 少数股东权益 - 现金流量 - 调节 |
| cfs_discontinued_ops_net_tax_reconcile | Double | 终止经营 - G/(L) - 税后净额 - CF - 调节 |
| cfs_equity_earnings_reconcile | Double | 净收益中的权益公司/（损失） - CF - 进行调节 |
| cfs_accounting_change_reconcile | Double | 会计变更 - 现金流量 - 调节 |
| cfs_income_tax_expense_reconcile | Double | 所得税费用 - 现金流量 - 调节 |
| cfs_financing_income_expense_reconcile | Double | 财务收入/（支出）-现金流量-调节 |
| cfs_other_non_cash_adj | Double | 其他非现金项目和调整 - CF - 调节 |
| cfs_depr_depletion_amort_impair_reconcile | Double | 折旧、损耗和摊销，包括减值 -CF 进行调节 |
| cfs_depr_depletion_ppe_reconcile | Double | 折旧和消耗 - PPE - CF - 协调 |
| cfs_accretion_aro_reconcile | Double | 资产报废义务的增加 - CF - 调节 |
| cfs_impairment_ppe_intang_reconcile | Double | 减值 - PPE，包括无形资产 - CF - 调节 |
| cfs_impairment_inv_property_reconcile | Double | 减值 - 投资性房地产 - 现金流量 |
| cfs_amort_intang_deferred_charges_reconcile | Double | 摊销 - Intang 和递延 Chrgs - CF - 调节 |
| cfs_amort_deferred_policy_acq_reconcile | Double | 摊销 - 递延保单取得成本 - 调节 |
| cfs_amort_other_intang_deferred_reconcile | Double | 摊销 - 其他无形资产和递延 Chrgs - 调节 |
| cfs_loan_loss_provision_impairment_reconcile | Double | 包括减值在内的贷款损失拨备 - 增量/（减量） - CF |
| cfs_impairment_fin_fixed_assets_reconcile | Double | 金融固定资产减值 - CF - 调节 |
| cfs_otti_losses_reconcile | Double | 投资损失 - 暂时性减值除外 - CF |
| cfs_deferred_tax_credits_reconcile | Double | 递延公司税和所得税抵免 - CF - 协调 |
| cfs_asset_sale_gl_reconcile | Double | 资产出售 - 收益/（损失） - 现金流量 - 调节 |
| cfs_ppe_intang_sale_gl_reconcile | Double | PPE，包括无形资产 - 收益/（损失） - CF |
| cfs_inv_trading_property_realized_gl_reconcile | Double | 投资和交易财产 - 已实现 G/(L) CF 调节 |
| cfs_inv_sec_gl_reconcile | Double | 投资证券 - 收益/（损失） - 现金流量 |
| cfs_fin_assets_unrealized_gl_reconcile | Double | 金融资产 - 未实现 G/(L) - CF - 调节 |
| cfs_inv_property_unrealized_gl_reconcile | Double | 投资性房地产 - 未实现收益/（损失） - 现金流量 |
| cfs_share_based_payments_reconcile | Double | 基于股份的支付 - 现金流量 - 调节 |
| cfs_income_taxes_paid_reimbursed | Double | 所得税 - 已付/（已报销） - 现金流量 |
| cfs_interest_paid_cash | Double | 支付利息 - 现金 |
| cfs_int_div_received_total | Double | 利息和股息 - 已收 - 总计 - 现金流量 |
| cfs_distributions_non_consolidated_real_estate | Double | 收到的分配 - 非 Con 房地产实体 - CF |
| cfs_cf_operating_before_wc | Double | 营运上限变动前的经营活动现金流量 |
| cfs_wc_increase_decrease | Double | 营运资金 - 增加/（减少） - 现金流量 |
| cfs_receivables_finance_lease_change | Double | 应收账款 - 融资和租赁 - 减少/（增加） - CF |
| cfs_accounts_receivable_change | Double | 应收账款 - 减少/（增加） - 现金流量 |
| cfs_inventories_change | Double | 库存 - 减少/（增加） - 现金流量 |
| cfs_segregated_cash_change | Double | 独立现金 - 减少/（增加） - 现金流量 |
| cfs_lending_deposits_banks_lt_change | Double | 贷款和存款 - 应收银行款项 - LT - Decr/(Incr) - CF |
| cfs_inv_sec_change_operating | Double | 投资证券 - 减少/（增加） - 运营 CF |
| cfs_inv_sec_purchased_operating | Double | 投资证券 - 购买 - 运营 - 现金流量 |
| cfs_inv_sec_sold_matured_operating | Double | 投资证券 - 已出售/到期 - 运营 - 现金流量 |
| cfs_insurance_receivables_change | Double | 保险应收账款减少/（增加）-现金流量 |
| cfs_deferred_policy_acq_costs_change | Double | 递延保单获取成本 - 减少/（增加） - CF |
| cfs_loans_customer_change | Double | 贷款 - 客户 - 减少/（增加） - 现金流量 |
| cfs_loans_origination_purchase | Double | 贷款 - 发放/购买 - 现金流 |
| cfs_loans_repayments_sales | Double | 贷款 - 还款/销售 - 现金流量 |
| cfs_prepaid_expenses_change | Double | 预付费用 - 减少/（增加） - 现金流量 |
| cfs_other_assets_change | Double | 其他资产 - 减少/（增加） - 现金流量 |
| cfs_collateralized_agreements_assets_change | Double | 抵押协议（资产） - Decr/（Incr） - CF |
| cfs_accounts_payable_change | Double | 应付账款 - 增加/（减少） - 现金流量 |
| cfs_accrued_expenses_change | Double | 应计费用 - 增加/（减少） - 现金流量 |
| cfs_insurance_provisions_change | Double | 保险准备金 - 增加/（减少） - 现金流量 |
| cfs_deposits_change_total | Double | 存款 - 增加/（减少） - 总计 - 现金流量 |
| cfs_deposits_banks_fi_change | Double | 存款 - 存入银行和金融机构 - 增量/（减量） CF |
| cfs_deposits_customers_change | Double | 存款 - 客户 - 增加/（减少） - 现金流量 |
| cfs_insurance_payables_reinsurance_change | Double | 保险应付账款（包括再保险） - 增量/（减量） - CF |
| cfs_accounts_payable_accrued_change | Double | 应付帐款和应计费用 - 增量/（减量） - CF |
| cfs_trading_liabilities_change | Double | 交易负债 - 增加/（减少） - 现金流量 |
| cfs_taxes_payable_change | Double | 应交税费 - 增加/（减少） - 现金流量 |
| cfs_op_lease_liabilities_change | Double | 经营租赁负债 - 增加/（减少） - CF |
| cfs_other_liabilities_change_total | Double | 其他负债 - 增加/（减少） - 总计 - 现金流量 |
| cfs_collateralized_agreements_liab_change | Double | 抵押协议（负债） - 增量/（减量） - CF |
| cfs_other_assets_liabilities_change_net | Double | 其他资产和负债 - 增加/（减少） - 净额 - CF |
| cfs_net_cf_operating | Double | 经营活动产生的现金流量净额 |
| cfs_capex_net | Double | 资本支出 - 净额 - 现金流量 |
| cfs_ppe_purchased_sold_net | Double | 财产、厂房和设备 - 购买/（出售） - 净值 - CF |
| cfs_ppe_purchased | Double | 财产厂房和设备 - 购买 - 现金流量 |
| cfs_lease_equipment_purchased | Double | 租赁设备 - 购买 - 现金流量 |
| cfs_ppe_sold | Double | 出售的财产厂房和设备 - 现金流量 |
| cfs_lease_equipment_sold | Double | 租赁设备 - 出售 - 现金流量 |
| cfs_inv_property_purchased_sold_net_reit | Double | 投资物业购买/（出售）净额 - 总计 - REIT - CF |
| cfs_inv_property_purchased_reit | Double | 投资物业 - 购买 - REIT - 现金流量 |
| cfs_inv_property_capex_improve_maint | Double | 资本支出 - 投资物业改进和维护 CF |
| cfs_inv_property_sold_reit | Double | 投资物业 - 已售 - 房地产投资信托基金 - 现金流量 |
| cfs_intangible_purchased_sold_net | Double | 无形资产 - 购买/（出售） - 净额 - 总计 - CF |
| cfs_intangible_purchased_acquired | Double | 无形资产 - 购买/获得 - 现金流量 |
| cfs_intangible_sold | Double | 无形资产 - 出售 - 现金流量 |
| cfs_software_development_costs | Double | 软件开发成本 - 现金流 |
| cfs_intangible_assets_net_cf | Double | 无形资产 - 净额 - 现金流量 |
| cfs_capex_total | Double | 资本支出 - 总计 |
| cfs_business_acquisition_disposal_net | Double | 收购和处置已出售/（收购）业务净额 - CF |
| cfs_business_acquisition | Double | 收购业务 - 现金流量 |
| cfs_business_sold | Double | 业务 - 出售 - 现金流量 |
| cfs_investments_excl_loans_change | Double | 不包括贷款的投资 - 减少/（增加） - CF |
| cfs_inv_property_excl_capex_change | Double | 投资物业不包括资本支出 - 已售/（购买） - 净额 - CF |
| cfs_inv_sec_sold_purchased_net | Double | 未分类投资证券 - 已售/（购买）净值 CF 总额 |
| cfs_inv_sec_sold_matured | Double | 投资证券 - 已出售/到期 - 未分类 - CF |
| cfs_inv_sec_purchased | Double | 投资证券 - 购买 - 未分类 - 现金流量 |
| cfs_fhlb_stock_sold_purchased_net | Double | FHLB 股票 - 已售/（已购买） - 净额 - 现金流量 |
| cfs_inv_associate_jv_sold_purchased | Double | 投资 - 联营公司和合资企业 - 出售/（购买） - CF |
| cfs_real_estate_jv_payments | Double | 房地产合资企业 - 收购付款 - 现金流量 |
| cfs_deriv_hedge_sold_purchased_total | Double | 衍生金融工具对冲卖出/（买入）CF总计 |
| cfs_inv_loans_change_net | Double | 贷款投资 - 减少/（增加） - 净额 - 现金流量 |
| cfs_other_inv_cf_change | Double | 其他投资现金流 - 减少/（增加） |
| cfs_net_cf_investing | Double | 投资活动产生的净现金流量 |
| cfs_dividends_paid_cash_total | Double | 已付股息 - 现金 - 总计 - 现金流量 |
| cfs_common_dividends_paid | Double | 股息 - 普通股 - 现金支付 |
| cfs_preferred_dividends_paid | Double | 股息 - 优先 - 现金支付 |
| cfs_policyholder_accounts_deposits_withdrawals_net | Double | 保单持有人账户 - 存款/（取款） - 净额 - CF |
| cfs_policyholder_deposits | Double | 存款 - 保单持有人账户 - 现金流量 |
| cfs_policyholder_withdrawals | Double | 保单持有人账户提款 - 现金流 |
| cfs_stock_issuance_retirement_net | Double | 股票 - 总计 - 发行/（退出） - 净额 - 现金流量 |
| cfs_stock_issuance_retirement_excl_options | Double | 股票 - 发行/（退役）净额，不包括期权/认股权证 - CF |
| cfs_stock_common_pref_other_issuance_retirement_net | Double | 股票 - 普通优先股和其他发行/（退休）净 CF |
| cfs_stock_common_pref_other_issued | Double | 股票 - 普通优先股和其他 - 发行/出售 - 现金流量 |
| cfs_stock_common_pref_other_repurchased | Double | 股票 - 普通优先股和其他 - 回购/退役 - CF |
| cfs_common_stock_issuance_retirement_net | Double | 股票 - 普通 - 发行/（退出） - 净额 - 现金流量 |
| cfs_common_stock_issued | Double | 股票 - 普通股 - 发行/出售 - 现金流量 |
| cfs_common_stock_repurchased | Double | 股票 - 普通股 - 回购/退役 - 现金流量 |
| cfs_pref_stock_issuance_retirement_net | Double | 股票 - 优先股 - 发行/（退出） - 净额 - 现金流量 |
| cfs_pref_stock_issued | Double | 股票 - 优先股 - 发行/出售 - 现金流量 |
| cfs_pref_stock_repurchased | Double | 股票 - 优先股 - 回购/退役 - 现金流量 |
| cfs_other_equity_issuance_retirement_net | Double | 股票 - 其他股权 - 发行/（退出） - 净额 - CF |
| cfs_other_equity_issued | Double | 股票 - 其他股权 - 已发行/出售 - 现金流量 |
| cfs_other_equity_repurchased | Double | 股票 - 其他股权 - 回购/退役 - 现金流量 |
| cfs_options_exercised | Double | 已行使期权 - 现金流量 |
| cfs_warrants_converted | Double | 认股权证转换 - 现金流量 |
| cfs_minority_interests_jv_net | Double | 少数股东权益和合资企业 - 净额 - 现金流量 |
| cfs_debt_lt_st_issuance_retirement_total | Double | 债务 - LT 和 ST - 发行/（收回） - 总计 - CF |
| cfs_debt_issued_reduced_lt_st | Double | 债务 - 已发行/（减少） - 长期和短期 - 现金流量 |
| cfs_debt_issued_lt_st | Double | 债务 - 已发行 - 长期和短期 - 现金流量 |
| cfs_debt_reduced_lt_st | Double | 债务 - 减少 - 长期和短期 - 现金流 |
| cfs_debt_issued_reduced_st_total | Double | 债务 - 已发行/（减少） - 短期 - 总计 - 现金流量 |
| cfs_debt_issued_st | Double | 债务 - 已发行 - 短期 - 现金流量 |
| cfs_debt_reduced_st | Double | 债务 - 减少 - 短期 - 现金流 |
| cfs_debt_issued_reduced_lt | Double | 债务 - 已发行/（减少） - 长期 - 现金流量 |
| cfs_debt_issued_lt | Double | 债务 - 已发行 - 长期 - 现金流量 |
| cfs_debt_reduced_lt | Double | 债务 - 减少 - 长期 - 现金流 |
| cfs_lease_liabilities_issued_reduced | Double | 租赁负债 - 已发行/（减少） - 现金流量 |
| cfs_lease_liabilities_issued | Double | 租赁负债 - 已发行 - 现金流量 |
| cfs_lease_liabilities_reduced | Double | 租赁负债 - 减少 - 现金流量 |
| cfs_collateralized_agreements_liab_change | Double | 抵押协议（负债） - 增量/（减量） - CF |
| cfs_repo_liabilities_change | Double | REPO 负债 - 增加/（减少） - 现金流量 |
| cfs_hybrid_financial_liab_change | Double | 混合金融工具（负债）- 增量/（减量）CF |
| cfs_other_financing_cf_change | Double | 其他融资现金流 - 增加/（减少） |
| cfs_net_cf_financing | Double | 筹资活动产生的现金流量净额 |
| cfs_discontinued_ops_cf_operating | Double | 终止经营业务产生的净现金流量 - 经营活动 |
| cfs_discontinued_ops_cf_investing | Double | 终止经营业务产生的净现金流量 - 投资活动 |
| cfs_discontinued_ops_cf_financing | Double | 终止经营业务产生的净现金流量 - 融资活动 |
| cfs_discontinued_ops_cf_other | Double | 终止经营业务产生的净现金流量 - 其他 |
| cfs_discontinued_ops_cf_total | Double | 终止经营业务产生的净现金流量 - 总计 |
| cfs_non_classified_cf | Double | 非分类现金流量 |
| cfs_fx_effects_cf | Double | 外汇影响 - 现金流量 |
| cfs_net_change_cash | Double | 现金净变化 - 总计 |
| cfs_net_cf_continuing_ops | Double | 持续经营业务产生的净现金 |
| cfs_net_cf_discontinued_ops | Double | 终止经营业务产生的净现金 |
| cfs_cash_beginning_balance | Double | 净现金 - 期初余额 |
| cfs_cash_ending_balance | Double | 净现金 - 期末余额 |
| cfs_income_taxes_paid_reimbursed_supp | Double | 所得税 - 已付/（已报销） - 现金流量 - 补充 |
| cfs_interest_paid_cf_supp | Double | 已付利息 - 现金流量 - 补充 |
| cfs_interest_fin_leases_paid_supp | Double | 支付的融资租赁利息 - 现金流量 - 补充 |
| cfs_int_div_received_supp | Double | 利息和股息 - 收到 - 现金流量 - 补充 |
| cfs_wc_cf_direct_supp | Double | 营运资金 - 现金流量 - 直接 - 补充 |
| cfs_cf_operating_before_wc_int | Double | 工作上限和国际变动前运营活动产生的现金流 |
| cfs_non_gaap_free_cf | Double | 非公认会计原则自由现金流 - 公司报告 |
| cfs_contract_assets_change | Double | 合同资产 - 减少/（增加） - 现金流量 |
| cfs_contract_liabilities_change | Double | 合同负债 - 增加/（减少） - 现金流量 |
| cfs_contract_assets_liabilities_net_cf | Double | 合同资产/负债 – 净额 – 现金流量 |
| cfs_cash_dividends_common_buyback_net | Double | 支付现金股息和普通股回购 - 净额 |
| cfs_common_stock_buyback_net | Double | 普通股回购 - 净额 |
| cfs_depr_depletion_amort_cf | Double | 折旧消耗和摊销 - 现金流量 |
| cfs_free_cf_to_equity | Double | 股本自由现金流 |
| cfs_free_operating_cf | Double | 自由经营现金流 |
| cfs_levered_free_operating_cf | Double | 杠杆自由经营现金流 |
| cfs_dividends_provided_paid_common | Double | 提供/支付的股息 - 普通 |
| cfs_reported_cf_operating | Double | 报告 - 来自经营活动的现金 |
| cfs_reported_cf_investing | Double | 报告 - 来自投资活动的现金 |
| cfs_reported_cf_financing | Double | 报告 - 来自融资活动的现金 |

资产负债表(bs)

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| bs_cash_and_short_term_investments | Double | 现金和短期投资 |
| bs_cash_and_cash_equivalents | Double | 现金及现金等价物 |
| bs_short_term_investments | Double | 短期投资 - 总计 |
| bs_financial_assets_st | Double | 金融资产 - 短期 |
| bs_cash_and_short_term_deposits_banks_total | Double | 现金和短期银行存款 - 总计 |
| bs_cash_and_short_term_deposits_banks | Double | 现金和短期银行存款 |
| bs_funds_central_banks | Double | 中央银行资金 |
| bs_lending_long_term_deposits_banks | Double | 银行贷款和长期存款 |
| bs_interbank_loans_deposits | Double | 同业拆借及同业长期存款 |
| bs_money_market_placements | Double | 货币市场配置 |
| bs_collateralized_agreements_rev_repos | Double | 抵押协议 Rev REPO 和 Sec 借入 - 资产 |
| bs_securities_collateral | Double | 抵押品下持有的证券 |
| bs_securities_purchased_repos_fed_funds | Double | 根据回购协议购买的证券和出售的联邦基金 |
| bs_securities_purchased_repos | Double | 根据回购协议购买的证券 |
| bs_fed_funds_sold_assets | Double | 出售的联邦基金 - 资产 |
| bs_securities_purchased_repos_fed_funds_total | Double | 根据回购协议购买的证券和出售的联邦基金总计 |
| bs_securities_borrowed | Double | 借入证券 |
| bs_deriv_hedge_st | Double | 衍生金融工具 - 对冲 - 短期 |
| bs_deriv_hedge_total | Double | 衍生金融工具 - 对冲 - 总计 |
| bs_loans_receivables_net_st | Double | 贷款和应收账款 - 净额 - 短期 |
| bs_trade_receivables_net | Double | 贸易账户和应收贸易票据 - 净额 |
| bs_trade_receivables_gross | Double | 贸易账户和应收贸易票据 - 总额 |
| bs_provision_trade_receivables | Double | 规定 - 贸易账户和应收贸易票据 |
| bs_unbilled_utility_revenue_st | Double | 未开票公用事业收入 - 短期 |
| bs_loans_st | Double | 贷款 - 短期 |
| bs_finance_lease_receivables_st | Double | 融资租赁应收款 - 短期 |
| bs_income_tax_receivables_st | Double | 所得税 - 应收账款 - 短期 |
| bs_other_receivables | Double | 应收账款 - 其他 - 总计 |
| bs_provision_doubtful | Double | 规定 - 呆账 |
| bs_receivables_over_one_year_st | Double | 一年以上应收款计入短期应收款 |
| bs_loans_receivables_total | Double | 贷款和应收账款 - 总计 |
| bs_banking_loans_net | Double | 银行相关贷款 - 净额 |
| bs_loans_gross | Double | 贷款 - 总额 |
| bs_consumer_installment_loans | Double | 贷款 - 消费及分期付款 |
| bs_finance_lease_hp_loans | Double | 贷款 - 融资租赁和惠普 |
| bs_commercial_industrial_loans | Double | 贷款 - 商业和工业 |
| bs_broker_fi_loans | Double | 贷款 - 经纪人和金融机构 |
| bs_other_customer_loans_gross | Double | 贷款 - 客户 - 其他 - 总额 |
| bs_foreign_loans | Double | 贷款 - 国外 |
| bs_mortgage_real_estate_loans | Double | 贷款 - 抵押贷款/房地产 |
| bs_loans_held_for_sale | Double | 贷款 - 持有待售 |
| bs_unearned_customer_income | Double | 非劳动收入 - 客户 |
| bs_loan_loss_reserves | Double | 贷款损失准备金 |
| bs_trade_receivables_total | Double | 贸易账款和应收贸易票据 - 总计 |
| bs_trade_receivables_gross_total | Double | 应收帐款和应收票据 - 贸易 - 总额 - 总计 |
| bs_provision_doubtful_trade_payable | Double | 提供可疑贸易账款和应付商业票据总计 |
| bs_receivables_brokers_clearing | Double | 来自客户经纪人和清算组织的应收账款 |
| bs_finance_lease_receivables_net_lt_st | Double | 融资租赁应收款 - 净额 - 长期和短期 |
| bs_finance_lease_receivables_gross_lt_st | Double | 融资租赁应收款 - 长期和短期 - 总额 |
| bs_provision_finance_lease_receivables | Double | 拨备 - 应收融资租赁款 - 长期和短期 |
| bs_unearned_income_finance_lease | Double | 非劳动收入 - 融资租赁 - 长期和短期 |
| bs_interest_receivables_bank | Double | 应收利息 - 银行 |
| bs_receivables_total | Double | 应收账款 - 总计 |
| bs_insurance_premium_receivables | Double | 应收保险费 |
| bs_income_tax_receivables | Double | 所得税 - 应收账款 |
| bs_other_receivables | Double | 应收账款 - 其他 |
| bs_provision_doubtful_total | Double | 拨备 - 呆账 - 总计 |
| bs_inventories_total | Double | 库存 - 总计 |
| bs_raw_materials | Double | 库存 - 原材料 |
| bs_work_in_progress | Double | 库存 - 进行中的工作 |
| bs_finished_goods | Double | 库存 - 产成品 |
| bs_inventories_other | Double | 库存 - 其他 - 总计 |
| bs_cost_in_excess_billings | Double | 库存 - 成本超过比林斯 |
| bs_gas_in_storage | Double | 库存 - 储存气体 |
| bs_lifo_reserve | Double | 库存 - LIFO 储备 |
| bs_biological_assets_st | Double | 生物资产 - 短期 |
| bs_prepaid_expenses_st | Double | 预付费用 - 短期 |
| bs_assets_held_for_sale_st | Double | 持有待售资产/终止经营——短期 |
| bs_other_current_assets_total | Double | 其他流动资产 - 总计 |
| bs_deferred_tax_asset_st | Double | 递延税 - 资产 - 短期 |
| bs_deferred_costs_st | Double | 递延成本 - 短期 |
| bs_restricted_accounts_st | Double | 受限账户 - 短期 |
| bs_regulatory_assets_st | Double | 监管资产 - 短期 |
| bs_other_current_assets | Double | 其他流动资产 |
| bs_total_current_assets | Double | 流动资产总额 |
| bs_investments_lt | Double | 投资 - 长期 |
| bs_segregated_cash_deposits_inv | Double | 隔离 - 现金存款和投资 |
| bs_investments_including_loans | Double | 包括贷款在内的投资 - 总计 |
| bs_investments_total | Double | 投资 - 总计 |
| bs_inv_sec_afs_htm_hft_total | Double | 投资证券 - 可供出售、HTM 和 HFT - 总计 |
| bs_inv_sec_trading | Double | 投资证券 - 为交易而持有 |
| bs_inv_sec_afs_htm | Double | 可供出售并持有至到期的投资证券 |
| bs_inv_sec_afs_total | Double | 投资证券 - 可供出售 - 总计 |
| bs_mbs_afs_htm | Double | 可供出售/持有至到期的抵押贷款支持证券 |
| bs_govt_sec_afs_htm | Double | 政府证券 - 可供出售/持有至到期 |
| bs_inv_sec_fair_value_other | Double | 投资证券 - 以公允价值指定 - 其他 |
| bs_inv_sec_fixed_income | Double | 投资证券 - 固定收益 |
| bs_inv_sec_equity | Double | 投资证券 - 股票 |
| bs_affiliated_non_controlled | Double | 关联公司 - 非控制 |
| bs_non_affiliated_non_controlled | Double | 非关联公司 - 非控制 |
| bs_inv_sec_other | Double | 投资证券 - 其他 |
| bs_commodities | Double | 商品 |
| bs_fhlb_stock | Double | FHLB 股票 - 资产 |
| bs_investment_property | Double | 投资物业 |
| bs_investment_property_net | Double | 投资物业 - 净额 |
| bs_investment_property_gross | Double | 投资物业 - 总额 |
| bs_inv_property_acc_depr_impair | Double | 投资性房地产 - 累计折旧和减值 |
| bs_private_equity_other_inv | Double | 投资 - 私募股权及其他 - 总计 |
| bs_other_inv_total | Double | 投资 - 其他 - 总计 |
| bs_mortgage_policy_loans_other | Double | 贷款 - 抵押贷款政策及其他 |
| bs_policy_loans | Double | 保单贷款 |
| bs_other_loans | Double | 贷款 - 其他 |
| bs_inv_afs_htm_lt | Double | 投资 - 可供出售/持有至到期 - 长期 |
| bs_marketable_sec_lt | Double | 有价证券 - 长期 |
| bs_financial_assets_lt | Double | 金融资产 - 长期 |
| bs_inv_associate_jv_unconsolidated | Double | 对联营公司、合资公司和 Unconsol 子公司的投资 |
| bs_receivables_loans_lt | Double | 应收账款和贷款 - 长期 |
| bs_trade_receivables_net_lt | Double | 应收账款和应收票据 - 贸易 - 净额 - 长期 |
| bs_trade_receivables_gross_lt | Double | 应收账款和票据 - 贸易 - 总额 - 长期 |
| bs_loans_lt | Double | 贷款 - 长期 |
| bs_finance_lease_receivables_lt | Double | 融资租赁应收款 - 长期 |
| bs_other_receivables_net_lt | Double | 应收账款 - 其他 - 净额 - 长期 |
| bs_provision_doubtful_lt | Double | 规定 - 呆账 - 长期 |
| bs_deriv_hedge_lt | Double | 衍生金融工具 - 对冲 - 长期 |
| bs_ppe_net_total | Double | 房地产厂房和设备 - 净额 - 总计 |
| bs_assets_leased_out_operating_lease_net | Double | 经营租赁项下出租的资产 - 净额 |
| bs_ppe_excl_leased_out_net | Double | PPE - 不包括出租资产 - 净额 - 总计 |
| bs_land_buildings_net | Double | 土地和建筑物 - 网络 |
| bs_land_improvements_net | Double | 土地/改良 - 净额 |
| bs_buildings_net | Double | 建筑物 - 网络 |
| bs_leasehold_improvements_net | Double | 租赁权改善 - 净额 |
| bs_plant_machinery_equipment_net | Double | 工厂机械及设备 - 网 |
| bs_transport_equipment_net | Double | 运输设备 - 网 |
| bs_computer_software_equipment_net | Double | 计算机软件及设备 - 网络 |
| bs_construction_in_progress_net | Double | 在建工程 - 网络 |
| bs_ppe_capital_lease_net | Double | 物业厂房及设备 - 资本租赁 - 净额 |
| bs_rou_tangible_total_net | Double | 使用权有形资产 - 总计 - 净额 |
| bs_rou_operating_lease_net | Double | 有形资产使用权 - 经营租赁 - 净额 |
| bs_rou_cap_fin_lease_net | Double | 有形资产使用权 - 资本/融资租赁 - 净额 |
| bs_ppe_other_net | Double | 物业厂房及设备 - 其他 - 净值 |
| bs_natural_resources_biological_net | Double | 自然资源/生物资产 - 净额 |
| bs_mining_exploration_net | Double | 采矿/勘探特定资产 - 净额 |
| bs_utility_plant_net | Double | 公用事业工厂 - 网络 |
| bs_ppe_gross_total | Double | 房地产厂房和设备 - 总额 - 总计 |
| bs_assets_leased_out_operating_lease_gross | Double | 经营租赁项下出租的资产 - 总额 |
| bs_ppe_excl_leased_out_gross | Double | PPE - 不包括出租资产 - 总额 |
| bs_land_buildings_gross | Double | 土地和建筑物 - 总额 |
| bs_land_improvements_gross | Double | 土地/改良 - 总额 |
| bs_buildings_gross | Double | 建筑物 - 总量 |
| bs_leasehold_improvements_gross | Double | 租赁权益改善 - 总额 |
| bs_plant_machinery_equipment_gross | Double | 工厂机械和设备 - 总量 |
| bs_transport_equipment_gross | Double | 运输设备 - 总量 |
| bs_computer_software_equipment_gross | Double | 计算机软件和设备 - 总额 |
| bs_construction_in_progress_gross | Double | 在建工程 - 总额 |
| bs_ppe_capital_lease_gross | Double | 房地产厂房和设备 - 资本租赁 - 总额 |
| bs_rou_tangible_total_gross | Double | 使用权有形资产 - 总计 - 总额 |
| bs_rou_operating_lease_gross | Double | 使用权有形资产 - 经营租赁 - 总额 |
| bs_rou_cap_fin_lease_gross | Double | 使用权有形资产 - 资本/融资租赁 - 总额 |
| bs_ppe_other_gross | Double | 房地产厂房和设备 - 其他 - 总额 |
| bs_natural_resources_biological_gross | Double | 自然资源/生物资产 - 总额 |
| bs_mining_exploration_gross | Double | 采矿/勘探特定资产 - 总额 |
| bs_utility_plant_gross | Double | 公用设施 - 总量 |
| bs_ppe_acc_depr_impair_total | Double | PPE - 累计折旧和减值 - 总计 |
| bs_assets_leased_out_operating_lease_acc_depr_impair | Double | 根据经营租赁租出的资产 - 累计折旧和减值 |
| bs_ppe_excl_leased_out_acc_depr_impair | Double | PPE - 不包括租赁资产 - 累计折旧和减值 - 总计 |
| bs_land_buildings_acc_depr_impair | Double | 土地和建筑物 - 累计折旧和减值 |
| bs_land_improvements_acc_depr_impair | Double | 土地/改良设施 - 累计折旧和减值 |
| bs_buildings_acc_depr_impair | Double | 建筑物 - 累计折旧和减值 |
| bs_leasehold_improvements_acc_depr_impair | Double | 租赁权益改善 - 累计折旧和减值 |
| bs_plant_machinery_equipment_acc_depr_impair | Double | 厂房、机械和设备 - 累计折旧和减值 |
| bs_transport_equipment_acc_depr_impair | Double | 运输设备 - 累计折旧和减值 |
| bs_computer_software_equipment_acc_depr_impair | Double | 计算机软件和设备 - 累计折旧和减值 |
| bs_construction_in_progress_acc_depr_impair | Double | 在建工程 - 累计折旧和减值 |
| bs_ppe_capital_lease_acc_depr_impair | Double | 资本租赁下的个人防护装备 - 累计折旧和减值 |
| bs_rou_tangible_total_acc_depr | Double | 使用权有形资产总计 - 累计折旧 |
| bs_rou_operating_lease_acc_depr | Double | 有形资产使用权 - 经营租赁 - Accum Depr |
| bs_rou_cap_fin_lease_acc_depr | Double | 有形资产使用权 - 上限/融资租赁 - Accum Depr |
| bs_ppe_other_acc_depr_impair | Double | 财产、厂房和设备 - 其他 - Accum Depr & Impair |
| bs_utility_plant_acc_depr_impair | Double | 公用事业工厂 - 累计折旧和减值 |
| bs_mining_exploration_acc_depr_impair | Double | 采矿/勘探特定资产 - 累积折旧和减值 |
| bs_natural_resources_biological_acc_depr_impair | Double | 自然资源/生物资产 - 累计减值和减值 |
| bs_deferred_policy_acq_costs | Double | 递延保单获取成本 |
| bs_reinsurance_assets | Double | 再保险资产 |
| bs_deposits_held_reinsurance | Double | 存款 - 再保险项下持有 |
| bs_reinsurance_recoverable_insurance_provisions | Double | 再保险可收回 - 在保险条款中 |
| bs_reinsurance_recoverable_unearned_premiums | Double | 再保险可收回 - 未到期保费 |
| bs_reinsurance_recoverable_outstanding_claims | Double | 再保险可收回 - 未决索赔 |
| bs_reinsurance_recoverable_benefit_loss_reserve | Double | 再保险可收回 - 利益和损失准备金 |
| bs_reinsurers_share_separate_variable_acct | Double | 再保险公司在单独和可变账户/关联负债中的份额 |
| bs_reinsurance_recoverable_other | Double | 再保险可收回 - 其他 |
| bs_separate_variable_account_assets | Double | 独立和可变账户 - 资产 |
| bs_assets_held_for_sale_lt | Double | 持有待售资产/终止经营——长期 |
| bs_assets_held_for_sale_lt_st | Double | 持有待售资产/终止经营 - LT & ST |
| bs_insurance_related_assets_bank | Double | 保险相关资产 - 银行 |
| bs_other_non_current_assets_total | Double | 其他非流动资产 - 总计 |
| bs_restricted_accounts_lt | Double | 受限账户 - 长期 |
| bs_deferred_tax_asset_lt | Double | 递延税款 - 资产 - 长期 |
| bs_deferred_charges_lt | Double | 延期费用 - 长期 |
| bs_prepaid_expenses_lt | Double | 预付费用 - 长期 |
| bs_inventories_lt | Double | 库存 - 长期 |
| bs_regulatory_assets_lt | Double | 监管资产 - 长期 |
| bs_pension_assets_lt | Double | 养老金资产 - 长期 |
| bs_other_non_current_assets | Double | 其他非流动资产 |
| bs_other_assets_total | Double | 其他资产 - 总计 |
| bs_accrued_investment_income | Double | 应计投资收益 |

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| bs_restricted_accounts_cash | Double | 受限账户 - 现金 |
| bs_pension_benefits_overfunded | Double | 养老金福利 - 资金过剩 - 总计 |
| bs_deferred_charges | Double | 延期费用 |
| bs_deferred_tax_asset_lt_st | Double | 递延税款 - 资产 - 长期和短期 |
| bs_prepaid_expenses_total | Double | 预付费用 - 总计 |
| bs_decommissioning_funds | Double | 退役基金 |
| bs_regulatory_assets_total | Double | 监管资产 - 总计 |
| bs_other_assets | Double | 其他资产 |
| bs_intangible_assets_net | Double | 无形资产 - 总计 - 净额 |
| bs_goodwill_net | Double | 超过购买资产的商誉/成本 - 净额 |
| bs_intangibles_excl_gw_net | Double | 无形资产 - 不包括商誉 - 净额 - 总计 |
| bs_core_deposits_net | Double | 核心存款 - 净额 |
| bs_mortgage_servicing_rights_net | Double | 抵押贷款服务权 - 网络 |
| bs_asset_mgmt_contracts_net | Double | 资产管理合约 - 净额 |
| bs_customer_relations_net | Double | 客户群/关系 - 网络 |
| bs_tenant_relationships_leases_net | Double | 租户关系及就地租约 - 网络 |
| bs_above_market_rent_leases_net | Double | 高于市场租金/租赁 - 净额 |
| bs_leasing_rights_net | Double | 租赁权 - 净额 |
| bs_computer_software_intang_net | Double | 计算机软件 - 无形资产 - 净 |
| bs_r_and_d_costs_net | Double | 研究与开发成本 - 净额 |
| bs_brands_patents_trademarks_net | Double | 品牌、专利、商标、营销和艺术 - 网 |
| bs_licenses_franchises_contracts_net | Double | 许可证、特许经营权、版权、基于合同 - Net |
| bs_rou_intangibles_net | Double | 使用权无形资产 - 净额 |
| bs_other_intangibles_net | Double | 无形资产 - 其他 - 净额 |
| bs_intangible_assets_gross | Double | 无形资产 - 总额 - 总计 |
| bs_goodwill_gross | Double | 超出购买资产的商誉/成本 - 总额 |
| bs_intangibles_excl_gw_gross | Double | 无形资产 - 不包括商誉 - 总额 |
| bs_core_deposits_gross | Double | 核心存款 - 总额 |
| bs_mortgage_servicing_rights_gross | Double | 抵押贷款服务权 - 总额 |
| bs_asset_mgmt_contracts_gross | Double | 资产管理合同 - 总额 |
| bs_customer_relations_gross | Double | 客户群/关系 - 总额 |
| bs_tenant_relationships_leases_gross | Double | 租户关系和就地租赁 - 总额 |
| bs_above_market_rent_leases_gross | Double | 高于市场租金/租赁 - 总额 |
| bs_leasing_rights_gross | Double | 租赁权 - 总额 |
| bs_computer_software_intang_gross | Double | 计算机软件 - 无形资产 - 总额 |
| bs_r_and_d_costs_gross | Double | 研究与开发成本 - 总额 |
| bs_brands_patents_trademarks_gross | Double | 品牌、专利、商标、营销和艺术 - 总金额 |
| bs_licenses_franchises_contracts_gross | Double | 许可证、特许经营权、版权、基于合同的 - 总额 |
| bs_rou_intangibles_gross | Double | 使用权无形资产 - 总额 |
| bs_other_intangibles_gross | Double | 无形资产 - 其他 - 总额 - 总计 |
| bs_intangible_assets_acc_amort_impair | Double | 无形资产 - 累计摊销和减值 - 总计 |
| bs_goodwill_acc_amort_impair | Double | 商誉 - 累计摊销和减值 |
| bs_intangibles_excl_gw_acc_amort_impair | Double | 无形资产（不包括商誉） - 累计摊销和减值总计 |
| bs_core_deposits_acc_amort_impair | Double | 核心存款 - 累计摊销和减值 |
| bs_mortgage_servicing_rights_acc_amort_impair | Double | 抵押贷款服务权 - 累计摊销和减值 |
| bs_asset_mgmt_contracts_acc_amort_impair | Double | 资产管理合同 - 累计摊销和减值 |
| bs_customer_relations_acc_amort_impair | Double | 客户群/关系 - 累计摊销和减值 |
| bs_tenant_relationships_leases_acc_amort_impair | Double | 租户关系和就地租赁 -Accum Amort & Imp |
| bs_above_market_rent_leases_acc_amort_impair | Double | 高于市场租金/租赁 - 累计摊销和减值 |
| bs_leasing_rights_acc_amort_impair | Double | 租赁权 - 累计摊销和减值 |
| bs_computer_software_intang_acc_amort_impair | Double | 计算机软件 - 无形资产 - 累计摊销和减值 |
| bs_r_and_d_costs_acc_amort_impair | Double | 研究与开发成本 - 累计摊销和减值 |
| bs_brands_patents_trademarks_acc_amort | Double | 品牌、专利、商标、营销和艺术 - Accum Amort |
| bs_licenses_franchises_contracts_acc_amort_impair | Double | 许可证、特许经营权、版权 - Accum Amort & Impair |
| bs_rou_intangibles_acc_amort | Double | 使用权无形资产 - 累计摊销 |
| bs_other_intangibles_acc_amort_impair | Double | 其他无形资产 - 累计摊销和减值 |
| bs_total_non_current_assets | Double | 非流动资产总额 |
| bs_total_assets | Double | 总资产 |
| bs_trade_payable_accruals_st | Double | 贸易应付账款和应计费用 - 短期 |
| bs_trade_payable_st | Double | 贸易账户和应付贸易票据 - 短期 |
| bs_accrued_expenses_st | Double | 应计费用 - 短期 |
| bs_insurance_reserves_total | Double | 保险准备金 - 总计 |
| bs_benefit_loss_reserves_gross | Double | 损益准备金 - 总额 |
| bs_benefit_loss_reserves_life_gross | Double | 损益准备金 - 生命 - 总额 |
| bs_benefit_loss_reserves_non_life_gross | Double | 收益和损失准备金 - 非人寿 - 总额 |
| bs_unearned_premiums_gross | Double | 非应得保费 - 总额 |
| bs_policy_contract_claims_gross | Double | 保单和合同索赔 - 总额 |
| bs_policyholders_funds | Double | 保单持有人资金 |
| bs_insurance_reserves_other_gross | Double | 保险准备金 - 其他 - 总额 - 总计 |
| bs_separate_variable_account_liabilities | Double | 独立和可变账户 - 负债 |
| bs_deposits_total | Double | 存款 - 总计 |
| bs_deposits_non_int_bearing | Double | 存款 - 无息 |
| bs_deposits_int_bearing | Double | 存款 - 带息存款 |
| bs_customer_deposits_total | Double | 存款 - 客户 - 总计 |
| bs_demand_deposits_customer | Double | 存款-活期-客户 |
| bs_savings_deposits_customer | Double | 存款 - 储蓄 - 客户 |
| bs_other_deposits_customer | Double | 存款 - 其他 - 客户 |
| bs_deposits_banks_fi | Double | 存款 - 银行及金融机构存款 |
| bs_demand_deposits_banks_fi | Double | 存款 - 活期存款 - 存放银行和金融机构款项 |
| bs_savings_deposits_banks_fi | Double | 存款 - 储蓄 - 银行和金融机构存款 |
| bs_other_deposits_banks_fi | Double | 存款 - 其他 - 银行及金融机构存款 |
| bs_trading_liabilities | Double | 交易负债 |
| bs_debt_total | Double | 债务 - 总计 |
| bs_st_debt_current_portion_lt_debt | Double | 短期债务和长期债务的当前部分 |
| bs_st_debt_notes_payable | Double | 短期债务和应付票据 |
| bs_st_bank_borrowings_excl_collateral | Double | 短期银行借款不包括抵押融资 |
| bs_collateralized_financing_repo_liab | Double | 抵押融资协议 REPO 融资贷款 - Liab |
| bs_securities_loaned | Double | 证券 - 借出 |
| bs_securities_sold_repo_fed_funds_purchased | Double | 根据回购协议出售的证券和购买的联邦基金 |
| bs_securities_sold_repo | Double | 根据回购协议出售的证券 |
| bs_fed_funds_purchased | Double | 购买的联邦资金 |
| bs_securities_received_collateral_obligation | Double | 作为抵押品收到的证券 - 返还义务 |
| bs_current_portion_lt_debt_incl_cap_leases | Double | 长期债务的当前部分包括资本化租赁 |
| bs_current_portion_lt_debt_excl_cap_leases | Double | 长期债务的当前部分（不包括资本化租赁） |
| bs_cap_leases_current_portion | Double | 资本化租赁 - 当前部分 |
| bs_hybrid_financial_liability_current | Double | 混合金融工具 - 负债 - 当前部分 |
| bs_fhlb_advances_current | Double | FHLB 进展 - 当前部分 |
| bs_deriv_liab_hedge_st | Double | 衍生负债 - 对冲 - 短期 |
| bs_liabilities_held_for_sale_st | Double | 为出售/终止经营而持有的负债 - ST |
| bs_income_tax_payable_st | Double | 所得税 - 应付 - 短期 |
| bs_dividends_distributions_payable | Double | 应付股息/分配 |
| bs_operating_lease_liab_current | Double | 经营租赁负债 - 当前部分/短期 |
| bs_intangible_liability | Double | 无形负债 |
| bs_below_market_rent_leases_gross | Double | 低于市场租金/租赁 - 总额 |
| bs_below_market_rent_leases_acc_amort_impair | Double | 低于市场租金/租赁 - 累计摊销和减值 |
| bs_below_market_rent_leases_net | Double | 低于市场租金/租赁 - 净额 |
| bs_other_current_liabilities_total | Double | 其他流动负债 - 总计 |
| bs_deferred_income_st | Double | 递延收入 - 短期 |
| bs_security_deposits | Double | 保证金 |
| bs_billings_excess_cost_st | Double | 超出成本的账单 - 短期 |
| bs_customer_advances_st | Double | 客户预付款 - 短期 |
| bs_deferred_tax_liab_st | Double | 递延税 - 负债 - 短期 |
| bs_provisions_st | Double | 规定 - 短期 |
| bs_regulatory_liab_st | Double | 监管责任 - 短期 |
| bs_other_current_liabilities | Double | 其他流动负债 |
| bs_total_current_liabilities | Double | 流动负债总额 |
| bs_accounts_payable_accruals_lt | Double | 应付账款包括应计费用 - 长期 |
| bs_trade_payable_lt | Double | 贸易应付账款 - 长期 |
| bs_accrued_expenses_lt | Double | 应计费用 - 长期 |
| bs_debt_lt_total | Double | 债务 - 长期 - 总计 |
| bs_lt_debt_excl_cap_leases | Double | 长期债务（不包括资本化租赁） |
| bs_non_convertible_debt_lt | Double | 债务 - 不可转换 - 长期 |
| bs_convertible_debt_lt | Double | 可转换债务 - 长期 |
| bs_hybrid_financial_liability_lt | Double | 混合金融工具 - 负债 - 长期 |
| bs_mandatorily_redeemable_trust_certificates_lt | Double | 强制性可赎回信托证书 - 长期 |
| bs_other_mandatorily_redeemable_equity_lt | Double | 其他强制赎回权益工具 - 长期 |
| bs_preferred_stock_liability_portion_lt | Double | 优先股 - 负债部分 - 长期 |
| bs_fhlb_advances_lt | Double | FHLB 进展 - 长期 |
| bs_cap_lease_obligations_lt | Double | 资本化租赁义务 - 长期 |
| bs_deriv_liab_hedge_lt | Double | 衍生负债 - 对冲 - 长期 |
| bs_liabilities_held_for_sale_lt | Double | 持有待售/终止经营的负债 - 长期 |
| bs_income_tax_payable_lt_st | Double | 所得税 - 应付 - 长期和短期 |
| bs_dividends_payable | Double | 应付股息 |
| bs_deferred_tax_investment_tax_credits_lt | Double | 递延税和投资税收抵免 - 长期 |
| bs_deferred_tax_liab_lt | Double | 递延税款 - 负债 - 长期 |
| bs_deferred_tax_liab_untaxed_reserves | Double | 递延税款 - 负债 - 未征税准备金 |
| bs_payables_trust_account | Double | 应付账款 - 信托账户 |
| bs_payables_accrued_expenses | Double | 应付账款和应计费用 |
| bs_trade_payables_total | Double | 贸易应付账款 - 总计 |
| bs_payable_reinsurance_brokers_agents | Double | 应付账款 - 再保险和经纪人/代理人 |
| bs_interest_payable | Double | 应付利息 |
| bs_other_payables_total | Double | 其他应付款项 - 总计 |
| bs_payables_customers_brokers_dealers | Double | 应付账款 - 客户经纪人、经销商和清算组织 |
| bs_accrued_expenses | Double | 应计费用 |
| bs_deriv_liab_hedge | Double | 衍生负债 - 对冲 |
| bs_operating_lease_liab_lt_st | Double | 经营租赁负债 - 长期和短期 |
| bs_segregated_liabilities_total | Double | 独立负债 - 总计 |
| bs_operating_lease_liab_lt | Double | 经营租赁负债 - 长期 |
| bs_other_non_current_liabilities_total | Double | 其他非流动负债 - 总计 |
| bs_provisions_lt | Double | 规定 - 长期 |
| bs_post_employment_benefits_pension_other_lt | Double | 离职后福利 - 养老金及其他 - 长期 |
| bs_asset_retirement_obligation_lt | Double | 资产报废义务 - 长期 |
| bs_provisions_litigation_lt | Double | 条款 - 诉讼 - 长期 |
| bs_provisions_restructuring_lt | Double | 规定 - 重组 - 长期 |
| bs_provisions_environmental_lt | Double | 规定 - 环境义务 - 长期 |
| bs_provisions_other_lt | Double | 规定 - 其他 - 长期 |
| bs_customer_advances_lt | Double | 客户预付款 - 长期 |
| bs_deferred_revenue_lt | Double | 递延收入 - 长期 |
| bs_regulatory_liabilities_lt | Double | 监管负债 - 长期 |
| bs_other_non_current_liabilities | Double | 其他非流动负债 |
| bs_other_liabilities_total | Double | 其他负债 - 总计 |
| bs_provisions | Double | 规定 |
| bs_post_employment_benefits_pension_other | Double | 离职后福利 - 养老金及其他 |
| bs_provisions_other_than_pension | Double | 规定 - 养老金和退休后除外 |
| bs_regulatory_liabilities_total | Double | 监管负债 - 总计 |
| bs_billings_excess_costs_total | Double | 超出成本的账单 - 总计 |
| bs_customer_advances_total | Double | 客户预付款 - 总计 |
| bs_deferred_revenue_income | Double | 递延收入/收入 |
| bs_other_liabilities | Double | 其他负债 |
| bs_liabilities_held_for_sale_lt_st | Double | 为出售/终止经营而持有的负债 - LT & ST |
| bs_insurance_liabilities | Double | 保险责任 |
| bs_minority_interest_non_equity | Double | 少数股东权益 - 非股权 |
| bs_total_non_current_liabilities | Double | 非流动负债总额 |
| bs_total_liabilities | Double | 总负债 |
| bs_shareholders_equity_parent | Double | 股东权益 - 归属于母公司控股 - 合计 |
| bs_preferred_equity | Double | 优先股股东权益 |
| bs_preferred_stock_redeemable_total | Double | 优先股 - 可赎回 - 总计 |
| bs_preferred_stock_redeemable_convertible | Double | 优先股 - 可赎回 - 可转换 |
| bs_preferred_stock_non_redeemable | Double | 优先股 - 不可赎回 |
| bs_preferred_stock_convertible_non_redeemable | Double | 优先股 - 可转换 - 不可赎回 |
| bs_preferred_equity_contributed | Double | 优先股 - 贡献 |
| bs_preferred_stock_esop | Double | 优先股 - 为员工持股计划发行 |
| bs_preferred_stock_treasury | Double | 优先股 - 库存/回购 |
| bs_esop_guarantees_preferred_deferred_comp | Double | ESOP 保证 - 优先薪酬和延期薪酬 |
| bs_preferred_stock_redeemable_temporary | Double | 优先股 - 可赎回 - 临时股权 |
| bs_common_equity_parent | Double | 归属于母公司股东的普通股 |
| bs_common_stock_treasury | Double | 普通股 - 库存/回购 |
| bs_common_stock_esop | Double | 普通股 - 以 ESOP 或信托/递延补偿形式持有 |
| bs_common_equity_contributed | Double | 普通股 - 出资 |
| bs_common_stock_issued_paid | Double | 普通股 - 已发行并已支付 |
| bs_limited_partner | Double | 有限合伙人 |
| bs_common_stock_additional_paid_in_capital | Double | 普通股 - 附加资本支付，包括期权储备 |
| bs_common_share_capital_incl_apic | Double | 普通股资本，包括额外实收资本 - 总计 |
| bs_distributions_excess_earnings | Double | 超出收益的分配 |
| bs_equity_non_contributed_reserves_retained | Double | 股本 - 非缴款 - 储备金和留存收益 |
| bs_retained_earnings_total | Double | 留存收益 - 总计 |
| bs_accumulated_oci_total | Double | 综合收入 - 累计 - 总计 |
| bs_inv_unrealized_gl | Double | 投资 - 未实现损益 |
| bs_hedging_reserves | Double | 对冲储备 |
| bs_fx_translation_adj | Double | 外币换算调整 - 累计 |
| bs_oci_pension_liabilities | Double | 综合收入 - 养老金负债 |
| bs_oci_unearned_compensation | Double | 综合收入 - 非劳动报酬 |
| bs_revaluation_reserves | Double | 重估储备 |
| bs_oci_other_total | Double | 综合收入 - 其他 - 总计 |
| bs_other_reserves_equity_total | Double | 其他储备金/权益 - 总计 |
| bs_goodwill_written_off | Double | 商誉 - 累计冲销 |
| bs_untaxed_special_reserves | Double | 免税/特别储备金 |
| bs_negative_consol_goodwill_written_off | Double | 针对 Rsrv 注销的负 Consol Diff 商誉 |
| bs_equity_other | Double | 股权 - 其他 |
| bs_general_partner | Double | 普通合伙人 |
| bs_deferred_shares | Double | 递延股份 |
| bs_social_capital | Double | 社会资本 |
| bs_policy_holder_equity | Double | 保单持有人权益 |
| bs_common_equity_total | Double | 普通股 - 总计 |
| bs_minority_interest_equity | Double | 少数股东权益 - 股权 |
| bs_hybrid_financial_instrument_equity | Double | 混合金融工具 - 股权部分 |
| bs_total_equity_incl_minority_hybrid | Double | 股东权益总额，包括少数股权和混合债务 |
| bs_total_liabilities_equity | Double | 负债和权益总额 |
| bs_common_shares_issued_total | Double | 普通股 - 已发行 - 总计 |
| bs_common_shares_outstanding_total | Double | 普通股 - 已发行 - 总计 |
| bs_common_shares_treasury_total | Double | 普通股 - 库存 - 总计 |
| bs_common_shares_authorized | Double | 普通股 - 授权 - 特定发行 |
| bs_common_shares_issued | Double | 普通股 - 已发行 - 特定发行 |
| bs_common_shares_outstanding | Double | 普通股 - 已发行 - 特定发行 |
| bs_common_shares_treasury | Double | 普通股 - 库存 - 特定发行 |
| bs_common_shares_issued_current | Double | 普通股 - 已发行 - 特定发行 - 当前 |
| bs_common_shares_outstanding_current | Double | 普通股 - 已发行 - 特定发行 - 当前 |
| bs_common_shares_treasury_current | Double | 普通股 - 库存 - 特定发行 - 当前 |
| bs_common_shares_issued_dr | Double | 普通股 - 已发行 - 特定发行 - DR |
| bs_common_shares_outstanding_dr | Double | 普通股 - 已发行 - 特定发行 - DR |
| bs_common_shares_treasury_dr | Double | 普通股 - 库存 - 特定发行 - DR |
| bs_common_shares_issued_cpo | Double | 普通股 - 已发行 - 特定发行 - CPO |

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| bs_common_shares_outstanding_cpo | Double | 普通股 - 已发行 - 特定发行 - CPO |
| bs_common_shares_treasury_cpo | Double | 普通股 - 金库 - 特定发行 - CPO |
| bs_preferred_shares_authorized | Double | 优先股 - 授权 - 特定发行 |
| bs_preferred_shares_issued | Double | 优先股 - 已发行 - 特定发行 |
| bs_preferred_shares_outstanding | Double | 优先股 - 已发行 - 特定发行 |
| bs_preferred_shares_treasury | Double | 优先股 - 金库 - 特定发行 |
| bs_preferred_shares_issued_current | Double | 优先股 - 已发行 - 特定发行 - 当前 |
| bs_preferred_shares_outstanding_current | Double | 优先股 - 已发行 - 特定发行 - 当前 |
| bs_preferred_shares_treasury_current | Double | 优先股 - 库存 - 特定发行 - 当前 |
| bs_asset_allocation_factor | Double | 资产配置因素 - 特定问题 |
| bs_asset_participation_factor | Double | 资产参与因子 - 特定问题 |
| bs_epra_nav_per_share | Double | 每股 EPRA 资产净值 |
| bs_epra_triple_nav_per_share | Double | EPRA 每股三重资产净值 (NNNAV) |
| bs_rou_tangible_total_net_supp | Double | 使用权有形资产 - 总计 - 净额 - 补充 |
| bs_rou_operating_lease_net_supp | Double | 有形资产使用权 - 经营租赁网 - 补充 |
| bs_rou_cap_fin_lease_net_supp | Double | 有形资产使用权 - 上限/融资租赁 - 净 - Suppl |
| bs_rou_tangible_total_gross_supp | Double | 使用权有形资产 - 总计 - 总额 - 补充 |
| bs_rou_operating_lease_gross_supp | Double | 有形资产使用权 - 经营租赁总额 - Suppl |
| bs_rou_cap_fin_lease_gross_supp | Double | 有形资产使用权 - 上限/融资租赁 - 总额 - Suppl |
| bs_rou_tangible_total_acc_depr_supp | Double | 使用权有形资产 - 总计 - Accum Depr - Suppl |
| bs_rou_operating_lease_acc_depr_supp | Double | 有形资产使用权 - Optg Lease Accum Depr Suppl |
| bs_rou_cap_fin_lease_acc_depr_supp | Double | 有形资产使用权 - 上限/融资租赁 Accum Depr Suppl |
| bs_ppe_excl_rou_cap_leases_net | Double | PPE - 不包括有形使用权和上限租赁 - 净额 |
| bs_ppe_excl_rou_cap_leases_gross | Double | PPE - 不包括有形使用权和上限租赁 - 总额 |
| bs_ppe_excl_rou_cap_leases_acc_depr | Double | PPE - 不包括有形使用权和上限租赁 - Accum Depr |
| bs_rou_intangibles_net_supp | Double | 使用权无形资产 - 净额 - 补充 |
| bs_rou_intangibles_gross_supp | Double | 使用权无形资产 - 总额 - 补充 |
| bs_rou_intangibles_acc_amort_supp | Double | 使用权无形资产 - 累计摊销 - Suppl |
| bs_total_operating_lease_liabilities | Double | 经营租赁负债总额 |
| bs_operating_lease_liab_lt_st_supp | Double | 经营租赁负债 - 长期和短期 - 补充 |
| bs_operating_lease_liab_current_supp | Double | 经营租赁负债 - 当前部分/ST - 补充 |
| bs_operating_lease_liab_lt_supp | Double | 经营租赁负债 - 长期 - 补充 |
| bs_finance_operating_lease_liab_total | Double | 融资和经营租赁负债 - 总计 |
| bs_debt_incl_fin_op_lease_liab | Double | 债务包括融资和经营租赁负债 |
| bs_net_debt | Double | 净债务 |
| bs_weighted_cost_debt_pct | Double | 加权债务成本 - % |
| bs_revolver_outstanding_supp | Double | 循环信贷额度 - 未偿 - 补充 |
| bs_revolver_unutilized_supp | Double | 循环信用额度 - 未使用/未使用金额 - 补充 |
| bs_revolver_total_principal_supp | Double | 循环信贷额度 - 本金总额 - 补充 |
| bs_islamic_investments_deposits | Double | 伊斯兰投资和存款 |
| bs_islamic_receivables_st | Double | 伊斯兰应收账款 - 短期 |
| bs_islamic_receivables_lt | Double | 伊斯兰应收账款 - 长期 |
| bs_islamic_financing_assets_total | Double | 伊斯兰融资资产 - 总计 |
| bs_islamic_investments_total | Double | 伊斯兰投资 - 总计 |
| bs_unrestricted_investment_accounts | Double | 无限制投资账户 |
| bs_other_islamic_deposits | Double | 其他伊斯兰存款 |
| bs_islamic_debt_lt_st | Double | 伊斯兰债务 - 长期和短期 |
| bs_islamic_debt_deposits_total | Double | 伊斯兰债务和存款 - 总计 |
| bs_debt_lt_maturities_total | Double | 债务 - 长期 - 到期日 - 总计 |
| bs_debt_lt_maturities_year1 | Double | 债务 - 长期 - 期限 - 1 年内 |
| bs_debt_lt_maturities_year2 | Double | 债务 - 长期 - 到期日 - 第 2 年 |
| bs_debt_lt_maturities_year3 | Double | 债务 - 长期 - 到期日 - 第 3 年 |
| bs_debt_lt_maturities_year4 | Double | 债务 - 长期 - 到期日 - 第 4 年 |
| bs_debt_lt_maturities_year5 | Double | 债务 - 长期 - 到期日 - 第 5 年 |
| bs_debt_lt_maturities_year6 | Double | 债务 - 长期 - 到期日 - 第 6 年 |
| bs_debt_lt_maturities_year7 | Double | 债务 - 长期 - 到期日 - 第 7 年 |
| bs_debt_lt_maturities_year8 | Double | 债务 - 长期 - 到期日 - 第 8 年 |
| bs_debt_lt_maturities_year9 | Double | 债务 - 长期 - 到期日 - 第 9 年 |
| bs_debt_lt_maturities_year10 | Double | 债务 - 长期 - 到期日 - 10 年 |
| bs_debt_lt_maturities_remaining | Double | 债务 - 长期 - 到期日 - 剩余 |
| bs_debt_lt_maturities_2_3_years | Double | 债务 - 长期 - 期限 - 2-3 年 |
| bs_debt_lt_maturities_4_5_years | Double | 债务 - 长期 - 期限 - 4-5 年 |
| bs_debt_lt_maturities_year6_beyond | Double | 债务 - 长期 - 到期日 - 第 6 年及以后 |
| bs_cap_lease_maturities_total | Double | 资本租赁到期日 - 总计 |
| bs_cap_lease_maturities_year1 | Double | 资本租赁到期日 - 一年内到期 |
| bs_cap_lease_maturities_year2 | Double | 资本租赁到期日 - 第 2 年到期 |
| bs_cap_lease_maturities_year3 | Double | 资本租赁到期 - 第 3 年到期 |
| bs_cap_lease_maturities_year4 | Double | 资本租赁到期 - 第 4 年到期 |
| bs_cap_lease_maturities_year5 | Double | 资本租赁到期 - 第 5 年到期 |
| bs_cap_lease_maturities_year6 | Double | 资本租赁到期 - 第 6 年到期 |
| bs_cap_lease_maturities_year7 | Double | 资本租赁到期 - 第 7 年到期 |
| bs_cap_lease_maturities_year8 | Double | 资本租赁到期 - 第 8 年到期 |
| bs_cap_lease_maturities_year9 | Double | 资本租赁到期 - 第 9 年到期 |
| bs_cap_lease_maturities_year10 | Double | 资本租赁到期 - 第 10 年到期 |
| bs_cap_lease_maturities_remaining | Double | 资本租赁到期日 - 剩余到期日 |
| bs_cap_lease_maturities_interest | Double | 资本租赁到期日 - 利息成本 |
| bs_cap_lease_maturities_executory | Double | 资本租赁到期日 - 执行成本 |
| bs_cap_lease_maturities_2_3_years | Double | 资本租赁到期日 - 2-3 年内到期 |
| bs_cap_lease_maturities_4_5_years | Double | 资本租赁到期日 - 4-5 年内到期 |
| bs_cap_lease_maturities_year6_beyond | Double | 资本租赁到期日 - 第 6 年及以后到期 |
| bs_contract_assets_unearned_revenue_billings_total | Double | 合同资产总计 - 未实现收入和进度账单 |
| bs_contract_assets_unearned_revenue_billings_st | Double | 合同资产 - ST 未实现收入和进度账单 |
| bs_contract_assets_unearned_revenue_billings_lt | Double | 合同资产 - LT 未实现收入和进度账单 |
| bs_inv_property_fair_value | Double | 投资性房地产 - 公允价值 |
| bs_contract_liabilities_unearned_revenue_billings_total | Double | 合同负债总计 - 未实现收入和进度账单 |
| bs_contract_liabilities_unearned_revenue_billings_st | Double | 合同负债 - ST 未实现收入和进度账单 |
| bs_contract_liabilities_unearned_revenue_billings_lt | Double | 合同责任 - LT 未实现收入和进度帐单 |
| bs_investment_contracts_technical_liabilities | Double | 投资合同 - 技术责任 |
| bs_insurance_contracts_technical_liabilities | Double | 保险合同 - 技术责任 |
| bs_minority_interest_total | Double | 少数股东权益 - 总计 |
| bs_accruals_st | Double | 应计费用 - 短期 |
| bs_asset_accruals | Double | 应计资产 |
| bs_cash_cash_equiv_total | Double | 现金及现金等价物 - 总计 |
| bs_cash_securities | Double | 现金及证券 |
| bs_cash_short_term_inv_total | Double | 现金和短期投资 - 总计 |
| bs_debt_incl_pref_equity_minority | Double | 债务，包括优先股和少数股东权益 - 总计 |
| bs_demand_deposits_total | Double | 活期存款 - 总计 |
| bs_earning_assets | Double | 赚取资产 |
| bs_equity_sec_real_estate | Double | 股本证券及房地产 |
| bs_invested_assets_total | Double | 投资资产 - 总计 |
| bs_investment_securities | Double | 投资证券 |
| bs_investments_permanent | Double | 投资 - 永久 |
| bs_net_book_capital | Double | 净账本资本 |
| bs_net_operating_assets | Double | 净经营资产 |
| bs_non_reserve_liabilities | Double | 非储备负债 |
| bs_provisions_total | Double | 准备金 - 总计 |
| bs_savings_deposits_total | Double | 储蓄存款 - 总计 |
| bs_shareholders_equity_common | Double | 股东权益 - 普通股 |
| bs_tangible_total_equity | Double | 有形总股本 |
| bs_tangible_book_value | Double | 有形账面价值 |
| bs_total_book_capital | Double | 账面资本总额 |
| bs_total_capital | Double | 总资本 |
| bs_total_lt_capital | Double | 长期资本总额 |
| bs_total_fixed_assets_net | Double | 固定资产总额 - 净额 |
| bs_trading_account | Double | 交易账户 |
| bs_unearned_revenue_total | Double | 未实现收入 - 总计 |
| bs_working_capital | Double | 营运资金 |
| bs_working_capital_non_cash | Double | 营运资金 - 非现金 |
| bs_working_capital_excl_other_current | Double | 营运资金，不包括其他流动资产和负债 |
| bs_book_value_excl_other_equity | Double | 不包括其他权益的账面价值 |
| bs_common_shareholders_number | Double | 普通股股东 - 数量 |
| bs_reinsurance_liabilities | Double | 再保险责任 |
| bs_cash_banks_total | Double | 手头现金和银行存款 - 总计 |
| bs_cash_st_inv_receivables_total | Double | 现金、短期投资和应收账款 - 总计 |
| bs_current_assets_excl_cash_st_inv | Double | 流动资产（不包括现金和短期投资）——总计 |
| bs_current_liabilities_excl_current_debt | Double | 流动负债（不包括流动债务）-总计 |
| bs_int_bearing_liabilities_total | Double | 有息负债 - 总计 |
| bs_loans_gross_total | Double | 贷款 - 总额 - 总计 |
| bs_loans_net_total | Double | 贷款 - 净额 - 总计 |
| bs_other_assets_lt_st_total | Double | 其他短期和长期资产 - 总计 |
| bs_other_liabilities_lt_st_total | Double | 其他短期和长期负债 - 总计 |
| bs_provision_doubtful_receivables_total | Double | 呆账准备金和应收票据 - 总计 |
| bs_loan_loss_reserves_total | Double | 贷款损失准备金 - 总计 |
| bs_tangible_book_value_loan_loss_reserves | Double | 有形账面价值和贷款损失准备金 - 总计 |
| bs_trade_receivables_net_total | Double | 贸易账款和应收贸易票据 - 净额 - 总计 |
| bs_total_available_funds | Double | 可用资金总额 |
| bs_current_assets_excl_inventories | Double | 流动资产总额（不包括库存总额） |
| bs_total_debt_excl_islamic | Double | 总债务不包括伊斯兰债务 |
| bs_benefit_claims_reserves_gross | Double | 福利和索赔准备金 - 总额 |
| bs_book_value_excl_aci | Double | 账面价值不包括累计综合收益 |
| bs_cash_st_inv_net_debt | Double | 现金和短期投资 - 扣除债务 |
| bs_current_portion_lt_debt_incl_cap_leases_hybrid | Double | 长期债务的当前部分，包括资本化租赁和混合金融工具 |
| bs_deposits_net | Double | 存款 - 净额 |
| bs_inv_equity_real_estate_mortgages | Double | 股权、房地产和抵押贷款投资 |
| bs_net_debt_incl_pref_equity_minority | Double | 净债务包括优先股和少数股东权益 |
| bs_ppe_excl_utility_plant_net | Double | 财产、厂房和设备，不包括公用设施 - 净值 |
| bs_tangible_book_value_excl_other_equity | Double | 有形账面价值（不包括其他权益） |
| bs_operating_lease_payments_total | Double | 经营租赁付款 - 总计 |
| bs_op_lease_payments_year1 | Double | 经营租赁付款 - 第一年到期 |
| bs_op_lease_payments_year2 | Double | 经营租赁付款 - 第 2 年到期 |
| bs_op_lease_payments_year3 | Double | 经营租赁付款 - 第 3 年到期 |
| bs_op_lease_payments_year4 | Double | 经营租赁付款 - 第 4 年到期 |
| bs_op_lease_payments_year5 | Double | 经营租赁付款 - 第 5 年到期 |
| bs_op_lease_payments_year6 | Double | 经营租赁付款 - 第 6 年到期 |
| bs_op_lease_payments_year7 | Double | 经营租赁付款 - 第 7 年到期 |
| bs_op_lease_payments_year8 | Double | 经营租赁付款 - 第 8 年到期 |
| bs_op_lease_payments_year9 | Double | 经营租赁付款 - 第 9 年到期 |
| bs_op_lease_payments_year10 | Double | 经营租赁付款 - 第 10 年到期 |
| bs_op_lease_payments_remaining | Double | 经营租赁付款 - 剩余期限 |
| bs_op_lease_payments_interest | Double | 经营租赁付款 - 利息成本/估算利息 |
| bs_op_lease_payments_2_3_years | Double | 经营租赁付款 - 2-3 年内到期 |
| bs_op_lease_payments_4_5_years | Double | 经营租赁付款 - 4-5 年内到期 |
| bs_op_lease_payments_year6_beyond | Double | 经营租赁付款 - 第 6 年及以后到期 |
| bs_credit_exposure | Double | 信用暴露 |
| bs_assets_under_management | Double | 管理资产（AUM） |
| bs_capital_adequacy_total_value | Double | 资本充足率 - 总计（值） |
| bs_capital_adequacy_tier1_value | Double | 资本充足率 - 一级（价值） |
| bs_capital_adequacy_core_tier1_value | Double | 资本充足率 - 核心一级（价值） |
| bs_capital_adequacy_hybrid_tier1_value | Double | 资本充足率 - 混合一级资本（包含在一级资本中） |
| bs_capital_adequacy_tier2_value | Double | 资本充足率 - 二级（价值） |
| bs_capital_adequacy_tier3_value | Double | 资本充足率 - 第三级（价值） |
| bs_capital_adequacy_total_pct | Double | 资本充足率 - 总计 (%) |
| bs_capital_adequacy_tier1_pct | Double | 资本充足率 - 一级 (%) |
| bs_capital_adequacy_core_tier1_pct | Double | 资本充足率 - 核心一级 (%) |
| bs_capital_adequacy_tier2_pct | Double | 资本充足率 - 二级资本 (%) |
| bs_capital_adequacy_tier3_pct | Double | 资本充足率 - 第三级 (%) |
| bs_risk_weighted_assets | Double | 风险加权资产 |
| bs_liquidity_coverage_ratio_pct | Double | 流动性覆盖率 - 巴塞尔 3 - % |
| bs_solvency_margin_ratio_insurance | Double | 偿付能力充足率——保险 |
| bs_leverage_ratio_pct | Double | 杠杆率 - 巴塞尔 3 - % |
| bs_net_stable_funding_ratio_pct | Double | 净稳定资金比率 - 巴塞尔 3 - % |
| bs_solvency_ratio_insurance | Double | 偿付能力充足率 – 保险 |
| bs_non_performing_assets_loans_other | Double | 不良资产 - 贷款及其他 |
| bs_non_performing_assets_other | Double | 不良资产 - 贷款除外 |
| bs_loans_non_performing_impaired | Double | 贷款 - 不良贷款和受损贷款 |
| bs_loans_impaired_total | Double | 贷款 - 减值 - 总计 |
| bs_loans_impaired_non_performing | Double | 贷款 - 减值 - 不良 |
| bs_loans_impaired_sub_performing | Double | 贷款 - 减值 - 表现不佳和表现但减值 |
| bs_loans_performing_non_performing_not_impaired | Double | 贷款 - 表现良好和不良 - 未减值 |
| bs_loans_non_performing_past_due | Double | 贷款 - 不良 - 未减值但逾期 |
| bs_loans_non_performing_past_due_0_90 | Double | 贷款 - 非绩效 - 未受损但逾期 - 0 至 90 天 |
| bs_loans_non_performing_past_due_90 | Double | 贷款 - 不良 - 未减值但逾期 - 90 天 |
| bs_loans_performing_not_past_due | Double | 贷款 - 执行 - 未减值且未逾期 |
| bs_impaired_assets_total | Double | 减值资产 - 总计 |
| bs_impaired_assets_loans_other | Double | 减值资产 - 减值贷款及其他 |
| bs_impaired_assets_excl_loans | Double | 减值资产 - 不包括减值贷款 |
| bs_loans_stage1_gross | Double | 贷款 - 第一阶段 - 总额，总计 |
| bs_loans_stage2_gross | Double | 贷款 - 第 2 阶段 - 总额，总计 |
| bs_loans_stage3_gross | Double | 贷款 - 第 3 阶段 - 总额，总计 |
| bs_loans_not_past_due | Double | 贷款 - 未逾期 |
| bs_loans_total_past_due | Double | 贷款 - 逾期总额 |
| bs_loans_past_due_lt_90 | Double | 贷款 - 逾期 \< 90 天 |
| bs_loans_past_due_remaining | Double | 贷款 - 逾期 - 剩余部分 |
| bs_loans_poci_gross | Double | 购买或发放的贷款信用减损总额，总计 |
| bs_other_assets_stage1_gross | Double | 其他资产 - 第一阶段，总额 |
| bs_other_assets_stage2_gross | Double | 其他资产 - 第 2 阶段，总额 |
| bs_other_assets_stage3_gross | Double | 其他资产 - 第 3 阶段，总额 |
| bs_int_earning_assets_avg | Double | 生息资产 - 平均 |
| bs_int_bearing_liabilities_avg | Double | 有息负债 - 平均 |
| bs_employees_ft_period_end | Double | 员工 - 全职/全职当量 - 期末 |
| bs_employees_ft_current | Double | 员工 - 全职/同等全职员工 - 当前日期 |
| bs_employees_pt_period_end | Double | 员工 - 兼职 - 期末 |
| bs_order_backlog | Double | 订单积压 |
| bs_customer_acceptances_assets | Double | 客户承兑负债 - 资产 |
| bs_customer_acceptances_liabilities | Double | 客户承兑责任 - 责任 |
| bs_reported_total_assets | Double | 报告-总资产 |
| bs_reported_total_liabilities | Double | 报告 - 负债总额 |
| bs_reported_equity_excl_new_stock | Double | 报告股东权益，不包括新股认购 |
| bs_reported_equity | Double | 报告 - 股东权益 |
| bs_reported_net_assets | Double | 报告-净资产 |
| bs_reported_net_assets_to_assets | Double | 报告 - 净资产与总资产之比 |
| bs_reported_roa | Double | 报告 - 资产回报率 |
| bs_reported_roe | Double | 报告 - 股本回报率 |
| bs_wavg_discount_rate_finance_lease | Double | 加权平均折扣率 - 融资租赁 |
| bs_wavg_discount_rate_op_lease | Double | 加权平均折扣率 - 经营租赁 - 美国公认会计准则 |
| bs_wavg_lease_term_yrs_finance_lease | Double | Wgt 平均剩余租赁期限（年）- 融资租赁 |
| bs_wavg_lease_term_yrs_op_lease | Double | Wgt 平均剩余租赁期限（年） - Op Lease - US GAAP |
| bs_loans_net_non_performing_reported | Double | 贷款 - 不良贷款净额 - 公司报告 |
| bs_loans_net_non_performing_pct | Double | 贷款 - 不良贷款净额 - % |
| bs_provision_coverage_ratio_pct | Double | 拨备覆盖率 - % |
| bs_short_term_lending | Double | 短期 - 贷款 |
| bs_long_term_lending | Double | 长期 - 贷款 |
| bs_casa_ratio_pct | Double | CASA 比率 - % |
| bs_collection_efficiency_pct | Double | 收集效率 - % |
| bs_st_lending_to_total_pct | Double | 短期贷款占总贷款的百分比 |
| bs_lt_lending_to_total_pct | Double | 长期 - 贷款占贷款总额 - % |
| bs_level1_assets_fair_value | Double | 1 级资产 - 公允价值 |
| bs_level1_liabilities_fair_value | Double | 1 级负债 - 公允价值 |
| bs_level2_assets_fair_value | Double | 2 级资产 - 公允价值 |
| bs_level2_liabilities_fair_value | Double | 2 级负债 - 公允价值 |
| bs_level3_assets_fair_value | Double | 第三级资产 - 公允价值 |
| bs_level3_liabilities_fair_value | Double | 第三级负债 - 公允价值 |

利润表(is)

| 字段 | 类型 | 描述 |
|:---|:---|:---|
| is_revenue_goods_services | Double | 商品和服务收入 |
| is_sales_goods_services_net | Double | 商品和服务销售 - 净额 - 未分类 |
| is_rental_property_revenue | Double | 租赁及物业相关营业收入 |
| is_rental_income_gross | Double | 租金及相关收入 - 总额 |
| is_tenant_service_charges | Double | 租户服务费报销 |
| is_rental_income_gross | Double | 租金收入 - 总额 |
| is_property_dev_revenue | Double | 房地产开发收入 |
| is_property_mgmt_revenue | Double | 物业管理服务收入 |
| is_property_revenue_other | Double | 房地产相关营业收入 - 其他 |
| is_hotel_revenue | Double | 酒店收入 |
| is_hotel_rooms_revenue | Double | 酒店收入 - 客房数 |
| is_hotel_lease_income | Double | 酒店收入 - 酒店租赁收入 |
| is_hotel_food_beverage_revenue | Double | 酒店收入 - 餐饮 |
| is_hotel_other_revenue | Double | 酒店收入 - 其他 |
| is_utility_revenue | Double | 公用事业收入 - 总计 |
| is_utility_other_revenue | Double | 公用事业收入 - 其他公用事业业务 |
| is_utility_steam_revenue | Double | 公用事业收入 - Steam 运营 |
| is_utility_water_revenue | Double | 公用事业收入 - 水务运营 |
| is_utility_gas_revenue | Double | 公用事业收入 - 天然气运营 |
| is_utility_electric_revenue | Double | 公用事业收入 - 电力运营 |
| is_utility_non_utility_revenue | Double | 公用事业收入 - 非公用事业运营 |
| is_sales_returns_allowances_adj | Double | 销售退货津贴和其他收入调整 |
| is_revenue_taxes | Double | 收入税 |
| is_gross_business_revenue | Double | 业务活动总收入 - 总计 |
| is_int_div_income_net | Double | 利息和股息收入/（支出）-净额-财务 |
| is_int_div_income_total | Double | 利息和股息收入 - 财务 - 总计 |
| is_int_income_loans_deposits | Double | 利息收入 - 贷款/存款 |
| is_int_fees_loans_receivables | Double | 贷款和应收账款的利息和费用 |
| is_int_income_deposits_banks | Double | 利息收入 - 存放其他金融机构的款项 |
| is_int_income_collateral_fin | Double | 利息收入 - 抵押融资 |
| is_int_div_income_inv_sec | Double | 利息和股息收入 - 投资证券 - 金融 |
| is_int_div_income_afs_htm | Double | 利息和股息收入 - Invst Sec AFS/HTM - 金融 |
| is_int_div_income_trading | Double | 利息和股息收入 - 交易账户资产融资 |
| is_int_div_income_other | Double | 利息和股息收入 - 其他 - 金融 |
| is_int_expense_total | Double | 利息支出 - 财务 - 总计 |
| is_int_expense_oper_fin | Double | 利息支出 - 运营融资 - 业务 |
| is_int_expense_deposits | Double | 利息支出 - 存款 |
| is_int_expense_collateral | Double | 利息支出 - 抵押融资 |
| is_int_expense_other | Double | 利息费用 - 其他 - 总计 |
| is_int_expense_external_fin | Double | 利息支出-对外融资业务 |
| is_return_unrestricted_inv | Double | 无限制投资账户的回报 |
| is_net_premiums_earned | Double | 赚取的净保费 |
| is_premiums_written_gross | Double | 保费保费 - 总额 |
| is_premiums_written_life | Double | 保费总额 - 人寿/长期保险 |
| is_premiums_written_non_life | Double | 承保保费 - 总额 - 非人寿/普通保险 |
| is_premiums_ceded_unearned | Double | 分出和不劳而获的保费 - 再保险 |
| is_premiums_ceded_written | Double | 保费分给再保险 - 书面 |
| is_premiums_ceded_unearned_premiums | Double | 分给再保险的保费——不劳而获 |
| is_unearned_premiums | Double | 不劳而获的保费 |
| is_non_int_business_rev_net | Double | 非利息业务收入/（支出） - 净额 - 总计 |
| is_net_comm_fees_income | Double | 佣金和费用净收入/（支出）- 业务收入 |
| is_fees_comm_income | Double | 手续费及佣金收入 |
| is_fees_comm_expense | Double | 费用及佣金支出 |
| is_inv_income_gross | Double | 投资收入 - 总额 - 投资 |
| is_dividend_income | Double | 股息收入 - 投资 |
| is_int_income_inv | Double | 利息收入 - 投资 |
| is_inv_income_other | Double | 投资收入 - 其他 - 总计（投资） |
| is_trust_fiduciary_income | Double | 信托和信托收入/佣金和费用 |
| is_trust_income | Double | 信托收益 |
| is_net_fx_income | Double | 外汇净收入/（支出）-营业收入 |
| is_inv_income_net_insurance | Double | 投资收入/（支出）-净额-保险 |
| is_inv_income_gross_insurance | Double | 投资收入 - 总额 - 保险 - 总计 |
| is_inv_expense_insurance | Double | 投资费用 - 保险 - 总计 |
| is_inv_loans_gain_loss | Double | 投资和贷款 - 业务 - 收益/（损失） |
| is_realized_gain_loss | Double | 已实现资本收益/（损失）-总计 |
| is_inv_sec_realized_gl | Double | 投资证券 - 已实现收益/（损失） |
| is_commodities_realized_gl | Double | 商品 - 已实现收益/（损失） |
| is_fx_realized_gl | Double | 外汇 - 已实现收益/（损失） - 资本 |
| is_deriv_hedge_realized_gl | Double | 衍生品 - 对冲 - 业务 - 已实现收益/（损失） |
| is_other_realized_gl | Double | 无差别/其他已实现收益/（损失） |
| is_unrealized_gl | Double | 资本收益/（损失） - 未实现 - 总计 |
| is_inv_sec_unrealized_gl | Double | 投资证券 - 未实现收益/（损失） |
| is_commodities_unrealized_gl | Double | 商品 - 未实现收益/（损失） |
| is_fx_unrealized_gl | Double | 外汇收益/（损失）-未实现-资本 |
| is_deriv_hedge_fair_value_gl | Double | 按公允价值进行衍生品对冲 - 收益/（损失） |
| is_other_unrealized_gl | Double | 未区分/其他未实现收益/（损失） |
| is_net_inv_loans_gl | Double | 净投资和贷款收益/（损失）-业务收入 |
| is_inv_sec_business_gl | Double | 投资证券 - 业务 - 收益/（损失） |
| is_inv_sec_afs_htm_realized_gl | Double | 投资证券 - AFS/HTM - 已实现收益/（损失） |
| is_trading_inv_gl | Double | 交易投资/交易账户收入 - 收益/（损失） |
| is_trading_inv_realized_gl | Double | 交易投资 - 已实现收益/（损失） |
| is_trading_inv_unrealized_gl | Double | 交易投资 - 未实现收益/（损失） |
| is_inv_sec_unclassified_gl | Double | 投资证券 - 未分类业务 - 收益/（损失） |
| is_inv_gl_other | Double | 投资收益/（损失）-其他 |
| is_loans_settlement_gl | Double | 贷款结算 - 收益/（损失） |
| is_deriv_hedge_unclassified_gl | Double | 衍生品对冲 - 业务 - 收益/（损失） - 未分类 |
| is_deriv_hedge_gl | Double | 衍生品 - 对冲 - 业务 - 收益/（损失） |
| is_sale_fin_instr_gl_other | Double | 出售金融工具的收益/（损失） - 其他 |
| is_net_income_insurance_bank | Double | 保险净收入/（费用） - 银行 |
| is_premiums_earned_other_income_insurance_bank | Double | 保险保费及其他收入 - 银行 - 总计 |
| is_claims_benefits_other_exp_insurance_bank | Double | 保险索赔、福利及其他费用 - 银行 - 总计 |
| is_net_income_lease_revenue | Double | 来自 Optg 和融资租赁的净收入/（费用）- 收入 |
| is_financing_revenue | Double | 融资相关业务收入 |
| is_business_financing_revenue_other | Double | 业务相关融资收入 - 其他 |
| is_business_related_revenue_other | Double | 业务相关活动收入 - 其他 - 总计 |
| is_royalty_income | Double | 特许权使用费收入 - 商业 |
| is_net_revenue_banking_insurance | Double | 净收入/（支出） - 银行业务 - 保险 |
| is_revenue_banking_insurance | Double | 银行业务收入 - 保险 |
| is_expenses_banking_insurance | Double | 银行业务费用（收入）- 保险 |
| is_op_revenue_capital_account | Double | 营业收入 - 资本账户（投资信托） |
| is_op_revenue_revenue_account | Double | 营业收入 - 收入账户（投资信托） |
| is_revenue_business_total | Double | 业务活动收入 - 总计 |
| is_cost_operating_revenue | Double | 营业收入成本 |
| is_cost_financing | Double | 融资相关运营成本 |
| is_loan_loss_provision | Double | 贷款损失拨备和减值 |
| is_cost_revenues_total | Double | 收入成本 - 总计 |
| is_cost_revenues | Double | 收入成本 - 未分类 |
| is_production_taxes_royalty | Double | 生产税和特许权使用费 |
| is_amortization_cogs | Double | 收入成本摊销 |
| is_depreciation_cogs | Double | 收入成本折旧 |
| is_labor_expenses_cogs | Double | 劳动力费用，包括以销货成本计算的基于股票的薪酬 |
| is_material_expenses | Double | 材料费 |
| is_material_expenses_inventory_utility | Double | 材料费用 - 库存自己的工作和公用事业未分类 |
| is_utility_fuel_expense | Double | 公用事业收入成本 - 燃料费用 |
| is_utility_fuel_purchased | Double | 公用事业收入成本 - 购买转售燃料 |
| is_utility_purchased_power | Double | 公用事业收入成本 - 购买电力 |
| is_own_work_capitalized | Double | 自己的工作资本化 |
| is_inventory_change | Double | 库存变化 |
| is_materials_purchased | Double | 采购材料 |
| is_ground_lease_rental_expense | Double | 收入成本中的土地租赁/租金费用 |
| is_property_op_exp_rental | Double | 物业运营费用 - 房地产租赁 |
| is_property_op_exp_hotel | Double | 物业运营费用 - 酒店 |
| is_property_direct_exp_other | Double | 物业直接费用 - 按类型 - 其他 |
| is_real_estate_taxes | Double | 房地产税 |
| is_property_maintenance_charges | Double | 物业维修及服务费 |
| is_property_rental_expense | Double | 物业相关支出 - 租赁业务/投资物业 |
| is_cost_revenues_other | Double | 收入成本 - 其他 - 总计 |
| is_operating_interest_expense | Double | 经营利息支出不包含在净利息收入中 |
| is_gross_profit | Double | 毛利润 - 工业/房地产 - 总计 |
| is_insurance_claims_reserves | Double | 保险索赔/准备金 - 总计 |
| is_insurance_benefits_paid | Double | 已付保险金 - 当前 |
| is_life_insurance_benefits | Double | 已支付的人寿保险福利 |
| is_non_life_insurance_benefits | Double | 支付的非人寿保险福利 |
| is_lt_insurance_reserves | Double | 长期保险准备金 - 总额 |
| is_loss_adjustment_expense | Double | 损失调整费用 |
| is_insurance_benefits_ceded | Double | 保险利益让渡 |
| is_current_claims_benefits_ceded | Double | 当前的保险索赔和利益让渡 |
| is_lt_insurance_reserves_ceded | Double | 放弃长期保险准备金 |
| is_dividends_policyholders | Double | 保单持有人红利 |
| is_underwriting_expenses | Double | 承保费用 |
| is_policy_acq_costs | Double | 保单获取成本 - 总计 |
| is_policy_acq_costs | Double | 保单获取成本 - 未分类 |
| is_amort_deferred_policy_acq | Double | 递延保单获取成本的摊销 |
| is_policy_acq_costs_other | Double | 保单获取成本 - 其他 |
| is_underwriting_commissions | Double | 向代理人承保佣金 |
| is_fee_comm_exp_insurance | Double | 费用及佣金支出 - 保险 |
| is_underwriting_expense_other | Double | 未分类承保费用 - 其他 |
| is_expenses_banking_insurance | Double | 银行业务费用 - 保险 |
| is_sga_expenses | Double | 销售一般及行政费用 - 总计 |
| is_sga_expenses | Double | 销售一般及行政费用 - 未分类 |
| is_labor_expenses_sga | Double | SGA 费用中包含基于股票的薪酬的人工费用 |
| is_r_and_d_expense | Double | 研究开发费用 |
| is_exploration_expense | Double | 勘探/干孔费用（包括核销） |
| is_depreciation_sga | Double | 销售一般及行政费用的折旧 |
| is_amort_intangibles_sga | Double | SGA 费用中无形资产的摊销 |
| is_o_and_m_utility | Double | 操作与维护（公用事业） |
| is_inv_mgmt_fees | Double | 投资管理费 |
| is_inv_mgmt_base_fees | Double | 投资管理 - 基本费用 |
| is_incentive_fees | Double | 绩效/激励投资费 |
| is_sga_other | Double | 销售一般及行政费用 - 其他 - 总计 |
| is_advertising_expense | Double | 广告费 |
| is_property_other_taxes | Double | 财产税和其他税项 |
| is_rental_expense | Double | 租金费用 |
| is_occupancy_expense | Double | 入住费用 - 其他 |
| is_pre_opening_expenses | Double | 开业前费用 |
| is_doubtful_accounts_provision | Double | 呆账准备金和核销 |
| is_equipment_occupancy_expense | Double | 设备/占用费用 - 银行/金融 - 其他 |
| is_other_operating_expense_net | Double | 其他运营支出/（收入）- 净额 |
| is_other_operating_income | Double | 其他营业收入 - 总计 |
| is_other_operating_expense | Double | 其他营业费用 |
| is_decommissioning_provision | Double | 退役基金和环境义务的规定 |
| is_operating_provisions_change | Double | 经营准备金 - 增加/（减少） |
| is_bank_guarantee_contributions | Double | 向银行担保基金的捐款和转账 |
| is_non_recurring_op_adj | Double | 非经常性调整 - 运营 - 减少/（增加） |
| is_supplementary_op_adj | Double | 补充调整 - 运营 - 减少/（增加） |
| is_op_expenses_revenue_acct | Double | 营业费用 - 收入账户 |
| is_op_expenses_capital_acct | Double | 营业费用 - 资本账户 |
| is_op_expenses_total | Double | 营业费用 - 总计 |
| is_total_op_exp_before_int_loan_loss | Double | 利息支出和贷款损失证明前的总运营支出 |
| is_op_profit_before_non_recurring | Double | 扣除非经常性收入/（费用）之前的营业利润 |
| is_financing_income_net | Double | 融资收入/（支出） - 净额 - 总计 |
| is_int_expense_net | Double | 利息支出 - 扣除（利息收入） |
| is_int_income_non_bank | Double | 利息收入 - 非银行 |
| is_int_expense_net_cap | Double | 利息支出 - 扣除资本化利息 |
| is_int_expense_capital_fin | Double | 资本融资利息支出 - 总额 |
| is_hybrid_div_liability | Double | 混合金融工具的股息 - 负债 |
| is_int_capitalized | Double | 利息资本化 |
| is_allowance_construction_funds | Double | 建设期间使用的资金补贴 - 债务部分 |
| is_non_int_financial_income | Double | 非利息财务收入/（支出） - 总计 |
| is_dividend_inv_income | Double | 股息及投资收益 |
| is_fx_gl_non_business | Double | 外汇收益/（损失）- 非业务 |
| is_amort_deferred_financing | Double | 递延融资费用摊销 |
| is_sale_inv_gl | Double | 投资出售 AFS、HTM 和交易 - 收益/（损失） |
| is_accretion_closure_expense | Double | 增生 - 场地关闭和复垦费用 |
| is_non_int_fin_income_other | Double | 非利息财务收入/（支出） - 其他 - 净额 |
| is_sale_fixed_assets_gl | Double | 出售有形和无形固定资产 - 收益/（损失） |
| is_sale_leased_assets_gl | Double | 出售租赁固定资产 - （收益/损失） |
| is_equity_earnings_bt | Double | 税前权益收益/（损失），包括非经常性收益 |
| is_non_recurring_equity_earnings | Double | 税前非经常性股权收益部分 |
| is_other_non_op_income | Double | 其他非营业收入/（支出）-总计 |
| is_non_op_rental_income | Double | 营业外租金收入 |
| is_transfer_untaxed_reserves | Double | 转自/（转至）免税储备金 |
| is_trading_deriv_gl | Double | 衍生品交易 - 收益/（损失） |
| is_deriv_hedge_effective_gl | Double | 衍生品 - 对冲 - 有效收益/（损失） |
| is_deriv_hedge_realized_gl | Double | 衍生品 - 对冲 - 已实现收益/（损失） |
| is_non_recurring_non_op_adj | Double | 非经常性调整 - 非运营 - Decr/（Incr） |
| is_supplementary_non_op_adj | Double | 补充调整 - 非运营 - Decr/（Incr） |
| is_normalized_pretax_profit | Double | 标准化税前利润 |
| is_non_recurring_income | Double | 非经常性收入/（支出） - 总计 |
| is_impairment_tangible_intangible | Double | 减值 - 有形和无形固定资产 |
| is_impairment_fixed_assets | Double | 减值 - 固定资产 |
| is_impairment_goodwill | Double | 减值 - 商誉 |
| is_impairment_intangibles_excl_gw | Double | 减值 - 无形资产（不包括商誉） |
| is_impairment_oil_gas | Double | 减值 - 石油和天然气资产 |
| is_impairment_inv_property | Double | 减值 - 投资性房地产 |
| is_impairment_fin_inv | Double | 减值 - 金融投资 |
| is_impairment_deferred_costs | Double | 减值 - 递延成本 |
| is_otti_losses | Double | 除临时投资减值损失外 |
| is_restructuring_charges | Double | 重组费用 |
| is_r_and_d_in_process | Double | 研究与开发 - 进行中 |
| is_property_acquisition_exp | Double | 与财产相关的购置费用 |
| is_write_off_real_estate | Double | 待售房地产的核销 |
| is_litigation_expenses | Double | 诉讼费用/和解 |
| is_exceptional_claims | Double | 支付的特殊索赔和福利（灾难） |
| is_ipo_merger_costs | Double | 与首次公开募股和合并相关的成本 |
| is_deriv_hedge_gl | Double | 衍生品 - 对冲 - 收益/（损失） |
| is_early_term_deriv_hedge_gl | Double | 衍生品提前终止 - 对冲 - 收益/（损失） |
| is_deriv_hedge_ineffective_gl | Double | 衍生品 - 对冲 - 无效收益/（损失） |
| is_unrealized_deriv_adj | Double | 未实现的衍生品套期调整 |
| is_early_extinguish_lease_debt_gl | Double | 租赁相关债务的提前清偿 - 收益/（损失） |
| is_negative_goodwill | Double | 负商誉的确认 |
| is_fv_adj_inv_property | Double | 公允价值调整 - 投资性房地产 |
| is_fv_adj_biological_assets | Double | 公允价值调整 - 生物资产 |
| is_fv_adj_fin_inv | Double | 公允价值调整 - 金融投资 |
| is_fv_adj_other_assets | Double | 公允价值调整 - 其他资产 |
| is_disaster_compensation | Double | 灾难赔偿 - 税前 |
| is_debt_restructuring_gl | Double | 债务重组 - 收益/（损失） |
| is_sale_acquisition_group_gl | Double | 集团公司的出售和收购 - 收益/（损失） |
| is_inventory_valuation_gl | Double | 库存估值 - 收益/（损失） |
| is_covid_19_income_expense | Double | COVID-19 非经常性收入/（支出） - 总计 |
| is_covid_19_other | Double | COVID-19 非经常性收入/（费用）- 其他 |
| is_covid_19_provisions | Double | COVID-19 一次性规定 |
| is_covid_19_restructuring | Double | COVID-19 重组费用和规定 |
| is_covid_19_impairment | Double | COVID-19 长期资产减值 |
| is_covid_19_grants | Double | COVID-19 一次性政府补助金 |
| is_other_non_recurring | Double | 非经常性收入/（支出）-其他-总计 |
| is_income_bt | Double | 税前收入 |
| is_income_taxes | Double | 所得税 |
| is_taxes_capital | Double | 资本账户税 |
| is_taxes_revenue | Double | 收入账户税 |
| is_income_tax_provision | Double | 所得税准备金 - 未分类 |
| is_income_tax_provision | Double | 所得税准备金 – 未分类 |
| is_income_taxes_domestic | Double | 所得税 - 国内 |
| is_income_taxes_foreign | Double | 所得税 - 外国 |
| is_income_taxes_other_region | Double | 所得税 - 其他（按地区） |
| is_income_taxes_current | Double | 本年度所得税 - 当前 |
| is_income_taxes_domestic_current | Double | 所得税 - 国内 - 当期 |
| is_income_taxes_foreign_current | Double | 所得税 - 外国 - 经常 |
| is_income_taxes_other_current | Double | 所得税 - 其他 (KFAS/NLST) - 当前 |
| is_income_taxes_deferred | Double | 所得税 - 递延 |
| is_income_taxes_domestic_deferred | Double | 所得税 - 国内 - 递延 |
| is_income_taxes_foreign_deferred | Double | 所得税 - 外国 - 递延 |
| is_income_taxes_other_deferred | Double | 所得税 - 其他 - 递延 |
| is_income_taxes_other_type | Double | 所得税 - 其他（按类型） |
| is_net_income_after_tax | Double | 税后净利润 |
| is_equity_earnings_affiliates | Double | 附属公司的收益/（损失）权益（税后） |
| is_non_recurring_equity_earnings | Double | 非经常性股权收益部分 |
| is_after_tax_adj_other | Double | 税后调整 - 其他 - 收入/（支出） - 总计 |
| is_tax_impact_discontinued_ops | Double | 对税前停产业务的估计税收影响 |
| is_zakat | Double | 天课 |
| is_after_tax_special_reserves | Double | 税后调整 - 特别储备金 |
| is_income_before_discontinued | Double | 终止经营和非经常性项目之前的收入 |
| is_extraordinary_after_tax | Double | 特别活动 - 税后 - 收益/（损失） |
| is_discontinued_ops_net | Double | 终止经营净额 - 总计 - 收入/（支出） |
| is_discontinued_ops_income | Double | 终止经营 - 净额 - 收入/（支出） |
| is_sale_discontinued_ops_gl | Double | 出售终止经营业务 - 净值 - 收益/（损失） |
| is_discontinued_ops_bt | Double | 税前已终止经营业务总计 - 收入/（支出） |
| is_discontinued_ops_bt_income | Double | 税前终止经营 - 收入/（支出） |
| is_sale_discontinued_ops_bt_gl | Double | 税前出售已终止业务 - 收益/（损失） |
| is_discontinued_ops_tax | Double | 停产业务 - 税务影响 |
| is_accounting_changes | Double | 会计准则变更的影响 |
| is_extraordinary_items | Double | 非凡物品 |
| is_covid_19_tax_charge | Double | COVID-19 所得税 - 一次性费用/（贷项） |
| is_extraordinary_tax_impact | Double | 特别项目 - 税收影响 |
| is_net_income_before_minority | Double | 扣除少数股东权益之前的净利润 |
| is_minority_interest | Double | 少数股东权益 |
| is_net_income | Double | 扣除少数股东权益后的净利润 |
| is_hybrid_debt_interest | Double | 利息支出 - 混合债务工具 - 股权 |
| is_general_partner_dist | Double | 普通合伙人的分配 |
| is_preferred_shares_dist | Double | 优先股分配 |
| is_policyholders_surplus | Double | 保单持有人盈余 |
| is_earnings_adj | Double | 净利润的盈利调整 - 其他费用/（收入） |
| is_income_available_common | Double | 普通股可用收入 |
| is_oci_start | Double | 其他综合收入 - 起跑线 |
| is_oci_fx | Double | 其他综合收入 - 外币 |
| is_oci_unrealized_inv_gl | Double | 其他综合收入 - 未实现投资收益/（损失） |
| is_oci_hedging_gl | Double | 其他综合收益 - 对冲收益/（损失） |
| is_oci_revaluation | Double | 其他综合公司 - 有形和无形资产重估 |
| is_oci_other | Double | 其他综合收入 - 其他 |
| is_oci_unearned | Double | 其他综合收入 - 非劳动收入 |
| is_oci_discontinued | Double | 其他综合收益 - 已终止经营业务 |
| is_oci_associated | Double | 其他综合收入 - 联营公司 |
| is_oci_pension | Double | 其他综合收入 - 养老金相关 |
| is_oci_tax | Double | 其他综合收入 - 所得税 |
| is_oci_net | Double | 其他综合收入 - 税后 - 总计 |
| is_comprehensive_income_before_minority | Double | 扣除少数股东权益之前的综合收入 - 总计 |
| is_comprehensive_income_minority | Double | 综合收入 - 少数股东权益 - 总计 |
| is_comprehensive_income_pref_div | Double | 综合收益 - 优先股股息 |
| is_comprehensive_income_parent | Double | 综合收益 - 母公司股东 - 合计 |
| is_basic_eps_inc_exord | Double | 净利润基本包括特别项目，普通 - 总计 |
| is_income_common_excl_exord | Double | 普通人可获得的收入（不包括特殊项目） |
| is_basic_eps_shares | Double | 用于计算基本每股收益的股份 - 总计 |
| is_eps_basic_inc_exord | Double | EPS - 基本 - 包括特殊项目、普通 - 总计 |
| is_eps_basic_excl_exord | Double | EPS - 基本 - 不包括特殊项目，普通 - 总计 |
| is_eps_basic_normalized | Double | EPS - 基本 - 不包括特殊项目 - 标准化 - 总计 |
| is_eps_basic_non_gaap | Double | 每股收益 - 基本 - 非 GAAP - 总计 |
| is_allocated_net_income_inc_exord | Double | 分配的净利润，包括 Exord，普通 - 特定问题 |
| is_earnings_alloc_factor_basic | Double | 收益分配因素 - 基本 - 特定问题 |
| is_basic_eps_shares_issue | Double | 用于计算基本每股收益的股份 - 特定问题 |
| is_eps_basic_inc_exord_issue | Double | EPS - 基本 - 包括特殊、常见 - 特定问题 |
| is_eps_basic_excl_exord_issue | Double | EPS - 基本 - 排除 Exord 项目，常见 - 特定问题 |
| is_eps_basic_normalized_issue | Double | EPS - 基本 - 排除 Exord 项目 - 标准化 - 特定问题 |
| is_eps_basic_non_gaap_issue | Double | EPS - 基本 - 非 GAAP - 特定问题 |
| is_basic_eps_shares_dr | Double | 用于计算基本每股收益的股票 - 特定问题 - DR |
| is_eps_basic_inc_exord_dr | Double | EPS - 基本 - 包括 Exord 项目，常见 - 特定问题 - DR |
| is_eps_basic_excl_exord_dr | Double | EPS - 基本 - 排除 Exord，通用 - 特定问题 - DR |
| is_eps_basic_normalized_dr | Double | EPS - 基本排除 Exord 项目规范化特定问题 - DR |
| is_eps_basic_non_gaap_dr | Double | EPS - 基本 - 非 GAAP - 特定问题 - DR |
| is_basic_eps_shares_cpo | Double | 用于计算基本每股收益的股票 - 特定发行 - CPO |
| is_eps_basic_inc_exord_cpo | Double | EPS - 基本 - 包括 Exord 项目，常见 - 特定问题 - CPO |
| is_eps_basic_excl_exord_cpo | Double | EPS - 基本 - 不包括 Exord，通用 - 特定问题 - CPO |
| is_eps_basic_normalized_cpo | Double | EPS - 基本排除 Exord 项目规范化特定问题 - CPO |
| is_eps_basic_non_gaap_cpo | Double | EPS - 基本 - 非 GAAP - 特定问题 - CPO |
| is_eps_basic_discontinued | Double | EPS - 基本来自停产行动和特殊物品 |
| is_participation_weight_primary | Double | EPS Calc 的主要参与权重 - 特定问题 |
| is_earnings_participation_factor | Double | 收益参与因子 - 特定问题 |
| is_priority_dividends | Double | 优先股息 - 特定问题 |
| is_comp_eps_basic_issue | Double | 每股综合收益 - 基本 - 特定问题 |
| is_comp_eps_basic_dr | Double | 综合每股收益 - 基本问题特定预托凭证 |
| is_comp_eps_basic_cpo | Double | 综合每股收益 - 基本问题特定 CPO |
| is_dilution_adj | Double | 稀释调整 |
| is_diluted_eps_inc_exord | Double | 摊薄净利润，包括非经常性项目，普通 - 总计 |
| is_diluted_income_excl_exord | Double | 稀释收入，不包括非常项目，普通 |
| is_diluted_shares | Double | 用于计算稀释每股收益的股份 - 总计 |
| is_eps_diluted_inc_exord | Double | EPS - 稀释后 - 包括特殊项目，普通 - 总计 |
| is_eps_diluted_excl_exord | Double | EPS - 稀释 - 不包括适用于共同总计的 Exord 项目 |
| is_eps_diluted_normalized | Double | EPS - 稀释后 - 不包括特殊项目 - 标准化 - 总计 |
| is_eps_diluted_non_gaap | Double | 每股收益 - 稀释后 - 非 GAAP - 总计 |
| is_allocated_diluted_inc_exord | Double | 已分配稀释净额公司，包括 Exord、普通问题特定问题 |
| is_earnings_alloc_factor_diluted | Double | 盈利分配系数 - 稀释 - 特定问题 |
| is_diluted_shares_issue | Double | 用于计算每股收益的股份 - 稀释 - 特定发行 |
| is_eps_diluted_inc_exord_issue | Double | EPS - 稀释 - 包括 Exord 项目，常见 - 特定问题 |
| is_eps_diluted_excl_exord_issue | Double | EPS - 稀释 - 不包括 Exord 项目，常见 - 特定问题 |
| is_eps_diluted_normalized_issue | Double | EPS - 稀释 - 不包括 Exord 项目 - 标准化 - 问题规范 |
| is_eps_diluted_non_gaap_issue | Double | 每股收益 - 稀释 - 非 GAAP - 特定问题 |
| is_diluted_shares_dr | Double | 用于计算稀释每股收益的股票 - 特定问题 - DR |
| is_eps_diluted_inc_exord_dr | Double | EPS - 稀释 - 包括 Exord、普通 - 特定问题 - DR |
| is_eps_diluted_excl_exord_dr | Double | EPS - 稀释 - 不包括 Exord，普通 - 特定问题 - DR |
| is_eps_diluted_normalized_dr | Double | EPS - Dil - 排除 Exord 项目 - 标准化 - 问题规范 - DR |
| is_eps_diluted_non_gaap_dr | Double | EPS - 稀释 - 非 GAAP - 特定问题 - DR |
| is_diluted_shares_cpo | Double | 用于计算稀释每股收益的股票 - 特定发行 - CPO |
| is_eps_diluted_inc_exord_cpo | Double | EPS - 稀释 - 包括 Exord，普通 - 特定问题 - CPO |
| is_eps_diluted_excl_exord_cpo | Double | EPS - Dil - 排除 Exord 项目，常见 - 特定问题 - CPO |
| is_eps_diluted_normalized_cpo | Double | EPS Dil - 排除 Exord 项目 - 标准化 - 问题规范 - CPO |
| is_eps_diluted_non_gaap_cpo | Double | EPS - 稀释 - 非 GAAP - 特定问题 - CPO |
| is_eps_diluted_discontinued | Double | EPS - 因停产业务和特殊项目而稀释 |
| is_comp_eps_diluted_issue | Double | 每股综合收益 - 稀释 - 特定问题 |
| is_comp_eps_diluted_dr | Double | 综合每股收益 - 稀释发行特定预托凭证 |
| is_comp_eps_diluted_cpo | Double | 综合每股收益 - 稀释 - 特定问题 - CPO |
| is_dps_common_gross | Double | 每股股息 - 普通股 - 总额 - 特定发行股 |
| is_dps_common_net | Double | 每股股息 - 普通 - 净额 - 特定发行 |
| is_dps_special | Double | 每股股息 - 特别 - 特定发行 |
| is_dps_special_net | Double | 每股股息 - 特别 - 净额 - 特定发行 |
| is_dps_common_gross_dr | Double | 每股股息 - 普通股息 - 总额 - 特定发行 - DR |
| is_dps_common_net_dr | Double | 每股股息 - 普通股息 - 净额 - 特定发行 - DR |
| is_dps_special_gross_dr | Double | 每股股息 - 特别 - 总额 - 特定发行 - DR |
| is_dps_special_net_dr | Double | 每股股息 - 特别 - 净额 - 特定发行 - DR |
| is_dps_common_gross_cpo | Double | 每股股息 - 普通股 - 总额 - 特定发行股 - CPO |
| is_dps_common_net_cpo | Double | 每股股息 - 普通股息 - 净额 - 特定发行 - CPO |
| is_dps_special_gross_cpo | Double | 每股股息 - 特别 - 总额 - 特定发行 - CPO |
| is_dps_special_net_cpo | Double | 每股股息 - 特别 - 净额 - 特定发行 - CPO |
| is_ebit | Double | 息税前利润 (EBIT) |
| is_ebitda | Double | 利息税折旧及摊销前利润 |
| is_ebitda_exploration | Double | 利息税前收益 Depr 摊销及勘探费用 |
| is_ebitda_lease | Double | 利息税前收益 Depr & Amort & Optg Lease Pymt |
| is_depr_inv_property | Double | 折旧 - 投资性房地产 - 补充 |
| is_depr_amort | Double | 折旧和摊销 - 补充 |
| is_depr_expense | Double | 折旧费用 - 总计 - 补充 |
| is_depr_finance_lease_rou | Double | 折旧 - 融资租赁使用权资产 - 补充 |
| is_amort_total | Double | 摊销 - 总计 - 补充 |
| is_goodwill_amort | Double | 商誉摊销 - 补充 |
| is_other_intang_amort | Double | 无形摊销 - 其他 - 补充 |
| is_amort_below_above_market_leases | Double | 低于/高于市场租赁的摊销 - 补充 |
| is_amort_tenant_leases | Double | 租户关系和就地租赁的摊销 - Supp |
| is_amort_license_contract | Double | 许可、特许经营权、版权、基于合同的供应的金额 |
| is_amort_software | Double | 计算机软件摊销 - 补充 |
| is_amort_brands_patents | Double | 品牌、专利、商标、市场和艺术的数量 -Suppl |
| is_amort_fin_lease_rou | Double | 融资租赁使用权资产摊销 - 补充 |
| is_amort_cap_r_and_d | Double | 资本化研发费用摊销 - 补充 |
| is_amort_deferred_costs | Double | 递延成本摊销 - 补充 |
| is_depr_depletion_amort | Double | 折旧消耗和摊销 - 总计 |
| is_depreciation | Double | 折旧 - 总计 |
| is_amort_intang_incl_gw | Double | 包括商誉在内的无形资产摊销 - 总计 |
| is_amort_goodwill | Double | 商誉摊销 - 总计 |
| is_amort_intang_excl_gw | Double | 无形资产摊销（不包括商誉） - 总计 |
| is_amort_deferred_charges | Double | 递延费用摊销 - 总计 |
| is_islamic_financing_income | Double | 伊斯兰融资和投资收入 |
| is_islamic_income | Double | 伊斯兰收入 |
| is_r_and_d_total | Double | 研发费用 - 费用化和资本化 - 总计 - 补充 |
| is_r_and_d_expense | Double | 研究与开发费用 - 补充 |
| is_r_and_d_capitalized | Double | 研究与开发费用 - 资本化 - 补充 |
| is_labor_expenses | Double | 人工及相关费用 - 总计 |
| is_labor_expenses_supp | Double | 人工及相关费用 - 补充 |
| is_stock_comp_net_tax | Double | 股票补偿费用 - 税后 - 补充 |
| is_stock_comp_pretax | Double | 股票补偿费用 - 税前 - 补充 |
| is_stock_comp_tax_benefit | Double | 股票补偿 - 税收优惠 - 补充 |
| is_auditor_fees | Double | 审计费 |
| is_audit_related_fees | Double | 审计相关费用 |
| is_tax_fees | Double | 税费 |
| is_fees_other | Double | 费用 - 其他 |
| is_non_gaap_revenue | Double | 非 GAAP 收入 - 公司报告 |
| is_non_gaap_op_income | Double | 非公认会计原则运营收入 - 公司报告 |
| is_non_gaap_net_income | Double | 非 GAAP 调整后净利润 - 公司报告 |
| is_non_gaap_ebitda | Double | 非 GAAP 调整后 EBITDA - 公司报告 |
| is_non_gaap_eps_basic | Double | 非公认会计准则每股收益基本 - 公司报告 |
| is_non_gaap_eps_diluted | Double | 非 GAAP 摊薄每股收益 - 公司报告 |
| is_non_gaap_op_margin | Double | 非 GAAP 营业利润率 % - 公司报告 |
| is_reported_net_income_ng | Double | 报告 - 净利润 - 非 GAAP |
| is_reported_non_recurring_ng | Double | 报告 - 非经常性项目 - 非 GAAP |
| is_reported_tax_impact_ng | Double | 报告 - 非经常性项目的税务影响 - 非公认会计原则 |
| is_reported_normalized_ni | Double | 报告 - 标准化净利润 |
| is_non_recurring_tax_impact | Double | 非经常性/异常项目 - 税收影响 |
| is_non_recurring_tax_impact | Double | 非经常性项目 - 对所得税的影响 |
| is_normalized_after_tax | Double | 标准化税后利润 |
| is_normalized_ni_cont_ops | Double | 持续经营业务标准化净利润 |
| is_normalized_ni | Double | 标准化净利润 - 底线 |
| is_normalized_ebit | Double | 息税前利润 (EBIT) - 标准化 |
| is_normalized_ebitda | Double | 利息税前收益折旧及摊销 - 标准化 |
| is_deriv_realized_gl_rev | Double | 衍生品 - 已实现收益/（损失） - 收入 - 补充 |
| is_deriv_realized_gl_cogs | Double | 衍生品 - 已实现收益/（损失） - COGS - Suppl |
| is_deriv_realized_gl_int | Double | 衍生品 - 已实现收益/（损失） - 利息费用补充 |
| is_deriv_realized_gl_other | Double | 衍生品 - 已实现收益/（损失） - 其他 - 补充 |
| is_deriv_realized_gl_total | Double | 衍生品 - 已实现收益/（损失） - 总计 - 补充 |
| is_deriv_hedge_gl_total | Double | 衍生品 - 对冲 - 收益/（损失） - 总计 - 补充 |
| is_unrealized_deriv_adj | Double | 对冲衍生品的未实现调整 - Suppl |
| is_deriv_hedge_realized_gl_total | Double | 衍生品 - 对冲 - 已实现收益/（损失） - 总计 - 补充 |
| is_deriv_hedge_effective_gl | Double | 衍生品 - 对冲 - 有效收益/（损失） - 补充 |
| is_deriv_hedge_ineffective_gl | Double | 衍生品 - 对冲 - 无效收益/（损失） - Suppl |
| is_early_term_deriv_hedge_gl | Double | 衍生品对冲提前终止 - 收益/（损失） - Suppl |
| is_trading_deriv_gl | Double | 衍生品交易 - 收益/（损失） - 补充 |
| is_loan_losses_net | Double | 贷款损失 - 净额 |
| is_loan_recoveries | Double | 贷款回收 - 实际 |
| is_loan_losses | Double | 贷款损失 - 实际 |
| is_avg_employees | Double | 员工 - 平均 |
| is_operating_lease_expense | Double | 租金/经营租赁费用 |
| is_advertising_expense | Double | 广告费用 - 补充 |
| is_exploration_expense | Double | 勘探费用 |
| is_us_gaap_adj | Double | 美国公认会计准则调整 |
| is_int_div_income_after_llp | Double | LLP 后的利息和股息收入 - 净 - 财务 |
| is_revenue_after_loan_prov | Double | 扣除贷款拨备后的收入 - 净额 - 财务 |
| is_purchase_inv_sec | Double | 购买投资证券 - 补充 |
| is_sale_inv_sec | Double | 投资证券销售 - 补充 |
| is_epra_net_income | Double | EPRA/经常性净利润 |
| is_sec_comm_fees | Double | 证券活动的佣金和费用 |
| is_cost_revenue_inc_o_and_m | Double | 收入成本，包括运营和维护（公用事业）总计 |
| is_cost_revenues_excl_depr | Double | 不包括折旧的收入成本 |
| is_fx_gl | Double | 外汇收益/（损失） |
| is_generation_cost | Double | 发电成本 |
| is_interest_expense | Double | 利息支出 |
| is_inv_gl | Double | 投资收益/（损失） |
| is_inv_income_insurance | Double | 投资收入 - 保险 |
| is_losses_benefits_insurance | Double | 损失福利和调整 - 保险 |
| is_non_int_expense_bank | Double | 非利息费用 - 银行 |
| is_operating_expenses | Double | 营业费用 |
| is_premiums_ceded_unearned_total | Double | 分出和不劳而获的保费 - 总计 |
| is_sga_excl_r_and_d | Double | 销售一般及行政费用，不包括研发费用 |
| is_total_claim_loss_exp | Double | 索赔和损失费用总额 |
| is_underwriting_commissions | Double | 承保及佣金 |
| is_underwriting_exp_insurance | Double | 承保费用 - 保险 |
| is_net_premiums_written | Double | 净保费承保 |
| is_losses_benefits_total | Double | 损失、收益和调整 - 总计 |
| is_op_exp_excl_non_cash | Double | 不包括非现金费用的运营费用 - 总计 |
| is_premiums_earned | Double | 已赚取保费 - 总计 |
| is_commissions_fees | Double | 佣金和费用 |
| is_est_tax_rate | Double | 预计税率 |
| is_exploration_int_exp_after_tax | Double | 勘探费用和利息费用（税后） |
| is_fixed_charges | Double | 固定费用 |
| is_income_common_before_depr_amort | Double | 折旧和摊销前普通股可用收入 |
| is_income_bt_before_loan_prov | Double | 税前收入和贷款损失拨备 |
| is_income_earning_assets | Double | 赚取资产的收入 |
| is_revenue_net_int_before_loan_prov | Double | 贷款损失拨备前的收入扣除利息支出 |
| is_tax_adj_op_income | Double | 税收调整后营业收入 |
| is_underwriting_minus_losses | Double | 承保费用减去损失、福利和调整 - 保险 |
| is_water_steam_revenue | Double | 水和蒸汽收入 |
| is_reported_recurring_revenue | Double | 报告 - 收入 - 经常性 |
| is_reported_net_premiums_written | Double | 报告 - 净保费承保 |
| is_reported_revenue | Double | 报告 - 收入 - 总计 |
| is_reported_op_revenue | Double | 报告-营业收入 |
| is_reported_cost_revenues | Double | 报告 - 收入成本 |
| is_reported_sga | Double | 报告 - 销售一般及行政费用 |
| is_reported_gross_profit | Double | 报告 - 毛利润 |
| is_reported_op_profit | Double | 报告-营业利润 |
| is_reported_op_margin | Double | 报告 - 营业利润率 |
| is_reported_ordinary_profit | Double | 报告 - 普通利润 |
| is_reported_net_income | Double | 报告 - 税后净利润 |
| is_reported_basic_eps | Double | 报告 - 基本每股收益 |
| is_reported_diluted_eps | Double | 报告 - 稀释每股收益 |
| is_reported_business_profit | Double | 报告 - 营业利润 - 净额 |
| is_lease_expense_total | Double | 租赁费用-总计-补充 |
| is_operating_lease_expense | Double | 运营/租赁费用 - 补充 |
| is_depr_fin_lease_rou | Double | 融资租赁 ROU 资产折旧 - 补充 |
| is_amort_fin_lease_rou | Double | 融资租赁 ROU 资产摊销 - 补充 |
| is_variable_lease_expense | Double | 可变租赁费用 - 未分类 - 补充 |
| is_variable_op_lease_expense | Double | 可变经营租赁费用 - 美国公认会计准则 - 补充 |
| is_variable_fin_lease_expense | Double | 可变融资租赁费用 - 补充 |
| is_int_exp_fin_lease | Double | 融资租赁负债的利息支出 - Supplement |
| is_short_term_lease_cost | Double | 短期租赁成本 - 补充 |
| is_sublease_income | Double | 转租收入 - 补充 |
| is_ffo | Double | 运营资金 (FFO) - REIT |
| is_effective_tax_rate | Double | 实际有效税率 |
| is_statutory_tax_rate | Double | 正常有效法定税率 |

#### 2.4. 使用示例

##### 2.4.1. 获取一定季度内某只股票的财务季度报告

```python
import tqx_data
result = tqx_data.get_financial_statement(
    market="hk",
    symbol="0700.HK",
    start_quarter="2020q1",
    end_quarter="2024q4",
    date="20241014",
    is_latest=False,
    fields=[]
)
print(result)
```

**响应示例**

```text
symbol fy_period date ... is_write_off_real_estate is_zakat quarter
0 0700.HK FY2020Q1 20200513 ... None None 2020q1
1 0700.HK FY2020Q2 20200826 ... None None 2020q2
... ... ... ... ... ... ...
14 0700.HK FY2023Q3 20231115 ... None None 2023q3
```

##### 2.4.2. 获取一定季度内某只股票的最新财务季度报告且使用fields

```python
import tqx_data

result = tqx_data.get_financial_statement(
    market="hk",
    symbol="0700.HK",
    start_quarter="2020q1",
    end_quarter="2024q4",
    date="20241014",
    is_latest=True,
    interim_type="cumulative",
    fields=["symbol", "fy_period", "date", "bs_asset_accruals"],
)
print(result)
```

**响应示例**

```text
symbol fy_period date bs_asset_accruals
0 0700.HK FY2024Q2 20240827 1.497963e+12
```

这里的“最新”表示 `0700.HK` 在 `20241014` 及之前公告日期最大的一行。它不返回每个历史财期各自的
最新版，因此不能直接用于同比计算。

##### 2.4.3. 历史截面和同比计算

```python
import re
import numpy as np
import pandas as pd
import tqx_data

as_of_date = "20250101"
rows = tqx_data.get_financial_statement(
    market="nb",
    symbol=["NVDA.NB", "AVGO.NB"],
    start_quarter="2023q1",
    end_quarter="2024q4",
    date=as_of_date,
    is_latest=False,
    interim_type="cumulative",
    fields=[
        "symbol", "fy_period", "date",
        "is_reported_revenue", "is_revenue_business_total",
        "is_reported_gross_profit", "is_gross_profit",
        "cfs_net_cf_operating", "cfs_reported_cf_operating",
    ],
)

# 同一财期可能存在多次披露，只保留截止日前公告日期最新的版本。
rows["date_key"] = pd.to_datetime(rows["date"], errors="coerce")
rows = rows.dropna(subset=["symbol", "fy_period", "date_key"])
rows = rows.sort_values("date_key").drop_duplicates(
    ["symbol", "fy_period"], keep="last"
)

def parse_period(value):
    match = re.fullmatch(r"FY(\d{4})(.+)", str(value).upper())
    return (int(match.group(1)), match.group(2)) if match else None

def previous_year_period(value):
    parsed = parse_period(value)
    return f"FY{parsed[0] - 1}{parsed[1]}" if parsed else None

def period_sort_key(value):
    parsed = parse_period(value)
    if not parsed:
        return (0, 0, "")
    year, suffix = parsed
    rank = {"Q1": 1, "H1": 2, "Q2": 2, "Q3": 3,
            "H2": 4, "Q4": 4, "FY": 4}.get(suffix, 0)
    return (year, rank, suffix)

def first_finite(row, candidates):
    for field in candidates:
        value = pd.to_numeric(row.get(field), errors="coerce")
        if pd.notna(value) and np.isfinite(value):
            return float(value)
    return None

# 按财期而不是公告日期选择当前可见的最新财期，再匹配上年同财期。
period_keys = rows["fy_period"].map(period_sort_key)
rows[["period_year", "period_rank", "period_suffix"]] = pd.DataFrame(
    period_keys.tolist(), index=rows.index
)
latest = rows.sort_values(
    ["symbol", "period_year", "period_rank", "period_suffix", "date_key"]
).groupby("symbol", as_index=False).tail(1)
history = rows.set_index(["symbol", "fy_period"])
screening = []
for _, current in latest.iterrows():
    prior_key = (current["symbol"], previous_year_period(current["fy_period"]))
    if prior_key[1] is None or prior_key not in history.index:
        continue
    prior = history.loc[prior_key]
    current_revenue = first_finite(
        current, ["is_reported_revenue", "is_revenue_business_total"]
    )
    prior_revenue = first_finite(
        prior, ["is_reported_revenue", "is_revenue_business_total"]
    )
    gross_profit = first_finite(
        current, ["is_reported_gross_profit", "is_gross_profit"]
    )
    operating_cf = first_finite(
        current, ["cfs_net_cf_operating", "cfs_reported_cf_operating"]
    )
    if None in (current_revenue, prior_revenue, gross_profit, operating_cf):
        continue
    if current_revenue <= 0 or prior_revenue <= 0:
        continue
    revenue_growth = current_revenue / prior_revenue - 1.0
    gross_margin = gross_profit / current_revenue
    screening.append({
        "symbol": current["symbol"],
        "fy_period": current["fy_period"],
        "revenue_growth": revenue_growth,
        "gross_margin": gross_margin,
        "operating_cf": operating_cf,
        "eligible": revenue_growth > 0.20 and gross_margin > 0.20 and operating_cf > 0,
    })

screening = pd.DataFrame(screening)
```

收入、毛利和经营现金流在不同公司可能只填充兼容字段之一。常用候选依次为：

- 收入：`is_reported_revenue`、`is_revenue_business_total`
- 毛利：`is_reported_gross_profit`、`is_gross_profit`
- 经营现金流：`cfs_net_cf_operating`、`cfs_reported_cf_operating`

选择字段后先用 `pd.to_numeric(..., errors="coerce")` 转换，删除空字符串、`NaN` 和正负无穷；收入同比的
上年同财期收入必须大于 0。财期应按返回的 `fy_period` 实际后缀匹配，不要假定所有市场都只返回季度格式。

##### 2.4.4. 为一年回测构建无未来数据的动态财务面板

下面演示一次预取、逐调仓日切片的关键顺序。`period_sort_key`、`previous_year_period` 和字段清洗可以复用
上一节函数：

```python
import pandas as pd
import tqx_data

backtest_end = "20251231"
all_rows = tqx_data.get_financial_statement(
    market="nb",
    symbol=nasdaq_100_symbols,
    # 公司财年可能领先公告自然年；同时要覆盖同比所需的上年同财期。
    start_quarter="2023q1",
    end_quarter="2026q4",
    date=backtest_end,
    is_latest=False,
    interim_type="cumulative",
    fields=required_financial_fields,
)
all_rows["date_key"] = pd.to_datetime(all_rows["date"], errors="coerce")
all_rows = all_rows.dropna(subset=["symbol", "fy_period", "date_key"])

def visible_financials(as_of_date):
    cutoff = pd.to_datetime(as_of_date, format="%Y%m%d")

    # 必须先按调仓日过滤，再处理同一财期的重述版本。
    visible = all_rows[all_rows["date_key"] <= cutoff].copy()
    visible = visible.sort_values("date_key").drop_duplicates(
        ["symbol", "fy_period"], keep="last"
    )
    assert visible.empty or visible["date_key"].max() <= cutoff

    keys = visible["fy_period"].map(period_sort_key)
    visible[["period_year", "period_rank", "period_suffix"]] = pd.DataFrame(
        keys.tolist(), index=visible.index
    )
    latest = visible.sort_values(
        ["symbol", "period_year", "period_rank", "period_suffix", "date_key"]
    ).groupby("symbol", as_index=False).tail(1)
    return visible, latest

panel_rows = []
for rebalance_date in rebalance_dates:  # 例如每 5 个交易日
    history, latest = visible_financials(rebalance_date)
    history = history.set_index(["symbol", "fy_period"])
    for _, current in latest.iterrows():
        prior_period = previous_year_period(current["fy_period"])
        prior_key = (current["symbol"], prior_period)
        if prior_period is None or prior_key not in history.index:
            continue
        prior = history.loc[prior_key]
        # 按 2.4.3 的兼容字段和有限值规则计算同比、毛利率、经营现金流。
        metrics = calculate_financial_metrics(current, prior)
        if metrics is None:
            continue
        panel_rows.append({
            "date": rebalance_date,
            "symbol": current["symbol"],
            "fy_period": current["fy_period"],
            "source_date": current["date"],
            **metrics,
        })

financial_panel = pd.DataFrame(panel_rows)
```

`calculate_financial_metrics` 应返回清洗后的 `revenue_growth`、`gross_margin`、`operating_cf` 和 `eligible`。
若调仓频率是每 5 个交易日，面板也按每 5 个交易日生成；财务数值可以在两次公告之间保持不变，但资格
判断必须在新公告后的下一调仓日更新。不要在 `handle_data` 每个 bar 重新查询接口，应在离线阶段或
`initialize` 中一次构建并缓存面板。

**四. 交易工具**

**1.获取汇率数据**

#### 1.1. 方法名：get_currency

#### 1.2. 入参

| 字段 | 类型 | 描述 | 是否必填 |
|:---|:---|:---|:---|
| start_date | Optional\[str\] | 开始日期,eg:"20250702" | 非必填 |
| end_date | Optional\[str\] | 结束日期,eg:"20250702" | 非必填 |
| fields | Optional\[Union\[str, List\[str\]\]\] | 汇率列表 | 非必填 |

#### 1.3. 响应参数

| 字段    | 类型   | 描述         |
|:--------|:-------|:-------------|
| date    | str    | 日期         |
| CNY_HKD | double | 人民币对港币 |
| CNY_USD | double | 人民币对美元 |
| HKD_USD | double | 港币对美元   |
| HKD_CNY | double | 港币对人民币 |
| USD_CNY | double | 美元对人民币 |
| USD_HKD | double | 美元对港币   |

#### 1.4. 使用示例

##### 1.4.1. 获取单支港股的部分回测因子

```python
import tqx_data
result = tqx_data.get_currency(
    start_date="20260101",
    end_date="20260131",
    field=[],
)
print(result)
```
