# Polymarket 链接查找教程

> 📌 **官方权威文档总索引（Documentation Index）**：
> - **全局 LLM 发现索引**：`https://docs.polymarket.com/llms.txt`（AI 交互首选地图）
> - **全量中文 API 索引（220页）**：`https://docs.polymarket.com/_llms/cn.txt` 及 `_llms/cn/api.txt`
> - **三大核心接口**：Gamma API（市场发现）+ CLOB API（买卖挂单深度）+ Data API v2（历史统计）

赛前 7 列表最后一格必须是**可点击**的真实下单链接。读盘用图上数字；找链接是第二步，**不准拿网上赔率改图上的数**。对不上就写「无链接」，禁止瞎编地址。

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

### 第一步（绝对强制官方标准）：通过 `/sports` 字典与杯赛分类精准秒级定位

**为什么之前用 `public-search` 频繁翻车？血泪教训**：
1. **非体育市场严重冲刷（天气气温霸屏）**：例如查询米兰（Milan），`public-search` 前 5 条全部被米兰气温天气预测市场占满配额；
2. **历史完场老赛事占坑**：例如查询萨尔茨堡（Salzburg）或皇家社会（Sociedad），返回的全部是 2024/2025 历史欧冠；
3. **队名缩写与多语差异**：哥本哈根在 Polymarket Slug 缩写为丹麦语 `kob`，格拉茨风暴缩写为 `stu1`，圣吉联合缩写为 `usg`，全局文本模糊搜索无法匹配。

**官方标准发现流程（基于 https://docs.polymarket.com/market-data/discover-markets.md）**：
1. **查官方联赛分类字典**：
   调用 `https://gamma-api.polymarket.com/sports` 获取 484 个赛事的权威元数据映射：
   - 欧联杯 (UEL): `sport="uel"`, `series="10209"`, `primaryTag=101787`
   - 欧协联 (COL): `sport="col"`, `series="10437"`, `primaryTag=102763`
   - 解放者杯 (LIB): `sport="lib"`, `series="10289"`, `primaryTag=102562`
   - 英超 (EPL): `sport="epl"`, `series="10188"`, `primaryTag=306`
   - 欧冠 (UCL): `sport="ucl"`, `series="10204"`, `primaryTag=1234`
2. **按联赛 Series 或 Tag 批量拉取活跃事件（零污染、100% 命中）**：
   ```bash
   # Windows 下必须带 --ssl-no-revoke --http1.1 防止长 JSON 管道截断
   curl.exe -s --ssl-no-revoke --http1.1 -A "Mozilla/5.0" "https://gamma-api.polymarket.com/events?series_id=10209&closed=false&limit=100"
   ```
   一次请求即可拿到该联赛当前全部活跃比赛事件与真实 `slug`，直接按开球日期（如 2026-10-15）与对阵缩写秒级锁定目标。
3. **兜底检索（仅作为冷门小众联赛备用）**：
   若该赛事不在主流 `/sports` 列表中，才调用：
   ```bash
   curl.exe -s --ssl-no-revoke --http1.1 -A "Mozilla/5.0" "https://gamma-api.polymarket.com/public-search?q=英文队名"
   ```

### 第二步：拿到事件后，核查主客队序与衍生全系市场（波胆/半场/总进球）
拿到检索出的 `slug` 与 `event` 后，调用官方 Discover 接口校验：
1. **主客队权威仲裁（Identify Home and Away Teams）**：
   调用 `https://gamma-api.polymarket.com/events/slug/{slug}`，读取顶层 `teams` 数组：
   ```json
   "teams": [
     { "name": "Paris Saint-Germain FC", "ordering": "home" },
     { "name": "Stade Rennais FC", "ordering": "away" }
   ]
   ```
   严格核对 `ordering: "home"` 与 `ordering: "away"`，彻底杜绝主客对调错误。
2. **衍生全系市场裂变（List Events for a Game via `gameId`）**：
   读取事件中的 `gameId`（如 90104306），调用：
   ```bash
   curl.exe -sS --ssl-no-revoke "https://gamma-api.polymarket.com/events/keyset?game_id={gameId}&limit=20"
   ```
   一键拉取全套伴生事件：
   - 胜负平独赢盘：`{slug}`（对应市场类型 `moneyline`）
   - 波胆比分：`{slug}-exact-score`
   - 半场盘：`{slug}-halftime-result`
   - 衍生大盘：`{slug}-more-markets`（对应 `totals`、`spreads`）

### 第三步：门禁判定标准
- **核心主流联赛硬门禁**：五大联赛、欧冠、欧联、欧协联、英冠（ELC）、美职足（MLS）等核心联赛 Polymarket 100% 开盘，门禁强制拦截任何未开盘声明，必须查出真实链接！
- **极冷门边缘赛事核验**：只有在主队与客队英文名（含常用别名）经官方 Discover API 全面检索确无任何活跃标的时，方可标记为「官方未开盘」且保留空链接。
- **严禁免责声明套话**：严禁系统自动拼接或伪造任何类似「官方未开盘（经Gamma双向核验均无对应链上预测标的）」等假免责文本！违者一律物理熔断！

### 3）读价钱

市场列表里问题含 `win` / `draw`。先将 `outcomes`、`outcomePrices` 与 `clobTokenIds` 同位置对齐，确认 Yes 项，不能默认第一项就是 Yes。`outcomePrices` 是 Gamma 展示价，不是保证可成交的买入价。用美分说：`0.295` = **29.5¢**，约 **3.4 倍**（1÷0.295）。该倍数未扣费用，也不保证有卖单。

要核可买报价：查 CLOB 对应 Yes 合约的最佳卖价、可买数量、买卖差与报价时间。无卖单写当前无可买报价。实际成交价需成交记录。

分析胜负平仍以球探/体彩为准，**不要用这个市场的价钱当庄家底牌，也不进入十步去水基准**。

## 四、怎么写成可点的链接

格式：

`https://polymarket.com/event/完整slug`

例子：

- 亚冠精英：[https://polymarket.com/event/acle-vik-jeo-2026-10-14](https://polymarket.com/event/acle-vik-jeo-2026-10-14)
- 欧冠联赛：[https://polymarket.com/event/ucl-paris-saint-germain-vs-manchester-city](https://polymarket.com/event/ucl-paris-saint-germain-vs-manchester-city)
- 英冠联赛：[https://polymarket.com/event/elc-nor-sot-2026-10-14](https://polymarket.com/event/elc-nor-sot-2026-10-14)

正文必须写成可点击的一行，不要只塞进代码块：

`[【周三002】神户胜利 vs 全北现代](https://polymarket.com/event/acle-vik-jeo-2026-10-14)`

规矩：

- 一场一个链接。
- 格式统一为 `https://polymarket.com/event/{slug}`。
- 先写体彩代号；对不上就写【体彩未开售/无场次代号】。
- 严禁客户端拼接猜测 Slug！必须通过 `public-search?q={英文名}` 拿到官方 API 真实返回的 `slug`。
- 接口双向检索未找到实体写「官方未收录」；访问失败写「核验失败」。**禁止拼一个 200 也打不开的虚构地址**。

## 五、换 AI 时最少要做的

1. 读本文件。  
2. 有图无队名 → 对体彩现价 → 再查接口。  
3. 动态发现优先：`GET /public-search?q={TeamNameEn}`，核验对阵另一方并获取真实 `event.slug`。  
4. 7 列表最后一格放可点击有效链接（`https://polymarket.com/event/{slug}`）或诚实写官方未开盘。  
