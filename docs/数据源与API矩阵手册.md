# 数据源与全网 API 矩阵手册 (Data Sources & API Matrix Manual)

> 本手册记录「倍率分析推演」系统已接入的数据源。盘口主源是球探网；其他来源齐全且对得上才能代，缺、错、少就不能代。

---

## 一、系统多源数据架构总览

系统采用统一接口契约（输出标准 `agent.analysis` / `agent.schedule`）。盘口主源是球探；伤停辅源、交易接口、体彩三项静态赔。验收门看亚盘/欧指流水与主客场近6，不把伤停空表当成整场缺数据：

| 数据类别 | 主用数据源（Primary） | 补抓路径（齐全且对得上才能代） | 官方/开放 API 直连（Direct API） |
| :--- | :--- | :--- | :--- |
| **盘口与赔率时序** | 球探网 (titan007) - 14 家机构逐笔时序 | 线上一律 `/browseros-neo` 直开球探页；其他来源齐全且对得上才能代 | The Odds API（仅尖锐验真，缺亚洲机构与波胆时不能单用） |
| **微观伤停与阵容** | 球探分析页「阵容情况」 | 英超官方 FPL API / Big Balls（仅部分俱乐部联赛） | Football-Data.org |
| **实战交易与对冲** | Polymarket Gamma 官方接口 | — | CLOB 原生订单簿 |
| **体彩场次编号与休市** | 球探 `odds_jc.txt`（镜像竞彩编号） | — | 中国体彩官方网关 `webapi.sporttery.cn`（核对场次代号、开售窗口、节假日休市；三项静态赔不是完整盘口资料） |

---

## 二、已实装运行的数据源清单

### 1. 赔率时序与全盘指数（主源：titan007）
- **特点**：全网唯一免费、免密钥、免登录提供 14 大主流机构（威廉、立博、伟德、平博、Bwin、SNAI、必发等）分钟级升降盘历史的信道。
- **获取内容**：亚盘盘水变化表、大小球盘水变化表、欧赔逐笔时序、皇冠全比分波胆、进球区间倍率。
- **抓取通道**：爱马仕 `/browseros-neo` 直开球探页。`scripts/sporttery-sniper/src/titan007.js` 仅离线解析与单测。

### 2. 主源失败怎么办
- **线上不先跑脚本**：禁止 `npm run schedule` / `analyze` / `review`。
- **打不开页或缺资料**：重试 `/browseros-neo` 同一家球探页并落盘。仍缺验收门：置顶提醒并贴页上原句；当面聊天先停，等主人回再继续；定时任务置顶后继续十步，不准跳过。
- **其他来源**：亚盘/欧指流水、机构盘口、主客场/近6数字齐全、没错、对得上 → 可以代。错了、空了、少了一截 → 不能代。伤停格「暂无数据」不是缺数据，贴原句后继续十步。
- **体彩官方网关**：核对竞彩场次编号、当日是否开售、节假日休市。三项静态赔不是完整盘口资料。接口：`https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry?channel=c`（须带浏览器头与 `Referer: https://www.lottery.gov.cn/`）。开售为 0 场即休市/未开售。

### 3. 微观阵容与伤停双引擎
- **英超官方 FPL API**：
  - 接口：`https://fantasy.premierleague.com/api/bootstrap-static/`；
  - 属性：**100% 英超联盟官方权威数据**，永久免费、无频率限制，直接输出全员伤停部位、伤情状态及出战概率（如 0%、25%、75%）。
- **Big Balls Sports Data API**：
  - 接口：`https://api.bigballsdata.com/v1/injuries`；
  - 覆盖：西甲、意甲、德甲、法甲、美职联；
  - 凭证：优先自动读取项目通用配置 `config/api_keys.json`（见 `config/datasources.json` 统一索引）；
  - 调度模块：`scripts/sporttery-sniper/src/injury-service.js`。

### 4. 预测市场与美分撮合（Polymarket Gamma API）
- **接口**：`https://gamma-api.polymarket.com/events?slug={slug}`；
- **用途**：拉取真实撮合池美分买入价（如 28.5¢ = 3.5倍），在 6 列表中提供真实一键下注直达链接，专用于冷平反向狙击。

---

## 三、海外免费储备 API 矩阵

### 1. Football-Data.org
- **定位**：欧洲五大联赛及欧战官方赛程、积分榜、H2H 历史战绩权威备用库。
- **免费配额**：每分钟 10 次请求（永久免费，无需付费）。
- **本地凭证**：已预配于项目通用配置 `config/api_keys.json`（含主备两条 Token，模板见 `config/api_keys.example.json`）。

### 2. The Odds API (`the-odds-api.com`)
- **定位**：欧美顶级做市商（Pinnacle 平博、Bet365、Betfair 必发）无偏赔率与尖锐盘口验真辅轨。
- **免费配额**：Starter 方案每月 500 次免费请求（已配置活跃 Key 至 `config/api_keys.json`）。
- **决策架构**：详见 `docs/adr/0012-professional-odds-api-time-series-integration.md`。

### 3. BrowserOS neo 真实浏览器直连通道
- **定位**：球探网全维度真实数据采集正式入口（不是脚本失败后的备胎），提取 14 大机构逐笔时序、亚盘大小球及 Crown 波胆全指数并保存为本地数据快照（`data/`）。

### 4. Sofascore 手机免密钥数据流
- **定位**：免注册、免密钥、零成本获取实时比赛的进球期望值（xG）、首发站位与全场攻防技统数据。

---

## 四、维护与安全守则

1. **凭证隔离与通用性**：所有商业/官方 API 密钥统一存放于项目标准配置 `config/api_keys.json`，并由 `.gitignore` 严格阻断，严禁泄露进公共代码仓库。
2. **零成本原则**：所有选型以**永久免费配额**为硬性前提，严禁引入强制付费或月租绑卡服务。
3. **一致性检查**：运行 `python scripts/check_consistency.py --print-ok` 确保图谱拓扑 100% 连通与数据契约一致。
