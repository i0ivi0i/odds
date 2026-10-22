# 单场 28 端点唯一契约（人类镜像）

- **机器唯一源**：`config/endpoints.json`
- **本文件角色**：人类可读镜像；代码只读 JSON，不解析本表。
- **计数恒等式**：`28 = 4 core + 7 AH + 7 OU + 7 EU + 1 Polymarket + 2 panorama`
- **选择器铁律**：21 张 `changeDetail` 流水表只用 `#odds2 table`；`AsianOdds_n.aspx` 与 `OverDown_n.aspx` 两张全景总表才用 `#table_odds`。
- **编码铁律**：`1x2d.js`、分析页、波胆页、`analy.json`、Polymarket 用 UTF-8；所有 `changeDetail` 与两张全景总表用 GB18030。

- **双轨架构铁律**：Tier 1 为聚合核心端点（CDN秒出，从不封禁，含 23 家做市商欧指时序）；Tier 2 为单家流水与全景表（礼貌温和单并发，遭遇 IIS DIPR 临时掐断时平滑降级自愈）。

| # | Key | 组 | Tier | URL | 编码 | 选择器 | 必需 | 空态 | 门禁 |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| 1 | `1x2d.js` | core | 1 | `https://1x2d.titan007.com/{match_id}.js` | UTF-8 | 无 | 是 | 禁止空 | 21 个 euro cid 齐全 |
| 2 | `analysis.html` | core | 1 | `https://zq.titan007.com/analysis/{match_id}cn.htm` | UTF-8 | 无（完整 HTML） | 是 | 禁止空 | 页面有真实内容，无 WAF |
| 3 | `odds.html` | core | 1 | `https://zq.titan007.com/analysis/odds/{match_id}.htm` | UTF-8 | 无（完整 HTML） | 是 | 禁止空 | 页面有真实内容，无 WAF |
| 4 | `analy.json` | core | 1 | `https://zq.titan007.com/default/getAnalyData?sid={match_id}&t=1` | UTF-8 | 无 | 是 | `had:null` 合法 | JSON 可解析 |
| 5 | `ah_1.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=1&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 6 | `ah_3.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=3&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 7 | `ah_8.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=8&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 8 | `ah_12.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=12&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 9 | `ah_47.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=47&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 10 | `ah_42.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=42&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 188Bet 专用 |
| 11 | `ah_48.html` | AH | 2 | `https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID=48&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 12 | `ou_1.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=1&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 13 | `ou_3.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=3&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 14 | `ou_8.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=8&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 15 | `ou_12.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=12&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 16 | `ou_47.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=47&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 17 | `ou_42.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=42&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 188Bet 专用 |
| 18 | `ou_48.html` | OU | 2 | `https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID=48&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 19 | `eu_1.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=1&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 20 | `eu_3.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=3&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 21 | `eu_8.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=8&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 22 | `eu_12.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=12&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 23 | `eu_47.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=47&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 24 | `eu_42.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=42&l=0` | GB18030 | `#odds2 table` | 是 | `not_offered` 合法 | 188Bet 欧指可为空 |
| 25 | `eu_48.html` | EU | 2 | `https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID=48&l=0` | GB18030 | `#odds2 table` | 是 | 有未开盘证据才可空 | 7 家核心表 |
| 26 | `polymarket.json` | Polymarket | 1 | `https://gamma-api.polymarket.com/events?slug={polymarket_slug}` | UTF-8 | 无 | 是 | `[]` 合法 | JSON 可解析 |
| 27 | `asian_odds.html` | panorama | 2 | `https://vip.titan007.com/AsianOdds_n.aspx?id={match_id}` | GB18030 | `#table_odds` | 是 | 禁止空 | 初即全景表 |
| 28 | `over_under.html` | panorama | 2 | `https://vip.titan007.com/OverDown_n.aspx?id={match_id}` | GB18030 | `#table_odds` | 是 | 禁止空 | 初即全景表 |

## 空态与错误码

- `not_offered`：合法未开盘。必须带证据：Polymarket 返回 `[]`、`analy.json` 的 `had` 为 `null`、188Bet 的 `eu_42` 为空、HKJC 次级联赛亚盘页面明确写未开盘。
- `forbidden`：不允许空；空即 `empty_required_endpoint`。
- `duplicate_cid`：21 个 euro cid 有重复。
- `duplicate_odds_triplet`：同一机构同一时间出现重复赔率三元组。
- `bookmaker_mismatch`：表头机构与 key 不符。
- `entity_mismatch`：`1x2d.js` 的 `ScheduleID` 或队名与目标不符。
- `waf_blocked`：页面含 `Just a moment...`、`Cloudflare`、`Access Denied` 等盾标记。
- `replacement_char`：解码后含 U+FFFD。
