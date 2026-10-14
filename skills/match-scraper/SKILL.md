---
name: match-scraper
description: "从球探体育(titan007)抓取竞彩足球赛程数据与单场【推演源数据】。在用户说「抓取赛程」「获取今日比赛」「进货」「拉取推演源数据」或赛前分析阶段一进行推演源数据抓取与门禁质检时使用。"
metadata: { "emoji": "📆" }
---

# 赛程与推演源数据采集（match-scraper）

本技能包含两大工作模式：
- **模式一：赛程同步与索引初始化**（每日 11:10 或用户查询）：抓取当日竞彩足球全量赛程，落盘 `data/{YYYY-MM-DD}/meta.md` 并写入 memory。
- **模式二：【推演源数据】抓取与门禁质检**（赛前分析阶段一专属搬运工）：Scrapling MCP 并发秒取 5 大接口，通过 SnapshotAssembler 组装落盘为 `data/{销售日}/{matchId}.md`【推演源数据】，并运行 `cli.py` 门禁过验（exit 0）。

用 Skill `/scrapling-official` 官方原生流水线并发抓取球探页面。严禁调用外部独立浏览器（如 `browseros-neo`），禁止先跑 `npm run schedule`。

## 前提条件

- 数据进货 100% 独家归属 Skill `/scrapling-official` ↔ MCP `scrapling`（官方四级闭环）。严禁调用外部独立浏览器！
- 严禁在根目录或任何位置自写临时 `.py` 脚本！
- 抓取赛程目标页面：`https://jc.titan007.com/index.aspx` 抽编号、比赛 ID、开球、对阵、分析页。
- 抓取推演源数据目标页面：单场 5 大数据源（分析页、波胆页、竞彩接口、1x2d.js、7家变盘流水）。
- 抓不到或场次不全：置顶报告，结束流程，不写残缺记录进 memory。
- **每次必须实时重新抓取**，不得复用之前抓取的旧数据。

## Scrapling 官方防反爬隐身与智能自愈规约（Stealth & Adaptive Self-Healing）

为了确保系统永不被球探网风控与反爬 WAF 识别阻断，全流程进货必须严格贯彻官方原生隐身与自愈双核机制：

1. **全真隐身装配与网络协议锁（Stealth Engine & Protocol Lock）**：
   - **动态协议自协商（首选 H2 极速，异常动态退避 H1）**：首选 HTTP/2 极速多路复用流，享受最高并发性能；若遇源站 Nginx 抛出 HTTP/2 `PROTOCOL_ERROR` 或流重置，自适应引擎即刻无感自愈降级至 HTTP/1.1（`CurlHttpVersion.V1_1` 与 `--disable-http2`），兼顾现代极速与极端容灾；
   - **真实 TLS 指纹模拟**：优先调用 `StealthySession` 或 `impersonate="chrome"`（全真模拟最新 Chrome 协议特征与扩展套件，杜绝裸奔请求）；
   - **Canvas 动态加噪（`hide_canvas=True`）**：在渲染和图层计算中注入微扰随机噪声，从根源粉碎 WAF 针对 Canvas 画布指纹的聚类追踪；
   - **WebRTC 泄露封锁（`block_webrtc=True`）**：强制 WebRTC 遵循全局路由，绝对禁止本地局域网 IP 与真实出口 IP 被静默探测；
   - **显卡特征自洽（`allow_webgl=True`）**：维持完整 WebGL 上下文，彻底消灭无头浏览器（Headless）特征漏洞；
   - **拟真访问来源（上下文 Referer 拓扑映射）**：变盘流水端点绑定 `https://zq.titan007.com/analysis/odds/{mid}.htm`，百家欧指绑定 `https://titan007.com/`，内部子域禁用默认 `google_search` 覆盖，彻底消除外源异常流量特征。

2. **官方智能自愈与元素改版自适应（Adaptive Scraping & Element Memory）**：
   - **专属记忆库重定向（Project SQLite Storage）**：配置 `selector_config={"adaptive": True, "storage_args": {"storage_file": "data/scrapling_storage.db"}}`，将元素结构指纹统一持久化落盘至项目专属库，杜绝散落在环境包目录；
   - **语义唯一标识（Semantic Identifiers）**：为 7 大做市商时序端点绑定专属标识契约（亚盘 `ah_{cid}_table`、大小球 `ou_{cid}_table`、欧指 `eu_{cid}_table`），避免跨端点指纹覆盖；
   - **指纹记忆自动存储（`auto_save=True`）**：初次解析变盘流水表格时，自动将目标表格的几何拓扑与 DOM 结构指纹存入本地 SQLite；
   - **改版自动重定位（`adaptive=True`）**：当球探网前端改版、ID `#table_odds` 被删或 Class 名混淆时，Scrapling 依据 `identifier` 自动提取指纹并计算相似度，无感寻回正确表格节点；
   - **多级提取与标签兜底**：使用 `get_all_text()` 穿透提取包含全部子行子列的完整纯净文本，并配置 `page.relocate({"tag": "table", "text": "盘口"}, percentage=30)` 作为最终兜底防线。

3. **拟人化流量控制与会话保持（Autothrottle & Session Persistence）**：
   - **分块并发军规**：单批物理切片严格锁定 $\le 6\sim 8$ URLs；
   - **拟人随机抖动（Jitter）**：批次间隔执行 `0.3s ~ 0.65s` 动态随机抖动，彻底粉碎等间隔机械节拍特征；
   - **会话 Cookie 继承（Session Reuse）**：优先使用 `FetcherSession` / `StealthySession` 维持全局连接，继承主站鉴权 Cookie，杜绝离散探测嫌疑；
   - **智能指数退避**：遭遇网络抖动或偶发 HTTP 429 频控时，自动启动退避重试（退避间隔 1s、2s、4s），严禁高频硬冲引发 WAF 阻断。

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

### 步骤 1：协议流直取球探竞足页
调用 MCP `scrapling` 工具：
```json
{
  "url": "https://jc.titan007.com/index.aspx",
  "extraction_type": "markdown",
  "network_idle": true
}
```
**若打不开，必须立即向主人置顶发出严重警报提示「🚨 球探赛程页无法打开，数据通道受阻！」**，同时记录工具错误、失败状态与恢复待办。严禁静默或掩盖。

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

# 第二部分：模式二·单场【推演源数据】采集与门禁质检（阶段一专属搬运工）

【推演源数据】（`data/{销售日}/{matchId}.md`）是推演大脑（`deep-analysis`）做深度推演的**唯一真实物理原材料**，绝非事后可选备份日志！无新鲜源数据严禁下锅！
编排者在阶段一作为纯物理进货搬运工，必须在此并发采集 5 大数据源，组装落盘并通过门禁检验后方可交付。

### 0. 单场/多场极速进货执行路径（搬运工 Subagent 专属操作规程）
当被主会话以 `Data Ingest Worker` 派发执行进货任务时，搬运工严格按照开箱即用 2 步闭环执行，绝无任何模糊地带，严禁查阅代码源码、严禁在终端漫游：
- **【指令范围与批次切片原则】**：
  - 推演目标场次（Scope）完全由主人指令决定（「全部」= 当日开售全量排队；「早盘」= ≤22:00；「晚盘」= >22:00；「指定」= 仅指定场次）；
  - **4~6 场仅仅是单批并发（Batch Size）的物理切片**，用于防止网络超时，**绝对不可将批次切片误当成推演总数！**
- **【前置零漫游硬禁令（Zero Pre-flight Thrashing）】**：
  搬运工被派发后的第 1 个动作必须且只能是执行进货落盘命令！严禁在抓取前执行任何 `git log`、`git status`、pytest/unittest 检查；严禁思考盘赔逻辑或定性胜负！
- **【官方 Scrapling 原生纯净进货管道（Zero Ad-hoc Python 铁律）】**：
  1. **步骤 1：调用官方 Scrapling MCP `bulk_get` 并发直取（分块军规 ≤6~8 URLs + 选择器下推）**：
     直接调用官方 MCP 工具 `scrapling bulk_get`（`impersonate="chrome"`, `css_selector="table"`, `main_content_only=false`, `stealthy_headers=true`），按官方分块军规分 3~4 组并发直取 26 端点，将返回原始报文打包存入 `data/{销售日}/raw/{matchId}.json`，零手写爬虫脚本！
     - **【源站 WAF 阻断/断连三级脱困阶梯（Anti-Block Escalation）】**：
       ① 一级阶梯（默认）：`bulk_get` 必须显式携带 `impersonate="chrome"`，拟真最新 Chrome 浏览器 TLS 握手指纹；
       ② 二级阶梯（会话复用）：若源站频控或频繁断连，调用 `scrapling session_make_request` 复用同一会话连接池；
       ③ 三级阶梯（隐身脱困）：若遭遇强反爬拦截，单点调用 `scrapling stealthy_fetch`（全真模拟真实浏览器指纹）单点突破；
       ④ **【推演态零散脚本硬禁令（Zero-Script Iron Rule）】**：严禁主会话或搬运工在 `scratch/` 或任何目录创建任何 `.py` 临时脚本！所有异常排查唯一法定命令为 `python 校验/src/adapter/cli.py --diagnose-gate <file>`，违者直接视为严重违规！
  2. **步骤 2：调用现有法定离线装配器与门禁**：
     运行现成受测命令：
     `python 校验/src/adapter/cli.py --assemble-bundle data/{销售日}/raw/{matchId}.json --output data/{销售日}/{matchId}.md`
     `python 校验/src/adapter/cli.py --match data/{销售日}/{matchId}.md --max-age-minutes 30`
  3. **步骤 3：回传状态（Announce Completion）**：
     单场门禁 exit 0 (PASS) 拿到后，搬运工立即向主会话 announce 汇报：「✅ 【{matchId}】推演源数据已确定性装配落盘并过验放行 (exit 0)」，结束搬运任务！

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

### 2. 欧洲指数 23 家法定机构全覆盖与全时序解构（抓取时内存提纯，严禁 Raw Dump）
- 请求端点：`https://1x2d.titan007.com/{matchId}.js`
- **【Scrapling 官方抓取时提纯铁律（In-Flight Targeted Extraction）】**：
  1. **禁止直接回传 Raw JS 至对话上下文**：`1x2d.js` 包含全网 163 家机构数万行变盘，严禁将原始大包作为工具输出抛给 Agent 上下文；
  2. **流入内存即刻提纯与原样落盘**：使用预编译法定 23 家 ID 集合（`80, 545, 281, 90, 177, 115, 82, 81, 104, 255, 110, 432, 976, 2, 474, 649, 800, 482, 386, 826, 16, 1129`）与 `Titan007RawParser` 直取，并将原始返回存入 `raw/{matchId}/1x2d.js` 供门禁溯源比对；
  3. **丢弃外来野鸡机构**：其余 140+ 家机构立即抛弃，向外传递的欧指结构严格控制在 23 家以内；
  4. **单场数据预算硬顶**：单场提取结果向外交付体积严格限制在 **5KB 以内（约 1,000 Tokens）**，超过 10KB 视为严重采集违规。

### 3. 单场 5 大数据源抓取时精准提取规范（Scrapling 官方选择器下推）
1. **微观阵容与基本面**：`https://zq.titan007.com/analysis/{matchId}cn.htm`
   - **必须选择器下推 (Selector Pushdown)**：强制传递 `css_selector="#team_lineup"`（仅阵容表格）或战绩精简容器，禁止抓取整页 50 场交锋与裁判档案原始 HTML；
2. **Crown 皇冠全指数波胆**：`https://zq.titan007.com/analysis/odds/{matchId}.htm`（提取 0:0~4:4 波胆赔率矩阵）
3. **体彩官方玩法与代号**：`https://zq.titan007.com/default/getAnalyData?sid={matchId}&t=1`（仅提取 HAD/HHAD 赔率与让球数）
4. **百家欧指与时序**：`https://1x2d.titan007.com/{matchId}.js`（仅提取法定 23 家初即盘与真实返还率/凯利，严禁默认 `90.0` 或 `[0.94, 0.88, 0.84]`）
5. **7 大做市商亚盘与大小球流水**：`https://vip.titan007.com/changeDetail/handicap.aspx` 与 `overunder.aspx`（7家核心流水，GB18030 解码，剔除滚球，5列纯净表格：`时间戳 | 机构 | 主水/大球 | 盘口 | 客水/小球`）
6. **Polymarket 链上预测市场**：严格遵循官方 Discover Markets API 规约（严禁客户端拼凑/猜测 Slug！）。使用主队或客队官方英文名动态检索 Gamma API（`https://gamma-api.polymarket.com/public-search?q={HomeTeamEn}`），从返回 events 中核验对阵另一方与日期获取真实 `event.slug`、核验 `teams[].ordering` 主客顺序，并通过 `events/keyset?game_id={gameId}` 关联波胆/半场全系标的，生成标准下单链接 `https://polymarket.com/event/{slug}`。若已开盘提取挂单写入 `polymarket.json`；若经主客双向检索确无活跃标的，如实落盘双向核验凭据（`{"url": "官方未开盘（经Gamma双向核验均无对应链上预测标的）", "polymarketUrl": "官方未开盘（经Gamma双向核验均无对应链上预测标的）", "polymarketPrices": "官方未开盘"}`），严禁编造汉字或模板假 Slug！

### 4. 组装落盘与物理门禁核验（进货合格线）
- 通过 `python 校验/src/adapter/cli.py --assemble-bundle data/{销售日}/raw/{matchId}.json --output data/{销售日}/{matchId}.md` 组装落盘并生成 `raw/{matchId}.json` 加密封印（全天赛程总览汇总于 `data/{销售日}/meta.md`）；
- 执行门禁物理命令：
  - 单场核验：`python 校验/src/adapter/cli.py --match data/{销售日}/{matchId}.md --max-age-minutes 30`
  - 批量核验：`python 校验/src/adapter/cli.py --batch data/{销售日} --max-age-minutes 30 --isolate-failed`
- 若返回 `FAIL`（如法定做市商流水覆盖不足、缺少时序、字段错位、SHA-256 封印被篡改或与 `raw/{matchId}.json` 原文不符），物理熔断停止流程，必须重新从真实源装配并拿到 `exit 0` 后方可交接给推演分析师。

### 5. 多场与全量场次分批进货规约（Batch Ingest Protocol）
1. **分组分批（Batching）**：全天赛事（如13场或26场）必须按 4~6 场为一组分批拉取，单组构造 4~8 个核心数据端点并发拉取并下推选择器，严禁一次性狂发数十个 URL 导致底层 Scrapling 进程溢出超时；
2. **装配与同步**：每组数据落地后立即调用 `cli.py --assemble-bundle` 装配落盘至 `data/{销售日}/{matchId}.md`（同时落盘 `raw/{matchId}.json`），并调用 `cli.py --sync-meta data/{销售日}` 同步索引状态；
3. **故障隔离放行**：运行 `python 校验/src/adapter/cli.py --batch data/{销售日} --max-age-minutes 30 --isolate-failed`，异常场次自动移入 `.quarantine` 隔离区，合格集群放行推进推演阶段！

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
