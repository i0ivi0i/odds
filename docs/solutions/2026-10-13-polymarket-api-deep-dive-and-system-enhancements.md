# Polymarket 官方 API 深度研读与足球系统架构增补方案

> **文档性质**：基于 Polymarket 官方开发文档 (`https://docs.polymarket.com/market-data/discover-markets#api`) 深度研读总结，针对本足球推演系统的架构级演进建议。

---

## 一、官方 API 核心架构发现

### 1. 核心端点分层架构（Gamma API）

| 业务场景 | 官方端点 | 优势与特性 |
| :--- | :--- | :--- |
| **精准事件直探** | `GET /events/slug/{slug}` | 确定性 O(1) 访问，零模糊排序干扰，直接返回主客队与市场列表 |
| **单场衍生盘全景** | `GET /events/keyset?game_id={game_id}` | 单次调用聚合比赛全套衍生标的（主盘、半场、波胆、大小球） |
| **联赛与球队元数据** | `GET /sports` 与 `GET /teams?league={league}` | 官方 481 项赛事分类与球队官方 3 字缩写字典 |
| **盘口类型过滤** | `GET /sports/market-types` | 支持 `moneyline`（胜平负）、`spreads`（让球）、`totals`（大小球） |

---

## 二、四大架构级增补落地方案

### 1. 采集链路：从“模糊搜索”升级为“Slug直探 + GameId裂变”
- **现状缺陷**：依赖 `public-search?q={Team}`，易受欧战交易量挤占导致国内联赛标的丢失；
- **增补设计**：
  1. 首选直探：按 `{league}-{home3}-{away3}-{YYYY-MM-DD}` 直接请求 `/events/slug/{slug}`；
  2. 提取 `gameId`（如马尔默卡尔马的 `5107619`）；
  3. 请求 `/events/keyset?game_id={gameId}`，一键拉取全部关联市场。

### 2. 盘口维度穿透：去中心化流动性全面赋能 4 大推演维度
Polymarket 为同一场足球赛提供 6 大标准伴生事件（Companion Events），与本系统深度契合：
- **胜负平 1X2**：`{slug}` ➔ 对齐百家欧指与体彩 HAD；
- **半场胜负平**：`{slug}-halftime-result` ➔ 对齐半全场双盘博弈与 Winkelmann 假摔；
- **波胆比分**：`{slug}-exact-score` ➔ 对齐 Crown 皇冠全指数波胆矩阵；
- **大小球进球数**：`{slug}-more-markets` ➔ 对齐 7 大法定做市商 OU 盘口。

### 3. 主客队权威校验：利用 `teams[].ordering` 消除对调与倒挂
- 官方响应顶层提供 `teams` 数组，每个球队对象明确标注：
  ```json
  {"name": "Malmo FF", "abbreviation": "mal", "ordering": "home"},
  {"name": "Kalmar FF", "abbreviation": "kal", "ordering": "away"}
  ```
- 门禁 `verifier.py` 可将此字段作为主客对齐的权威仲裁标准，杜绝主客对调错误。

### 4. 字典权威化：利用 `/teams` 建立本地官方缩写缓存库
- 以前团队缩写依赖经验推断，容易出现 `mal` vs `mff`、`new` vs `ncl` 的分歧；
- 通过 `GET /teams?league={league}` 可离线缓存官方全量缩写字典，拼装命中率达 100%。
