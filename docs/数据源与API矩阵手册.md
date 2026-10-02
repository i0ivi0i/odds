# 数据源与全网 API 矩阵手册 (Data Sources & API Matrix Manual)

> 本手册记录「倍率分析推演」系统中所有已接入、热备中以及储备的多元足球数据源与免费开放 API，彻底杜绝单点依赖。

---

## 一、系统多源数据架构总览

系统采用统一接口契约设计（输出标准 `agent.analysis` / `agent.schedule`），底层以“插座式适配器”链接多方数据，互为热备：

| 数据类别 | 主用数据源（Primary） | 热备数据源（Secondary） | 官方/开放 API 直连（Direct API） |
| :--- | :--- | :--- | :--- |
| **盘口与赔率时序** | 球探网 (titan007) - 14 家机构逐笔时序 | 澳客网 (Okooo) + 体彩官方网关 | The Odds API (`the-odds-api.com`) |
| **微观伤停与阵容** | 英超官方 FPL API | Big Balls Sports Data API | Football-Data.org |
| **实战交易与对冲** | Polymarket Gamma 官方接口 | — | CLOB 原生订单簿 |
| **体彩排期与结算** | 球探 `odds_jc.txt` 镜像 | 澳客移动版 `m.okooo.com/jczq` | 中国体彩官方网关 `webapi.sporttery.cn` |

---

## 二、已实装运行的数据源清单

### 1. 赔率时序与全盘指数（主源：titan007）
- **特点**：全网唯一免费、免密钥、免登录提供 14 大主流机构（威廉、立博、伟德、平博、Bwin、SNAI、必发等）分钟级升降盘历史的信道。
- **获取内容**：亚盘盘水变化表、大小球盘水变化表、欧赔逐笔时序、皇冠全比分波胆、进球区间倍率。
- **调度模块**：`scripts/sporttery-sniper/src/titan007.js`。

### 2. 双轨自动熔断热备（备源：澳客网 + 体彩官方网关）
- **触发机制**：由 `scripts/sporttery-sniper/src/failover-manager.js` 统一监管。主源超时或异常时自动重试 1 次，若依然打不开，**1 秒内平滑切换至备用源**。
- **数据保障**：通过 `scripts/sporttery-sniper/src/okooo-adapter.js` 无缝接管基础赛程、澳彩/皇冠/365/易胜博亚让盘口与欧指骨架。
- **透明声明**：切换后自动在输出中附带透明通知：`⚠️【数据源提示：主源响应异常，已由备用热备数据源(澳客/官方镜像)无缝接管保障推演】`。
- **决策架构**：详见 `docs/adr/0001-multi-source-odds-failover-adapter.md`。

### 3. 微观阵容与伤停双引擎
- **英超官方 FPL API**：
  - 接口：`https://fantasy.premierleague.com/api/bootstrap-static/`；
  - 属性：**100% 英超联盟官方权威数据**，永久免费、无频率限制，直接输出全员伤停部位、伤情状态及出战概率（如 0%、25%、75%）。
- **Big Balls Sports Data API**：
  - 接口：`https://api.bigballsdata.com/v1/injuries`；
  - 覆盖：西甲、意甲、德甲、法甲、美职联；
  - 凭证：自动读取 `~/.gemini/config/bigballs_tokens.json`；
  - 调度模块：`scripts/sporttery-sniper/src/injury-service.js`。

### 4. 预测市场与美分撮合（Polymarket Gamma API）
- **接口**：`https://gamma-api.polymarket.com/events?slug={slug}`；
- **用途**：拉取真实撮合池美分买入价（如 28.5¢ = 3.5倍），在 6 列表中提供真实一键下注直达链接，专用于冷平反向狙击。

---

## 三、海外免费储备 API 矩阵

### 1. Football-Data.org
- **定位**：欧洲五大联赛及欧战官方赛程、积分榜、H2H 历史战绩权威备用库。
- **免费配额**：每分钟 10 次请求（永久免费，无需付费）。
- **本地凭证**：已预配于 `~/.gemini/config/football_data_tokens.json`（含主备两条 Token）。

### 2. The Odds API (`the-odds-api.com`)
- **定位**：国际顶级做市商（Pinnacle 平博、Bet365、Betfair 必发）无偏赔率与历史变动查询。
- **免费配额**：Starter 方案每月 500 次免费请求（无需绑卡）。
- **决策架构**：详见 `docs/adr/0012-professional-odds-api-time-series-integration.md`。

### 3. Sofascore 手机免密钥数据流
- **定位**：免注册、免密钥、零成本获取实时比赛的进球期望值（xG）、首发站位与全场攻防技统数据。

---

## 四、维护与安全守则

1. **凭证隔离**：所有商业/官方 API 密钥一律存放于本地 `~/.gemini/config/`，严禁硬编码进公共代码仓库。
2. **零成本原则**：所有选型以**永久免费配额**为硬性前提，严禁引入强制付费或月租绑卡服务。
3. **一致性检查**：运行 `python scripts/check_consistency.py --print-ok` 确保图谱拓扑 100% 连通与数据契约一致。
