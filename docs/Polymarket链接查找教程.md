# Polymarket 链接查找教程

赛前 6 列表最后一格必须是**可点击**的下单链接。读盘用图上数字；找链接是第二步，**不准拿网上赔率改图上的数**。对不上就写「无链接」，禁止瞎编地址。

主人买的是预测市场里的胜/平/负（尤其是平），**不推国内让球对冲**。

## 一、先有场次代号和对阵

### 已经知道「周二012 / 西班牙 vs 克罗地亚」

直接进入第三节。

### 主人只发了时序图（没队名）

1. 记下图上**最后一行**胜、平、负，以及让球档（-1 / +1 / -2）和让胜、让平、让负。
2. 拉体彩现价（Windows 要加证书开关和浏览器伪装，否则会被拦）：

```bash
curl.exe -sS --ssl-no-revoke -A "Mozilla/5.0" -H "Referer: https://www.lottery.gov.cn/" "https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry?channel=c"
```

3. 用终盘三档数字去对 `had`（胜平负）和 `hhad`（让球，含 `goalLine`）。**三档都对上才算同一场**。只对上胜平负、让球对不上，不算。
4. 对上了：写出【周X00X】主队 vs 客队。对不上：**不给链接**，问主人是哪场、哪家公司。

2026-09-29 实例：图上终盘 3.15 / 2.92 / 2.13 且 +1 让胜 1.53 = 周二012 卢森堡 vs 冰岛；终盘 1.11 / 6.60 / 13.00 且 -2 让平 3.65 = 周二013 西班牙 vs 克罗地亚。数字像欧国联、对上却是友谊赛的，要标明不是欧国联。

## 二、日期怎么取

链接里的日期是**开球日（国际日期）**，不是中国日历的「明天凌晨」。

中国 02:45 开球（例如 2026-09-30 02:45）→ 链接日期常用 **2026-09-29**。拿不准就用队名去搜，不要死拼日期。

## 三、标准三步核验法（强制全网检索，严禁偷懒调死接口）

**为什么之前总是查不到？血泪教训**：
1. **中英文断层**：Polymarket 全站为纯英文（如 "West Ham United", "QPR"），直接用中文队名调用 Polymarket API 必定 100% 返回空！
2. **标签碎片化**：Polymarket 联赛标签极细（如英冠是 `efl-championship`，英超是 `premier-league`），只查 `soccer` 会漏掉大量次级与杯赛市场！
3. **严禁只调 API 碰壁即放弃**：严禁仅凭 API 返回 `[]` 就草率判定“未开盘”！

### 第一步（绝对强制首选）：实网全网精准检索
必须先使用 `web_search` 或 Google 检索，由搜索引擎自动完成中英文映射与最新 slug 定位：
```bash
# 语法：site:polymarket.com/event "主队英文名/别名" "客队英文名/别名"
site:polymarket.com/event "West Ham" "Queens Park Rangers"
```
或直接由 `BrowserOS neo` 访问 `https://polymarket.com/sports` 在页面顶端搜索框输入英文队名查找。

### 第二步：拿到页面 slug 后，核查流动性与可买报价
拿到 Google 检索出的链接或 slug 后，再调用官方接口或 BrowserOS neo 校验实盘交易池：
```bash
curl.exe -sS --ssl-no-revoke -A "Mozilla/5.0" "https://gamma-api.polymarket.com/events?slug=检索到的完整slug"
```

### 第三步：门禁判定标准
- 只有在：① `web_search (site:polymarket.com/event)` 查无此赛；② BrowserOS neo 页面搜索确认无池；③ Gamma API 英文全称无记录。
- **三者全部落空时**，才准许打标【Polymarket 未开放独立交易池】！
- 凡未经第一步全网实网检索就敢写“未开放”的，一律按作弊与虚假汇报严肃处理！

### 3）读价钱

市场列表里问题含 `win` / `draw`。先将 `outcomes`、`outcomePrices` 与 `clobTokenIds` 同位置对齐，确认 Yes 项，不能默认第一项就是 Yes。`outcomePrices` 是 Gamma 展示价，不是保证可成交的买入价。用美分说：`0.295` = **29.5¢**，约 **3.4 倍**（1÷0.295）。该倍数未扣费用，也不保证有卖单。

要核可买报价：查 CLOB 对应 Yes 合约的最佳卖价、可买数量、买卖差与报价时间。无卖单写当前无可买报价。实际成交价需成交记录。

分析胜负平仍以球探/体彩为准，**不要用这个市场的价钱当庄家底牌，也不进入十步去水基准**。

## 四、怎么写成可点的链接

格式：

`https://polymarket.com/zh/sports/联赛缩写/完整slug`

例子：

- 欧国联：[https://polymarket.com/zh/sports/unl/unl-lux-isl-2026-09-29](https://polymarket.com/zh/sports/unl/unl-lux-isl-2026-09-29)
- 友谊赛可能是 `fifa-friendly` 或 `fif`，以标签为准，例如美国 vs 智利：`fif-usa-chl-2026-09-29`

正文必须写成可点击的一行，不要只塞进代码块：

`[【周二012】卢森堡 vs 冰岛（平局 29.5¢ / 约 3.4 倍）](https://polymarket.com/zh/sports/unl/unl-lux-isl-2026-09-29)`

规矩：

- 一场一个链接。
- 先写体彩代号；对不上就写【体彩未开售/无场次代号】。
- 推平：链到该场页面，并写明平局现价。
- 推比分：告诉主人点队名下的 **Exact Score（准确比分）**，不要假装页面一打开就是波胆。
- 接口未找到实体写「未找到市场」，访问失败写「核验失败」；只有核实实体及开放状态后才写「未开盘」。**禁止拼一个 200 也打不开的地址**。

## 五、换 AI 时最少要做的

1. 读本文件。  
2. 有图无队名 → 对体彩现价 → 再查接口。  
3. 先 `events?slug=`，空了再 `public-search`。  
4. 6 列表最后一格放可点击链接或诚实写无。  
