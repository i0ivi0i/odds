## TOOLS.md - 工具使用指南

Skills 定义了工具的工作方式。此文件记录当前仓库中可用的数据抓取工具与命令。常用工具或者插件之类的"使用方法"得到更新或者技巧之后，也要在本文件进行记录更新。

---

## 核心系统：官方 Scrapling 原生数据采集体系（Skill scrapling-official ↔ MCP scrapling）

**绝对刚性红线（100% Scrapling 独家立宪与外部浏览器绝对红线）**：
1. **进货通道 100% 独家**：系统数据采集进货 100% 独家归属 **`Skill /scrapling-official` ↔ `MCP scrapling`** 官方原生流水线！
2. **严禁调用外部独立浏览器**：全流程绝对严禁在任何数据采集、赛程同步、变盘流水或页面抓取环节调用外部独立浏览器（如 `Skill /browseros-neo` ↔ `MCP browseros_neo`）！外部独立浏览器仅限主人亲自交互浏览，AI 在常规和异常业务流中绝对禁止擅自启动或降级调用！
3. **全流程严禁任何临时 `.py` 脚本、跑批脚本、数据清洗脚本、复盘对账脚本或 `python -c`！** 违者视为严重工程违规与作弊。
4. **【平台工具 `execute_code` 绝对硬锁禁令】**：全流程绝对严禁调用平台工具 `execute_code` 执行任何 Python 脚本代码！严禁借 `execute_code` 编写爬虫抓取逻辑、数据清洗或对账代码！数据获取必须且只能直接调用官方 MCP 工具（`mcp__scrapling__*`），推演查看必须且只能直接调用官方 MCP 工具（`mcp__evoontology__*`）。违反者视为严重违规越权！
5. **【Scrapling 官方零代码立宪（Zero-Custom-Script Law）】**：官方 D4Vinci/Scrapling 原生设计哲学为 "Without Writing Any Code"。系统进货 100% 独家依赖官方 Scrapling MCP 工具（`bulk_get`, `open_request_session`, `session_make_request`），直接利用原生 `extraction_type="markdown"` 直出纯净表格与结构。绝对严禁编写任何第三方 `.py` 解析器、手搓正则表达式或 Node 胶水脚本，杜绝开历史倒车与自研死锁！
6. **【Polymarket 链上单事件精准约束（Anti-Frame-Overflow Law）】**：调用 Polymarket Gamma API 时，必须且只能精准请求单事件唯一 slug（`https://gamma-api.polymarket.com/events?slug={slug}`），绝对严禁调用无参数 `/events` 大列表；单次返回体确保 $\le 10\text{KB}$；若未开盘直接在文件记录 `[官方未开盘]`，彻底根除 Antigravity MCP 协议栈 `JSON-RPC frame exceeded maximum line length` 溢出崩溃！
7. **【Scrapling 原生 JSON 支持与 CLI 扩展名分流规范（Native JSON & CLI Boundary）】**：Scrapling 框架**绝对原生深度支持 JSON**（内置 `page.json()`、`Adaptor.json()` 与 `result.items.to_json()`，直解为标准结构化字典）。需要严格区分的是官方 CLI 导出工具（`Convertor.write_content_to_file`）在设计上仅面向网页抓取，参数强制限定输出扩展名为 `.html`、`.md`、`.txt` 三类。凡通过 CLI 命令行请求非 HTML 纯文本或静态数据流（如 `1x2d.js`、`analy.json`、`polymarket.json`）时，CLI 命令行输出必须统一使用 `.txt` 后缀（如 `1x2d.txt`、`analy.txt`、`polymarket.txt`），绝非 Scrapling 不支持 JSON！程序消费时依托官方原生 `.json()` / `Adaptor.json()` 反序列化；若直接指定 `.js` 或 `.json` 后缀会导致底层引擎抛出 `ValueError: Unknown file type` 异常并静默丢失！
8. **【Scrapling 官方编码与二进制流保真军规（Raw Bytes & Encoding Protocol）】**：球探网二级变盘流水页面（`changeDetail/*.aspx`）为历史遗留的 `gb18030` 编码。必须严格依循 Scrapling 官方 `Selector(content, encoding='gb18030')` 与保留 `page.body`（原始二进制流）的设计规约，抓取或装配环节必须基于原始字节流显式以 `gb18030` 解码（如 `new TextDecoder('gb18030').decode(buf)`），绝对严禁在外部以默认 UTF-8 强行转换为字符串，彻底杜绝队名、盘口汉字乱码与正则脱靶！
9. **【法定 23 家做市商 Anti-Mismatch 字典防漏门禁（Bookmaker Hash Map Law）】**：在解析 `1x2d.js` 时，`var game=Array(...)` 中各字符串以竖线 `|` 分割，其首项 `parts[0]` 为做市商机构 ID（cid），而 `parts[1]` 为赔率 ID（oddsId）。系统必须且只能以法定 23 家权威 cid 集合为键构建 Hash Map 进行 $O(1)$ 常数级精准匹配提取，绝对禁止将 `parts[1]` 错当为 cid，绝对禁止通过线性索引偏移遍历！所有 23 家做市商必须 100% 逐项布尔对账，缺任何一家直接阻断报警！
10. **【Scrapling 官方四大原生护栏规约（Official 4 Native Guardrails）】**：
    - **护栏一：Anti-Mismatch Guardrail（防错防串）**：抓取前显式建立端点 URL 字典，返回批量数据时强制双向断言特征词（亚盘核对 `Crown 亚让/让球`、大小球核对 `高于/低于`、欧指核对 `百家做市/返还率`），杜绝跨市场数据串号或列数组偏移；二级流水页面依循 GB18030 二进制流原生保真解码；
    - **护栏二：Anti-Omission 23 家布尔断言（防漏 23 家）**：装配战区三欧指时，逐项布尔校验 23 家做市商（Boolean Checklist），除体彩深盘不开单固、次级联赛未开亚盘显式标记「官方未开盘」外，任何主流机构静默缺失直接判定为进货失败；
    - **护栏三：In-Flight Selector Pushdown & 26 端点 Schema 防伪（防塞垃圾伪造）**：HTML 页面底层下推 `css_selector` 在 Cython 引擎过滤 90%+ 噪声；底层存证 `raw/{matchId}.json` 强制校验 26 个特定 API 键（`1x2d.js`, `analysis.html`, `odds.html`, `analy.json`, 7家机构21张流水HTML与polymarket.json），塞乱码填充直接导致 Schema 破裂抛出异常，从根源杜绝 AI 伪造体积；
    - **护栏四：Dynamic DOM Escalation Guardrail（动态渲染升级，防空壳抽稀）**：若 Level 1 `bulk_get` 遇到客户端动态构建的空表格骨架（数据行数 $< 2$ 且含动态加载脚本），自动升阶至 `mcp__scrapling__stealthy_fetch(network_idle=True)`，等待网络静默再抽取 DOM，彻底杜绝只抓 190 行残缺骨架！
11. **【Scrapling 官方自适应指纹记忆边界（Adaptive Scraping vs Live Odds）】**：
    - **自适应记忆的物理本质**：官方自适应抓取通过 `auto_save=True` 记录元素 DOM 祖先结构和特征指纹（本地重定向至 `storage_args={"storage_file": "data/scrapling_storage.db"}`），开启 `adaptive=True` 可以在目标网页改版时依据相似度自动重定位元素（Auto-healing），杜绝选择器因样式变更报错；
    - **严禁当成赔率缓存**：**Adaptive 记忆的是 DOM 结构指纹，绝对不是赔率数字缓存！** 足球博弈赔率每分钟都在波动，每次分析必须实时重新并发获取活水数据，严禁借记忆偷懒复用旧盘口！

**Scrapling 官方两级分层进货架构与会话闭环军规（D4Vinci/Scrapling Native Specs）**：
依循官方原生分层理念，球探网纯静态服务端渲染接口与动态反爬接口严格分流：
- **Level 1（纯 HTTP 协议流，首选必选）**：毫秒级响应，零无头浏览器启动损耗。所有球探网静态数据（赛程列表 `index.aspx`、百家欧指 `1x2d.js`、变盘流水 `handicap.aspx`、微观阵容 `analysis/{id}cn.htm`）默认 100% 优先采用 `mcp__scrapling__bulk_get` 或 `session_make_request`，开启 `impersonate="chrome"` 与 `stealthy_headers=true`（单批切片 $\le 6\sim 8$ URLs，前置下推选择器 `css_selector="#table_odds"`）；
- **Level 2（Playwright 无头浏览器，升阶容灾）**：仅在 Level 1 返回 HTTP 403/503 或源站下发 Cloudflare Turnstile 等动态人机挑战盾时，在 Scrapling 内部升阶至 `mcp__scrapling__stealthy_fetch`。静态数据严禁无故直接调用 Level 2 浏览器！
- **官方会话生命周期闭环（强制）**：长连接进货调用 `open_request_session` 创建会话 ➔ `session_make_request` 并发拉取 ➔ 文件确认落盘后**强制调用 `close_session(session_id=...)` 显式销毁连接句柄**，杜绝后台空闲资源泄漏！

- **阶段 0：赛程索引确定性自检与 Scrapling 极速直落（Zero-State Hard Lock）**：
  - 凡触发赛前分析、赛程同步或手动推演，大模型唤醒后**第 0 秒第一工具动作**必须且只能先检查 `data/{销售日}/meta.md` 是否存在且新鲜（< 2小时）；
  - 若缺失或超期，首选调用 Level 1 协议流 `mcp__scrapling__bulk_get(urls=["https://jc.titan007.com/index.aspx"], extraction_type="markdown", impersonate="chrome", stealthy_headers=true)`（遇 403 升阶至 `fetch`）秒级提取全天场次 ➔ 原子落盘 `data/{销售日}/meta.md` 与追加 `memory/{销售日}.md`（全程 < 2 秒）；
  - **严禁漫游翻书铁律**：在 `data/{销售日}/meta.md` 确立前，绝对禁止阅读 `skills/deep-analysis` 技能、绝对禁止查看任何 Python 源码、绝对禁止思考盘赔逻辑！
- **批量赛事分批并发矩阵与进货门禁规约（First-Action Batch Matrix）**：
  - 赛程索引就绪后，由主人指令锁定推演范围（全部/早盘/晚盘/指定，严禁任何 AI 将分批大小当成推演总数！）；
  - 构造候选场次分批矩阵（严格按 4~6 场为一组 Batch、4~8 URLs 协议流并发 + 选择器下推），调用 `mcp__scrapling__bulk_get` 分批秒取数据；
  - **法定装配落盘与物理清空重抓**：专职搬运工直接通过 Scrapling MCP 并发拉取 26 端点与 Polymarket 解析，装配落盘至 `data/{销售日}/{matchId}.md`（同时落盘 `raw/{matchId}.json` 原子存证包）；**严禁大模型手动拼接 Markdown 避免封条失真！凡触发重新推演，第一动作绝对强制物理清空旧快照，严禁在旧文件上用 replace_file_content 局部打补丁改时间作弊伪造活水！**
  - 严禁单场串行磨洋工，严禁单批超载倾倒，未见快照物理落盘且新鲜有效（<30分钟）前，绝对禁止开脑推演！
- **主力全包引擎：Skill `/scrapling-official` ↔ MCP `scrapling`（法定 26 端点无损原子存证矩阵）**：
  - 原生集成 Chrome 136+ TLS 指纹伪装与抗封锁能力，单场比赛必须且只能全量并发拉取以下 **法定 26 个底层物理端点**，完整装配为 `raw/{matchId}.json`（严禁缺失任何端点）：
| 序号 | Payload Key | 请求目标 URL 规范 | 编码 | 选择器下推 / 模式 | 业务作用 |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **1** | `1x2d.js` | `https://1x2d.titan007.com/{mid}.js` | UTF-8 | 纯文本直取 (内存提纯23家) | 百家欧指初即盘、返还率、凯利及变盘流水 |
| **2** | `analysis.html` | `https://zq.titan007.com/analysis/{mid}cn.htm` | UTF-8 | 可选 `#team_lineup` | 微观首发阵容、主客进球时段、伤停名单 |
| **3** | `odds.html` | `https://zq.titan007.com/analysis/odds/{mid}.htm` | UTF-8 | 可选 `#analy_sbAllOdds` | Crown 皇冠 0:0~4:4 波胆、半全场指数 |
| **4** | `analy.json` | `https://zq.titan007.com/default/getAnalyData?sid={mid}&t=1` | UTF-8 | JSON 原生响应 | 中国体彩官方 HAD/HHAD 让球数与半场数据 |
| **5~11** | `ah_{cid}.html` (7家亚盘) | `https://vip.titan007.com/changeDetail/handicap.aspx?id={mid}&companyID={cid}&l=0` *(cid: 1, 3, 8, 12, 47, 42, 48)* | GB18030 | `css_selector="#table_odds"` | 澳彩/皇冠/365/易胜博/平博/188/马会亚盘变盘流水 |
| **12~18** | `ou_{cid}.html` (7家大小) | `https://vip.titan007.com/changeDetail/overunder.aspx?id={mid}&companyID={cid}&l=0` *(cid: 1, 3, 8, 12, 47, 42, 48)* | GB18030 | `css_selector="#table_odds"` | 法定 7 大机构大小球变盘时序流水 |
| **19~25** | `eu_{cid}.html` (7家欧指) | `https://vip.titan007.com/changeDetail/1x2.aspx?id={mid}&companyID={cid}&l=0` *(cid: 1, 3, 8, 12, 47, 42, 48)* | GB18030 | `css_selector="#table_odds"` | 法定 7 大机构欧洲胜平负变盘时序流水 |
| **26** | `polymarket.json` | `https://gamma-api.polymarket.com/events?slug={slug}` | UTF-8 | JSON 精准单事件 | 链上真实去中心化真金白银定价概率 |
  - **常规与异常流程 100% 由 Scrapling 官方内部四级闭环极速完成，严禁启动外部独立浏览器！**
- **赛后复盘赛果极速提取规约（赋能 skills/post-review 的 Scrapling 选择器下推通道）**：
  - 赛后复盘获取已完场比分时，作为 `skills/post-review` 的底层数据通道，调用 `mcp__scrapling__bulk_get` 批量并发抓取 `https://live.titan007.com/detail/{matchId}cn.htm`；
  - **强制配置选择器下推**：指定 `css_selector=".score, .analyhead, .team-name"` 仅提取比分与主客队名核心节点，彻底过滤百 KB 庞杂 HTML；
  - **百字节极速直出**：每场仅返回数十至百余字节的纯净文本直接作为技能输入送入模型上下文，由 `skills/post-review` 规约直接驱动对账与概率打分；
  - **全流程严禁编写任何 `.py` 正则提取脚本、清洗脚本或中间统计代码！**
- **自主智能调度与职责界限（物理门禁不僭越大脑）**：
  - AI 大模型拥有完全自主的选择、切换与组合调度权；
  - 无论选用哪一个工具，最终进货必须原子落盘底层无损存证 `data/YYYY-MM-DD/raw/{matchId}.json`，供 EvoOntology 官方 MCP 提取微观数据；同时组装落盘工整单文件 `data/YYYY-MM-DD/{matchId}.md` 作为人类可视化复盘简报（全天赛程索引统一汇总于 `data/YYYY-MM-DD/meta.md`），确保物理源数据新鲜有效（<30分钟）。
  - **核心分工红线**：物理文件只做**数据纯净度客观存证**（防空骨架、防字段错位、防缺机构），**绝对不包含任何代码推演判断、绝不输出预测胜负**。所有倍率推演、博弈破译与做市商反审全权由 **AI 大模型的大脑自主完成**，语义机位由 EvoOntology 官方原生 MCP 支持！
  - **EvoOntology 专属视网膜铁律（只负责看，不负责理解）**：全系统搜查、观看任何比赛数据必须使用 EvoOntology 官方 MCP 工具。EvoOntology 专属负责看数据（按机位定向检索、字段精准提取与投喂切片），严禁大模型直接用 `view_file` 裸视庞杂原始 JSON 或全篇 Markdown，坚决消灭上下文爆炸、漏读与幻觉！

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

凡因字段错位、数据污染或时间戳缺失导致文件无效的，AI 必须重新精准获取并纠偏归位。

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
4. **官方原生隐身、指纹模拟与会话复用标准（SSOT 统一溯源）**：
   - **Chrome 协议指纹模拟**：全流程统一调用 `impersonate="chrome"` 与 `stealthy_headers=true`，完全模拟真实 Chrome TLS/JA3 与请求头拓扑，规避 WAF 识别；
   - **选择器底层下推**：抓取 HTML 必须传递 `css_selector`，内存就地过滤 DOM，正文纯净提取 `main_content_only=true`；
   - **官方请求会话复用**：单场多端点请求推荐调用 `mcp__scrapling__open_request_session` 创建长连接，配合 `session_make_request` 复用底层连接，杜绝频繁离散握手；
   - **隐身规约统一溯源**：Chrome TLS 伪装、请求头注入与分组并发机制 **100% 依循 [`match-scraper`](skills/match-scraper/SKILL.md) 官方规约**执行；
   - 本宪法专注规范：法定 23 家白名单、7 家变盘时序、数据 Schema 与防错位断言，消除跨文件冗余复制与参数漂移。
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

#### Scrapling MCP 官方原生会话与反爬隐身调用范式（Session Lifecycle Standard）
```json
// 1. 开辟全真 Chrome 长连接会话（复用 TLS/JA3 指纹与 TCP 连接池）
mcp__scrapling__open_request_session({
  "impersonate": "chrome",
  "stealthy_headers": true,
  "timeout": 30
})
// 返回 session_id (如 "req_sess_3000474")

// 2. 复用会话拉取百家欧指（带上下文 Referer，内存提纯法定 23 家）
mcp__scrapling__session_make_request({
  "session_id": "req_sess_3000474",
  "url": "https://1x2d.titan007.com/3000474.js",
  "headers": {
    "Referer": "https://titan007.com/"
  }
})

// 3. 复用会话并发拉取 7 家法定亚盘/大小球变盘流水（选择器下推，GB18030 解码）
mcp__scrapling__session_make_request({
  "session_id": "req_sess_3000474",
  "url": "https://vip.titan007.com/changeDetail/handicap.aspx?id=3000474&companyID=1&l=0",
  "css_selector": "#table_odds",
  "headers": {
    "Referer": "https://vip.titan007.com/"
  }
})

// 4. 采集完成必须强制显式关闭会话，释放句柄
mcp__scrapling__close_session({
  "session_id": "req_sess_3000474"
})

// 5. 遭遇 403 / 503 或 Cloudflare 挑战盾时，自动升阶至隐身无头浏览器（Level 2）
mcp__scrapling__stealthy_fetch({
  "url": "https://zq.titan007.com/analysis/3000474cn.htm",
  "solve_cloudflare": true,
  "css_selector": "#team_lineup",
  "network_idle": true
})
```

#### 实战踩坑必记
1. **GB18030 编码陷阱与二进制流保真**：球探二级页面（`changeDetail/*.aspx`）为旧版 GB18030 编码，外部严禁以 UTF-8 强行转换为 string（否则队名和盘口会变成乱码导致解析脱靶），必须获取 `page.body` 原始二进制流后通过 `new TextDecoder('gb18030').decode(buf)` 或 Scrapling 原生 `Selector(content, encoding='gb18030')` 进行精准解码；
1.1. **CLI 文件扩展名硬约束**：官方 Scrapling CLI（`Convertor.write_content_to_file`）仅支持 `.txt`、`.html`、`.md` 三大格式。抓取 `1x2d.js`、`analy.json`、`polymarket.json` 等非 HTML 资源时，落盘必须指定 `.txt` 后缀（如 `1x2d.txt`、`analy.txt`），若直接传 `.js` 或 `.json` 会被底层抛出 `ValueError: Unknown file type` 导致静默丢失；
1.2. **欧指 1x2d.js 字段解构与 23 家 Hash Map 字典防漏**：`var game=Array(...)` 中各字符串以竖线 `|` 分割，其首项 `parts[0]` 为机构 ID（cid），而 `parts[1]` 为赔率 ID（oddsId）。严禁将 `parts[1]` 错当为 cid！必须以法定 23 家机构权威 cid 集合为唯一键做 $O(1)$ 哈希字典映射匹配，严禁通过线性切片偏移遍历；
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
- **本质定义（What it is）**：【推演源数据】（`data/YYYY-MM-DD/{matchId}.md`）是自动化流水线**阶段一**由 Scrapling 极速协议流并发秒取 5 大法定接口（分析页阵容与技统、波胆页 Crown 指数、竞彩官方全玩法、百家欧指 `1x2d.js` 与变盘流水 `changeDetail`），精纯组装落盘的**唯一物理原材料与客观事实底牌**。
- **核心意义（What it means）**：
  1. **物理级防伪防火墙**：它是系统**两阶段硬隔离的核心物理边界**。没有 exit 0 的物理源数据，大模型绝对禁止动脑思考与输出赛果，彻底铲除凭记忆脑补、无根据猜想和时序克隆；
  2. **唯一法定证据链**：它是大模型 10 步深度推演、证据引用与赛后回查对账的唯一只读证据凭证；
  3. **门禁生死线**：底层数据物理落盘且新鲜（<30分钟），经 EvoOntology 语义校验（`validate_semantics`）通过后，方准发放给首席分析师。
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
| 机构类型 | 公司ID (cid) | 机构标准名称 | 做市属性分类 | 核心业务职能与博弈定位 |
| :---: | :---: | :--- | :--- | :--- |
| 核心做市 | **80 / 1** | **澳彩 (Macau)** | 亚洲母盘 / 核心做市 | 亚洲盘口风向标，抽水低、操盘稳健，防守意图明显 |
| 核心做市 | **545 / 3** | **皇冠 (Crown)** | 核心做市 / 资金晴雨表 | 全球最大受注平台，贴水敏感，反映真实主力资金动向 |
| 商业做市 | **281 / 8** | **Bet365 (365bet)** | 商业做市 / 散户巨头 | 散户筹码最集中，善用微调高低水诱导大众偏好 |
| 核心做市 | **90 / 12** | **易胜博 (Easybet)** | 核心做市 / 操盘激进 | 亚洲传统老庄，深盘开盘激进，变盘果断 |
| 欧陆防守 | **177 / 47** | **平博 (Pinnacle)** | 欧陆防守 / 低抽水标杆 | 全球最高赔付限额与最低抽水率，真实概率去水基准 (CORP) |
| 亚洲哨兵 | **432 / 48** | **香港马会 (HKJC)** | 亚洲防守哨兵 | 专营做市，极度厌恶风险，临盘降赔防守信号极强 |
| 亚洲哨兵 | **42** | **188 (188bet)** | 亚洲自营哨兵 | 与皇冠/365形成铁三角，防范异动资金冲击 |
| 英伦母盘 | **115** | **威廉希尔 (William Hill)** | 英伦母盘 / 欧陆标杆 | 欧洲传统老牌，胜平负经典分布，散户基准定价 |
| 英伦母盘 | **82** | **立博 (Ladbrokes)** | 英伦母盘 / 欧陆标杆 | 经常与威廉希尔形成微差互搏，观察欧陆分流意图 |
| 核心做市 | **81** | **伟德 (Victor Chandler)** | 核心做市 | 英系老牌，胜平负返还率高，敏感度高 |
| 欧陆保守 | **104** | **Interwetten** | 欧陆保守标杆 | 奥地利老牌，平局赔率通常压极低，欧洲防守探针 |
| 商业做市 | **255** | **Bwin** | 商业做市 | 欧洲大众品牌，平负赔率波动大，易于诱导散户 |
| 意系哨兵 | **110** | **SNAI** | 意系防守哨兵 | 意大利本土垄断机构，对意系赛事（意甲/意乙）具备绝对内幕定力 |
| 交易所 | **2** | **Betfair (必发)** | 交易所撮合市场 | 纯撮合交易，反映挂牌大单与真实市场对冲头寸 |
| 老庄机构 | **474** | **SBO (利记)** | 老庄机构 | 东南亚传统庄家，走地敏锐，早盘防守 |
| 老庄机构 | **649** | **沙巴 (IBCBET)** | 老庄机构 | 亚洲知名体育平台，亚盘受注量大 |
| 论文样本 | **800** | **Marathon (马拉松)** | 学术论文样本 | 返还率极高（97%+），极限去水对账基准 |
| 论文样本 | **482** | **Betway (必威)** | 学术论文样本 | 欧洲主流机构，对账参考 |
| 论文样本 | **386** | **Unibet (优胜客)** | 学术论文样本 | 北欧大型机构，对北欧联赛具有极高定价权威 |
| 论文样本 | **826** | **Paddy Power** | 学术论文样本 | 爱尔兰巨头，擅长炒作热门与利用大众偏见 |
| 论文样本 | **16** | **10Bet** | 学术论文样本 | 辅助样本做市商 |
| 终端履约 | **1129** | **中国体彩 (Sporttery)** | 终端履约与开售核验 | 仅用于核验场次编号（如周一001）、单固/让球玩法及销售截断 |
（严格按 1x2d.js 原始报文提纯上述法定白名单机构，严禁对未开盘机构填充假赔率；底层 raw 存证完整封存 26 端点）

---

## 四、核心做市商与终端标的真实变盘时序流水（法定 7 家 × 3 盘 = 21 张全量大表，逐行原样零篡改）
### 1. 澳彩 (欧亚双盘核心, 核心做市, cid=80)
#### 亚盘真实变盘流水 / #### 大小球真实变盘流水 / #### 欧指真实变盘流水（3 张表）
### 2. 皇冠 (欧亚双盘核心, 核心做市, cid=545)（3 张表）
### 3. Bet365 (商业做市散户巨头, cid=281)（3 张表）
### 4. 易胜博 (操盘激进老庄, cid=90)（3 张表）
### 5. 平博 (欧陆防守标杆, cid=177)（3 张表）
### 6. 188Bet (亚洲自营哨兵, cid=115)（3 张表）
### 7. 香港马会 (亚洲防守哨兵, cid=82)（3 张表）
*注：7 家机构各输出亚盘、大小球、欧指共 21 张独立流水大表，倒序排列，有几行写几行，严禁截断与抽稀！*

---

## 五、波胆与终端履约标的（Crown 比分矩阵 & 体彩官方玩法 & Polymarket）
- **Crown 皇冠 0:0 ~ 4:4 比分矩阵赔率**：完整表格呈现各比分初即赔率；
- **中国体育彩票官方代号与赔率**：HAD 普通胜平负与 HHAD 让球胜平负让球数与初即赔率；
- **Polymarket 预测市场**：链上挂单与点击链接。
```

#### 人类可视化简报（`matchId.md`）黄金物理装配门禁硬指标（Hard Integrity Gates）
1. **行数硬门禁（Line Count Gate）**：装配后的 `data/{销售日}/{matchId}.md` 行数必须 **$\ge 350$ 行**（满配对齐 380~450 行黄金标杆，文件体积 $\ge 15\text{KB}$），严禁生成 100~200 行的残缺抽稀半成品；
2. **战区全覆盖门禁（5-Section Completeness Gate）**：必须 100% 包含上述全量 5 大战区（阵容/战绩/23家欧指/21张变盘流水/波胆体彩），缺少任何一个战区直接阻断并报错；
3. **21 张变盘流水表硬门禁（21 Odds Tables Gate）**：战区四中 7 大法定机构的亚盘、大小球、欧指必须各自独立建表，共计 **21 张流水表格**（官方合法未开盘除外），严禁偷工减料只留亚盘或只留 4 家；
4. **23 家欧洲指数全景对比门禁（23 Bookmakers Gate）**：战区三必须完整列出法定 23 家初即盘、返还率与凯利指数，严禁删减；
5. **熔断与重新装配**：凡任何指标不达标，进货流水线立即自动熔断，阻断进入推演阶段，强制重新基于底层 26 端点原始存证全量装配！
```
- **原汁原味真实流水与加密封条铁律（Zero Fabrication & Cryptographic Seal）**：
  1. **彻底废除 T0～T4 凑数切片与主观形态列**：源数据文件只准存储 100% 客观原始数字与真实分秒时间戳，严禁在源数据中混入任何主观博弈定性文案（如“中盘假摔震仓”），所有博弈破译统一留到阶段二由首席分析师基于真实流水推演；
  2. **原始报文直读装配与 SHA-256 哈希封条（`--assemble-bundle` & `raw/{matchId}.json`）**：
     - **单一原子防伪溯源包（标准规约）**：将 Scrapling 抓取的原始报文与剪枝文本打包为单个原子 JSON `data/{销售日}/raw/{matchId}.json`（含 `matchId`、`sealedAt`、`receipt` 与全量 26 个端点原始 payload 字符串）。**底层存证硬红线：`payloads` 对象必须包含全量 26 个端点真实报文字符串（1x2d.js、analysis.html、odds.html、analy.json、7家机构21张流水HTML与polymarket.json），严禁只写 receipt 收据头而不装载原始报文（严禁生成空收据）！**
     - **离线零脑补装配**：直接组装落盘至 `data/{销售日}/{matchId}.md`（或向后兼容保存原始 json），零大模型转抄直出 Markdown，并自动清理旧版零散目录；
     - **源数据真实无损**：严格保留真实变盘历史、状态词（`早`/`即`/`初盘`）与真实时间戳，杜绝任何人工抽稀或假造！
     - **真实网络溯源回执与服务端指纹防伪（Network Receipt & Provenance Verification）**：原子 JSON `raw/{matchId}.json` 强制包含 `"receipt"` 块（记录 26 个端点请求详情、HTTP 200 响应状态、字节大小、服务端指纹、原始载荷 SHA-256 与整包 networkSignature）；通过 EvoOntology 语义门禁（`validate_semantics`）与 Scrapling 原生回执核验载荷哈希一致性，彻底杜绝脱网伪造假数据！
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

- **自愈机制（Self-healing）**：EvoOntology 语义解析已打通攻防物理数据的多通道映射识别（无论是 `match.homeGoals/awayGoals`、`basicStatsText` 还是 `tactics.home/away` 结构化进失球，均可通过概念绑定精准提取），彻底消灭因字段命名差异导致的读取误报。

### 数据安全规则

- **赔率必须实时抓取**：每次分析都用 `/scrapling-official` 极速原生流水线实时拉取球探页最新数据，不复用 memory 中旧赔率。
- **只用赛前赔率**：过滤状态为“滚”的记录，并按开赛时间截断赛前变化历史。
- **缺失不臆造**：如果某家公司或某类市场缺失，报告中必须标注数据缺口，并降低对应维度权重。
- **平博用途**：平博可作为主流公司交叉验证参考，不单独用于决策依据。

### 官方 sports-math MCP 纯数学算力服务

标准东京大学 Shota Goto (2026) OO-EPC 官方原版去水计算器与 Dixon-Coles 修正泊松引擎已作为独立 MCP 服务封装挂载（宿主级 `sports-math`），仓库内 100% 物理剔除本地 `.py` 脚本，杜绝终端命令行调用与大模型心算失真。

#### 1. 欧指无偏去水（devig_oo_epc）
用于欧指分析第 4 步、四项论文质问之二及七列表第 5 列的点概率计算。
```json
call_mcp_tool(
  ServerName="sports-math",
  ToolName="devig_oo_epc",
  Arguments={"home_odds": 2.10, "draw_odds": 3.40, "away_odds": 3.55}
)
```
- 返回参数：`probabilities` (无偏胜平负点概率字典), `overround` (盘口原始抽水率), `converged` (布尔状态)。

#### 2. 比分分布与低比分修正泊松（poisson_dixon_coles）
用于比分基准推演与 Top 比分概率排序。
```json
call_mcp_tool(
  ServerName="sports-math",
  ToolName="poisson_dixon_coles",
  Arguments={"home_lambda": 1.45, "away_lambda": 1.10, "top_n": 6}
)
```
- 返回参数：`top_scores` (Top N 修正比分概率), `lambda_home`, `lambda_away`。

### EvoOntology 官方语义视网膜交互规约（Official Semantic Interaction Protocol v1）

系统全面对齐官方原生 `ruc-datalab/EvoOntology` 架构，建立标准化视网膜操作规约：

1. **视网膜绝对解耦宪章（The Eye & Camera Invariant）**：
   - 官方权威立宪：本体层 100% 独家充当“只读光学透镜与微观约束探针（Eyes and Cameras）”，严禁入侵推演与决策大脑；
   - 绝对禁止在本体层中编码任何比赛预测、绝不计算让球输赢、绝不做盘口好坏定性；推演与博弈破译 100% 全权由自研 AI 大模型完成。
   - 官方三大核心公理：`Semantic guidance is not a final answer`（语义指导不是最终答案）、`Semantic information should remain traceable`（语义信息保持可溯源）、`Native data operations remain the evidence source`（底层原生数据操作依然是证据唯一来源）。
2. **两阶段交互标准流（browse_semantics ➔ resolve_semantics）**：
   - **第一步：概念发现（browse_semantics）**：大模型根据分析需求定向检索 Term（如 `browse_semantics(query="欧指23家")`）；
   - **第二步：微观切片与状态核销（resolve_semantics）**：调用 `resolve_semantics(mentions=[23家机构])`，获取精确 `database_source: "raw_json"` 映射（`table: "europe1x2"`, `column: "平博"`），核对返回体中每家机构的 `status` 字段（`supported` 放行，非预期 `gap` 立即阻断报警）；
   - **第三步：认知契约卡前置对质（Constraint Probe）**：若返回的 `constraints` 中包含 `severity: block`，推演大模型必须在认知契约卡中显式开设 `【EvoOntology机位阻断对质】`，给出反向博弈破译，无对质严禁下槌！
3. **已激活三大做市阻断探针（Active Block Probes）**：
   - **探针一：`constraint_pinnacle_stability`（标杆定海神针警报）**：商业庄与体彩大幅降赔（$\ge 0.15$），但平博变动绝对值 $\le 0.03$ 纹丝不动，强制禁止将商业庄降赔定性为防守，强制对质平博未动原因；
   - **探针二：`constraint_headfake_rebound`（亚盘脉冲假摔警报）**：中盘亚盘主动升盘挂超满水（$\ge 1.04$）诱多，终盘仓皇退回初盘门槛，强制判定为假摔现行；
   - **探针三：`constraint_draw_extreme_high`（高平筹码真空通杀警报）**：欧指平赔极端高挂（$\ge 4.00$）处于筹码真空区，强制防范做市商通杀大众低赔筹码。
4. **防看错与防漏看 23 家数据机制（Anti-Misreading & Anti-Omission）**：
   - **防看错（Grounding Anchor）**：每个概念由 `Mapping` 刚性锚定至 `raw/{matchId}.json` 的确切字段，彻底杜绝大模型在庞杂报文中注意力漂移、行列张冠李戴与列名幻觉；
   - **防漏看（Status Gap Alarm）**：法定 23 家做市商通过 `terms.json` 全纳管；若出现任何非预期缺失，`resolve_semantics` 显式返回 `status: "gap"` 报警，绝不静默丢失。
5. **本体静态安全门禁（validate_semantics）**：
   - 严格执行 `validate_semantics(workspace="...")`，保障 Schema v1 规范（5 种官方 `relation_type`，标准 `confidence` 与约束分类），确保零语法与运行时错误。





## Polymarket 下单链接与法定第 6 接口（官方 Discover Markets API 检索标准）

> 📌 **官方权威文档索引（Documentation Index）**：`https://docs.polymarket.com/llms.txt`（AI 交互首选地图，全量中文详见 `_llms/cn.txt`）。

7 列表最后一格必须物理调用 Gamma API 真实核查（严禁脑补与跳过）：

### 1. 官方市场发现标准规约（Discover Markets via API - 严禁客户端拼接猜测 Slug）
Polymarket 官方架构明确立宪：**Slugs 不保证任何固定命名规律（如曼城vs巴黎为全名、林茨为 lin2、南安普敦为 sot），严禁客户端程序化拼接猜测 Slug！严禁使用 `public-search` 盲搜以防天气市场冲刷与历史完场老赛事占位！**
客户端猜测 Slug 是导致「404 坏链」与「误判未开盘」的唯一根因。必须严格依照官方标准流动态发现：
1. **第一步（查官方权威联赛字典与批量直取）**：调用 `GET https://gamma-api.polymarket.com/sports` 获取 `series_id`，再批量直取活跃事件：
   `GET https://gamma-api.polymarket.com/events?series_id={id}&closed=false&limit=100`
   Windows 环境带 `--ssl-no-revoke --http1.1` 防止长 JSON 管道截断；按对阵与比赛日期精准锁定目标；
   - 过滤与定位：按对阵与比赛日期精准锁定活跃目标；
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
2. **官方权威 `/sports` 规范发现（严禁盲搜）**：必须严格遵循官方标准：先从 `GET /sports` 获取联赛 `series_id` 或 `primaryTag`，调用 `GET /events?series_id={id}&closed=false` 批量拉取活跃赛事与真实 Slug，彻底杜绝被非体育市场（如气温预测）或历史完场老赛事冲刷导致的误判；
3. **主流核心联赛 100% 开盘硬门禁**：五大联赛、欧冠、欧联、欧协联、解放者杯等核心主流赛事在 Polymarket 官方 100% 常态化开盘，必须提供真实纯英文事件可点击链接；门禁严厉禁止任何类似『官方未开盘（经Gamma双向核验）』等免责套话！违者一律物理熔断；
4. **极小众边缘赛事确无标的处理**：仅限官方确未收录的小众二级边缘联赛，在经官方 Discover API 全面核验无标的时，方可如实标注未收录说明；欧洲指数法定要求自动对齐为 22 家传统机构，全量推演到底；
5. **虚构链接零容忍硬熔断**：凡检测到链接包含模板占位符、伪造前缀（如 `match-`）或中文字符，门禁直接触发 `FAIL` 物理熔断！

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
2. **确定性【推演源数据】自动化装配规范**：
   - 严禁大模型在会话里手写文本或拼凑散装 Markdown！原始数据采集后，直接将原子数据包转化为符合黄金契约的单文件 Markdown `data/YYYY-MM-DD/{matchId}.md`。
   - 负责结构化提纯法定 23 家欧指、7 大做市商双盘时序、Crown 波胆与官方玩法，保证字段 100% 规范无噪音。
3. **物理存证确认与新鲜度核验**：
   - 检查物理文件 `data/YYYY-MM-DD/{matchId}.md` 是否存在且新鲜（<30分钟）；
   - 数据齐全无误方可进入 10 步推演；若物理文件缺失或数据为空，必须立即中止并重新拉取。
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
  task: "深度分析 [英超] 阿森纳 vs 曼城（ID: 2950977）。读取 skills/deep-analysis/SKILL.md。严格按照模板，阶段一完成底层源数据落盘并过验，worker 通过 EvoOntology 官方 MCP 提取微观切片（严禁裸视海量原始报文）完成全部 10 步分析；超 4000 字须分段。通过 messaging 推送分析报告给主人。返回结构化综合评估结果（JSON 格式）。"
  label: "deep-analysis-2950977"
  runTimeoutSeconds: 900
```
