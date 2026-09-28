# Graph Report - 倍率分析推演  (2026-09-28)

## Corpus Check
- 64 files · ~54,558 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .json5 1)

## Summary
- 1064 nodes · 1306 edges · 63 communities (60 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- 泊松比分量化模型
- 1. 确认分析依据公司列表
- 球探数据爬虫与抓取
- 盘赔十步深度分析
- Agent运行编排与人格总纲
- 泊松比分量化模型
- 盘赔十步深度分析
- 盘赔十步深度分析
- 10.1 离线拟合思路（以后可精细化）
- 1. 目标与范围
- 泊松比分量化模型
- ref_node_url
- 1.1 操作分级定义
- absolutizeVipUrl()
- 泊松比分量化模型
- 泊松比分量化模型
- 泊松比分量化模型
- 泊松比分量化模型
- 泊松比分量化模型
- Agent运行编排与人格总纲
- 1. 是什么
- 泊松比分量化模型
- 泊松比分量化模型
- 泊松比分量化模型
- appendCompanyList()
- 001 赫尔蒙德 vs 坎布尔
- 2.1 判定总进球倾向
- arrCup：赛事基础信息
- 赛事初筛与准入规则
- 1.1 单场比分概率 P(i:j)
- 1. 标题与场次信息（首段开头）
- SKILL.md
- 精选推荐与串关策略
- 赛事初筛与准入规则
- package.json
- buildOddsHistoryUrls
- 3.1 在 λ 与风格判定中的使用
- 泊松比分量化模型
- Agent运行编排与人格总纲
- 球探数据爬虫与抓取
- 泊松比分量化模型
- 盘赔十步深度分析
- 赛事初筛与准入规则
- 001 场案例分析
- 精选推荐与串关策略
- 1. MEMORY.md 中 CLV 用
- Agent运行编排与人格总纲
- SKILL.md
- SKILL.md
- SKILL.md
- 盘赔十步深度分析
- alignedOddsRow()
- 003 场完整分析案例（2026-03-
- 赛后核验与复盘归档
- Agent运行编排与人格总纲
- 球探数据爬虫与抓取
- 主人决策与配置偏好
- 赛后核验与复盘归档
- 主人决策与配置偏好
- 2026-03-11 — 高危操作未等待
- 造热 vs 降热 典型形态
- IDENTITY.md - Who Am
- Feature Requests

## God Nodes (most connected - your core abstractions)
1. `fetchMatchData()` - 17 edges
2. `buildAnalysisContext()` - 16 edges
3. `buildReviewContext()` - 15 edges
4. `cleanText()` - 15 edges
5. `value()` - 14 edges
6. `main()` - 13 edges
7. `累计战绩` - 13 edges
8. `执行流程` - 13 edges
9. `parseDetailHtml()` - 12 edges
10. `下注决策手册（版本 1）` - 12 edges

## Surprising Connections (you probably didn't know these)
- `十步盘赔深度分析法 (10-step Deep Analysis)` --incorporates--> `泊松比分预测模型 (Dixon-Coles & Poisson Modeling)`  [INFERRED]
  skills/deep-analysis/SKILL.md → scripts/poisson_calc.py
- `六阶段赛事初筛流程 (Match Screening Workflow)` --consumes_data_from--> `球探数据采集引擎 (sporttery-sniper)`  [INFERRED]
  skills/match-screening/SKILL.md → scripts/sporttery-sniper/package.json
- `赛后复盘与记忆沉淀 (Post Review & Memory System)` --uses_review_command--> `球探数据采集引擎 (sporttery-sniper)`  [INFERRED]
  skills/post-review/SKILL.md → scripts/sporttery-sniper/package.json
- `十步盘赔深度分析法 (10-step Deep Analysis)` --depends_on--> `球探数据采集引擎 (sporttery-sniper)`  [INFERRED]
  skills/deep-analysis/SKILL.md → scripts/sporttery-sniper/package.json
- `足球庄家倍率精算师 (Persona / Role)` --adheres_to--> `赔率分析推演铁律 (A+B 推演准则)`  [INFERRED]
  IDENTITY.md → SOUL.md

## Import Cycles
- None detected.

## Communities (63 total, 3 thin omitted)

### Community 0 - "泊松比分量化模型"
Cohesion: 0.08
Nodes (42): argparse, 口径一致性防护 (Consistency Check Guard), 泊松比分预测模型 (Dixon-Coles & Poisson Modeling), dataclasses, json, math, os, pathlib (+34 more)

### Community 1 - "1. 确认分析依据公司列表"
Cohesion: 0.05
Nodes (41): 1. 确认分析依据公司列表, 2. 赔率数据归属与整理, 3. 赔率数据整理规则, 4 家一致的“操盘手法一致”识别（亚盘专用）, 4 家一致的“操盘手法一致”识别（大小球专用）, 8. 存档原始赔率数据, 变动历史分析示例（亚盘，必须像这样写）, 变动历史分析示例（大小球，必须像这样写） (+33 more)

### Community 2 - "球探数据爬虫与抓取"
Cohesion: 0.11
Nodes (37): applyLatestEuropeHistoryToCompanies(), applyLatestHistoryToCompanies(), clearMarketCurrent(), DEFAULT_REQUEST_DELAY_RANGE_MS, extractArrayFunctionStrings(), extractArrayLiteral(), HANDICAP_NAMES, handicapName() (+29 more)

### Community 3 - "盘赔十步深度分析"
Cohesion: 0.06
Nodes (36): 2.1 盘口数据, 2.2 判断实盘 or 错盘, 2.3 错盘分类（如为错盘）, 2.4 浅盘形态细分（如为浅盘）, 3.1 水位数据, 3.2 水位变化历史（关键时点）, 3.3 综合判断（不机械）, 4.1 欧指数据（威廉/365 交叉认证） (+28 more)

### Community 4 - "Agent运行编排与人格总纲"
Cohesion: 0.06
Nodes (34): AGENTS.md - 足彩分析工作流操作手册, Subagent 注意事项, 一、工作流程总览, 七、红线与安全, 三、技能流程指引, 不使用 Subagent 的情况, 主人中途干预, 九、群聊规则 (+26 more)

### Community 5 - "泊松比分量化模型"
Cohesion: 0.06
Nodes (34): 10.1 串关：用 EV 和相关性约束, 10.2 特殊盘口的期望拆分, 1.1 必须直接跳过的场次（乱局）, 2.1 用泊松算出基础概率, 2.2 欧指平均：胜平负 EV, 2.3 欧指平均：大小球 EV（可选）, 3.1 平博：尖锐参考盘（胜平负 / 亚盘 / 大小球）, 3.2 亚盘四家：澳彩 / 皇冠 / Bet365 / 易胜博 (+26 more)

### Community 6 - "盘赔十步深度分析"
Cohesion: 0.06
Nodes (30): 4.1 看初盘：谁是庄家心里的「正路上盘」, 4.2 看盘变：盘口往哪边走, 4.3 看水位：顺资金，还是反资金, 4.4 非EV版的小结（纯看盘时的方向感）, 5.1 「盘深就下盘，盘浅就上盘」, 5.2 单看一瞬间的水位判断冷热, 5.3 把单家公司当作「真理」, 5.4 各种江湖口诀（降盘=必冷、低平赔=必平…） (+22 more)

### Community 7 - "盘赔十步深度分析"
Cohesion: 0.07
Nodes (29): λ值计算, 三线一致性, 亚盘推断, 交锋往绩, 价值评估, 关键点, 博德闪耀缺阵, 大小球推断 (+21 more)

### Community 8 - "10.1 离线拟合思路（以后可精细化）"
Cohesion: 0.07
Nodes (28): 10.1 离线拟合思路（以后可精细化）, 10.2 日常使用规则（经验参数版）, 1.1 公式, 1.2 性质, 3.1 所需数据, 3.2 步骤一：基础 λ（仅用主队主场 + 客队客场）, 3.3 步骤二：掺入近六场（加权）, 3.4 步骤三：伤停修正（可选） (+20 more)

### Community 9 - "1. 目标与范围"
Cohesion: 0.07
Nodes (27): 1. 目标与范围, 2. 整体架构, 3.1 比赛基础信息 `matches`, 3.2 联赛与球队 `leagues` / `teams`, 3.3 赔率时间序列 `odds_snapshots`, 3.4 赛果 `results`, 3. 数据结构设计, 4.1 赛程相关 (+19 more)

### Community 10 - "泊松比分量化模型"
Cohesion: 0.07
Nodes (26): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 与泊松概率对比, 主队, 主队（λ₁=1.53）, 主队 / 客队进球数 (+18 more)

### Community 11 - "ref_node_url"
Cohesion: 0.14
Nodes (25): ref_node_url, formatHistoryWindow(), localDateString(), main(), parseCliArgs(), parseFormat(), printHelp(), tryParseFormat() (+17 more)

### Community 12 - "1.1 操作分级定义"
Cohesion: 0.08
Nodes (24): 1.1 操作分级定义, 1.2 高危操作清单 🔴, 1.3 中危操作清单 🟡, 1.4 低危操作清单 🟢, 1.5 操作预览与确认规范, 1. 回滚前创建保护性备份, 1. 操作分级与确认机制, 2026-03-10 14:32 (+16 more)

### Community 13 - "absolutizeVipUrl()"
Cohesion: 0.15
Nodes (24): absolutizeVipUrl(), attrOfFirst(), cleanText(), detectHistoryRowFormat(), extractCells(), extractFormation(), findFirstPositiveIndex(), firstMatch() (+16 more)

### Community 14 - "泊松比分量化模型"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.34）, 主队 / 客队进球数, 主队 赫尔蒙德 (+13 more)

### Community 15 - "泊松比分量化模型"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.12）, 主队 克雷莫纳, 主队 / 客队进球数 (+13 more)

### Community 16 - "泊松比分量化模型"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.22）, 主队 / 客队进球数, 主队 阿纳西 (+13 more)

### Community 17 - "泊松比分量化模型"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.27）, 主队 / 客队进球数, 主队 朴茨茅斯 (+13 more)

### Community 18 - "泊松比分量化模型"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.49）, 主队 / 客队进球数, 主队 巴列卡诺 (+13 more)

### Community 19 - "Agent运行编排与人格总纲"
Cohesion: 0.09
Nodes (21): 1. 确保 OpenClaw 已安装且 pansuan agent 已创建, 2. 复制 Workspace 文件, 3. 合并配置, 4. 安装 agent-browser, 5. 刷新 Skills, 6. 测试, Agent（pansuan）— OpenClaw 足彩分析师 Agent, 使用方式 (+13 more)

### Community 20 - "1. 是什么"
Cohesion: 0.10
Nodes (19): 1. 是什么, 2. 作用, 2. 加载位置与优先级, 3. 作用, 3. 使用方式, 4. 使用方式, OpenClaw：AGENTS.md 与 Skills 说明, 一、Workspace 里的 AGENTS.md (+11 more)

### Community 21 - "泊松比分量化模型"
Cohesion: 0.10
Nodes (19): Memory 摘要, 深度分析报告：马洛卡 VS 西班牙人, 第 10 步：泊松比分建模, 第 1 步：基本面分析, 第 1 段：基本面 + 伤停 + 自开盘, 第 2 步：伤停分析, 第 2 段：欧指分析, 第 3 步：欧洲指数（胜平负）赔率分析 (+11 more)

### Community 22 - "泊松比分量化模型"
Cohesion: 0.10
Nodes (19): 执行步骤, 步骤 1：读取推荐记录, 步骤 2：获取比赛结果, 步骤 3.5：分析质量自评（泊松模型质量）, 步骤 3：逐场核对, 步骤 4.5：反事实分析, 步骤 4：分析复盘（逐场，不只看未命中）, 步骤 5：计算统计 (+11 more)

### Community 23 - "泊松比分量化模型"
Cohesion: 0.11
Nodes (18): 1.1 双泊松模型（Bivariate Poisson）, 1.2 Dixon–Coles 修正, 2.1 Poisson 回归 / 负二项回归, 3.1 Logistic / 多项 Logit, 3.2 树模型 / 集成模型（Random Forest / XGBoost / LightGBM）, 4.1 多家赔率反演的「综合隐含概率」, 7.1 总体原则, 7.2 程序层（服务 / 库）职责 (+10 more)

### Community 24 - "appendCompanyList()"
Cohesion: 0.22
Nodes (17): appendCompanyList(), appendCorrectScoreRows(), appendCrowFullIndex(), appendEuropeCompanyList(), appendEuropeHistories(), appendGroupedHistories(), appendHeadToHead(), appendHistory() (+9 more)

### Community 25 - "001 赫尔蒙德 vs 坎布尔"
Cohesion: 0.12
Nodes (15): 001 赫尔蒙德 vs 坎布尔, 002 克雷莫纳 vs 佛罗伦萨, 003 阿纳西 vs 特鲁瓦, 004 布伦特福德 vs 狼队, 005 朴茨茅斯 vs 德比郡, 006 巴列卡诺 vs 莱万特, 一、统一流程（学习用）, 三、逐场分析（按流程执行） (+7 more)

### Community 26 - "2.1 判定总进球倾向"
Cohesion: 0.13
Nodes (14): 2.1 判定总进球倾向, 2.2 进攻 / 防守强弱, 2.3 主客场 & 近况修正, 3.1 长期大小球盘, 3.2 让球盘表现, 5.1 大小球方向, 5.2 比分权重（用在 w(i:j) 上）, 一、你到底需要什么级别的「风格」？ (+6 more)

### Community 27 - "arrCup：赛事基础信息"
Cohesion: 0.13
Nodes (14): arrCup：赛事基础信息, arrCupKind：阶段与轮次定义, arrTeam：球队字典, extraInfo：加时、点球与晋级说明, G：赛程与赛果, jh：核心业务数据, S：分组积分榜, titan007 欧冠杯 CupMatch c103.js 数据结构分析 (+6 more)

### Community 28 - "赛事初筛与准入规则"
Cohesion: 0.13
Nodes (14): 写入记忆, 初筛本意与分析逻辑, 执行流程, 赛事初筛（match-screening）, 输入, 输出, 输出格式, 阶段 0：预处理与标签 (+6 more)

### Community 29 - "1.1 单场比分概率 P(i:j)"
Cohesion: 0.14
Nodes (13): 1.1 单场比分概率 P(i:j), 1.2 胜平负与比分的关系, 2.1 基本思路, 2.2 操作步骤, 4.1 从胜平负 / 亚盘反推比分范围, 4.2 用比分辅助「盘口纠结」, 一、从 λ 到比分概率, 三、用泊松 + 赔率筛选「有价值的比分」 (+5 more)

### Community 30 - "1. 标题与场次信息（首段开头）"
Cohesion: 0.14
Nodes (13): 1. 标题与场次信息（首段开头）, 2. 分析过程（第 1～3 段，可多段）, 3. 结论（最后一段，必须含以下全部）, 一、推送结构总览, 三、检查清单（主人/复盘用）, 二、必含块与顺序, 四、模拟示例（周日 018 巴萨 vs 塞维利亚）, 【深度分析 周日 018 第 1 段/共 5 段】 (+5 more)

### Community 31 - "SKILL.md"
Cohesion: 0.14
Nodes (13): 前提条件, 异常处理, 执行步骤, 查看其他日期赛程, 步骤 1：检查脚本目录, 步骤 2：运行脚本同步赛程, 步骤 3：解析脚本输出, 步骤 4：格式化输出并写入 memory (+5 more)

### Community 32 - "精选推荐与串关策略"
Cohesion: 0.14
Nodes (13): 执行步骤, 推荐输出（recommendation）, 无推荐场景, 步骤 1：逐场推送分析报告（内容格式规范）, 步骤 2：精选（全部分析完成后执行）, 步骤 3：生成汇总消息（含精选 + 串关建议）, 步骤 4：推送汇总, 步骤 5：写入记忆 (+5 more)

### Community 33 - "赛事初筛与准入规则"
Cohesion: 0.18
Nodes (8): 足球庄家倍率精算师 (Persona / Role), 六阶段赛事初筛流程 (Match Screening Workflow), 赔率分析推演铁律 (A+B 推演准则), 赛后复盘与记忆沉淀 (Post Review & Memory System), 精选推荐与串关决策 (Recommendation & Parlay Strategy), 球探数据采集引擎 (sporttery-sniper), 十步盘赔深度分析法 (10-step Deep Analysis), 主人 (User / Master Decision Maker)

### Community 34 - "package.json"
Cohesion: 0.15
Nodes (12): engines, node, name, private, scripts, analyze, review, schedule (+4 more)

### Community 35 - "buildOddsHistoryUrls"
Cohesion: 0.22
Nodes (13): buildOddsHistoryUrls(), buildRequestHeaders(), createHumanLikeFetch(), launchLoop(), launchPendingRequests(), runRequest(), fetchMatchData(), fetchOddsHistories() (+5 more)

### Community 36 - "3.1 在 λ 与风格判定中的使用"
Cohesion: 0.17
Nodes (11): 3.1 在 λ 与风格判定中的使用, 3.2 在比分权重与大小球中的使用, 3.3 在盘深 / 盘浅判断中的使用, 4.1 荷乙, 4.2 意乙, 一、为什么要按联赛配置？, 三、如何在现有手册中使用联赛配置, 二、每个联赛需要配置哪些东西？ (+3 more)

### Community 37 - "泊松比分量化模型"
Cohesion: 0.21
Nodes (11): 总结：怎么比较才叫“值得下注”, 案例一：布伦特福德 vs 狼队（真实赔率）, 案例三：巴列卡诺 vs 莱万特（假设赔率：主略被低估）, 案例二：赫尔蒙德 vs 坎布尔（假设赔率：主队被低估）, 步骤 1：赔率 → 隐含概率, 步骤 1：赔率 → 隐含概率, 步骤 2：逐项比较, 步骤 2：逐项比较 (+3 more)

### Community 38 - "Agent运行编排与人格总纲"
Cohesion: 0.17
Nodes (11): sessions_spawn — 启动后台 subagent, Subagent 工具, TOOLS.md - 工具使用指南, 单场深度分析数据抓取, 数据安全规则, 数据范围, 核心工具：sporttery-sniper, 赛后复盘数据抓取 (+3 more)

### Community 39 - "球探数据爬虫与抓取"
Cohesion: 0.23
Nodes (10): ref_node_assert, ref_node_test, cleanTeamLabel(), fetchJcSchedule(), normalizeJcSaleDate(), parseAnalysisHtml(), parseHeadToHeadRecords(), parseJcScheduleOddsText() (+2 more)

### Community 40 - "泊松比分量化模型"
Cohesion: 0.18
Nodes (10): 2.1 初盘 EV 计算, 2.2 即时盘 EV 计算, 3.1 泊松对 2.5 球线的看法, 3.2 多家公司大小球盘口（2.5 球）走势概览, 3.3 是否有大小球价值？, 一、基础信息与泊松结果（来自 `006-巴列卡诺-vs-莱万特-泊松分析.md`）, 三、大小球 2.5：走势 + 泊松判断, 二、胜平负：欧指平均 vs 泊松（价值判断） (+2 more)

### Community 41 - "盘赔十步深度分析"
Cohesion: 0.18
Nodes (10): 下一步, 交锋往绩, 伤停, 基本面（分析页）, 已获取数据, 待抓取, 深度分析进度 - 2950955 里斯本 vs 博德闪耀, 状态 (+2 more)

### Community 42 - "赛事初筛与准入规则"
Cohesion: 0.18
Nodes (10): 1. 编排写入深度分析时可能覆盖当日已有场次（中）, 2. 「去掉第3场」后精选用的列表未持久化（中）, 3. 初筛 0 场时编排写入的 ## 推荐格式未统一（低）, 4. 复盘时 memory 文件不存在未明确（低）, 5. 深度分析「此场已分析」时的行为未定义（低）, 6. 浏览器共享导致并行 worker 数据串号（高 — 待解决）, 一、发现的 BUG / 漏洞, 三、建议修改优先级 (+2 more)

### Community 43 - "001 场案例分析"
Cohesion: 0.18
Nodes (11): 001 场案例分析, 判断速查表, 升盘 + 升水的双重性（难点）, 后续行动, 如何区分阻 vs 诱？, 我们的局限与应对, 核心认知（庄家视角）, 案例验证表（持续更新） (+3 more)

### Community 44 - "精选推荐与串关策略"
Cohesion: 0.18
Nodes (10): MEMORY.md - 长期记忆, 串关统计, 关键教训, 各玩法命中率, 各联赛命中率, 安全边界, 比分预测统计, 策略调优记录 (+2 more)

### Community 45 - "1. MEMORY.md 中 CLV 用"
Cohesion: 0.20
Nodes (9): 1. MEMORY.md 中 CLV 用词与「各玩法」不统一, 2. 主会话「无赛程时」行为略模糊, 3. 两套比分时「比分首选」未约定, 4. 已分析过再分析：询问 vs 跳过, 一、已确认一致的部分, 三、可选优化（非漏洞）, 二、建议修补的漏洞 / 不一致, 四、小结 (+1 more)

### Community 46 - "Agent运行编排与人格总纲"
Cohesion: 0.20
Nodes (9): AGENTS.md — 工作区操作手册（提纲模板）, 一、工作流程总览, 七、可配置参数（可选）, 三、红线与安全, 二、记忆与写入规则, 五、与 Skills / TOOLS 的关系, 六、群聊与心跳（可选）, 四、内外边界 (+1 more)

### Community 47 - "SKILL.md"
Cohesion: 0.20
Nodes (9): 何时使用, 前提条件, 执行步骤, 步骤 1：获取今日日期与时间范围, 步骤 2：拉取日历/待办/通知, 步骤 3：汇总并格式化, 步骤 4：（可选）写入 memory, 每日检查（daily-check） (+1 more)

### Community 48 - "SKILL.md"
Cohesion: 0.20
Nodes (9): 何时使用, 前提条件, 执行步骤, 数据抓取（data-fetch）, 步骤 1：确认数据源与范围, 步骤 2：执行抓取, 步骤 3：解析与校验, 步骤 4：输出与落盘（可选） (+1 more)

### Community 49 - "SKILL.md"
Cohesion: 0.20
Nodes (9): 何时使用, 前提条件, 执行步骤, 报告生成（report-generate）, 步骤 1：确定报告类型与输入来源, 步骤 2：收集与筛选内容, 步骤 3：按模板组织报告, 步骤 4：输出与留痕 (+1 more)

### Community 50 - "盘赔十步深度分析"
Cohesion: 0.22
Nodes (9): 一、盘口大类, 三、浅盘三种形态（重点）, 二、错盘分类, 五、分析框架（完整版）, 六、案例记录, 四、其他错盘类型, 浅盘阻上 vs 浅盘诱上 对比, 盘口分类体系（主人亲授 · 2026-03-18） (+1 more)

### Community 51 - "alignedOddsRow()"
Cohesion: 0.33
Nodes (9): alignedOddsRow(), findTableByLabel(), parseCrowCorrectScores(), parseCrowFullIndexData(), parseCrowGoalBands(), parseCrowTeamTotals(), reverseScore(), tableRows() (+1 more)

### Community 52 - "003 场完整分析案例（2026-03-"
Cohesion: 0.25
Nodes (8): 003 场完整分析案例（2026-03-18 反思）, 8 维度完整分析, 关键信号识别, 反思（核心教训）, 实际结果：1-1 平局 ✅, 比赛信息, 盘赔分析, 综合判断

### Community 53 - "赛后核验与复盘归档"
Cohesion: 0.25
Nodes (8): 2784765 场（意甲 拉齐奥 1-0 AC 米兰）复盘总结, 主人点评, 亚盘数据, 基本面 8 维度, 核心教训, 浅盘形态判断, 盘口类型判断, 赛果验证

### Community 54 - "Agent运行编排与人格总纲"
Cohesion: 0.25
Nodes (7): SOUL.md - 你是谁, 性格, 核心原则, 核心特质, 沟通风格, 行为边界, 连续性

### Community 55 - "球探数据爬虫与抓取"
Cohesion: 0.29
Nodes (6): sporttery-sniper, 使用方式, 抓取范围, 数据注意事项, 部署, 验证

### Community 56 - "主人决策与配置偏好"
Cohesion: 0.40
Nodes (5): 8 维度清单（每次分析必须逐项填写）, 为什么必须完整？, ⚠️ 基本面分析强制规则（2026-03-18 主人强调）, 案例：001 场完整分析, 综合评估方法

### Community 57 - "赛后核验与复盘归档"
Cohesion: 0.50
Nodes (3): Heartbeat 检查清单, 赛前分析补漏, 赛后复盘补漏

### Community 58 - "主人决策与配置偏好"
Cohesion: 0.50
Nodes (3): USER.md - About Your Human, 投注偏好, 输出偏好

### Community 60 - "造热 vs 降热 典型形态"
Cohesion: 0.67
Nodes (3): 造热 vs 降热 典型形态, 造热形态（吸引资金 = 多数人买错）, 降热形态（阻挡资金 = 少数人买对）

## Knowledge Gaps
- **629 isolated node(s):** `name`, `version`, `private`, `type`, `test` (+624 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 692 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `累计战绩` connect `精选推荐与串关策略` to `001 场案例分析`, `盘赔十步深度分析`, `003 场完整分析案例（2026-03-`, `赛后核验与复盘归档`, `主人决策与配置偏好`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `name`, `version`, `private` to the rest of the system?**
  _629 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `泊松比分量化模型` be split into smaller, more focused modules?**
  _Cohesion score 0.0821256038647343 - nodes in this community are weakly interconnected._
- **Should `1. 确认分析依据公司列表` be split into smaller, more focused modules?**
  _Cohesion score 0.047619047619047616 - nodes in this community are weakly interconnected._
- **Should `球探数据爬虫与抓取` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `盘赔十步深度分析` be split into smaller, more focused modules?**
  _Cohesion score 0.05555555555555555 - nodes in this community are weakly interconnected._
- **Should `Agent运行编排与人格总纲` be split into smaller, more focused modules?**
  _Cohesion score 0.05714285714285714 - nodes in this community are weakly interconnected._