---
name: match-scraper
description: "从球探体育(titan007)抓取竞彩足球赛程数据与单场【推演源数据】。不仅在用户说「抓取赛程」「获取今日比赛」「进货」「拉取推演源数据」时使用，当任何 Agent / Subagent 在定时任务、自动化工作流、阶段零（赛程自检与索引初始化）或阶段一（推演源数据抓取与门禁质检）需要获取数据时也必须主动调用。"
metadata: { "emoji": "📆" }
---

# 赛程与推演源数据采集（match-scraper）

本技能包含两大工作模式：
- **模式一：赛程同步与索引初始化**（每日 11:10 定时触发、用户主动查询、或任何 Agent 阶段零自检缺盘触发）：抓取当日竞彩足球全量赛程，落盘 `data/{YYYY-MM-DD}/meta.md` 并写入 memory。
- **模式二：【推演底层源数据】抓取与人类视图装配**（赛前分析阶段一专属搬运工 / Agent 蜂群自驱调用）：Scrapling MCP 并发秒取法定 26 个底层端点，秒级落盘底层真实存证 `data/{销售日}/raw/{matchId}.json` 解锁推演；同步组装落盘 `data/{销售日}/{matchId}.md` 作为人类可视化复盘简报。

用 Skill `/scrapling-official` 官方原生流水线并发抓取球探页面。严禁调用外部独立浏览器（如 `browseros-neo`），禁止先跑 `npm run schedule`。

## 前提条件

- 数据进货 100% 独家归属 Skill `/scrapling-official` ↔ MCP `scrapling`（官方四级闭环）。严禁调用外部独立浏览器！
- **【全语种零临时脚本硬铁律】**：绝对严禁编写任何临时脚本（无论语言是 `.py`、`.ps1`、`.js`、`.bat`、`.sh`，违规次数严格锁定为 0）！绝对禁止在 terminal 执行任何散装脚本代码！
- **【零磁盘中转垃圾硬铁律】**：绝对严禁在磁盘创建任何 `tmp_*` 暂存文件夹，绝对严禁倾倒任何 `.txt` 原始中间文件！全流程 100% 内存流式直出落盘！
- **【Scrapling 原生 Markdown 直转】**：变盘流水页面（21 张大表）强制传 `css_selector="#table_odds"` 与 `extraction_type="markdown"`，由 Scrapling C/Cython 引擎原地生成纯净 Markdown 表格，内存直取直接拼入人类简报，严禁手写任何胶水解析脚本！
- 抓取赛程目标页面：`https://jc.titan007.com/index.aspx` 抽编号、比赛 ID、开球、对阵、分析页。
- 抓取推演源数据目标页面：单场法定 26 个底层端点（分析页、波胆页、竞彩接口、1x2d.js、7家做市商亚欧大 21 张变盘流水、Polymarket 链上预测）。
- 抓不到或场次不全：置顶报告，结束流程，不写残缺记录进 memory。
- **每次必须实时重新抓取**，不得复用之前抓取的旧数据。

## Scrapling 官方防反爬隐身、分层架构与四大原生护栏规约（Official Stealth & 4 Native Guardrails）

为了确保系统永不被球探网风控与反爬 WAF 识别阻断，全流程进货必须严格依循 D4Vinci/Scrapling 官方两级分层架构与四大原生护栏参数契约：

0. **Scrapling 官方自适应记忆（Adaptive Scraping）物理边界澄清**：
   - **DOM 特征指纹自愈（官方设计本质）**：Scrapling 的记忆机制是将元素的 DOM 结构指纹（标签、属性、祖先拓扑、兄弟路径）持久化存储于 SQLite 中。当目标网站改版、改 class 名或微调结构时，利用相似度算法自动重定位目标元素，防止爬虫因选择器失效报错；
   - **绝非赔率数值缓存**：**Adaptive 记忆的是网页骨架指纹，绝对不是赔率数字缓存！** 足球博弈赔率每时每刻都在发生真金白银的变动（即时活水），绝不能用历史记忆替代最新盘口，每次推演必须通过 Scrapling MCP 实时全量抓取。

1. **官方两级分层进货架构（Tiered Ingestion Architecture）**：
   - **Level 1（纯 HTTP 协议流，首选必选）**：基于 `curl_cffi`，毫秒级响应，零无头浏览器启动开销。所有球探网静态服务端渲染端点（赛程页 `index.aspx`、百家欧指 `1x2d.js`、变盘流水 `handicap.aspx`、微观阵容 `analysis/{id}cn.htm`）默认 100% 优先采用 `mcp__scrapling__bulk_get` 或 `session_make_request`。
   - **Level 2（Playwright 无头浏览器，升阶容灾）**：仅在 Level 1 返回 HTTP 403/503、频繁超时，或源站下发 Cloudflare Turnstile 等动态人机挑战盾时，在 Scrapling 内部升阶至 `mcp__scrapling__stealthy_fetch`。静态数据严禁无故直接调用 Level 2 浏览器！

2. **官方四大原生护栏（The 4 Scrapling Native Guardrails）**：
   - **护栏一：Anti-Mismatch Guardrail（防错位防串号护栏）**：
     - **URL 与市场实体显式绑定**：在并发抓取前显式建立端点 URL 字典（如 `ah_url`, `ou_url`, `eu_url`, `1x2d_url`），绝不依赖盲目的数组索引遍历；
     - **特征词双向断言**：处理批量返回时，必须校验专属特征词（亚盘验证 `Crown 亚让/让球`、欧指验证 `百家做市/返还率`、大小球验证 `高于/低于`），发现错位立即报警阻断，杜绝跨盘串号与数据张冠李戴；
     - **GB18030 二进制保真解码**：球探网二级变盘流水页面（`changeDetail/*.aspx`）必须基于原始 bytes 显式以 `gb18030` 解码，严禁外部默认 UTF-8 强解导致队名盘口汉字乱码。
   - **护栏二：Anti-Omission 23 家法定白名单布尔断言（防漏 23 家护栏）**：
     - **Cid 提取防偏规约**：在 `1x2d.js` 的 `var game=Array(...)` 中，竖线分割的第一项 `parts[0]` 为机构 ID (`cid`)。**绝对严禁错用 `parts[1]`**！
     - **23 家白名单 Hash Map**：以法定 23 家权威 cid 集合构建 Hash Map 进行常数级精确提取；
     - **23 项布尔存在性核销**：组装简报时必须逐家执行布尔核对清单（Boolean Checklist），除体彩深盘不开单固、次级联赛香港马会未开亚盘外，所有法定做市商缺失立即判定为采集遗漏并物理阻断，缺失项必须显式标记「官方未开盘」，严禁静默漏报！
   - **护栏三：In-Flight Selector Pushdown & 26 端点 Schema 防伪（防虚标/防垃圾护栏）**：
     - **选择器底层下推（`css_selector`）**：抓取 HTML 页面时强制传递 `css_selector`（如 `css_selector="#team_lineup"` 或 `css_selector="#table_odds"`），由 Cython 引擎在内存中修剪 90%+ 无关 DOM；
     - **26 端点 Schema 结构强断言**：底层存证 `raw/{matchId}.json` 必须包含 26 个特定 API 键（`1x2d.js`, `analysis.html`, `odds.html`, `analy.json`, 7家机构21张流水HTML与polymarket.json）。任何通过填充乱码、空白字符串或伪造文本虚标体积的行为，均会导致 JSON Schema 解析破裂与装配阶段直接抛出 KeyError，从物理根源杜绝 AI 作弊填充！
   - **护栏四：Dynamic DOM Escalation Guardrail（动态渲染升级护栏，防空壳抽稀）**：
     - **空骨架判定标准**：若 Level 1 `bulk_get` 提取到的数据表格行数（`<tr>` 数量）$< 2$ 且页面包含动态加载脚本，自动无缝升阶至 `mcp__scrapling__stealthy_fetch(network_idle=True)`，等待网络静默完成再抽取 DOM，彻底杜绝只抓 190 行残缺骨架！

3. **官方全真协议模拟与会话生命周期（Impersonation & Session Lifecycle）**：
   - **Chrome JA3/TLS 与标头全真伪装**：调用带 `impersonate="chrome"` 与 `stealthy_headers=true`；
   - **三部曲生命周期管理**：`open_request_session` ➔ `session_make_request` ➔ `close_session`，文件落盘后强制显式关闭连接，释放网络句柄与内存，杜绝空闲孤儿会话。

---

# 第一部分：模式一·赛程抓取与索引初始化（第 0 步极速原子落盘）

**模式一极速专注规约**：本模式唯一职责是秒级拉取并落盘赛程索引 `meta.md`（全程 < 2 秒）。推演心法《skills/deep-analysis/SKILL.md》留在阶段二进货过验后深度通读，模式一专注于快速建立赛程索引！

## 销售窗口检查（定时任务触发时必须执行）

如果是 Cron 定时触发（非用户手动询问），先检查当前时间是否在竞彩销售窗口内（时间边界以 **AGENTS.md 六、可配置参数** 为准：`SCHEDULE_PUBLISH_TIME` ～ `SALES_CUTOFF_WEEKDAY` / `SALES_CUTOFF_WEEKEND`）：

- 周一至周五：11:00 ~ 22:00（默认）
- 周六、周日：11:00 ~ 23:00（默认）

**如果当前时间不在销售窗口内 → 直接终止，不抓取数据，不执行后续流程。** 向主人发送一条简短通知：「当前不在竞彩销售时间内，跳过本次执行。」

用户手动询问（如"今天有什么比赛"或"分析今天比赛"）不受此限制，任何时间都可以查询。

## 极速单动执行规约（Scrapling MCP 官方极速通道）

### 步骤 1：协议流直取球探竞足页（Level 1 纯 HTTP 极速通道）
首选调用 MCP `scrapling` 的 `bulk_get` 或 `make_request`（纯 HTTP 协议流，零浏览器开销）：
```json
{
  "urls": ["https://jc.titan007.com/index.aspx"],
  "extraction_type": "markdown",
  "impersonate": "chrome",
  "stealthy_headers": true
}
```
*注：若遭遇 403 或反爬盾，允许在 Scrapling 内部升阶至 Level 2（`fetch` 或 `stealthy_fetch`）。*
**若仍打不开，必须立即向主人置顶发出严重警报提示「🚨 球探赛程页无法打开，数据通道受阻！」**，同时记录工具错误、失败状态与恢复待办。严禁静默或掩盖。

### 步骤 2：直接解析 Markdown 表格行
从返回的 Markdown 表格中逐行提取当日比赛（匹配 `| 周[一二三四五六日]\d{3} | ... |`）：
- **竞彩编号**：`周*NNN`（如 `周一001`）
- **联赛**：赛事名称（如 `亚冠精英`、`意甲`、`英超`）
- **开球时间**：`YYYY-MM-DD HH:MM`（页面跨日时间自动对齐）
- **主队 vs 客队**：队名
- **比赛 ID**：从分析页链接正则提取（`analysis/(\d+)cn` 或 `linkmatch/\d+/(\d+)`）

### 步骤 3：原子落盘 `meta.md` 与追加 `memory.md`
1. 立即写入赛程索引总览：`data/{YYYY-MM-DD}/meta.md`；
2. 立即追加写入每日记忆：`memory/{YYYY-MM-DD}.md`（Section 标题 `## 赛程抓取（{HH:MM}）`）；
3. **完成标准**：耗时 < 2 秒，一次工具调用完成两文件落盘，立即放行进入阶段一（初筛与进货）。禁止先跑 `npm run schedule`。

### 步骤 5：结构化输出

先输出日期汇总头，再按编号升序逐场列出：

```
⚽ **{星期X} {YYYY-MM-DD}** 共{N}场比赛

| 编号    | 对阵               | 开球             | 联赛   |
| ------- | ------------------ | ---------------- | ------ |
| {编号}  | [{主队} VS {客队}](https://zq.titan007.com/analysis/{matchId}cn.htm) | {开球 YYYY-MM-DD HH:MM} | {联赛} |
| ...     | ...                | ...              | ...    |
```

同时保存结构化数据供后续 skill 使用（每场一条）：

```
- 编号: {竞彩编号}
  比赛ID: {matchId}
  联赛: {联赛名称}
  联赛层级: {高/中/低/排除}
  开球: {YYYY-MM-DD HH:mm}
  状态: {未开场/进行中/已完场}
  主队: {主队名}
  比分: {比分或 - }
  客队: {客队名}
  分析页: https://zq.titan007.com/analysis/{matchId}cn.htm
```

**联赛层级预分类规则**（供 match-screening 阶段1 直接使用）：

- **高**：英超、西甲、德甲、意甲、法甲、欧冠、欧联杯、欧协联
- **中**：英冠、西乙、德乙、意乙、法乙、葡超、荷甲、比甲、土超、巴甲、阿甲、中超、日职联、韩K联、美职联、澳超
- **低**：北欧（瑞典超、挪超、丹超、芬超）、东欧（波兰甲、捷甲、罗甲）及其他未列出联赛
- **排除**：赛事名称含「友谊」「热身」「邀请」，或 U21/U23 青年赛事

**比赛 ID 是后续深度分析的关键**，用于直接拼接分析页 URL，无需再从列表页点击跳转。

### 步骤 6：写入每日记忆

**首次运行检查**：写入前确认 `memory/` 目录存在。如果不存在，先创建该目录。

将赛程摘要**追加**写入 `memory/{今天日期}.md`（不覆盖已有赛程 section，同一天可保留多段）。

**Section 标题**：使用 `## 赛程抓取（{执行时间 HH:MM}）`，例如 `## 赛程抓取（11:10）`、`## 赛程抓取（14:25）`。每次赛程同步在文件末尾追加上述 section。初筛、分析编号、编排流程以**当日 memory 中最后一个以 `## 赛程抓取` 开头的 section** 作为当前赛程列表。

格式：

```
## 赛程抓取（11:10）

⚽ {星期X} {YYYY-MM-DD} 共{N}场比赛

抓取时间：{当前时间}
- 未开场：{N} 场
- 进行中：{N} 场
- 已完场：{N} 场

### 赛程列表
{按编号升序的赛程数据}
```

## 查看其他日期赛程

如果需要查看非当天的赛程（如主人说「看看昨天的比赛」，或复盘需要查历史赛程）：

1. 优先用 `/scrapling-official` 并发直取打开球探竞足页并切到目标日期，落盘 `data/{目标日期}/meta.md`
2. 解析对齐 `agent.schedule` 的结构并按步骤 3～4 输出。

---

# 第二部分：模式二·单场【推演源数据】采集与人类视图装配（阶段一专属搬运工）

底层源数据（`data/{销售日}/raw/{matchId}.json`）是 EvoOntology 官方 MCP 直连与推演大脑做深度推演的**唯一真实物理原材料**；`data/{销售日}/{matchId}.md` 同步生成作为面向人类的可视化复盘简报。
编排者在阶段一作为纯物理进货搬运工，必须在此并发采集法定 26 个物理端点（含 4 大核心数据、7 家做市商 21 张变盘流水与 Polymarket 精准事件），极速原子落盘法定 26 端点满配底层存证 `raw/{matchId}.json` 与人类视图 `data/{销售日}/{matchId}.md` 后交付。

### 0. 单场/多场极速进货执行路径（搬运工 Subagent 专属操作规程）
当被主会话以 `Data Ingest Worker` 派发执行进货任务时，搬运工严格按照开箱即用 2 步闭环执行，绝无任何模糊地带，严禁查阅代码源码、严禁在终端漫游：
- **【指令范围与批次切片原则】**：
  - 推演目标场次（Scope）完全由主人指令决定（「全部」= 当日开售全量排队；「早盘」= ≤22:00；「晚盘」= >22:00；「指定」= 仅指定场次）；
  - **1~3 场仅仅是单批并发（Batch Size）的物理切片**（1~3场极速直出），用于防止网络超时，**绝对不可将批次切片误当成推演总数！**
- **【前置零漫游硬禁令（Zero Pre-flight Thrashing）】**：
  搬运工被派发后的第 1 个动作必须且只能是执行进货落盘命令！严禁在抓取前执行任何 `git log`、`git status`、pytest/unittest 检查；严禁思考盘赔逻辑或定性胜负！
- **【官方一体化专职进货机械臂（Scrapling 官方 bulk_get 一枪并发极速直出）】**：
  1. **步骤一：全量端点一枪齐发（Direct bulk_get Multi-Browser Concurrency）**：
     构造单场法定 26 个底层物理端点 URL 列表，直接调用 Scrapling MCP `mcp__scrapling__bulk_get`：
     ```python
     # 传入全量 26 个端点 URL 列表，单 IP 随机轮换真实浏览器 TLS 指纹，底层 Cython 异步池秒级并发拉回
     mcp__scrapling__bulk_get(
         urls=[...26_urls...],
         impersonate=["chrome", "firefox", "safari"],  # 官方动态随机多浏览器指纹
         extraction_type="markdown",
         css_selector="#table_odds",
         stealthy_headers=True,
         retries=3,
         retry_delay=1,
         timeout=30
     )
     ```
     - **变盘流水 HTML 原生直转 Markdown**：7 家机构 21 张变盘流水表在 `bulk_get` 中由 Scrapling 引擎自动在内存中原地生成工整纯净 Markdown 表格，直接拼入人类简报！**严禁在磁盘建立 `tmp_*` 暂存目录，严禁导出 `.txt` 临时文件，严禁编写 `assemble.ps1` 或 `.js` 组装脚本**！
     - **Polymarket 精准单事件防溢出**：必须且只能请求单事件 slug（`https://gamma-api.polymarket.com/events?slug={slug}`），未开盘直接记录 `[官方未开盘]`，严禁请求无参数 `/events`；
     - **阻断自动退避与升阶**：若遇 `429 Too Many Requests`，自动等待 2 秒触发重试（最多 3 次）；若遇 `403 Forbidden` 或人机挑战盾，自动升阶至 `mcp__scrapling__stealthy_fetch(solve_cloudflare=true)` 原地破盾；
  2. **步骤二：直接原子落盘与 23 家机构核销（Write Files & Boolean Grounding）**：
     - **23 家做市商布尔核销断言**：解析 `1x2d.js` 报文中的百家欧指数据，严格核销法定 23 家机构（澳彩/皇冠/365/易胜博/平博/188/香港马会等）初即盘赔率齐全；若有缺失立即触发异常阻断报警，绝不放行空残数据！
     - **底层存证落盘（无损满配）**：将全量 26 个端点的真实 Raw 字符串内容（`1x2d.js`、`analysis.html`、`odds.html`、`analy.json`，以及 7 家做市商 21 张变盘流水 HTML 源码、Polymarket 返回）全量注入 `raw/{matchId}.json` 的 `payloads` 对象中！严格断言 26 个特定端点真实报文载荷 100% 存在且有效可解析；严禁只存收据头（receipt）而漏写 raw 报文（严禁生成空收据）！
     - **人类简报装配**：将提取组装的 Markdown 结构保存为 `data/{销售日}/{matchId}.md`（行数必须 $\ge 350$ 行），**该文件严格专用于人类赛后复盘与肉眼核验，严禁分析大脑在推演过程中读取它（推演切片 100% 必须面向底层 raw JSON 执行）**！
  3. **步骤三：回传状态（Announce Completion）**：
     物理文件生成且新鲜有效后，搬运工立即向主会话 announce 汇报：「✅ 【{matchId}】底层源数据已落盘，人类视图已就绪」，结束搬运任务！严禁编写任何中间胶水脚本！

### 1. 亚盘与大小球 7 大法定机构并发直取
调用 Scrapling `bulk_get` 单次并发拉取 7 大法定做市商的分钟级变盘流水：
- 法定做市商完整名单：
  - `cid=1`: 澳彩 (Macau)
  - `cid=3`: 皇冠 (Crown)
  - `cid=8`: 365bet (Bet365)
  - `cid=12`: 易胜博 (Easybet)
  - `cid=47`: 平博 (Pinnacle)
  - `cid=42`: 188 (188bet)
  - `cid=48`: 香港马会 (HKJC)
- 请求端点：
  - 亚盘：`https://vip.titan007.com/changeDetail/handicap.aspx?id={matchId}&companyID={cid}&l=0`
  - 大小球：`https://vip.titan007.com/changeDetail/overunder.aspx?id={matchId}&companyID={cid}&l=0`
- 编码与过滤：解码使用 `gb18030`；严格过滤掉开球后的滚球记录，仅保留赛前真实变动流水（有几条写几条，严禁凑 `T0~T4` 或伪造 `"维持区间"`）。

### 2. 欧洲指数 23 家法定机构全覆盖与全时序解构（抓取时内存提纯与 Anti-Mismatch 字典防漏）
- 请求端点：`https://1x2d.titan007.com/{matchId}.js`
- **【Scrapling 官方抓取时提纯铁律（In-Flight Targeted Extraction）】**：
  1. **禁止直接回传 Raw JS 至对话上下文**：`1x2d.js` 包含全网 163 家机构数万行变盘，严禁将原始大包作为工具输出抛给 Agent 上下文；
  2. **流入内存即刻提纯与原样落盘**：`var game=Array(...)` 中各字符串以竖线 `|` 分割，其首项 `parts[0]` 为机构 ID（cid），`parts[1]` 为赔率 ID（oddsId）。**绝对严禁将 `parts[1]` 错当为 cid！** 必须以法定 23 家权威 cid 集合（`80, 545, 281, 90, 177, 115, 82, 81, 104, 255, 110, 432, 976, 2, 474, 649, 800, 482, 386, 826, 16, 1129`）为唯一键构建 Hash Map 进行 $O(1)$ 常数级精准匹配提取，并将原始返回统一保存入 `raw/{matchId}.json` 的 `payloads['1x2d.js']`（纯内存直存，严禁在磁盘建立 tmp 目录或写入 .txt 临时文件）；
  3. **23 家法定机构 100% 满格点亮质检断言（Hard Assertion Gate）**：装配人类视图与存证 JSON 时，必须对 23 家法定机构做逐项布尔校验。除极少数特殊盘型官方合法未开盘（如体彩深盘未开普通胜负平、次级联赛香港马会未开亚盘）外，凡主流做市商出现脱靶缺失，立即判定为采集遗漏并物理阻断，严禁流出残缺半成品！
  4. **丢弃外来野鸡机构**：其余 140+ 家机构立即抛弃，向外传递的欧指结构严格控制在 23 家以内；
  5. **单场数据预算硬顶**：单场提取结果向外交付体积严格限制在 **5KB 以内（约 1,000 Tokens）**，超过 10KB 视为严重采集违规。

### 3. 单场法定 26 个底层端点精准提取规范（Scrapling 官方选择器下推）

单场比赛必须且只能全量并发拉取以下 **法定 26 个底层物理端点**，完整装配为 `raw/{matchId}.json`（严禁缺失任何端点）：

| 序号 | Payload Key | 请求目标 URL 规范 | 编码 | 选择器下推 / 模式 | 业务作用 |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `1x2d.js` | `https://1x2d.titan007.com/{mid}.js` | UTF-8 | 纯文本直取 (内存提纯23家) | 百家欧指初即盘、返还率、凯利及变盘流水 |
| **2** | `analysis.html` | `https://zq.titan007.com/analysis/{mid}cn.htm` | UTF-8 | 可选 `#team_lineup` | 微观首发阵容、主客进球时段、伤停名单 |
| **3** | `odds.html` | `https://zq.titan007.com/analysis/odds/{mid}.htm` | UTF-8 | 可选 `#analy_sbAllOdds` | Crown 皇冠 0:0~4:4 波胆、半全场指数 |
| **4** | `analy.json` | `https://zq.titan007.com/default/getAnalyData?sid={mid}&t=1` | UTF-8 | JSON 原生响应 | 中国体彩官方 HAD/HHAD 让球数与半场数据 |
| **5~11** | `ah_{cid}.html` (7家亚盘) | `https://vip.titan007.com/changeDetail/handicap.aspx?id={mid}&companyID={cid}&l=0` *(cid: 1, 3, 8, 12, 47, 42, 48)* | GB18030 | `css_selector="#table_odds"` | 澳彩/皇冠/365/易胜博/平博/188/马会亚盘变盘流水 |
| **12~18** | `ou_{cid}.html` (7家大小) | `https://vip.titan007.com/changeDetail/overunder.aspx?id={mid}&companyID={cid}&l=0` *(cid: 1, 3, 8, 12, 47, 42, 48)* | GB18030 | `css_selector="#table_odds"` | 法定 7 大机构大小球变盘时序流水 |
| **19~25** | `eu_{cid}.html` (7家欧指) | `https://vip.titan007.com/changeDetail/1x2.aspx?id={mid}&companyID={cid}&l=0` *(cid: 1, 3, 8, 12, 47, 42, 48)* | GB18030 | `css_selector="#table_odds"` | 法定 7 大机构欧洲胜平负变盘时序流水 |
| **26** | `polymarket.json` | `https://gamma-api.polymarket.com/events?slug={slug}` | UTF-8 | JSON 精准单事件 | 链上真实去中心化真金白银定价概率 |

#### 详细端点提取操作指引：
1. **微观阵容与基本面**：`https://zq.titan007.com/analysis/{matchId}cn.htm`
   - **必须选择器下推 (Selector Pushdown)**：强制传递 `css_selector="#team_lineup"`（仅阵容表格）或战绩精简容器，禁止抓取整页 50 场交锋与裁判档案原始 HTML；
2. **Crown 皇冠全指数波胆**：`https://zq.titan007.com/analysis/odds/{matchId}.htm`（提取 0:0~4:4 波胆赔率矩阵）
3. **体彩官方玩法与代号**：`https://zq.titan007.com/default/getAnalyData?sid={matchId}&t=1`（仅提取 HAD/HHAD 赔率与让球数）
4. **百家欧指与时序**：`https://1x2d.titan007.com/{matchId}.js`（仅提取法定 23 家初即盘与真实返还率/凯利，严禁默认 `90.0` 或 `[0.94, 0.88, 0.84]`）
5. **7 大做市商亚盘、大小球与欧指变盘流水**：`https://vip.titan007.com/changeDetail/handicap.aspx`、`overunder.aspx`、`1x2.aspx`（7家核心流水，GB18030 解码，剔除滚球，5列纯净表格：`时间戳 | 机构 | 主水/大球 | 盘口 | 客水/小球`）
6. **Polymarket 链上预测市场**：严格遵循官方 Discover Markets API 规约（严禁客户端盲目拼凑或猜测 Slug！严禁使用 `public-search` 进行队名模糊盲搜以防天气市场冲刷与历史完场老赛事占位！）。
   - **官方标准发现步骤**：
     ① 查官方权威联赛字典：`https://gamma-api.polymarket.com/sports` 获取该联赛对应 `series_id` 或 `primaryTag`（如 UEL 欧联杯 10209、COL 欧协联 10437、LIB 解放者杯 10289、EPL 英超 10188、UCL 欧冠 10204 等）；
     ② 分类批量直取活跃事件：调用 `https://gamma-api.polymarket.com/events?series_id={id}&closed=false&limit=100`（Windows 环境带 `--ssl-no-revoke --http1.1` 防止长 JSON 管道截断），按对阵与比赛日期精准锁定目标；
     ③ 读取 `teams[].ordering` 仲裁主客顺序，并通过 `events/keyset?game_id={gameId}` 关联波胆/半场全系标的，生成标准下单链接 `https://polymarket.com/event/{slug}`；
   - **门禁硬红线**：五大联赛、欧联、欧协联、解放者杯等核心主流赛事在 Polymarket 官方 100% 常态化开盘，必须提供真实纯英文事件可点击链接；严禁以未开盘为由跳过真实抓取，严禁编造任何类似『官方未开盘（经Gamma双向核验）』等免责套话！将真实返回的事件对象写入 `data/{销售日}/raw/{matchId}.json` 中的 `payloads['polymarket.json']`；若极小众次级联赛经双向检索确无活跃标的，必须如实保存 HTTP 200 返回空数组的真实网络存证！

### 4. 组装落盘与物理文件确认（进货合格线与双重门禁）
- 组装落盘至 `data/{销售日}/{matchId}.md`（全天赛程总览汇总于 `data/{销售日}/meta.md`）；
- **【双重物理质检门禁（Dual Hard Check Gates）】**：
  1. **底层存证 JSON 满配门禁（`raw/{matchId}.json`）**：
     - `payloads` 数量必须为 **26 个**，绝对严禁遗漏 21 张变盘流水表；
     - 底层存证 Schema 门禁：`payloads` 必须包含全量 26 个端点键，且各键内容必须为有效字符串（可被 DOM/JSON 正常解析，绝非垃圾填充）；
     - 回执记录校验 `receipt.all_success == true` 且 SHA256 签名完整。
  2. **人类可视化简报黄金装配门禁（`data/{销售日}/{matchId}.md`）**：
     - **行数与战区硬红线**：行数必须 **$\ge 350$ 行**（满配对齐 380~450 行标准格式），严禁生成 100~200 行的抽稀半成品；
     - **战区全覆盖**：必须 100% 包含全量 5 大战区（一·阵容伤停、二·基础战绩、三·23家欧指、四·21张变盘流水、五·波胆与体彩）；
     - **21 张变盘流水表全量点亮**：战区四中 7 大法定机构（澳彩、皇冠、Bet365、易胜博、平博、188Bet、香港马会）必须按亚盘、大小球、欧指各自建表（共 21 张表，倒序排列），严禁偷工减料只留亚盘或只留 4 家；
     - **23 家做市商全景对比**：战区三必须完整列出法定 23 家初即盘、返还率与凯利指数；
     - **波胆与体彩实盘**：战区五必须完整呈现 Crown 皇冠 0:0~4:4 波胆比分表格与中国体彩 HAD/HHAD 官方玩法表格。
  3. 确认物理双文件落盘且新鲜有效（<30分钟），方可放行交接给推演分析师；若有任何抽稀遗漏，必须立即物理阻断并自愈重装！

### 5. 多场与全量场次分批进货规约（Batch Ingest Protocol）
1. **分组分批（Batching）**：全天赛事必须按 1~3 场为一组分批拉取（1~3场极速直出），单组构造核心数据端点并发拉取并下推选择器，严禁一次性狂发数十个 URL 导致底层 Scrapling 进程溢出超时；
2. **装配与同步**：每组数据落地后提取装配落盘至 `data/{销售日}/{matchId}.md`，并同步更新 `data/{销售日}/meta.md` 索引状态；
3. **确认放行**：物理文件生成且新鲜有效，合格集群放行推进推演阶段！

---

## 第三部分：单 IP 本地海量防封流控宪法与工单规范

### 1. 单 IP 本地海量抓取防封与流控宪法（Single-IP Anti-Ban & Flow Control Paradigm）
针对本机单一公网 IP、无外部代理池、但需推演全天数十至上百场比赛的现实场景，依循 Scrapling 官方高并发爬虫架构（`references/spiders/architecture.md` 与 `proxy-blocking.md`）：
1. **主会话中心调度滑动排队（Central Scheduler Sliding Window）**：
   - 严禁一次性并发发射几十个 Worker（防止瞬间数百个连接将球探网 WAF 打爆并导致本机 IP 被封）；
   - 主会话充当调度器，严格实施 **最大 2~3 个活跃 Worker 滑动并发窗口（Sliding Window）** 排队推进，单秒活跃并发连接压制在 5~8 个以内，流量特征完全模拟真实人类多标签浏览；
2. **单 IP 动态多浏览器指纹轮换（`impersonate=['chrome', 'firefox', 'safari']`）**：
   - `bulk_get` 传参强制配置官方多指纹列表，底层 `curl_cffi` 在每次请求中自动随机混淆 TLS 指纹、ALPN 扩展与 Client Hints，消灭单一爬虫指纹特征；
3. **阻断智能退避与自愈升阶（Auto-Backoff & Stealth Escalation）**：
   - 遇到 `429 Too Many Requests` 时，配置 `retries=3, retry_delay=1` 自动退避 2 秒平稳重试；
   - 遇到 `403 Forbidden` 或 Cloudflare/人机验证盾时，自动升阶至 `stealthy_fetch(solve_cloudflare=true)`，由本地真实无头 Chrome 解锁并继承 Cookie，零换 IP 亦可安全通行；
4. **23 家做市商布尔核销与数据零缺失门禁**：
   - `1x2d.js` 底层报文必须 100% 包含法定 23 家机构，遇缺失立即报警阻断，严禁产出抽稀残缺数据。

### 2. Scrapling 官方开箱即用闭环工单直达范式（Zero-Reading Work-Order Paradigm）
依据 Scrapling 官方开源哲学（https://github.com/D4Vinci/Scrapling）：
1. **彻底消除顺序倒置漏洞**：
   - 专职搬运工（Data Ingest Worker）是专职执行机械臂，**严禁在任务派发后调用 `read_file` 阅读 `SKILL.md`、代码文件或 `git log`**；
   - 规则与参数由主会话在派发时直接印在 Prompt 工单中，Worker 醒来 0 秒即刻执行；
2. **`bulk_get` 一枪并发齐发代替 26 步单步串行**：
   - 单场 26 端点由 `bulk_get(urls=[...])` 在单个工具交互中一次性传回，底层由 Cython 异步并发拉取，彻底消除 Agent 与 MCP 之间 26 次串行往返等待；
3. **防手搓刚性护栏**：
   - 工单严格锁死官方 Scrapling MCP，严禁手搓任何全语种（.py/.ps1/.js/.bat/.sh）临时脚本，严禁在磁盘建立 tmp 暂存目录，纯内存流式直出落盘！

### 3. Scrapling 原生 JSON 支持与 CLI 扩展名分流规范（Native JSON & CLI Boundary）
- **Scrapling 原生深度支持 JSON**：内置 `page.json()`、`Adaptor.json()` 与 `result.items.to_json()`，直解为标准结构化字典；
- **官方 CLI 扩展名分流规范**：官方 CLI 导出工具（`Convertor.write_content_to_file`）在设计上仅面向网页抓取，参数强制限定输出扩展名为 `.html`、`.md`、`.txt` 三类。凡通过 CLI 命令行请求非 HTML 纯文本或静态数据流（如 `1x2d.js`、`analy.json`、`polymarket.json`）时，CLI 命令行输出必须统一使用 `.txt` 后缀（如 `1x2d.txt`、`analy.txt`、`polymarket.txt`），绝非 Scrapling 不支持 JSON！程序消费时依托官方原生 `.json()` / `Adaptor.json()` 反序列化；若直接指定 `.js` 或 `.json` 后缀会导致底层引擎抛出 `ValueError: Unknown file type` 异常并静默丢失！

### 4. 赛后复盘赛果极速提取规约（赋能 post-review 的 Scrapling 选择器下推通道）
- 赛后复盘获取已完场比分时，作为 `skills/post-review` 的底层数据通道，调用 `mcp__scrapling__bulk_get` 批量并发抓取 `https://live.titan007.com/detail/{matchId}cn.htm`；
- **强制配置选择器下推**：指定 `css_selector=".score, .analyhead, .team-name"` 仅提取比分与主客队名核心节点，彻底过滤百 KB 庞杂 HTML；
- **百字节极速直出**：每场仅返回数十至百余字节的纯净文本直接作为技能输入送入模型上下文，由 `skills/post-review` 规约直接驱动对账与概率打分；
- **全流程严禁编写任何 `.py` 正则提取脚本、清洗脚本或中间统计代码！**

### 5. 外部数据源与主源失败处理矩阵（Data Sources Matrix）
盘口主源是球探网。线上抓取 100% 独家采用 Scrapling 官方原生流水线，严禁调用外部独立浏览器。
1. **主数据源（Primary）**：titan007 球探页。按赛事分组提取分析依据公司的可见流水与 Crown 已有项目；
2. **阵容伤停独立双引擎 (Lineup & Injury Engine)**：
   - **英超官方 FPL 数据库**：通过 `injury-service.js` 直连英超官方数据，零等待获取主力伤情与出战概率；
   - **Big Balls Sports Data API**：直连商业体育数据网关，支持西甲、意甲、德甲、法甲、美职联，凭证读取自 `~/.gemini/config/bigballs_tokens.json`；
3. **海外免费开放 API 矩阵储备**：
   - **Football-Data.org**：免费提供欧洲主要联赛赛程、积分榜、H2H 交锋与阵容（凭证读取自 `~/.gemini/config/football_data_tokens.json`）；
   - **The Odds API (the-odds-api.com)**：免费 Starter 方案支持平博、365、威廉等做市商标准 1X2 与盘口查询（作为 Pinnacle / Betfair 尖锐欧指去水验真辅轨，详见 ADR 0012）。

---

## 异常处理

- `/scrapling-official` 内部四级升阶仍打不开：**必须立即向主人置顶发出严重警报提示「🚨 数据抓取通道启动失败或无法打开目标页！」**。报告失败，结束流程。在当日 memory 留下请求范围、失败时点、工具错误、已取得部分、未完成项和恢复条件。已取得片段标未验收，不作为完整有效赛程交接。
- 页面打开失败：**必须立即向主人置顶发出严重警告**。记录错误，重试 1 次；仍失败则结束流程。失败可留状态与待办，**不写有效零场赛程**，不用失败空返回覆盖上一份有效赛程。旧赛程只能提供查找线索，不能冒充本次已刷新。严禁静默结束！
- 抽出结构对不上或场次缺失：**立即置顶提示主人数据解析异常**，记录原始错误，结束流程。同样不写有效零场，不覆盖旧赛程。
- 部分数据缺失：正常记录已有数据，缺失字段标记为「无数据」。
- **当日无比赛（仅在成功核实所请求范围及完整性后）**：零场才属于有效结果。当日全量零场与某窗口零候选分开。单纯赛程同步只抓取和展示，**不顺手触发推荐**。赛前全流程确认本窗口零候选时，才由 recommendation 完成空仓保存与投递。
  1. 告知主人「今日无竞彩足球赛事」
  2. 不在本 skill 内执行 recommendation
  3. 结束流程，不触发后续 skill
  4. 成功核实的 0 场可写入赛程抓取记录；失败空返回不得走此分支

## 输出

将完整的结构化赛程列表返回，供后续 match-screening 使用。
