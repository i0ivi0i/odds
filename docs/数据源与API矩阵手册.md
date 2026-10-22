# 数据源与全网 API 矩阵手册 (Data Sources & API Matrix Manual)

> 本手册记录「倍率分析推演」系统已接入的数据源。盘口主源是球探网；其他来源齐全且对得上才能代，缺、错、少就不能代。

---

## 一、系统多源数据架构总览

系统采用统一接口契约（输出标准 `agent.analysis` / `agent.schedule`）。盘口主源是球探；伤停辅源、交易接口、体彩三项静态赔。验收门看亚盘/欧指流水与主客场近6，不把伤停空表当成整场缺数据：

| 数据类别 | 主用数据源（Primary） | 补抓路径（齐全且对得上才能代） | 官方/开放 API 直连（Direct API） |
| :--- | :--- | :--- | :--- |
| **盘口与赔率时序** | 球探网 (titan007) - 23 家机构逐笔时序 | 100% 独家官方 Scrapling MCP 并发直取；严禁调用外部独立浏览器 | The Odds API（仅尖锐验真，缺亚洲机构与波胆时不能单用） |
| **微观伤停与阵容** | 球探分析页「阵容情况」 | 英超官方 FPL API / Big Balls（仅部分俱乐部联赛） | Football-Data.org |
| **实战交易与对冲** | Polymarket Gamma 官方接口 | — | CLOB 原生订单簿 |
| **体彩场次编号与休市** | 球探 `odds_jc.txt`（镜像竞彩编号） | — | 中国体彩官方网关 `webapi.sporttery.cn`（核对场次代号、开售窗口、节假日休市；三项静态赔不是完整盘口资料） |

---

## 二、已实装运行的数据源清单

### 1. 赔率时序与全盘指数（主源：titan007）
- **特点**：球探页可免登录查看多家机构升降盘历史。当场覆盖以页面实际可见公司与行数为准，不是「全网唯一免费、14 家全覆盖、无频率限制」的保证。
- **获取内容**：亚盘盘水变化表、大小球盘水变化表、欧赔逐笔时序、皇冠已有比分/半全场/总进球项目。固定比分范围不冒充全池。
- **抓取通道**：100% 独家归属工位 1（`skills/match-scraper`，内嵌 Scrapling 0.5 官方武器库 ↔ MCP `scrapling`）。严禁调用外部独立浏览器，严禁编写临时 Python 脚本。
- **Scrapling 官方六大战区反污染装配机制**：
  1. **纯数据流（Text Stream）**：`1x2d.js`（百家欧指原始脚本）、`analy.json`、`polymarket.json`，无损直出；
  2. **双总表原生直转（Full Odds Markdown）**：亚盘总表 `AsianOdds_n.aspx` 与大小球总表 `OverUnder_n.aspx` 强制下推 `css_selector="#table_odds"` 与 `extraction_type="markdown"`，将全网主流做市商初盘与即盘 100% 直出无杂质 Markdown；
  3. **叶子选择器原地下推与源头 1:1 镜像流（Leaf Markdown & Source Fidelity）**：21 张流水表强制下推 `css_selector="#table_odds"` 与 `extraction_type="markdown"`，杜绝外层嵌套 table 引发的 130 列表格横向炸裂坍塌；**100% 忠实镜像球探网源网页纯倒序排列（最新临盘在顶端第 1 行、时间顺流递减、最早开盘在底端最后一行），严禁任何中间层代码将底行初盘抠出插在顶端，严禁机械截断丢失变盘记录**；
  4. **人类简报六大组件装配**：`{matchId}.md` 严禁全页 HTML 裸转 Markdown（杜绝会员广告与死骨架），严格从结构化数据提炼六大战区（伤停、战绩、23家欧指大表、主流做市商亚盘/大小初即大表、21张流水单表、波胆实盘），执行 Anti-Ad、Anti-Collapse、Anti-Placeholder、23 CIDs、Anti-Omission Initial Odds、Anti-Timeline-Distortion 六重品控防错门禁。

### 2. 主源失败怎么办
- **线上不先跑脚本**：严禁自写任何临时抓取脚本。
- **打不开页或缺资料**：在官方 Scrapling 内部四级闭环（`session_make_request` ➔ `make_request` ➔ `browser_fetch` ➔ 内置 real-chrome）升阶重试并落盘。仍缺验收门：置顶提醒并贴页上原句；当面聊天先停，等主人回再继续；定时任务置顶后继续十步，不准跳过。
- **其他来源**：亚盘/欧指流水、机构盘口、主客场/近6数字齐全、没错、对得上 → 可以代。错了、空了、少了一截 → 不能代。伤停格「暂无数据」不是缺数据，贴原句后继续十步。
- **体彩官方网关**：核对竞彩场次编号、当日是否开售、节假日休市。三项静态赔不是完整盘口资料。接口：`https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry?channel=c`（须带浏览器头与 `Referer: https://www.lottery.gov.cn/`）。开售为 0 场即休市/未开售。

### 3. 微观阵容与伤停双引擎
- **英超官方 FPL API**：
  - 接口：`https://fantasy.premierleague.com/api/bootstrap-static/`；
  - 属性：英超联盟官方数据。免费可用，但「永久免费、无频率限制」未经本轮实测。只覆盖英超俱乐部，空返回不得写成无伤停。
- **Big Balls Sports Data API**：
  - 接口：`https://api.bigballsdata.com/v1/injuries`；
  - 覆盖：西甲、意甲、德甲、法甲、美职联；
  - 凭证：优先自动读取项目通用配置 `config/api_keys.json`（见 `config/datasources.json` 统一索引）。

### 4. 预测市场与美分撮合（Polymarket）
- **Gamma**：`https://gamma-api.polymarket.com/events?slug={slug}`，只核实体和市场规则，不提供真实买入价。
- **CLOB**：`https://clob.polymarket.com`，核对应 Yes 合约的最佳卖价、可买数量、买卖差与报价时间。无卖单写当前无可买报价。
- **用途**：6 列表交付一键打开的交易页。Gamma 识别实体；订单簿提供报价参考。实际成交价需成交记录。倍数是未扣成本的条件总回收倍数，不称净收益或保证可成交。Polymarket 价格不进入十步推演或去水基准。

---

## 三、海外免费储备 API 矩阵

### 1. Football-Data.org
- **定位**：欧洲五大联赛及欧战官方赛程、积分榜、H2H 历史战绩权威备用库。
- **免费配额**：每分钟 10 次请求（永久免费，无需付费）。
- **本地凭证**：已预配于项目通用配置 `config/api_keys.json`（含主备两条 Token，模板见 `config/api_keys.example.json`）。

### 2. The Odds API (`the-odds-api.com`)
- **定位**：欧美顶级做市商（Pinnacle 平博、Bet365、Betfair 必发）无偏赔率与尖锐盘口验真辅轨。
- **免费配额**：Starter 方案每月 500 次免费请求（已配置活跃 Key 至 `config/api_keys.json`）。

### 3. Sofascore 手机免密钥数据流
- **定位**：免注册、免密钥获取实时比赛的进球期望值（xG）、首发站位与全场攻防技统。xG 与球员贡献不是本系统必需门槛；没有相关资料不能宣称已执行相应模型。

---

## 四、维护与安全守则

1. **凭证隔离与通用性**：所有商业/官方 API 密钥统一存放于项目标准配置 `config/api_keys.json`，并由 `.gitignore` 严格阻断，严禁泄露进公共代码仓库。
2. **零成本原则**：优先使用现有免费配额。未实测的「永久免费、无频率限制」不得写成已验证能力。
3. **算法单测验证**：运行 `py -3.13 -m unittest discover -s 算法/测试` 确保离线纯数学算法契约一致。
