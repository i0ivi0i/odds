## TOOLS.md - 工具使用指南

Skills 定义了工具的工作方式。此文件记录当前仓库中可用的数据抓取工具与命令。常用工具或者插件之类的"使用方法"得到更新或者技巧之后，也要在本文件进行记录更新。

---

## 核心系统：官方 Scrapling 原生数据采集体系（Skill scrapling-official ↔ MCP scrapling）

**绝对刚性红线（100% Scrapling 独家立宪与外部浏览器绝对红线）**：
1. **进货通道 100% 独家**：系统数据采集进货 100% 独家归属 **`Skill /scrapling-official` ↔ `MCP scrapling`** 官方原生流水线！
2. **严禁调用外部独立浏览器**：全流程绝对严禁在任何数据采集、赛程同步、变盘流水或页面抓取环节调用外部独立浏览器（如 `Skill /browseros-neo` ↔ `MCP browseros_neo`）！外部独立浏览器仅限主人亲自交互浏览，AI 在常规和异常业务流中绝对禁止擅自启动或降级调用！
3. **全流程严禁任何临时 `.py` 脚本、跑批脚本、数据清洗脚本、复盘对账脚本或 `python -c`！** 违者视为严重工程违规与作弊。

**Scrapling 官方内部四级闭环与分块并发军规**：
当遭遇网络重置或源站 WAF 限制时，必须且只能在 Scrapling 框架内部自洽升阶：
- **一级（极速协议并发）**：`mcp__scrapling__bulk_get` 并发直取（遵循官方分块军规：单批切片 $\le 6\sim 8$ URLs，每批之间加 0.3s `retry_delay`；前置下推选择器 `css_selector="#table_odds"`）；
- **二级（单步精准协议流）**：`mcp__scrapling__fetch(network_idle=true)`；
- **三级（指纹反爬绕过）**：`mcp__scrapling__stealthy_fetch`（模拟 TLS 指纹与规避 Cloudflare/WAF）；
- **四级（内部 Chrome 驱动）**：Scrapling 内部 `--real-chrome` 无头渲染受控驱动。

- **阶段 0：赛程索引确定性自检与 Scrapling 极速直落（Zero-State Hard Lock）**：
  - 凡触发赛前分析、赛程同步或手动推演，大模型唤醒后**第 0 秒第一工具动作**必须且只能先检查 `data/{销售日}/meta.md` 是否存在且新鲜（< 2小时）；
  - 若缺失或超期，调用 `mcp__scrapling__fetch(url="https://jc.titan007.com/index.aspx", extraction_type="markdown", network_idle=true)` 秒级提取全天场次 ➔ 原子落盘 `data/{销售日}/meta.md` 与追加 `memory/{销售日}.md`（全程 < 2 秒）；
  - **严禁漫游翻书铁律**：在 `data/{销售日}/meta.md` 确立前，绝对禁止阅读 `skills/deep-analysis` 技能、绝对禁止查看任何 Python 源码、绝对禁止思考盘赔逻辑！
- **批量赛事分批并发矩阵与进货门禁规约（First-Action Batch Matrix）**：
  - 赛程索引就绪后，由主人指令锁定推演范围（全部/早盘/晚盘/指定，严禁任何 AI 将分批大小当成推演总数！）；
  - 构造候选场次分批矩阵（严格按 4~6 场为一组 Batch、4~8 URLs 协议流并发 + 选择器下推），调用 `mcp__scrapling__bulk_get` 分批秒取数据；
  - **法定装配落盘与物理清空重抓**：搬运工直接调用官方 Scrapling MCP `bulk_get`（分块军规 ≤6~8 URLs + 选择器下推）并发拉取 26 端点写入 `raw/{matchId}.json` ➔ 运行离线受测命令 `python 校验/src/adapter/cli.py --assemble-bundle data/{销售日}/raw/{matchId}.json --output data/{销售日}/{matchId}.md` ➔ 单场验过；**严禁大模型手动拼接 Markdown 避免封条失真！凡触发重新推演，第一动作绝对强制物理清空旧快照，严禁在旧文件上用 replace_file_content 局部打补丁改时间作弊伪造活水！**
  - 严禁单场串行磨洋工，严禁单批超载倾倒，未见快照落盘并通过 `cli.py --batch ... --isolate-failed` 门禁（exit 0）前，绝对禁止开脑推演！
- **主力全包引擎：Skill `/scrapling-official` ↔ MCP `scrapling`（1~2 秒全量并发直取）**：
  - 原生集成 Chrome 136+ TLS 指纹伪装与抗封锁能力，通过 `mcp__scrapling__bulk_get` 一次性并发秒取单场全部 5 大数据源：
    1. **阵容伤停与基本面技统**：`https://zq.titan007.com/analysis/{id}cn.htm`（含伤停名单、主客得失球、盘路走势、进球时段、未来赛程）；
    2. **Crown 皇冠波胆与半全场**：`https://zq.titan007.com/analysis/odds/{id}.htm`（含 0:0~4:4 比分波胆、总入球、半全场、角球、必发指数）；
    3. **体彩全玩法与半场指数**：`https://zq.titan007.com/default/getAnalyData?sid={id}&t=1`（含体彩 HAD/HHAD/TTG/CRS/HAFU 及半场欧亚大）；
    4. **百家欧指与分钟级流水**：`https://1x2d.titan007.com/{id}.js`（含 23 家法定机构初即盘、返还率、凯利指数及全部变盘历史）；
    5. **7 大做市商亚盘与大小球流水**：`https://vip.titan007.com/changeDetail/handicap.aspx` 与 `overunder.aspx`。
  - **常规与异常流程 100% 由 Scrapling 官方内部四级闭环极速完成，严禁启动外部独立浏览器！**
- **赛后复盘赛果极速提取规约（赋能 skills/post-review 的 Scrapling 选择器下推通道）**：
  - 赛后复盘获取已完场比分时，作为 `skills/post-review` 的底层数据通道，调用 `mcp__scrapling__bulk_get` 批量并发抓取 `https://live.titan007.com/detail/{matchId}cn.htm`；
  - **强制配置选择器下推**：指定 `css_selector=".score, .analyhead, .team-name"` 仅提取比分与主客队名核心节点，彻底过滤百 KB 庞杂 HTML；
  - **百字节极速直出**：每场仅返回数十至百余字节的纯净文本直接作为技能输入送入模型上下文，由 `skills/post-review` 规约直接驱动对账与概率打分；
  - **全流程严禁编写任何 `.py` 正则提取脚本、清洗脚本或中间统计代码！**
- **自主智能调度与职责界限（物理门禁不僭越大脑）**：
  - AI 大模型拥有完全自主的选择、切换与组合调度权；
  - 无论选用哪一个工具，最终组装的目标文件必须落盘至工整单文件 `data/YYYY-MM-DD/{matchId}.md`（即本场法定的【推演源数据】；全天赛程索引与元数据明细统一汇总于 `data/YYYY-MM-DD/meta.md`），必须 100% 通过 `python 校验/src/adapter/cli.py --match ...` 物理安检门禁。
  - **核心分工红线**：门禁（`verifier.py`）只做**数据纯净度物理安检**（防空骨架、防字段错位、防缺机构），**绝对不负责推演判断、绝不输出预测胜负**。所有倍率推演与博弈破译全权由 **AI 大模型的大脑自主完成**！

---

### 2. 数据精准抓取与严禁错位（字段纯净与位置归位红线）

**最高数据铁律**：**数据一定要抓取正确，不要乱抓乱获取，绝对禁止把不对的数据放进不应该在的位置！**
数据采集必须实事求是、精准归位，严禁为了应付门禁而猜测脑补、拼凑假数据或把无关字段错位塞入【推演源数据】。各维度数据必须严格存放于专属语义字段：

| 数据维度 | 抓取内容与标准 | 对应【推演源数据】标准字段 | 严禁错位红线 |
| :--- | :--- | :--- | :--- |
| **分钟级变盘流水** | 澳彩/Crown/365/易胜博带时间戳的变盘时序 | `trendComparison` | 严禁缺少时间戳；严禁将未变盘的静态表头塞入流水 |
| **欧洲指数百家** | 从 1x2d 数据流提纯法定 23 家机构初即盘、返还率与凯利指数 | `european1x2Text` / `europeOddsSummary` | 严禁将亚盘让球水位误填入欧指；严禁丢失返还率 |
| **亚洲让球盘** | 主流机构初即盘盘口、上下盘水位及变盘记录 | `asianOddsText` | 严禁与大小球盘口混淆；严禁盘口与水位颠倒 |
| **大小球进球数** | 主流机构初即盘盘口、大球小球水位 | `overUnderOddsText` | 严禁将让球盘盘口填入大小球 |
| **微观首发与伤停** | 分析页「阵容情况」名单，若无则保留【暂无数据】原句 | `lineupData` | 严禁将上一场阵容当本场；无数据严禁脑补无人缺阵 |
| **真实场上压制力** | 控球率、射正比、角球、进球时段、未来赛程 | `tactics` | 严禁把表面积分排名直接当压制力指标 |
| **赛事性质与战意博弈** | 联赛争冠保级/杯赛淘汰/友谊赛走过场/死敌德比及庄家借题做市破译 | `tactics` / 战意博弈字段 | 严禁散户式盲信“战意强=必出”，必须反推庄家借散户狂热非对称收割 |
| **相同初盘与盘路** | 相同初盘历史胜率画像、近期盘路走势形态 | `profiling` | 严禁篡改初盘基准；严禁非结构化文本乱堆 |
| **Crown皇冠波胆** | `#analy_sbAllOdds` 中 0:0~4:4 比分矩阵赔率 | 波胆比分专属映射 | 严禁将总进球数赔率误当单场具体比分波胆 |

凡因字段错位、数据污染或时间戳缺失导致安检失败的，物理门禁（`verifier.py`）将立即硬拦截阻断，AI 必须重新精准获取并纠偏归位。

### 官方合法未开盘与推演到底准则（Anti-Drop Iron Rule）
1. **体彩深盘未开单固（HAD）**：若因实力悬殊深盘，中国体彩官方仅开让球胜平负（HHAD）而不开普通胜平负（HAD），欧指按 22 家法定机构自动放行，大模型必须推演体彩让球玩法，严禁丢弃比赛；
2. **次级联赛机构未开亚盘**：若香港马会（HKJC）等对英冠等次级联赛官方未开亚盘，装配器标记 `[("-", "官方未开盘", "-", "-", "未开盘")]`，亚盘按 6 家放行，严禁中断装配，比赛必须推演到底；
3. **推演覆盖率 100%**：严禁任何 AI 以特定机构未开盘为由擅自将开售赛事移出分析总表！所有开售场次必须全量穷尽推演。

---

### 2. Scrapling 极速提取与防错位规范（官方黑科技全开）

#### 官方三大能力全开配置与防错位防污染铁律
1. **抓取时选择器下推 (Selector Pushdown，严禁全量 DOM 倾倒)**：
   - 抓取 HTML 页面（如 `analysis/{id}cn.htm` 或 `odds/{id}.htm`）时，**必须显式下推 `css_selector` 参数**（如 `css_selector="#analy_sbAllOdds, #odds, #team_lineup, .analyhead"`）；
   - 底层 C/Cython 引擎在内存中就地剔除 90% 以上无关 DOM 树，单页文本从 200KB 压缩至 5KB 以内，秒回零超时，杜绝 Token 爆炸。
2. **小批分组并发规约（Batch Requesting，单批限 4~8 URLs）**：
   - 严禁单次向 `mcp__scrapling__bulk_get` 传入数十个长连接重型页面；
   - 批量矩阵请求严格按 **4~8 个 URL 为一组分批（Batching）并发**，各批间无缝秒级流转，杜绝 IPC 缓冲区溢出与 MCP 崩溃。
3. **抓取时流式内存截流 (In-Flight Hook，严禁 Raw JS 倾倒)**：
   - 请求 `1x2d.js` 时，数据流入内存第一时间使用法定 23 家 ID 集合直接筛选提纯；
   - 抛弃其余 140+ 家机构数据，向外交付仅包含法定 23 家初即盘的紧凑结构，单场数据严格压在 **5KB 以内**。
4. **防封与防火墙穿透 (TLS Fingerprint)**：
   - 必须标配 `impersonate="chrome"` + `stealthy_headers=True`；
   - 自动克隆真实 Chrome 136+ 协议特征，绕过 Cloudflare 与 OpenResty 握手拦截。
5. **精准语义防错位与防污染断言（最高铁律：绝不混淆、绝不认错）**：
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
// 1. 抓取百家欧指数据流（从 1x2d.js 提纯法定 23 家机构初即盘与时序，毫秒级直取）
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
2. **欧指百家非 SSR 与白名单提纯**：`oddslist/{id}.htm` 为空骨架，真实数据存储在 `https://1x2d.titan007.com/{id}.js` 中，直接抓 JS 文件并经法定 23 家白名单提纯收拢；
3. **欧指历史流水参数与并发直取**：`OddsHistory.aspx` 若只传 `sid` 和 `cid` 会返回空表，必须传 `id={odds_id}` 参数方可提取分钟级变盘流水；核心做市商（澳彩 1、Crown 3、Bet365 8）可直接请求 `vip.titan007.com/changeDetail/1x2.aspx` 直取全量时序；
4. **剔除滚球盘口**：调赔时序必须严格截断至比赛开球前，状态标记为“滚”或比分非 0:0 的记录必须物理剔除；
5. **体彩数据隔离铁律**：中国体彩仅用于核对场次代号（如周四001）、开售状态与节假日休市，其静态赔率绝不进入 AI 十步深度推演与概率计算！

---

### 3. Scrapling 原生微观伤停与波胆提取指南

- 官方 Scrapling 协议流直取分析页与波胆页，无需渲染浏览器，毫秒级提取微观阵容与 Crown 盘面。
- **微观伤停核验规范**：
  - Scrapling 并发拉取分析页（`https://zq.titan007.com/analysis/{matchId}cn.htm`），由装配器离线提取「阵容情况」表格；
  - 若页面明确印出缺阵名单，逐人记录姓名、位置与缺阵原因；
  - 若印出「暂无数据」，如实标注【暂无数据 / 伤停未核实】，保留页上原句，**允许继续十步但严禁脑补全主力或无人受伤**。
- **Crown 皇冠波胆与半全场**：
  - 从波胆页（`https://zq.titan007.com/analysis/odds/{matchId}.htm`）提取 0:0~4:4 比分波胆赔率矩阵及半全场赔率，作为泊松分布物理偏差对账的真实市场锚点。
- **即时走势与变盘流水**：
  - 欧指、亚盘、大小球的即时变盘流水，统一通过 Scrapling 并发拉取法定 7 家机构的 `changeDetail/*.aspx` 接口（结合 `css_selector="#table_odds"` 选择器下推），由装配器自动结构化提取，严禁依赖任何浏览器前端手工交互！

---

### 4. 【推演源数据】核心宪章与落盘规范（乔布斯式极简产品规范）

#### 🌟 宪章级释义：什么是【推演源数据】？意味着什么？位置与生命周期？
- **本质定义（What it is）**：【推演源数据】（`data/YYYY-MM-DD/{matchId}.md`）是自动化流水线**阶段一**由 Scrapling 极速协议流并发秒取 5 大法定接口（分析页阵容与技统、波胆页 Crown 指数、竞彩官方全玩法、百家欧指 `1x2d.js` 与变盘流水 `changeDetail`），经 `SnapshotAssembler` 精纯组装落盘的**唯一物理原材料与客观事实底牌**。
- **核心意义（What it means）**：
  1. **物理级防伪防火墙**：它是系统**两阶段硬隔离的核心物理边界**。没有 exit 0 的物理源数据，大模型绝对禁止动脑思考与输出赛果，彻底铲除凭记忆脑补、无根据猜想和时序克隆；
  2. **唯一法定证据链**：它是大模型 10 步深度推演、证据引用与赛后回查对账的唯一只读证据凭证；
  3. **门禁生死线**：必须通过 `cli.py --batch data/{销售日} --max-age-minutes 30` 终审检验（退出码 0），才准发放给首席分析师。
- **物理位置与生命周期（Where & Lifecycle）**：
  - **总索引位置**：`data/YYYY-MM-DD/meta.md`（全天赛程索引与状态大表）；
  - **单场文件位置**：`data/YYYY-MM-DD/{matchId}.md`（工整单文件，彻底废除单体大 JSON 与多级子目录）；
  - **时效生命周期**：最大有效期不超过 30 分钟（`--max-age-minutes 30`），开赛前必须处于鲜活状态。

#### 法定单场 Markdown 【推演源数据】黄金契约规范（Verbatim Raw Wire Contract）

任何单场比赛数据抓取与落盘必须严格遵守以下五大黄金模块契约结构，**一点数据不能造假、一点时间不能造假、甚至一个标点符号都不能篡改**：
```markdown
# 【竞彩编号】联赛 主队 vs 客队
- **比赛 ID**：{matchId}
- **开球时间**：YYYY-MM-DD HH:MM
- **场地与天气**：{球场} ｜ {天气}
- **Polymarket 预测市场**：https://polymarket.com/event/{slug} (主胜 X¢ | 平局 Y¢ | 客胜 Z¢)

---

## 一、微观阵容与首发伤停
- **主队**：号码 (位置) 姓名（具体伤因与影响）
- **客队**：号码 (位置) 姓名（具体伤因与影响，严禁脑补全主力或无人缺阵）

---

## 二、基础战绩与攻防客观底牌
- **主队近况**：主场近6场 X胜Y平Z负 (赛季主场场均进球 A，失球 B)
- **客队近况**：客场近6场 X胜Y平Z负 (赛季客场场均进球 C，失球 D)
- **赛程间隔**：主队距上场间隔 ｜ 客队未来赛程间隔
- **盘路画像**：主队相同初盘赢盘率 ｜ 客队近期盘路走势形态

---

## 三、欧洲指数百家做市商清单（法定 23 家）
| 机构类型 | 机构 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初返还 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还 | 凯利(主/平/客) |
（严格按 1x2d.js 原始报文提纯法定白名单机构，严禁对未开盘机构填充假赔率）

---

## 四、核心做市商与终端标的真实变盘时序流水（逐行原样零篡改）
### 第一战区：欧亚双盘全能做市商（澳彩/皇冠/Bet365/易胜博/平博/188Bet/香港马会，共7家）
（各家逐行原样列出赛前真实变盘记录：`| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |`；球探网有几行真实变盘就写几行，彻底废除 T0~T4 五阶段凑数、废除「维持区间」假行、废除主观「做市形态学识别」列！）
### 第三战区：终端履约实盘标的（中国体彩 HAD/HHAD + Polymarket 链上撮合，共2家）
（彻底废除第二战区 14 家纯欧指机构的凑数伪时序子表，其初即盘与凯利已在第三节完整呈现）

---

## 五、Crown 皇冠全指数波胆与比分矩阵
- **波胆比分赔率**：1:0 ｜ 2:0 ｜ 2:1 ｜ 0:0 ｜ 1:1 ｜ 0:1 ｜ 0:2 ｜ 1:2 ...
- **总进球赔率**：0~1球 ｜ 2~3球 ｜ 4~6球 ｜ 7+球
- **半全场赔率**：主/主 ｜ 主/和 ｜ 和/主 ｜ 和/和 ｜ 客/客 ...
```
- **原汁原味真实流水与加密封条铁律（Zero Fabrication & Cryptographic Seal）**：
  1. **彻底废除 T0～T4 凑数切片与主观形态列**：源数据文件只准存储 100% 客观原始数字与真实分秒时间戳，严禁在源数据中混入任何主观博弈定性文案（如“中盘假摔震仓”），所有博弈破译统一留到阶段二由首席分析师基于真实流水推演；
  2. **原始报文直读装配与 SHA-256 哈希封条（`--assemble-bundle` & `raw/{matchId}.json`）**：
     - **单一原子防伪溯源包（标准规约）**：将 Scrapling 抓取的原始报文与剪枝文本打包为单个原子 JSON `data/{销售日}/raw/{matchId}.json`（含 `matchId`、`mdSha256`、`rawSha256` 与全量原始 payload），彻底消灭 28 个零散文件；
     - **离线零脑补装配**：在终端运行 `python 校验/src/adapter/cli.py --assemble-bundle data/{销售日}/raw/{matchId}.json --output data/{销售日}/{matchId}.md`（或向后兼容 `--assemble-raw-dir`），零大模型转抄直出 Markdown，并自动清理旧版零散目录；
     - **双重哈希防伪与逐行溯源死锁**：门禁 `verifier.py` 严格校验 `TAMPERED_MARKDOWN_SEAL`、`TAMPERED_RAW_WIRE_SEAL` 与逐行 `RAW_PROVENANCE_MISMATCH` 核验——哪怕手动改动一个字符、截断一行变盘历史、篡改状态词（`早`/`即`/`初盘`）或捏造体彩时间戳，立即返回 `exit 1` 物理熔断！
     - **真实网络溯源回执与服务端指纹防伪（Network Receipt & Optional Live Probe）**：原子 JSON `raw/{matchId}.json` 强制包含 `"receipt"` 块（记录 27 个端点请求详情、HTTP 200 响应状态、字节大小、服务端指纹、原始载荷 SHA-256 与整包 networkSignature）；门禁 `verifier.py` 严格核验回执状态及载荷哈希一致性；支持通过 `--verify-network` 开启毫秒级远程实网抽检探测（`probe_remote_provenance`），彻底杜绝脱网伪造假数据！
- 输出结构严格遵循 `agent.analysis` 契约规范。
- **杜绝低级排版与骨架抓取错误（刚性规范）**：
  1. **结构化原生存储**：百家欧指必须通过 `1x2d.js` 解析后，结构化写入 `markets.europeCompanies` 数组（包含各公司初即盘、返还率与凯利独立对象），**严禁将百家数据挤入单行转义长文本**导致 JSON 仅有几十行假象！
  2. **精准容器下推提取（严禁全页乱倒）**：Scrapling 提取数据时必须使用精准 CSS 选择器（如 `#table_odds`、阵容表格）过滤，**严禁将包含“首页/足球直播”的整页导航栏文本塞入【推演源数据】**。
  3. **等待网络空闲与选择器下推**：动态页面抓取必须使用 `network_idle=true` 或指定 `css_selector`，确保真实数据完整装载，严禁保存未渲染的静态 HTML 空骨架（`<!DOCTYPE...`）。
  4. **法定 23 家白名单精准提纯（严禁算术平均陷阱）**：
     - **严禁算术平均**：系统严禁计算百家赔率的算术平均数！不同机构抽水率完全不同，直接平均违背概率公理且抹杀做市商意图。基准对账一律遵循「同公司三项去水（OO-EPC）后才聚合」；
     - **直接过滤落盘**：`1x2d.js` 流入后，直接按法定 23 家白名单（核心 14 家做市商 + 2 家终端 + 2 家老庄 + 5 家论文样本）筛选提纯写入 `markets.europeCompanies`；
     - **彻底抛弃垃圾小庄**：其余 140+ 家抄盘跟风小白标直接丢弃，不存明细，不折算伪平均，保持【推演源数据】纯净与高信噪比。
- Scrapling 原生流水线装配的【推演源数据】必须包含：
  1. `european1x2Text` 与 `markets.europeCompanies`：主流机构百家初即盘、返还率与凯利指数（法定 23 家提纯，严禁算术平均）；
  2. `markets.europeHistories`：包含核心做市商（澳彩、Crown、Bet365、易胜博等）完整的分钟级调赔时序（带时间戳、胜平负赔率、初/即状态），严禁仅有初即两点切片偷懒；
  3. `asianOddsText` / `overUnderOddsText`：7 大法定做市商（澳彩、Crown、Bet365、易胜博、平博、188、香港马会）分钟级变盘流水；
  4. `trendComparison`：带时间戳的变盘时序流水（包含亚盘与欧赔调水流水，供安检门禁核验）；
  5. `lineupData`：首发球员评分、伤停原句；
  6. `tactics`（含攻防进失球/场均进球物理数字）与 `profiling`（相同初盘画像与盘路走势）。

- **自愈机制（Self-healing）**：门禁 `verifier.py` 已打通攻防物理数据的多通道智能识别（无论是 `match.homeGoals/awayGoals`、`basicStatsText` 还是 `tactics.home/away` 结构化进失球，均可直接识别放行），彻底消灭因字段命名差异导致的拦截误报。

### 数据安全规则

- **赔率必须实时抓取**：每次分析都用 `/scrapling-official` 极速原生流水线实时拉取球探页最新数据，不复用 memory 中旧赔率。
- **只用赛前赔率**：过滤状态为“滚”的记录，并按开赛时间截断赛前变化历史。
- **缺失不臆造**：如果某家公司或某类市场缺失，报告中必须标注数据缺口，并降低对应维度权重。
- **平博用途**：平博可作为主流公司交叉验证参考，不单独用于决策依据。

### 数据质检与门禁验证套件（校验/src/adapter/cli.py）

```bash
# 运行全部质检单元测试与回归测试（130+项）
python -m unittest discover -s 校验/测试 -p "test_*.py"
```

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
# 单场比赛【推演源数据】 6 维度物理安检（核心数据缺失返回 exit 1 物理熔断）
python 校验/src/adapter/cli.py --match data/2026-10-07/2981506.md

# 结构化输出【推演源数据】安检法定收据（JSON格式）
python 校验/src/adapter/cli.py --match data/2026-10-07/2981506.md --json

# 全系统一致性、图谱连通性与算法单测联合健康巡检
python 校验/src/adapter/cli.py --system
```

## Polymarket 下单链接与法定第 6 接口（官方 Discover Markets API 检索标准）

> 📌 **官方权威文档索引（Documentation Index）**：`https://docs.polymarket.com/llms.txt`（AI 交互首选地图，全量中文详见 `_llms/cn.txt`）。

7 列表最后一格必须物理调用 Gamma API 真实核查（严禁脑补与跳过）：

### 1. 官方市场发现标准规约（Discover Markets via API - 严禁客户端拼接猜测 Slug）
Polymarket 官方架构明确立宪：**Slugs 不保证任何固定命名规律（如曼城vs巴黎为全名、林茨为 lin2、南安普敦为 sot），严禁客户端程序化拼接猜测 Slug！**
客户端猜测 Slug 是导致「404 坏链」与「误判未开盘」的唯一根因。必须严格依照官方标准流动态发现：
1. **第一步（免费文本动态搜索，首选）**：调用官方搜索接口获取候选事件列表：
   `GET https://gamma-api.polymarket.com/public-search?q={HomeTeamEn}`
   若主队英文词未命中或属杯赛，回退使用客队英文词：
   `GET https://gamma-api.polymarket.com/public-search?q={AwayTeamEn}`
2. **第二步（事件匹配与活性校验）**：
   - 在返回的 `events` 列表中，核验对阵另一方英文名称（`title` 或 `slug` 包含另一方）；
   - 核验事件状态：必须为当前活跃盘口（`active: true` 且 `closed: false`）；
   - 提取官方原生事件标识 `event.slug`（绝不自行拼凑）。
3. **第三步（标准前端下单链接）**：
   - 必须且只能输出官方标准链接格式：`https://polymarket.com/event/{event.slug}`
   - 示例：`https://polymarket.com/event/acle-vik-jeo-2026-10-14`、`https://polymarket.com/event/ucl-paris-saint-germain-vs-manchester-city`
4. **第四步（衍生盘全景裂变）**：
   - 通过主事件的 `gameId`（如 5107619），调用 `https://gamma-api.polymarket.com/events/keyset?game_id={gameId}`，一键解锁波胆比分（Exact Score）、半场盘（Halftime）与大小球。

### 2. 门禁硬红线与防伪存证（实事求是，去伪存真）
1. **实事求是原则（严禁为了逃避门禁而伪造 Slug）**：严禁凭空捏造带汉字、占位符或假缩写的虚构链接（如 `match-{id}`、`acle-神户胜-...` 等）！
2. **查无标的必须如实存证**：只有当主客双方英文关键词经 `public-search` 双向检索均未返回任何匹配 active 事件时，才允许实事求是标注『官方未开盘（经Gamma双向核验均无对应链上预测标的）』；
3. **门禁双向核验放行**：具备真实 Gamma 双向核验凭据且正文未编造挂单赔率时，门禁以 `WARN` 放行推演；欧洲指数法定要求自动对齐为 22 家传统机构，全量推演到底；
4. **虚构链接零容忍硬熔断**：凡检测到链接包含模板占位符、伪造前缀（如 `match-`）或中文字符，门禁直接触发 `FAIL` 物理熔断！

### 3. 纯英文环境铁律（English-Only Wire Protocol）
Polymarket 链上智能合约、标的名称及底层 Gamma 数据库 **100% 为纯英文环境**：
- **严禁用中文发请求**：严禁将任何中文队名或中文联赛用于 `q=` 搜索（如 `q=神户` 必返回空导致误判未开盘）；
- **英文队名精准提取**：必须从球探分析页顶部 `#headTeam` 容器或队徽英文属性提取官方英文名（`HomeTeamEn` / `AwayTeamEn`，如 `Vissel Kobe`、`Southampton`、`Feyenoord`）；
- **Slug 纯英文小写**：所有 Slug 命名一律为纯英文小写、数字与连字符，严禁包含任何非 ASCII 字符。

## 数据源与主源失败处理

盘口主源是球探网。资料齐不齐、对不对，不看网站姓什么（详见 ADR 0001）。**线上抓取 100% 独家采用 Scrapling 官方原生流水线，严禁先跑旧版 npm 脚本，严禁调用外部独立浏览器。**

### 1. 赔率与赛程
- **主数据源（Primary）**：titan007 球探页。当场按赛事分组提取分析依据公司的可见流水与 Crown 已有项目。14 家名单是宽覆盖描述，不是每场每市场全覆盖保证。
- **抓取通道**：100% 独家锁定 Scrapling 官方原生流水线（分析页、波胆页、竞彩玩法、1x2d 百家与欧亚变盘流水）。若遇网络波动，由专职搬运工在 Scrapling 框架内升阶重试；若仍缺，置顶如实提示并贴出原因。
- **公司矩阵（按赛事分组，页面或接口编号分别核对，不猜编号）**：
  - 欧洲及其他赛事欧指：威廉、365、立博、伟德、平博。
  - 德国欧指：威廉、365、Interwetten。
  - 亚洲欧指：澳彩、皇冠、365、易胜博、马会。
  - 亚盘、大小球：7 大法定做市商（澳彩 1、Crown 3、Bet365 8、易胜博 12、平博 47、188 42、香港马会 48）全量可见赛前流水，逐市场逐机构核查，严禁跨市场凑数。平博作为低抽水无偏做市商必须全量参与欧指、亚盘及大小球时序对账。
  - 变盘页 `companyID` 以当场页面链接为准。`config/datasources.json` 的 `tracked_bookmakers.id` 是另一套接口编号，不得直接套到变盘页。
- **缺失与冲突口径**：未检查、读取失败或未读完整、来源已查但未填、尚未发生、计算未执行、内部不可见。**凡已发生而读取失败、或读取不完整的，必须在报告开头向主人明确提示**；【推演源数据】顶层 `fetchedAt` 早于内部嵌入报价时间、静态摘要与原始流水反向冲突或市场字段错位时，标记证据冲突并禁止签发完整通过收据。
- **其他来源**：亚盘/欧指流水、机构盘口、主客场/近6数字齐全、没错、对得上 → 可以代。错了、空了、少了一截 → 不能代。伤停格「暂无数据」不是缺数据，如实标注未核实，不挡十步推演。
- **体彩官方网关**：核对场次编号、开售窗口、节假日休市（见 `config/datasources.json` 的 `sporttery_match_codes`）。三项静态赔本身不是完整盘口资料。找 7 列表链接时用它对照现价对场次。

### 2. 阵容伤停独立双引擎 (Lineup & Injury Engine)
- **英超官方 FPL 数据库**：通过 `injury-service.js` 直连英超官方数据，零等待获取主力伤情与出战概率。
- **Big Balls Sports Data API**：直连商业体育数据网关，支持西甲、意甲、德甲、法甲、美职联，凭证读取自 `~/.gemini/config/bigballs_tokens.json`。

### 3. 海外免费开放 API 矩阵储备
- **Football-Data.org**：免费提供欧洲主要联赛赛程、积分榜、H2H 交锋与阵容（凭证读取自 `~/.gemini/config/football_data_tokens.json`）。
- **The Odds API (the-odds-api.com)**：免费 Starter 方案支持平博、365、威廉等做市商标准 1X2 与盘口查询（作为 Pinnacle / Betfair 尖锐欧指去水验真辅轨，详见 ADR 0012）。

## 核心安全通道：Scrapling 官方原生直取与【推演源数据】落盘规范

专职搬运工调用 Scrapling 极速协议流并发直取，严禁调用外部独立浏览器（如 `browseros-neo`），不是让主人自己开网页，也不是另写外置爬虫。

1. **官方原生采集全维度数据**：
   - **百家欧指 1X2 与流水**：通过 Scrapling 直取 `1x2d.titan007.com/{id}.js`（提纯法定 23 家机构）与 `OddsHistory.aspx`（澳彩等核心依据公司变盘流水）；
   - **亚盘让球与大小球流水**：通过 Scrapling 直取 7 大法定做市商（澳彩 1、Crown 3、Bet365 8、易胜博 12、平博 47、188 42、香港马会 48）`changeDetail` 全量流水（GB18030 解码，选择器下推 `#table_odds`）；
   - **微观首发与伤停情况**：通过 Scrapling 访问分析页（`analysis/{id}cn.htm`）提取「阵容情况」与球员评分；
   - **Crown 皇冠波胆全指数**：通过 Scrapling 访问波胆页（`analysis/odds/{id}.htm`）提取 0:0～4:4 比分波胆赔率矩阵及半全场。
2. **确定性【推演源数据】自动化装配管道 (SnapshotAssembler)**：
   - 严禁大模型在会话里手写文本或拼凑散装 Markdown！原始数据采集后，通过确定性装配管道直接转化为符合黄金契约的单文件 Markdown 【推演源数据】：
     ```bash
     python 校验/src/adapter/cli.py --assemble raw_data.json --output data/YYYY-MM-DD/{matchId}.md
     ```
   - 装配器负责结构化提纯法定 23 家欧指、7 大做市商双盘时序、Crown 波胆与官方玩法，保证字段 100% 规范无噪音。
3. **物理安检门禁与反克隆核验**：
   - 运行 `python 校验/src/adapter/cli.py --match data/YYYY-MM-DD/{matchId}.md`。
   - 门禁执行 6 大黄金维度安检 + 第 9 道 `AUTHENTICITY` 真实性与防克隆核验（校验主客队名对齐、杜绝模板占位符、杜绝测试夹具时序克隆）。
   - **退出码硬熔断**：返回 exit 1 时必须立即物理阻断，严禁输出任何推演结论与预测表格！返回 exit 0 (PASS/WARN) 方可进入 10 步推演。
4. **伤停空表处理**：分析页抽出的阵容表若印「暂无数据」，如实标注【暂无数据 / 伤停未核实】，保留页上原句，**允许继续十步推演，严禁脑补无伤停**。
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
  task: "执行赛程同步。读取 skills/match-scraper/SKILL.md。严格按照模板，使用 /scrapling-official 抓球探竞足页全量赛程，禁止先跑 npm run schedule。通过 messaging 推送赛程列表给主人，写入 memory/{今天日期}.md。"
  label: "match-sync"

# 深度分析（编排 subagent 内部 spawn worker）
sessions_spawn:
  task: "深度分析 [英超] 阿森纳 vs 曼城（ID: 2950977）。读取 skills/deep-analysis/SKILL.md。严格按照模板，阶段一完成【推演源数据】落盘并过验，worker 纯只读加载【推演源数据】完成全部 10 步分析；超 4000 字须分段。通过 messaging 推送分析报告给主人。返回结构化综合评估结果（JSON 格式）。"
  label: "deep-analysis-2950977"
  runTimeoutSeconds: 900
```
