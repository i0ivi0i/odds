## TOOLS.md - 工具使用指南

Skills 定义了工具的工作方式。此文件记录当前仓库中可用的数据抓取工具与命令。常用工具或者插件之类的"使用方法"得到更新或者技巧之后，也要在本文件进行记录更新。

---

## 核心系统：双轨敏捷数据采集（Skill scrapling-official / browseros-neo 与对应 MCP）

数据采集采用**大模型自主调度的双轨敏捷架构**：系统正式装载并明确绑定两大核心 Skill 与其对应 MCP 服务。AI 大模型根据目标页面特性与即时网络状况，拥有完全自主、聪明智慧的决断权，灵活调度两军协同。

### 1. 技能与 MCP 双轨绑定及分工
- **Skill `/scrapling-official` ↔ MCP `scrapling`（极速协议流通道）**：
  - 原生集成 TLS 浏览器指纹伪装与抗封锁能力；
  - 毫秒级直取 163 家百家欧指数据流（`1x2d.titan007.com/{id}.js`）与四大机构分钟级变盘流水（`changeDetail`）；
  - 作为赛前高频盘赔时序数据提取的**首选高速通道**。
- **Skill `/browseros-neo` ↔ MCP `browseros_neo`（真实渲染通道）**：
  - 真实 Chromium 渲染环境，专攻球探单场分析页的「阵容情况」微观伤停原句、首发球员评分、积分榜战术技统与竞足全开大盘；
  - 当 Scrapling 遭遇未知动态加密或复杂交互验证时，作为**强力真实环境兜底**。
- **自主智能调度与物理门禁兜底**：
  - AI 大模型拥有完全自主的选择、切换与组合调度权；
  - 无论选用哪一个工具，最终组装的快照文件 `data/YYYY-MM-DD/{matchId}.json` 必须 100% 通过 `python 校验/src/adapter/cli.py --match ...` 物理安检门禁。

---

### 2. 数据精准抓取与严禁错位（字段纯净与位置归位红线）

**最高数据铁律**：**数据一定要抓取正确，不要乱抓乱获取，绝对禁止把不对的数据放进不应该在的位置！**
数据采集必须实事求是、精准归位，严禁为了应付门禁而猜测脑补、拼凑假数据或把无关字段错位塞入快照。各维度数据必须严格存放于专属语义字段：

| 数据维度 | 抓取内容与标准 | 对应快照标准字段 | 严禁错位红线 |
| :--- | :--- | :--- | :--- |
| **分钟级变盘流水** | 澳彩/Crown/365/易胜博带时间戳的变盘时序 | `trendComparison` | 严禁缺少时间戳；严禁将未变盘的静态表头塞入流水 |
| **欧洲指数百家** | 163 家主流机构初即盘、返还率与凯利指数 | `european1x2Text` / `europeOddsSummary` | 严禁将亚盘让球水位误填入欧指；严禁丢失返还率 |
| **亚洲让球盘** | 主流机构初即盘盘口、上下盘水位及变盘记录 | `asianOddsText` | 严禁与大小球盘口混淆；严禁盘口与水位颠倒 |
| **大小球进球数** | 主流机构初即盘盘口、大球小球水位 | `overUnderOddsText` | 严禁将让球盘盘口填入大小球 |
| **微观首发与伤停** | 分析页「阵容情况」名单，若无则保留【暂无数据】原句 | `lineupData` | 严禁将上一场阵容当本场；无数据严禁脑补无人缺阵 |
| **真实场上压制力** | 控球率、射正比、角球、进球时段、未来赛程 | `tactics` | 严禁把表面积分排名直接当压制力指标 |
| **相同初盘与盘路** | 相同初盘历史胜率画像、近期盘路走势形态 | `profiling` | 严禁篡改初盘基准；严禁非结构化文本乱堆 |
| **Crown皇冠波胆** | `#analy_sbAllOdds` 中 0:0~4:4 比分矩阵赔率 | 波胆比分专属映射 | 严禁将总进球数赔率误当单场具体比分波胆 |

凡因字段错位、数据污染或时间戳缺失导致安检失败的，物理门禁（`verifier.py`）将立即硬拦截阻断，AI 必须重新精准获取并纠偏归位。

---

### 2. Scrapling 实战使用指南与避坑参数

#### 运行环境与 CLI / MCP
- Python 3.13 全局环境，已安装 `scrapling[all]`。
- 已注册 Hermes 官方 MCP 服务 `scrapling`（包含 `make_request`, `fetch`, `stealthy_fetch` 等工具）。
- CLI 命令：
  ```bash
  scrapling extract get "https://1x2d.titan007.com/3085211.js" -o data/odds.js
  ```

#### Python 极速提取核心范式
```python
from scrapling.fetchers import Fetcher
import re

# 1. 抓取百家欧指数据流（163家机构初即盘与底层 odds_id，0.3秒直取）
res_1x2 = Fetcher.get(f"https://1x2d.titan007.com/{match_id}.js", impersonate="chrome")
text_1x2 = res_1x2.body.decode("utf-8", errors="ignore")

# 2. 抓取四大机构亚盘/大小球变盘流水（注意：必须使用 gb18030 解码，防中文乱码）
url_asia = f"https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID={cid}&l=0"
res_asia = Fetcher.get(url_asia, impersonate="chrome")
text_asia = res_asia.body.decode("gb18030", errors="ignore")

# 3. 抓取欧指分钟级流水（注意：必须携带从 1x2d 中解析到的 odds_id）
url_history = f"https://1x2.titan007.com/OddsHistory.aspx?id={odds_id}&sid={match_id}&cid={cid}&l=0"
res_history = Fetcher.get(url_history, impersonate="chrome")
text_history = res_history.body.decode("utf-8", errors="ignore")
```

#### 实战踩坑必记
1. **编码陷阱**：球探二级页面（`changeDetail/*.aspx`）为旧版编码，默认 UTF-8 会导致队名和盘口乱码，必须使用 `gb18030` 解码；
2. **欧指百家非 SSR**：`oddslist/{id}.htm` 为空骨架，真实 163 家公司数据存储在 `https://1x2d.titan007.com/{id}.js` 中，直接抓 JS 文件效率最高且最全；
3. **欧指历史流水参数**：`OddsHistory.aspx` 若只传 `sid` 和 `cid` 会返回空表，必须传 `id={odds_id}` 参数方可提取分钟级变盘流水。

---

### 3. BrowserOS neo 真实渲染使用指南

- 爱马仕专用浏览器内核，用于真实页面交互、全貌 DOM 抓取与微观阵容审阅。
- **微观伤停核验规范**：
  - 访问分析页（`https://zq.titan007.com/analysis/{matchId}cn.htm`），定位「阵容情况」表格；
  - 若页面明确印出缺阵名单，逐人记录姓名、位置与缺阵原因；
  - 若印出「暂无数据」，如实标注【暂无数据 / 伤停未核实】，保留页上原句，**允许继续十步但严禁脑补全主力或无人受伤**。
- **Crown 皇冠波胆与半全场**：
  - 从分析页 `#analy_sbAllOdds` 提取 0:0~4:4 比分波胆赔率矩阵及半全场赔率，作为泊松分布物理偏差对账的真实市场锚点。

---

### 4. 预赛快照与落盘标准

- 统一落盘路径：`data/YYYY-MM-DD/{matchId}.json`。
- 输出结构严格遵循 `agent.analysis` 契约规范。
- 无论通过 Scrapling 提取还是 BrowserOS neo 渲染，均必须包含：
  1. `european1x2Text`：主流机构百家初即盘、返还率与凯利指数；
  2. `asianOddsText` / `overUnderOddsText`：主流四大机构（澳彩、Crown、Bet365、易胜博）分钟级变盘流水；
  3. `trendComparison`：带时间戳的变盘时序流水（供安检门禁核验）；
  4. `lineupData`：首发球员评分、伤停原句；
  5. `tactics` 与 `profiling`：真实场上压制力技统、进球时段、未来赛程、相同初盘画像与盘路走势。

### 数据安全规则

- **赔率必须实时抓取**：每次分析都用 `/browseros-neo` 重开球探页，不复用 memory 中旧赔率。
- **只用赛前赔率**：过滤状态为“滚”的记录，并按开赛时间截断赛前变化历史。
- **缺失不臆造**：如果某家公司或某类市场缺失，报告中必须标注数据缺口，并降低对应维度权重。
- **平博用途**：平博可作为主流公司交叉验证参考，不单独用于决策依据。

### 验证脚本

```bash
cd scripts/sporttery-sniper
npm test
```

测试不需要真实网络请求，主要验证解析器、JSON 输出和本地样例。

### 纯数学去水算法工具（算法/src/adapter/cli.py）

标准东京大学 Shota Goto (2026) OO-EPC 官方原版去水计算器。
用于欧指分析第 4 步、四项论文质问之二及六列表第 4 列的点概率计算。杜绝大模型心算与概率失真。

```bash
# 标准计算（文本输出）
python 算法/src/adapter/cli.py 2.10 3.40 3.55

# 结构化计算（JSON输出，供程序与 Worker 消费）
python 算法/src/adapter/cli.py 2.10 3.40 3.55 --json
```

### 数据完整性质量守门人（校验/src/adapter/cli.py）

标准 10/10 纯 DDD 洋葱六边形架构质量守门人模块。
用于深度分析步骤 1.5、Worker 派发安检与全库一致性防回退巡检。对 6 大黄金维度实现物理硬熔断，彻底阻断大模型在数据残缺时偷懒说谎或脑补盘赔。

```bash
# 单场比赛快照 6 维度物理安检（核心数据缺失返回 exit 1 物理熔断）
python 校验/src/adapter/cli.py --match data/2026-10-07/2981506.json

# 结构化输出快照安检法定收据（JSON格式）
python 校验/src/adapter/cli.py --match data/2026-10-07/2981506.json --json

# 全系统一致性、图谱连通性与算法单测联合健康巡检
python 校验/src/adapter/cli.py --system
```

## Polymarket 下单链接

6 列表最后一格的查找步骤见 `docs/Polymarket链接查找教程.md`。读盘不改图上数字；找链接用体彩现价对场次，再用接口核实体，禁止瞎拼地址。

## 数据源与主源失败处理

盘口主源是球探网。资料齐不齐、对不对，不看网站姓什么（详见 ADR 0001）。**线上抓取采用 Scrapling 极速通道与 BrowserOS neo 协同双轨，严禁先跑旧版 npm 脚本。**

### 1. 赔率与赛程
- **主数据源（Primary）**：titan007 球探页。当场按赛事分组提取分析依据公司的可见流水与 Crown 已有项目。14 家名单是宽覆盖描述，不是每场每市场全覆盖保证。
- **抓取通道**：Scrapling（主攻欧亚变盘流水与 1x2d 百家数据流） + BrowserOS neo（主攻单场分析页阵容与微观交互），大模型自主抉择调度。若出现网络波动或残页，大模型自主调用另一通道补齐；若仍缺，置顶如实提示并贴出原因。
- **公司矩阵（按赛事分组，页面或接口编号分别核对，不猜编号）**：
  - 欧洲及其他赛事欧指：威廉、365、立博、伟德、平博。
  - 德国欧指：威廉、365、Interwetten。
  - 亚洲欧指：澳彩、皇冠、365、易胜博、马会。
  - 亚盘、大小球：澳彩、皇冠、365、易胜博；亚洲加马会。
  - 平博参与欧指，不参与现行亚盘、大小球分析。交易所报价与固定赔率分开，不混入同一去水基准。
  - 变盘页 `companyID` 以当场页面链接为准。`config/datasources.json` 的 `tracked_bookmakers.id` 是另一套接口编号，不得直接套到变盘页。
- **缺失口径**：未检查、读取失败或未读完整、来源已查但未填、尚未发生、计算未执行、内部不可见。**凡已发生而读取失败、或读取不完整的，必须在报告开头向主人明确提示**，原文不存在时写工具错误或读取状态，严禁静默掩盖。
- **其他来源**：亚盘/欧指流水、机构盘口、主客场/近6数字齐全、没错、对得上 → 可以代。错了、空了、少了一截 → 不能代。伤停格「暂无数据」不是缺数据，如实标注未核实，不挡十步推演。
- **体彩官方网关**：核对场次编号、开售窗口、节假日休市（见 `config/datasources.json` 的 `sporttery_match_codes`）。三项静态赔本身不是完整盘口资料。找 6 列表链接时用它对照现价对场次。

### 2. 阵容伤停独立双引擎 (Lineup & Injury Engine)
- **英超官方 FPL 数据库**：通过 `injury-service.js` 直连英超官方数据，零等待获取主力伤情与出战概率。
- **Big Balls Sports Data API**：直连商业体育数据网关，支持西甲、意甲、德甲、法甲、美职联，凭证读取自 `~/.gemini/config/bigballs_tokens.json`。

### 3. 海外免费开放 API 矩阵储备
- **Football-Data.org**：免费提供欧洲主要联赛赛程、积分榜、H2H 交锋与阵容（凭证读取自 `~/.gemini/config/football_data_tokens.json`）。
- **The Odds API (the-odds-api.com)**：免费 Starter 方案支持平博、365、威廉等做市商标准 1X2 与盘口查询（作为 Pinnacle / Betfair 尖锐欧指去水验真辅轨，详见 ADR 0012）。

## 核心安全通道：双轨协同直取与预赛快照落盘规范

调用 Scrapling 极速协议流与爱马仕 `/browseros-neo` 真实渲染，不是让主人自己开网页，也不是另写外置爬虫。

1. **协同采集全维度数据**：
   - **百家欧指 1X2 与流水**：通过 Scrapling 直取 `1x2d.titan007.com/{id}.js`（163家机构）与 `OddsHistory.aspx`（澳彩等核心依据公司变盘流水）；
   - **亚盘让球与大小球流水**：通过 Scrapling 直取澳彩、皇冠、365、易胜博四大公司 `changeDetail` 全量流水（GB18030解码）；
   - **微观首发与伤停情况**：通过 BrowserOS neo 访问分析页抽取「阵容情况」与球员评分；
   - **Crown 皇冠波胆全指数**：分析页 `#analy_sbAllOdds` 中 0:0～4:4 比分波胆赔率矩阵及半全场。
2. **本地快照存盘**：组装保存为 `data/YYYY-MM-DD/{matchId}.json`。
3. **物理安检门禁**：通过 `python 校验/src/adapter/cli.py --match ...` 检验数据完整性。门禁通过即进入 10 步深度推演；若门禁拦截，AI 自主调度补抓，拒绝无依据硬推。
4. **伤停空表处理**：分析页抽出的阵容表若印「暂无数据」，如实标注【暂无数据 / 伤停未核实】，保留页上原句，**继续十步推演，严禁脑补无伤停**。
5. **时点分立**：实际抓取、分析截至、报价、开球、保存与发布时间分开记录，严禁用赛后记录或未来时点倒填赛前。

## Subagent 工具

### 当前Hermes入口：delegate_task

用 `delegate_task(tasks=[{"goal":"任务","context":"所需背景与回传要求"}])` 派发任务；同批最多3个单场worker，不能要求worker再次委派。worker只回传待验收结果，不自行发送消息；主会话作为唯一写入者在整批摘要保存后交付。状态用 `delegate_task(action="list")`，停止用 `delegate_task(action="stop",subagent_id="实际ID")`。定时最终报告仅交调度器投递。

### sessions_spawn — 历史平台接口（非当前Hermes调用）

将耗时任务交给后台 subagent 执行，主会话立即返回，保持可用。

**参数**：

| 参数                | 必填 | 说明                                       |
| ------------------- | ---- | ------------------------------------------ |
| `task`              | 是   | 任务指令（subagent 收到的 prompt）         |
| `label`             | 否   | 标签，方便 `/subagents list` 识别          |
| `model`             | 否   | 指定 subagent 使用的模型（默认继承主会话） |
| `runTimeoutSeconds` | 否   | 超时秒数（默认 3600 = 60 分钟）            |

**返回**：`{ status: "accepted", runId, childSessionKey }` — 非阻塞，立即返回。

**历史使用示例（仅保留接口来源，包含的自行推送与嵌套派发不再执行）**：

```
# 赛程同步（单个 subagent）
sessions_spawn:
  task: "执行赛程同步。读取 skills/match-scraper/SKILL.md。严格按照模板，用 /browseros-neo 打开球探竞足页抓今日全量赛程，禁止先跑 npm run schedule。通过 messaging 推送赛程列表给主人，写入 memory/{今天日期}.md。"
  label: "match-sync"

# 深度分析（编排 subagent 内部 spawn worker）
sessions_spawn:
  task: "深度分析 [英超] 阿森纳 vs 曼城（ID: 2950977）。读取 skills/deep-analysis/SKILL.md。严格按照模板，先用 /browseros-neo 打开该场球探 5 页落盘，禁止先跑 npm run analyze，再完成全部 10 步分析；超 4000 字须分段。通过 messaging 推送分析报告给主人。返回结构化综合评估结果（JSON 格式）。"
  label: "deep-analysis-2950977"
  runTimeoutSeconds: 900
```
