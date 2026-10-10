## TOOLS.md - 工具使用指南

Skills 定义了工具的工作方式。此文件记录当前仓库中可用的数据抓取工具与命令。常用工具或者插件之类的"使用方法"得到更新或者技巧之后，也要在本文件进行记录更新。

---

## 核心系统：双轨敏捷数据采集（Skill scrapling-official / browseros-neo 与对应 MCP）

**绝对刚性红线**：**全流程严禁任何临时 `.py` 脚本、跑批脚本或 `python -c` 采集数据！**
严禁在根目录或任何位置自写散装爬虫脚本。数据采集必须严格使用且只能使用：
1. **`BrowserOS neo`**（真实 Chromium 浏览器环境，MCP 工具）；
2. **`Scrapling MCP`**（官方 MCP 极速协议通道）。
违者视为严重工程违规与作弊。

数据采集采用**大模型自主调度的双轨敏捷架构**：系统正式装载并明确绑定两大核心 Skill 与其对应 MCP 服务。AI 大模型根据目标页面特性与即时网络状况，拥有完全自主、聪明智慧的决断权，灵活调度两军协同。

### 1. 技能与 MCP 主辅架构（Scrapling 100% 全包主力 × BrowserOS 备用辅助）
- **主力全包引擎：Skill `/scrapling-official` ↔ MCP `scrapling`（1~2 秒全量并发直取）**：
  - 原生集成 Chrome 136+ TLS 指纹伪装与抗封锁能力，通过 `mcp__scrapling__bulk_get` 一次性并发秒取单场全部 5 大数据源：
    1. **阵容伤停与基本面技统**：`https://zq.titan007.com/analysis/{id}cn.htm`（含伤停名单、主客得失球、盘路走势、进球时段、未来赛程）；
    2. **Crown 皇冠波胆与半全场**：`https://zq.titan007.com/analysis/odds/{id}.htm`（含 0:0~4:4 比分波胆、总入球、半全场、角球、必发指数）；
    3. **体彩全玩法与半场指数**：`https://zq.titan007.com/default/getAnalyData?sid={id}&t=1`（含体彩 HAD/HHAD/TTG/CRS/HAFU 及半场欧亚大）；
    4. **百家欧指与分钟级流水**：`https://1x2d.titan007.com/{id}.js`（含 23 家法定机构初即盘、返还率、凯利指数及全部变盘历史）；
    5. **7 大做市商亚盘与大小球流水**：`https://vip.titan007.com/changeDetail/handicap.aspx` 与 `overunder.aspx`。
  - **常规流程 100% 由 Scrapling 独立极速完成，严禁无故启动缓慢的浏览器渲染！**
- **备用辅助兜底：Skill `/browseros-neo` ↔ MCP `browseros_neo`（仅限异常降级辅助）**：
  - 由于浏览器渲染速度慢、资源消耗高，**仅作为辅助备用通道**；
  - 仅当 Scrapling 遭遇极端反爬锁死、接口改版或必须执行前端点击交互时，才降级调用 BrowserOS neo 兜底。
- **自主智能调度与物理门禁兜底**：
  - AI 大模型拥有完全自主的选择、切换与组合调度权；
  - 无论选用哪一个工具，最终组装的工作快照文件必须落盘至工整单文件 `data/YYYY-MM-DD/{matchId}.md`（全天赛程索引与元数据明细统一汇总于 `data/YYYY-MM-DD/meta.md`），必须 100% 通过 `python 校验/src/adapter/cli.py --match ...` 物理安检门禁。

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
| **赛事性质与战意博弈** | 联赛争冠保级/杯赛淘汰/友谊赛走过场/死敌德比及庄家借题做市破译 | `tactics` / 战意博弈字段 | 严禁散户式盲信“战意强=必出”，必须反推庄家借散户狂热非对称收割 |
| **相同初盘与盘路** | 相同初盘历史胜率画像、近期盘路走势形态 | `profiling` | 严禁篡改初盘基准；严禁非结构化文本乱堆 |
| **Crown皇冠波胆** | `#analy_sbAllOdds` 中 0:0~4:4 比分矩阵赔率 | 波胆比分专属映射 | 严禁将总进球数赔率误当单场具体比分波胆 |

凡因字段错位、数据污染或时间戳缺失导致安检失败的，物理门禁（`verifier.py`）将立即硬拦截阻断，AI 必须重新精准获取并纠偏归位。

---

### 2. Scrapling 极速提取与防错位规范（官方黑科技全开）

#### 官方三大能力全开配置与防错位防污染铁律
1. **防封与防火墙穿透 (TLS Fingerprint)**：
   - 必须标配 `impersonate="chrome"` + `stealthy_headers=True`；
   - 自动克隆真实 Chrome 136+ 协议特征，绕过 Cloudflare 与 OpenResty 握手拦截。
2. **极速并发矩阵 (Bulk Get 并发加速)**：
   - 抓取多机构、多玩法（亚盘/大小球/欧指）时，**一律使用 `mcp__scrapling__bulk_get(urls=[...])` 一次性并发秒取**；
   - 避免逐条循环请求导致延迟与网络风暴。
3. **精准语义防错位与防污染断言（最高铁律：绝不混淆、绝不认错）**：
   - **URL 显式语义绑定**：`urls` 列表必须按固定契约构建，返回结果按索引 `result[i]` 严格回填对应机构对应玩法：
     - `handicap.aspx?companyID={cid}` 必须且只能解析为 `asianOddsText`（亚洲让球盘）；
     - `overunder.aspx?companyID={cid}` 必须且只能解析为 `overUnderOddsText`（大小球盘）；
     - `1x2.aspx` 或 `1x2d.js` 必须且只能解析为 `european1x2Text`（欧洲胜平负）；
   - **返回校验门禁断言**：提取内容后必须执行特征关键字校验：
     - 亚盘必须校验包含“大阪樱花/横滨水手”与让球字样；
     - 大小球必须校验包含“大球/小球”字样；
     - 欧指必须校验包含“主胜/平局/客胜”三项浮点数；
     - 一旦关键字不匹配，立即报错阻断，**严禁跨玩法交叉污染，严禁把不对的数据填进不该在的位置**！
4. **自适应元素记忆 (Adaptive Relocation)**：
   - 在解析微观首发或动态表格时，启用 `auto_save=True` 记忆元素指纹，改版时启用 `adaptive=True` 自动寻回。

#### Scrapling MCP 官方原生工具调用范式（严禁自写散装 Python 脚本）
```json
// 1. 抓取百家欧指数据流（163家机构初即盘与时序，毫秒级直取）
mcp__scrapling__make_request({
  "url": "https://1x2d.titan007.com/3000474.js",
  "impersonate": "chrome",
  "main_content_only": false
})

// 2. 7 大法定做市商亚盘/大小球变盘流水（bulk_get 并发矩阵秒取，绝不循环单拉）
mcp__scrapling__bulk_get({
  "urls": [
    "https://vip.titan007.com/changeDetail/handicap.aspx?id=3000474&companyID=1&l=0",
    "https://vip.titan007.com/changeDetail/overunder.aspx?id=3000474&companyID=1&l=0",
    "https://vip.titan007.com/changeDetail/handicap.aspx?id=3000474&companyID=3&l=0",
    "https://vip.titan007.com/changeDetail/overunder.aspx?id=3000474&companyID=3&l=0"
  ],
  "impersonate": "chrome",
  "main_content_only": false
})
```

#### 实战踩坑必记
1. **编码陷阱**：球探二级页面（`changeDetail/*.aspx`）为旧版编码，默认 UTF-8 会导致队名和盘口乱码，必须使用 `gb18030` 解码；
2. **欧指百家非 SSR**：`oddslist/{id}.htm` 为空骨架，真实 163 家公司数据存储在 `https://1x2d.titan007.com/{id}.js` 中，直接抓 JS 文件效率最高且最全；
3. **欧指历史流水参数与并发直取**：`OddsHistory.aspx` 若只传 `sid` 和 `cid` 会返回空表，必须传 `id={odds_id}` 参数方可提取分钟级变盘流水；核心做市商（澳彩 1、Crown 3、Bet365 8）可直接请求 `vip.titan007.com/changeDetail/1x2.aspx` 直取全量时序；
4. **剔除滚球盘口**：调赔时序必须严格截断至比赛开球前，状态标记为“滚”或比分非 0:0 的记录必须物理剔除；
5. **体彩数据隔离铁律**：中国体彩仅用于核对场次代号（如周四001）、开售状态与节假日休市，其静态赔率绝不进入 AI 十步深度推演与概率计算！

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

### 4. 预赛快照与落盘标准（乔布斯式极简产品规范）

- 统一落盘路径：工整单文件 `data/YYYY-MM-DD/{matchId}.md`（全天赛程总览与元数据汇总于 `data/YYYY-MM-DD/meta.md`）。彻底废除单体大 JSON 与多级子目录。

#### 法定单场 Markdown 快照黄金基准模板（Golden Baseline Template，以 3000474.md 为物理标杆）
```markdown
# 【竞彩编号】联赛 主队 vs 客队
- **比赛 ID**：{matchId}
- **开球时间**：YYYY-MM-DD HH:MM
- **场地与天气**：{球场} ｜ {天气}
- **Polymarket 预测市场**：https://polymarket.com/sports/{league}/{slug} (主胜 X¢ | 平局 Y¢ | 客胜 Z¢)

---

## 一、微观阵容与首发伤停
- **主队**：号码 (位置) 姓名（具体伤因与影响）
- **客队**：号码 (位置) 姓名（具体伤因与影响，严禁脑补全主力或无人缺阵）

---

## 二、基础战绩与攻防客观底牌
- **主队近况**：主场近6场 X胜Y平Z负 (赛季主场场均进球 A，失球 B)
- **客队近况**：客场近6场 X胜Y平Z负 (赛季客场场均进球 C，失球 D)
- **赛事性质与战意博弈**：赛事类型（争冠/保级/淘汰/友谊赛走过场/德比宿敌）。**庄家借战意做市破译**：散户执着于何种线性战意信仰，机构如何借机设立门槛或反向开盘收割。
- **赛程陷阱**：主队未来赛程 ｜ 客队未来赛程（重点标注未来3~4天是否有重大洲际杯赛分心）
- **盘路画像**：主队相同初盘赢盘率 ｜ 客队近期盘路走势形态

---

## 三、法定23家机构初即盘与凯利总表
| 机构类型 | 机构 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初返还 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还 | 凯利(主/平/客) |
（覆盖法定23家：核心做市14家 + 终端履约2家 + 老庄2家 + 论文样本5家）

---

## 四、法定23家机构五阶段时序生命周期矩阵（T0~T4 节点）
### 第一战区：欧亚双盘全能做市商（澳彩/皇冠/365/易胜博/平博/188Bet/马会，共7家）
（各家严格包含亚盘、大小球、欧指各5行生命周期）
### 第二战区：欧洲大陆与国际纯欧指做市商（威廉/立博/伟德/Interwetten/Bwin/SNAI/必发/利记/沙巴/5家论文，共14家）
（各家严格包含欧指5行生命周期与形态学识别）
### 第三战区：终端履约实盘标的（体彩官方 HAD/HHAD[-1] + Polymarket 链上撮合，共2家）

---

## 五、Crown 皇冠全指数波胆与比分矩阵
- **波胆比分赔率**：1:0 ｜ 2:0 ｜ 2:1 ｜ 0:0 ｜ 1:1 ｜ 0:1 ｜ 0:2 ｜ 1:2 ...
- **总进球赔率**：0~1球 ｜ 2~3球 ｜ 4~6球 ｜ 7+球
- **半全场赔率**：主/主 ｜ 主/和 ｜ 和/主 ｜ 和/和 ｜ 客/客 ...
```
- **乔布斯极简五阶段时序生命周期矩阵（T0～T4 各 1 行，绝不堆砌冗余流水）**：
  - **拒绝原始数据倾倒**：严禁把同一阶段内的 5~6 笔碎步微调原样倾倒进快照！这属于转储垃圾。T0～T4 不是文件夹，而是博弈的 5 个战略里程碑。
  - **每个机构每种玩法整整齐齐恰好 5 行**：
    1. **T0 初盘骨架（开盘~24h前，1行）**：取最初始挂单，锁定精算师无偏期望物理基准；
    2. **T1 早盘试探（24h~8h前，1行）**：取早盘测试散户偏见的关键位移点；
    3. **T2 中盘假摔（8h~3h前，1行）**：取中盘诱多诱空、制造假摔冲高的最极致震荡点（若未变动则明确标注“维持区间”，绝不留空）；
    4. **T3 临盘洗盘（3h~1h前，1行）**：取首发大名单酝酿与大资金涌入时的极限顶水/压水防守点；
    5. **T4 终盘关门（即时/分析时点，1行）**：弹性自适应当前分析时点！无论主人是提前几小时分析还是临开球分析，T4 均直接取当前分析发起时的最新即时盘（Current Latest），作为当前推演决策的最终关门定格态，绝死板硬卡 1 小时窗口。
  - **一眼看穿博弈剧本**：5 行横向贯穿，人眼与大模型 5 秒内瞬间穿透庄家 72 小时的做市剧本。
- 输出结构严格遵循 `agent.analysis` 契约规范。
- **杜绝低级排版与骨架抓取错误（刚性规范）**：
  1. **结构化原生存储**：百家欧指必须通过 `1x2d.js` 解析后，结构化写入 `markets.europeCompanies` 数组（包含各公司初即盘、返还率与凯利独立对象），**严禁将百家数据挤入单行转义长文本**导致 JSON 仅有几十行假象！
  2. **精准容器提取（严禁全页乱倒）**：BrowserOS neo 抓取阵容或赔率时，必须使用精准 CSS 选择器（如 `#analy_sbAllOdds`、阵容表格）或 `clean_dom_text` 过滤，**严禁将包含“首页/足球直播”的整页导航栏文本塞入快照**。
  3. **等待异步渲染**：对需浏览器渲染的 DOM 元素必须设置 `wait-selector` 等待数据真实装载，严禁保存未渲染的静态 HTML 空骨架（`<!DOCTYPE...`）。
  4. **法定 23 家白名单精准提纯（严禁算术平均陷阱）**：
     - **严禁算术平均**：系统严禁计算百家赔率的算术平均数！不同机构抽水率完全不同，直接平均违背概率公理且抹杀做市商意图。基准对账一律遵循「同公司三项去水（OO-EPC）后才聚合」；
     - **直接过滤落盘**：`1x2d.js` 流入后，直接按法定 23 家白名单（核心 14 家做市商 + 2 家终端 + 2 家老庄 + 5 家论文样本）切片写入 `markets.europeCompanies`；
     - **彻底抛弃垃圾小庄**：其余 140+ 家抄盘跟风小白标直接丢弃，不存明细，不折算伪平均，保持快照纯净与高信噪比。
- 无论通过 Scrapling 提取还是 BrowserOS neo 渲染，均必须包含：
  1. `european1x2Text` 与 `markets.europeCompanies`：主流机构百家初即盘、返还率与凯利指数（法定 23 家提纯，严禁算术平均）；
  2. `markets.europeHistories`：包含核心做市商（澳彩、Crown、Bet365、易胜博等）完整的分钟级调赔时序（带时间戳、胜平负赔率、初/即状态），严禁仅有初即两点切片偷懒；
  3. `asianOddsText` / `overUnderOddsText`：7 大法定做市商（澳彩、Crown、Bet365、易胜博、平博、188、香港马会）分钟级变盘流水；
  4. `trendComparison`：带时间戳的变盘时序流水（包含亚盘与欧赔调水流水，供安检门禁核验）；
  5. `lineupData`：首发球员评分、伤停原句；
  6. `tactics`（含攻防进失球/场均进球物理数字）与 `profiling`（相同初盘画像与盘路走势）。

- **自愈机制（Self-healing）**：门禁 `verifier.py` 已打通攻防物理数据的多通道智能识别（无论是 `match.homeGoals/awayGoals`、`basicStatsText` 还是 `tactics.home/away` 结构化进失球，均可直接识别放行），彻底消灭因字段命名差异导致的拦截误报。

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

7 列表最后一格必须物理调用 Gamma API 核查（严禁脑补与跳过）：
1. 关键词快查：`curl.exe -sS --ssl-no-revoke "https://gamma-api.polymarket.com/public-search?q={球队名}"`
2. 联赛全量查：`curl.exe -sS --ssl-no-revoke "https://gamma-api.polymarket.com/events?series_slug={series_slug}&active=true&closed=false"`
3. 直达链接规则：`https://polymarket.com/zh/sports/{series_slug}/{event_slug}`，附带实时价格（¢）。查无结果方可标注“确认未开盘”。详细步骤见 `docs/Polymarket链接查找教程.md`。

## 数据源与主源失败处理

盘口主源是球探网。资料齐不齐、对不对，不看网站姓什么（详见 ADR 0001）。**线上抓取采用 Scrapling 极速通道与 BrowserOS neo 协同双轨，严禁先跑旧版 npm 脚本。**

### 1. 赔率与赛程
- **主数据源（Primary）**：titan007 球探页。当场按赛事分组提取分析依据公司的可见流水与 Crown 已有项目。14 家名单是宽覆盖描述，不是每场每市场全覆盖保证。
- **抓取通道**：Scrapling（主攻欧亚变盘流水与 1x2d 百家数据流） + BrowserOS neo（主攻单场分析页阵容与微观交互），大模型自主抉择调度。若出现网络波动或残页，大模型自主调用另一通道补齐；若仍缺，置顶如实提示并贴出原因。
- **公司矩阵（按赛事分组，页面或接口编号分别核对，不猜编号）**：
  - 欧洲及其他赛事欧指：威廉、365、立博、伟德、平博。
  - 德国欧指：威廉、365、Interwetten。
  - 亚洲欧指：澳彩、皇冠、365、易胜博、马会。
  - 亚盘、大小球：7 大法定做市商（澳彩 1、Crown 3、Bet365 8、易胜博 12、平博 47、188 42、香港马会 48）全量可见赛前流水，逐市场逐机构核查，严禁跨市场凑数。平博作为低抽水无偏做市商必须全量参与欧指、亚盘及大小球时序对账。
  - 变盘页 `companyID` 以当场页面链接为准。`config/datasources.json` 的 `tracked_bookmakers.id` 是另一套接口编号，不得直接套到变盘页。
- **缺失与冲突口径**：未检查、读取失败或未读完整、来源已查但未填、尚未发生、计算未执行、内部不可见。**凡已发生而读取失败、或读取不完整的，必须在报告开头向主人明确提示**；快照顶层 `fetchedAt` 早于内部嵌入报价时间、静态摘要与原始流水反向冲突或市场字段错位时，标记证据冲突并禁止签发完整通过收据。
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
   - **亚盘让球与大小球流水**：通过 Scrapling 直取 7 大法定做市商（澳彩 1、Crown 3、Bet365 8、易胜博 12、平博 47、188 42、香港马会 48）`changeDetail` 全量流水（GB18030解码）；
   - **微观首发与伤停情况**：通过 BrowserOS neo 访问分析页抽取「阵容情况」与球员评分；
   - **Crown 皇冠波胆全指数**：分析页 `#analy_sbAllOdds` 中 0:0～4:4 比分波胆赔率矩阵及半全场。
2. **本地快照存盘（方案B纯净结构化规约）**：组装保存为 `data/YYYY-MM-DD/{matchId}.json`。序列化必须严格遵循 `json.dump(..., indent=2, ensure_ascii=False)`。全面废除在 `trendComparison`、`european1x2Text`、`asianOddsText` 中存放 `\t` 和 `
\n` 的转义长文本乱码；盘口、赔率与五阶段变盘流水一律采用原生结构化数组（`europe1x2`、`asianHandicap`、`overUnder`、`timeSeriesFlow`），杜绝大泥潭乱码，确保人眼秒懂与编辑器自然语法高亮。
3. **物理安检门禁**：通过 `python 校验/src/adapter/cli.py --match ...` 检验数据完整性。门禁已实现双模无缝兼容（同时支持原生纯净列表与传统字段）。门禁通过即进入 10 步深度推演；若门禁拦截，AI 自主调度补抓，拒绝无依据硬推。
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
