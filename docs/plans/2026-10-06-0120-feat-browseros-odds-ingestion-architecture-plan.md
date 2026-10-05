---
title: 基于 BrowserOS neo 真实浏览器直取与本地数据快照底账的足球推演系统重塑方案 - Plan
type: feat
date: 2026-10-06
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-brainstorm
execution: code
---

## Goal Capsule

- **Objective:** 彻底根除足彩推演系统中“纯代码脚本（Node/Python）遭遇球探网（titan007）TLS 握手层网络掐断，导致熔断切入备用源后消费写死假数据”的系统性隐患。建立以「BrowserOS neo 真实浏览器无感直取全量时序数据为主轨 + The Odds API 尖锐去水验真为辅轨 + 本地 `data/` 标准快照原子化留底」的全链路数据工程与推演闭环，恢复 100% 真实、毫秒级、零假数据的推演底座。
- **Means:** 严格遵循马斯克做减法与乔布斯极简原则，坚决不引入沉重碎片化的外部 Python 爬虫，零新增爬虫业务代码；直接依托爱马仕原生内置的 `browseros-neo` MCP 真实浏览器基础设施，定义标准轻量 DOM 提取规范；彻底拔除 `okooo-adapter.js` 中的硬编码假数据毒瘤；将提取产物标准化落盘为 `data/YYYY-MM-DD/{matchId}.json` 供推演引擎与定时任务无缝消费。
- **Product Authority:** 遵循主人最高立宪铁律：
  1. 严禁编写任何推演决策、倍率破译或死尺子门禁代码；
  2. 技术栈严格维持纯 Node.js / JavaScript (ESM) 与 Markdown，严禁擅自引入 `.py` 脚本；
  3. 数据抓取异常必须在报告最前端置顶透明披露，绝不静默掩盖或用假数据糊弄；
  4. 未经主人明确口令，绝对不擅自执行 git commit 或 push。
- **Stop Conditions:** 
  1. 彻底清除备用源硬编码假数据；
  2. 在 `TOOLS.md` 中固化 BrowserOS neo 标准提取模板；
  3. 微调 `skills/deep-analysis/SKILL.md` 确立优先消费真实快照规范；
  4. 完成 10-05 欧国联 3 场比赛真实数据采集落盘与推演纠偏；
  5. `py -3.13 scripts/check_consistency.py --print-ok` 满分通过，图谱 0 孤岛。
- **Execution Profile:** 纯 Markdown 技能规范更新、系统文档微调、假数据清除与实战推演验证。

---

## Product Contract

### Summary
本方案为足球倍率分析推演系统重塑数据采集底层管道与系统协同架构。针对球探网（titan007）对普通 Node.js / Python 纯代码请求实施 TCP/TLS 层面直接掐断（`socket hang up` / `ECONNRESET`），而真实 Chrome / BrowserOS neo 浏览器访问 100% 畅通且秒开全部 5 大页面的客观事实，方案废除原有易触发假数据的盲目熔断机制。确立由 BrowserOS neo 真实浏览器直接提取球探网全维度真实数据（基本面 94 表、Crown 皇冠波胆与半全场、澳彩/皇冠/365/易胜博亚盘大小球、35+ 次分钟级升降盘时序、百家欧指 165 家公司）并落盘为标准 `agent.analysis` JSON 文件；同时将已激活的 `the-odds-api.com` 专用于 Pinnacle 平博与 Betfair 必发的欧指尖锐验真，确保输入推演引擎的每一个数字真实可靠。

### Problem Frame
1. **纯代码通道被精准拦截（TLS 指纹识别）**：球探网服务器在 TLS 握手阶段通过客户端指纹识别拦截非浏览器流量，导致 Node.js `cli.js` 连续报 `socket hang up`。经实测，换用 Python 或 curl 同样被秒挂断，纯代码逆向与猫鼠游戏成本极高且极不稳定；
2. **热备源存在硬编码假数据隐患（致命毒瘤）**：既有 `okooo-adapter.js` 在备用接管时，对未抓取到的亚盘与大小球填入了写死的默认假数值（如固定半一盘 0.95/0.91、大小球 2.5 盘），导致系统昨晚在假盘口上做出了“欧深亚浅阻穿盘”的荒谬推演，险些造成重大决策事故；
3. **缺少真实数据离线沉淀中枢（快照断链）**：每次推演如果临场反复依赖脆弱的实时抓取，一旦网络抖动就容易中断。必须建立赛前真实数据快照落盘机制（`data/YYYY-MM-DD/{matchId}.json`），先存底账，再行推演；
4. **The Odds API 无法独立承担全量替代（能力边界错配）**：实测证实 `the-odds-api.com` 仅覆盖欧美区，完全缺失澳彩、皇冠、易胜博三大亚洲风控盘口，缺失皇冠波胆，且免费版无分钟级时序，不能盲目拿它代替球探网，必须明确其“尖锐验真辅助哨”的合理定位。

### Key Decisions
- **KD1. 彻底弃用代码逆向爬虫，全面转向 BrowserOS neo 真实浏览器直取**：不写复杂的代理轮换与防封逆向代码，直接调用爱马仕现成的 `browseros-neo` MCP 工具，利用真实 Chrome 指纹实现球探网 5 大核心页面的秒级无感采集。
  *(session-settled: user-directed — 遵循马斯克做减法与乔布斯极简原则，复用成熟基建，零新增技术债。Governs R1, R3)*
- **KD2. 坚决铲除 `okooo-adapter.js` 中的写死占位符假数据**：备用适配器严禁伪造任何盘口与水位。若数据源真实缺失，必须如实返回空数组并触发显式缺口告警（`dataWarnings`），宁可报警空仓，绝不给引擎喂假数据。
  *(session-settled: user-directed — 捍卫系统科学真实性红线。Governs R2)*
- **KD3. 确立「本地数据快照落盘 (`data/`) $\rightarrow$ 引擎离线推演」标准化交付契约**：推演前，BrowserOS 提取的数据必须规范写入 `data/YYYY-MM-DD/{matchId}.json`，作为赛前不可篡改的证据底账，实现采集与推演的物理隔离。
  *(session-settled: user-directed — 确保赛前证据可审计，赛后复盘有据可查。Governs R4, R5)*
- **KD4. 明确 The Odds API 为“Pinnacle / Betfair 尖锐验真辅轨”**：`the-odds-api.com` 仅用于欧指去水与平博盘口交叉验证，不越权承担亚洲四家盘口推演，恪守其数据能力边界。
  *(session-settled: user-directed — 数据各司其职，杜绝张冠李戴。Governs R6)*

### Requirements

#### 模块一：清除假数据与加固熔断底线 (Fake Data Elimination)
- R1. **彻底清除硬编码占位符**：审查并重构 `scripts/sporttery-sniper/src/okooo-adapter.js`，彻底移除所有写死的固定盘口、固定水位（如 `0.5/1`、`0.95`、`2.5` 等），缺失时一律返回 `null` 或 `[]`。
- R2. **数据缺口显式熔断报警**：当关键机构（澳彩/皇冠/365/易胜博）亚盘或大小球数据缺失时，强制在 payload 的 `dataWarnings` 中登记，并在输出最前端置顶显示 `⚠️【数据源缺口提示】`，严禁静默生成推荐。

#### 模块二：BrowserOS neo 全量数据提取标准确立 (BrowserOS Ingestion Standard)
- R3. **5 大核心页面无缝提取 SOP**：在 `TOOLS.md` 与技能手册中确立 BrowserOS neo 标准采集脚本，通过单次 `run` 调用或高效批处理，覆盖：
  - ① `analysis/{id}cn.htm`：提取基本面 94 表、战绩、积分、进失球及 `#analy_sbAllOdds` 皇冠波胆全指数；
  - ② `AsianOdds_n.aspx`：提取澳彩、皇冠、365、易胜博等初盘与即时盘；
  - ③ `OverDown_n.aspx`：提取大小球初盘与即时盘；
  - ④ `changeDetail/handicap.aspx`：提取皇冠/澳彩 35+ 次分钟级升降盘历史流水；
  - ⑤ `1x2/oddslist/{id}.htm`：提取百家欧赔及返还率。
- R4. **原子化本地落盘契约**：提取数据必须严格对齐 `agent.analysis` JSON Schema，并落盘至 `data/YYYY-MM-DD/{matchId}.json`。

#### 模块三：技能指引与架构微调 (Skill & Architecture Alignment)
- R5. **深度分析消费契约微调**：更新 `skills/deep-analysis/SKILL.md` 与 `AGENTS.md`，规定分析 worker 优先读取已落盘的 `data/YYYY-MM-DD/{matchId}.json`；若快照不存在或需刷新，唤醒 BrowserOS neo 采集。
- R6. **The Odds API 辅助验真规约**：在 `docs/数据源与API矩阵手册.md` 中固化其“欧美顶级做市商尖锐验真”定位，推演时仅在第 7 步合理性去水与平博让球对照中作为辅助输入。

#### 模块四：实战纠偏与闭环验证 (Live Correction & Verification)
- R7. **10-05 晚盘欧国联真实重算**：使用 BrowserOS neo 提取今晚法国 vs 比利时、意大利 vs 土耳其、波黑 vs 波兰 3 场比赛的真实数据快照，重新执行 10 步深度推演与四维认知契约卡冻结，彻底纠正 `memory/2026-10-05.md` 中被假数据污染的推演记录。

---

## Planning Contract

### Technical Architecture
```text
┌────────────────────────────────────────────────────────┐
│               BrowserOS neo (真实 Chrome)               │
│  - 真实 TLS 指纹，球探网 100% 畅通无阻                 │
│  - 一次性提取：基本面、皇冠波胆、亚盘大小球、35+笔时序 │
└──────────────────────────┬─────────────────────────────┘
                           │ 结构化组装 (agent.analysis)
                           ▼
┌────────────────────────────────────────────────────────┐
│          本地数据快照底账 (不可篡改留底)                │
│  - 路径: data/YYYY-MM-DD/{matchId}.json                │
│  - 作用: 赛前真实证据存盘，推演引擎 0 延迟秒读        │
└──────────────────────────┬─────────────────────────────┘
                           │ 纯净数据消费
                           ▼
┌────────────────────────────────────────────────────────┐
│               10 步深度推演与决策中枢                   │
│  - 泊松基准比分建模 (poisson_calc.py)                  │
│  - 真实时序破译 (法国一球/球半、波黑平手)              │
│  - The Odds API 平博/必发去水交叉验真                  │
│  - 四维认知契约卡冻结至 memory/YYYY-MM-DD.md           │
│  - 纯净交付 6 列表格与串关建议                         │
└────────────────────────────────────────────────────────┘
```

### Key Technical Decisions (KTDs)
1. **KTD1: 坚决不自写 Python 爬虫框架**：
   - 违反系统立宪纯 JS 架构；Python 的 requests/urllib 在球探防火墙面前同样因 TLS 指纹被秒断；维护代理池成本极高。
2. **KTD2: 为什么 BrowserOS neo 是终极钥匙？**
   - 它直接驱动本机真实 Chrome 内核，拥有 100% 真实的浏览器指纹，防火墙毫无理由拦截；爱马仕内置原生 MCP 接口，无需安装任何额外依赖。
3. **KTD3: 数据快照命名规范**：
   - 路径：`data/YYYY-MM-DD/{matchId}.json`；
   - 格式：顶层 `kind: "agent.analysis"`，内含 `match`, `detail`, `markets`, `crowFullIndex`, `timeline`。

### Sequencing & Dependencies
- **阶段一 (U1)**：清洗 `okooo-adapter.js`，拔除硬编码毒瘤，确保代码库干净；
- **阶段二 (U2)**：在 `TOOLS.md` 写入 BrowserOS neo 抓取 SOP 标准模板；
- **阶段三 (U3)**：确立 AI 大模型直接消费本地 `data/` 快照机制，零代码改动；
- **阶段四 (U4)**：微调 `skills/deep-analysis/SKILL.md` 与 `docs/数据源与API矩阵手册.md`，理顺消费逻辑与 The Odds API 定位；
- **阶段五 (U5)**：采集今晚 3 场比赛真实数据，落盘 `.json` 并重算真实六列表推演，完成实战纠偏。

---

## Implementation Units

### U1. 铲除备用源硬编码假数据与熔断加固
- **Goal:** 清除 `scripts/sporttery-sniper/src/okooo-adapter.js` 中所有写死的亚盘、大小球、水位占位符，遇缺失时如实报错报警。
- **Scope:** 修改 `scripts/sporttery-sniper/src/okooo-adapter.js` 与 `test/failover.test.js`。
- **Verification:** 运行 `npm test`，确认单测通过，且在无真实盘口时输出显式 `warnings`，不返回假赔率。

### U2. 编制 BrowserOS neo 全量数据抓取规范与 SOP
- **Goal:** 在 `TOOLS.md` 中确立使用 BrowserOS neo 一键提取球探 5 大核心页面并保存为标准 JSON 的标准指导流程。
- **Scope:** 修改 `TOOLS.md`，新增「BrowserOS neo 球探全量数据提取规范」章节，包含标准 JS 执行代码片段与字段映射。
- **Verification:** 代码片段在 BrowserOS 中实跑，能稳定输出包含基本面、波胆、多盘与逐笔时序的有效 JSON。

### U3. 确立 AI 引擎优先消费本地快照规范（零冗余代码）
- **Goal:** 遵循极简原则，不改动 `cli.js` 业务代码，由 AI 大模型在执行深度分析推演时优先直接读取 `data/*/{matchId}.json`。
- **Scope:** 文档与技能指引对齐。
- **Verification:** AI 模型直接读取本地快照并输出合规分析。

### U4. 技能手册与系统架构文档微调
- **Goal:** 同步更新 `skills/deep-analysis/SKILL.md`、`AGENTS.md` 与 `docs/数据源与API矩阵手册.md`。
- **Scope:**
  - 明确“数据源双轨热备：主源遭遇连接掐断时，通过 BrowserOS neo 直取真实数据落盘，禁止使用未核实的备用假数据”；
  - 明确 The Odds API 为 Pinnacle / Betfair 尖锐欧指验真通道；
  - 确保图谱拓扑与术语完全自洽。
- **Verification:** 运行 `py -3.13 scripts/check_consistency.py --print-ok` 满分通过，连通分量恒为 1，孤岛为 0。

### U5. 实战采集今晚欧国联 3 场比赛并完成推演纠偏
- **Goal:** 用 BrowserOS neo 提取 2981453（法国）、2981454（意大利）、2981504（波黑）真实数据快照存为 `data/2026-10-05/{matchId}.json`，重新生成客观真实的推演 6 列表并修正 `memory/2026-10-05.md`。
- **Scope:** 生成 3 个标准数据 JSON，更新 `memory/2026-10-05.md`。
- **Verification:** 对照真实盘口（法国一球/球半、意大利球半、波黑平手），推演逻辑与时序完全咬合，契约卡真实冻结。

---

## Verification Contract

1. **语法与一致性门禁**：
   - 执行：`py -3.13 scripts/check_consistency.py --print-ok`
   - 预期输出：`OK: 未发现口径回退且图谱0孤岛100%连通（skills/docs/scripts/graphify）`
2. **单测套件回归**：
   - 执行：`cd scripts/sporttery-sniper && npm test`
   - 预期输出：全部测试通过，零假数据断言失败。
3. **真实数据完备性检验**：
   - 检查 `data/2026-10-05/*.json`，确认每场比赛均包含真实亚盘档位、皇冠波胆数据与 10 次以上逐笔变盘时序。

---

## Definition of Done

- [ ] `okooo-adapter.js` 中所有硬编码占位符已彻底移除，缺失时触发报警；
- [ ] `TOOLS.md` 确立了标准的 BrowserOS neo 抓取流程与数据落盘规范；
- [ ] AI 推演引擎具备优先读取本地真实快照机制（零代码改动）；
- [ ] `skills/deep-analysis/SKILL.md` 与 `AGENTS.md` 完成口径微调，确立真实快照优先原则；
- [ ] 今晚 3 场欧国联比赛数据成功通过 BrowserOS neo 提取并落盘为 `data/2026-10-05/*.json`；
- [ ] `memory/2026-10-05.md` 中被假数据污染的推演已彻底纠正，四维契约卡基于真实盘口重新冻结；
- [ ] 全库一致性检查满分通过，Graphify 知识图谱 100% 强连通且 0 孤岛。
