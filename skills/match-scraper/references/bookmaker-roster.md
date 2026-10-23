# 法定 23 家做市商唯一名册（人类镜像）

- **机器唯一源**：`config/datasources.json` 的 `primary_odds.tracked_bookmakers`
- **本体依据**：`.evoontology/versions/ontology_v2/constraints.json` 的 `constraint_23_bookmakers_completeness`
- **本文件角色**：人类可读镜像；代码只读 JSON，不解析本表。
- **恒等式**：`23 = 21 个 euro_cid + 188Bet(change_cid=42) + Polymarket`
- **流水表恒等式**：`21 = 7 家核心机构 × (ah + ou + eu)`

| # | 官方名 | 别名 | euro_cid | change_cid | 必需端点 | 未开盘规则 |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| 1 | 澳彩 | Macauslot, 澳门 | 80 | 1 | `1x2d.js`, `ah_1`, `ou_1`, `eu_1` | AH/OU/EU 有未开盘证据才可空 |
| 2 | 皇冠 | Crown | 545 | 3 | `1x2d.js`, `ah_3`, `ou_3`, `eu_3` | AH/OU/EU 有未开盘证据才可空 |
| 3 | Bet365 | Bet 365, 365bet | 281 | 8 | `1x2d.js`, `ah_8`, `ou_8`, `eu_8` | AH/OU/EU 有未开盘证据才可空 |
| 4 | 易胜博 | Easybets, Easybet | 90 | 12 | `1x2d.js`, `ah_12`, `ou_12`, `eu_12` | AH/OU/EU 有未开盘证据才可空 |
| 5 | 平博 | Pinnacle | 177 | 47 | `1x2d.js`, `ah_47`, `ou_47`, `eu_47` | AH/OU/EU 有未开盘证据才可空 |
| 6 | 香港马会 | 马会, HKJC, HK Jockey Club | 432 | 48 | `1x2d.js`, `ah_48`, `ou_48`, `eu_48` | 次级联赛 AH/OU 可合法空；EU 需证据 |
| 7 | 188Bet | 188, 188bet | — | 42 | `ah_42`, `ou_42`, `eu_42` | `eu_42` 跳过并 `not_offered`；AH/OU 缺数据即 `not_offered`，绝不能用 18Bet 冒充 |
| 8 | 威廉希尔 | William Hill | 115 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 9 | 立博 | Ladbrokes | 82 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 10 | 伟德 | Vcbet, BetVictor | 81 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 11 | Interwetten | — | 104 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 12 | Bwin | — | 255 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 13 | SNAI | — | 110 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 14 | 必发 | Betfair | 2 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 15 | 利记 | Sbobet, SBOBET | 474 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 16 | 沙巴 | IBCBET, IBC | 649 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 17 | Marathon | Marathonbet, 马拉松 | 800 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 18 | Betway | 必威 | 482 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 19 | Unibet | 优胜客 | 386 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 20 | Paddy Power | PaddyPower | 826 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 21 | 10Bet | 10BET | 16 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered` |
| 22 | 中国体彩 | Lottery Official, 体彩, 竞彩 | 1129 | — | `1x2d.js` | 不在 `1x2d.js` 即 `not_offered`；HAD/HHAD 需独立核实 |
| 23 | Polymarket | — | — | — | `polymarket.json` | `[]` 即 `not_offered` |

## 非名册机构（不得计入 23）

| cid | 名称 | 处理 |
| :---: | :--- | :--- |
| 71 | Eurobet | 忽略，不计入 23 |
| 370 | Oddset | 忽略，不计入 23 |
| 18 | 12bet | 忽略，不计入 23 |
| 517 | Mansion88 / 明陞 | 忽略，不计入 23 |
| 976 | 18Bet | 忽略，不计入 23；绝不能填给 188Bet |

## 关键断言

- `euro_cid` 恰好 21 个非空且唯一。
- `change_cid` 恰好 7 个非空且唯一：1、3、8、12、47、42、48。
- 188Bet 的 `euro_cid` 为空、`change_cid=42`，只走 `changeDetail`。
- Polymarket 两个 cid 都为空，只走 `polymarket.json`。
- 同一 `euro_cid`、同一 `change_cid`、同一官方名不得重复。
