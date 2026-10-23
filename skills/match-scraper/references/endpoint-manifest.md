# 单场 28 端点唯一契约（人类镜像）

- **机器唯一源**：`config/endpoints.json`
- **本文件角色**：人类可读镜像；代码只读 JSON，不解析本表。
- **计数恒等式**：`28 = 4 core + 7 AH + 7 OU + 7 EU + 1 Polymarket + 2 panorama`
- **高防 CDN 铁律**：全部 28 端点已迁移至移动端云高防 CDN 集群（`txt.titan007.com` 与 `m.titan007.com`），彻底废弃被封禁的 PC 端 IIS 老旧节点。
- **统一编码铁律**：全部 28 端点原生统一为 UTF-8 编码，消除 GB18030 字符替换损坏风险。
- **纯结构化 JSON 升级**：亚盘与大小球全景总表升级为移动端原生 JSON 接口（`HandicapDataInterface.ashx`），单次请求聚合全网做市商初即盘与走地多盘口；`odds.html` 接入 `Lineup` 阵容微观数据，`analy.json` 接入 `shijian` 即时事件与 xG 技统。

| # | Key | 组 | Tier | URL | 编码 | 抽取类型 | 必需 | 空态 | 门禁 |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| 1 | `1x2d.js` | core | 1 | `https://txt.titan007.com/1x2/{match_id}.js` | UTF-8 | text | 是 | 禁止空 | 21 个 euro cid 齐全，包含150+家做市商 |
| 2 | `analysis.html` | core | 1 | `https://m.titan007.com/analy/Analysis/{match_id}.htm` | UTF-8 | html | 是 | 禁止空 | 积分榜、近期战绩、让球大小盘路 |
| 3 | `odds.html` | core | 1 | `https://m.titan007.com/analy/Lineup/{match_id}.htm` | UTF-8 | html | 是 | 禁止空 | 首发阵型、球员身价估值、医学伤病原因 |
| 4 | `analy.json` | core | 1 | `https://m.titan007.com/analy/shijian/{match_id}.htm` | UTF-8 | html | 是 | `not_offered` 合法 | 比赛关键事件、即时攻防、xG 预期进球 |
| 5 | `ah_1.html` | AH | 2 | `https://m.titan007.com/AsianDetail/1/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 澳彩单家完整变盘时序流水 |
| 6 | `ah_3.html` | AH | 2 | `https://m.titan007.com/AsianDetail/3/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 皇冠单家完整变盘时序流水 |
| 7 | `ah_8.html` | AH | 2 | `https://m.titan007.com/AsianDetail/8/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | Bet365单家完整变盘时序流水 |
| 8 | `ah_12.html` | AH | 2 | `https://m.titan007.com/AsianDetail/12/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 易胜博单家完整变盘时序流水 |
| 9 | `ah_47.html` | AH | 2 | `https://m.titan007.com/AsianDetail/47/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 平博单家完整变盘时序流水 |
| 10 | `ah_42.html` | AH | 2 | `https://m.titan007.com/AsianDetail/42/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 188Bet 亚洲自营哨兵流水 |
| 11 | `ah_48.html` | AH | 2 | `https://m.titan007.com/AsianDetail/48/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 香港马会单家完整变盘时序流水 |
| 12 | `ou_1.html` | OU | 2 | `https://m.titan007.com/OuDetail/1/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 澳彩大小球变盘流水 |
| 13 | `ou_3.html` | OU | 2 | `https://m.titan007.com/OuDetail/3/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 皇冠大小球变盘流水 |
| 14 | `ou_8.html` | OU | 2 | `https://m.titan007.com/OuDetail/8/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | Bet365大小球变盘流水 |
| 15 | `ou_12.html` | OU | 2 | `https://m.titan007.com/OuDetail/12/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 易胜博大小球变盘流水 |
| 16 | `ou_47.html` | OU | 2 | `https://m.titan007.com/OuDetail/47/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 平博大小球变盘流水 |
| 17 | `ou_42.html` | OU | 2 | `https://m.titan007.com/OuDetail/42/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 188Bet 大小球变盘流水 |
| 18 | `ou_48.html` | OU | 2 | `https://m.titan007.com/OuDetail/48/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 香港马会大小球变盘流水 |
| 19 | `eu_1.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/80/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 澳彩欧指变盘流水（euro_cid=80） |
| 20 | `eu_3.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/545/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 皇冠欧指变盘流水（euro_cid=545） |
| 21 | `eu_8.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/281/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | Bet365欧指变盘流水（euro_cid=281） |
| 22 | `eu_12.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/90/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 易胜博欧指变盘流水（euro_cid=90） |
| 23 | `eu_47.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/177/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 平博欧指变盘流水（euro_cid=177） |
| 24 | `eu_42.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/42/{match_id}.htm` | UTF-8 | markdown | 是 | `not_offered` 合法 | 188Bet 无 euro_cid；`skip_request=true`，不请求 18Bet |
| 25 | `eu_48.html` | EU | 2 | `https://m.titan007.com/CompensateDetail/432/{match_id}.htm` | UTF-8 | markdown | 是 | 有未开盘证据才可空 | 香港马会欧指变盘流水（euro_cid=432） |
| 26 | `polymarket.json` | Polymarket | 1 | `https://gamma-api.polymarket.com/events?slug={polymarket_slug}` | UTF-8 | text | 是 | `[]` 合法 | JSON 可解析，链上胜平负概率 |
| 27 | `asian_odds.html` | panorama | 2 | `https://m.titan007.com/HandicapDataInterface.ashx?scheid={match_id}&type=1&oddskind=0` | UTF-8 | text | 是 | 禁止空 | 全网主流做市商亚盘初即盘纯 JSON |
| 28 | `over_under.html` | panorama | 2 | `https://m.titan007.com/HandicapDataInterface.ashx?scheid={match_id}&type=1&oddskind=1` | UTF-8 | text | 是 | 禁止空 | 全网主流做市商大小球初即盘纯 JSON |

## 空态与错误码

- `not_offered`：合法未开盘。必须带证据：Polymarket 返回 `[]`、`analy.json` 无事件、188Bet 的 `eu_42` 为空、HKJC 次级联赛亚盘页面明确写未开盘。
- `forbidden`：不允许空；空即 `empty_required_endpoint`。
- `duplicate_cid`：21 个 euro cid 有重复。
- `duplicate_odds_triplet`：同一机构同一时间出现重复赔率三元组。
- `bookmaker_mismatch`：表头机构与 key 不符。
- `entity_mismatch`：`1x2d.js` 的 `ScheduleID` 或队名与目标不符。
- `schedule_id_mismatch`：`HandicapDataInterface.ashx` 返回的 `scheduleId` 与工单不符。
- `waf_blocked`：页面含 `Just a moment...`、`Cloudflare`、`Access Denied` 等盾标记。
- `replacement_char`：解码后含 U+FFFD。
