---
name: match-scraper
description: "从球探体育(titan007)抓取竞彩足球赛程数据与单场【推演源数据】。在用户说「抓取赛程」「获取今日比赛」「进货」「拉取推演源数据」或赛前分析阶段一进行推演源数据抓取与门禁质检时使用。"
metadata: { "emoji": "📆" }
---

# 赛程与推演源数据采集（match-scraper）

本技能包含两大工作模式：
- **模式一：赛程同步与索引初始化**（每日 11:10 或用户查询）：抓取当日竞彩足球全量赛程，落盘 `data/{YYYY-MM-DD}/meta.md` 并写入 memory。
- **模式二：【推演源数据】抓取与门禁质检**（赛前分析阶段一专属搬运工）：Scrapling MCP 并发秒取 5 大接口，通过 SnapshotAssembler 组装落盘为 `data/{销售日}/{matchId}.md`【推演源数据】，并运行 `cli.py` 门禁过验（exit 0）。

用 Skill `/scrapling-official` 并发抓取球探页面（`/browseros-neo` 备用辅助）。禁止先跑 `npm run schedule`。

## 前提条件

- 优先调用 Skill `/scrapling-official` ↔ MCP `scrapling`（协议流秒级抓取），`/browseros-neo` 作为真实渲染备用辅助。
- 严禁在根目录或任何位置自写临时 `.py` 脚本！
- 抓取赛程目标页面：`https://jc.titan007.com/index.aspx` 抽编号、比赛 ID、开球、对阵、分析页。
- 抓取推演源数据目标页面：单场 5 大数据源（分析页、波胆页、竞彩接口、1x2d.js、7家变盘流水）。
- 抓不到或场次不全：置顶报告，结束流程，不写残缺记录进 memory。
- **每次必须实时重新抓取**，不得复用之前抓取的旧数据。

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

1. 优先用 `/scrapling-official` 并发直取（或 `/browseros-neo` 备用辅助）打开球探竞足页并切到目标日期，落盘 `data/{目标日期}/meta.md`
2. 解析对齐 `agent.schedule` 的结构并按步骤 3～4 输出。

---

# 第二部分：模式二·单场【推演源数据】采集与门禁质检（阶段一专属搬运工）

【推演源数据】（`data/{销售日}/{matchId}.md`）是推演大脑（`deep-analysis`）做深度推演的**唯一真实物理原材料**，绝非事后可选备份日志！无新鲜源数据严禁下锅！
编排者在阶段一作为纯物理进货搬运工，必须在此并发采集 5 大数据源，组装落盘并通过门禁检验后方可交付。

### 0. 单场/多场极速进货执行路径（搬运工 Subagent 专属操作规程）
当被主会话以 `Data Ingest Worker` 派发执行进货任务时，搬运工必须严格按照以下极速 4 步走执行，严禁查阅无关技能、严禁动脑思考盘赔胜负：
- **【指令范围与批次切片原则】**：
  - 推演目标场次（Scope）完全由主人指令决定（「全部」= 当日开售全量排队；「早盘」= ≤22:00；「晚盘」= >22:00；「指定」= 仅指定场次）；
  - **4~6 场仅仅是单批并发（Batch Size）的物理切片**，用于防止网络超时，**绝对不可将批次切片误当成推演总数！**
- **【前置零漫游硬禁令（Zero Pre-flight Thrashing）】**：
  搬运工被派发后的第 1 个工具调用必须且只能是调用 MCP `scrapling` `bulk_get` 直取网络端点！严禁在抓取前执行任何 pytest/unittest/git diff 检查；必须按赛程编号（001~010）分批顺序推进，严禁擅自挑挑拣拣单抓单场，杜绝孤立切片假象！
1. **批次一：并发拉取 5 大主数据源**：
   调用 MCP `scrapling` `bulk_get` 一次性并发获取：分析页、Crown波胆、体彩HAD/HHAD、1x2d.js百家欧指；
2. **批次二：并发拉取 7 大法定做市商双盘流水**：
   调用 MCP `scrapling` `bulk_get` 一次性并发获取 7 家亚盘与 7 家大小球变盘流水（cid: 1, 3, 8, 12, 47, 42, 48）；
3. **批次三：并发拉取 Polymarket 活跃标的与链上价格（第 6 大法定接口）**：
   按官方 Discover-Markets 规范，优先调用 `https://gamma-api.polymarket.com/events/slug/{league}-{home3}-{away3}-{YYYY-MM-DD}` 瞬时直探；直探未命中时发起主队 `q={HomeTeamEn}` 与客队 `q={AwayTeamEn}` 双向搜索回退（**⚠️ 纯英文铁律**：Polymarket 数据库 100% 纯英文，严禁使用任何中文队名或中文联赛发请求，必须提取球探分析页 `#headTeam` 英文名或官方 3 字编码）。命中后提取 `slug`、撮合价格、`gameId`（用于伴生波胆/大小球盘口）与 `teams` 权威主客 `ordering`，拼接标准事件链接 `https://polymarket.com/event/{slug}`。
   **门禁硬红线**：主流核心联赛（英超/西甲/意甲/德甲/法甲/法乙/英冠/德乙/意乙/西乙/欧冠/欧联/欧协联/葡超/巴西甲/瑞典超/挪超/荷甲/美职联/亚冠）常态化活跃，门禁绝对禁止写未开盘；仅非核心冷门联赛经三阶真实检索确实无标的时，方准记录双向核验证据（如 `未开放（经Gamma双向核验q=Home与q=Away均无活跃标的）`）；
4. **法定确定性原子包直读装配与加密封印（零大模型转抄，含网络溯源回执）**：
   **绝对禁止大模型调用 `write_to_file` 或 `replace_file_content` 手写或修改 `data/{销售日}/{matchId}.md`，更严禁大模型在转抄 JSON 时截断变盘行或脑补体彩时间！** 搬运工将 Scrapling 抓取到的原始接口报文与网络溯源回执（包含 27 个端点 URL、HTTP 200 状态、字节长度、Server 头与 payload SHA-256）打包存为单文件 `data/{销售日}/raw/{matchId}.json`（彻底消灭28个散乱文件），在终端物理调用零转抄装配器：
   `python 校验/src/adapter/cli.py --assemble-bundle data/{销售日}/raw/{matchId}.json --output data/{销售日}/{matchId}.md`
   装配器由 Python 原生解析器（`Titan007RawParser`）100% 逐行原样直出 Verbatim Raw Wire Markdown（绝不漏掉任何一行变盘、绝不把 `早` 改成 `即`、绝不给缺失凯利填 `0.92`），并在 `raw/{matchId}.json` 内写入双重 SHA-256 加密封印（并自动清理旧版零散目录），同步调用 `python 校验/src/adapter/cli.py --sync-meta data/{销售日}` 更新索引状态！
5. **门禁过验与回传（防篡改、逐行溯源与回执三重死锁）**：
   终端物理运行 `python 校验/src/adapter/cli.py --match data/{销售日}/{matchId}.md --max-age-minutes 30`（支持 `--verify-network` 实网抽检，或批量安检 `--batch`）；
   - 门禁自动校验 `TAMPERED_MARKDOWN_SEAL`、`TAMPERED_RAW_WIRE_SEAL`、`RECEIPT_PAYLOAD_MISMATCH` 与 `RAW_PROVENANCE_MISMATCH`（逐行核对第 4 节亚盘/大小球/欧指流水行数、时间戳、水位、状态词 `早`/`即`/`初盘` 与 `raw/{matchId}.json` 原始报文及网络回执 100% 一致）；
   - 拿到 exit 0 (PASS) 后，立即向主会话 announce 汇报：「✅ 【{matchId}】推演源数据已确定性装配落盘并过验放行 (exit 0)」，结束阶段一。

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

- `/scrapling-official` 与 `/browseros-neo` 均打不开：**必须立即向主人置顶发出严重警报提示「🚨 数据抓取通道启动失败或无法打开目标页！」**。报告失败，结束流程。在当日 memory 留下请求范围、失败时点、工具错误、已取得部分、未完成项和恢复条件。已取得片段标未验收，不作为完整有效赛程交接。
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
