# Graph Report - 倍率分析推演  (2026-09-29)

## Corpus Check
- 65 files · ~62,186 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .json5 1)

## Summary
- 1180 nodes · 1755 edges · 85 communities (83 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 254 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3544d915`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- titan007.js
- 第一部分：赛前分析模板
- 盘口与走势阅读手册（简版）
- [欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告
- titan007.test.js
- SOUL.md - 你是谁
- 泊松概率计算手册（足彩用）
- titan007 抓取 → 缓存层 → 内部 API 化设计方案
- 泊松概率分析：布伦特福德 vs 狼队
- 案例 10（慢跌诱强杀大冷）：客胜慢跌破1.80掩护主胜爆冷【多德勒支 3:2 阿尔梅勒城】
- SAFETY.md
- 泊松概率分析：赫尔蒙德 vs 坎布尔
- 泊松概率分析：克雷莫纳 vs 佛罗伦萨
- 泊松概率分析：阿纳西 vs 特鲁瓦
- 泊松概率分析：朴茨茅斯 vs 德比郡
- 泊松概率分析：巴列卡诺 vs 莱万特
- Agent（pansuan）— OpenClaw 足彩分析师 Agent
- OpenClaw：AGENTS.md 与 Skills 说明
- 深度分析报告：马洛卡 VS 西班牙人
- 模型扩展与组合手册（除泊松之外）
- 累计战绩
- buildAnalysisContext
- 球队风格判定手册（简版）
- titan007 欧冠杯 CupMatch c103.js 数据结构分析
- cleanText
- fetchMatchData
- 比分建模与投注手册（泊松版）
- 执行流程
- TOOLS.md
- 盘赔分析系统化框架（2026-03-17 整理 · 主人亲授）
- check_consistency.py
- AGENTS.md - 足彩分析工作流操作手册
- 下注决策手册（版本 1）
- 联赛配置手册（泊松 + 盘口）
- poisson_lib.py
- scripts
- 赔率与泊松比较：何时值得下注（案例详解）
- 执行步骤
- 执行步骤
- 案例 31（狂砸低平2.65掩护天价冷负案）：平赔砸穿至2.65做终极蜜罐，负赔暴拉+0.62真空偷鸡【负3.55与让负1.53通杀案】
- verify_poisson.py
- 巴列卡诺 vs 莱万特：泊松 + 盘口综合实战案例
- 基本面（分析页）
- 一、发现的 BUG / 漏洞
- generate_deep_graph.py
- 赔率分析推演：庄家操盘逻辑与双盘联动推演心法
- recommendation/SKILL.md
- 二、建议修补的漏洞 / 不一致
- 每日检查（daily-check）
- 执行步骤
- 执行步骤
- 1. 不变量一：初赔骨架定位律（Bone Invariant：初盘定能量场）
- 案例 55（初盘<1.35与让胜单调破2.00真穿盘案）：胜1.33砸至1.31，平负双清退，让胜2.05砸入2.00真避险【胜1.31与让胜2.00穿盘双红案】
- parseCrowFullIndexData
- 精选推荐与串关决策 (Recommendation & Parlay Strategy)
- 4 家一致的“操盘手法一致”识别（亚盘专用）
- 三、逐场分析（按流程执行）
- AGENTS.md — 工作区操作手册（提纲模板）
- 执行步骤
- 盘口分类体系（主人亲授 · 2026-03-18）
- 案例 44（半球生死盘诱主杀闷平案）：主胜1.90半球热胆，让胜3.95否定穿盘，平赔3.22通杀主胜【平3.22与让负1.70双红案】
- 深度分析推送通知模板
- 四、模拟示例（周日 018 巴萨 vs 塞维利亚）
- 深度分析（deep-analysis）
- 执行流程
- 赛后复盘（post-review）
- 003 场完整分析案例（2026-03-18 反思）
- 2784765 场（意甲 拉齐奥 1-0 AC 米兰）复盘总结
- 案例 20（拉马努金注意到与相对斜率双降穿盘案）：初盘胜平同值3.30，让负狂砍0.28远超让平【客负1.70与让负3.52穿盘大捷案】
- 第 4 段：大小球 + 第 6-10 步摘要
- 案例 3：慢跌诱强杀冷负【格鲁吉亚 0:1 北爱尔兰】（周五006）
- sporttery-sniper
- 推荐输出（recommendation）
- 核心工具：sporttery-sniper
- 赛程抓取（match-scraper）
- 三、 赔率分析推演十大公理（胜平负 + 让球联动）
- 三、盘口与走势过滤危险热门
- 七、下注频率与资金管理（建议版）
- 步骤 1.5：校验脚本赔率与数据完整性
- 变动历史分析示例（大小球，必须像这样写）
- MEMORY.md
- 写入记忆
- Path
- Heartbeat 检查清单
- solve_lambda_for_over_prob

## God Nodes (most connected - your core abstractions)
1. `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` - 164 edges
2. `4 家一致的“操盘手法一致”识别（亚盘专用）` - 40 edges
3. `累计战绩` - 33 edges
4. `执行步骤` - 31 edges
5. `执行流程` - 26 edges
6. `fetchMatchData()` - 17 edges
7. `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告` - 17 edges
8. `泊松概率分析：布伦特福德 vs 狼队` - 17 edges
9. `buildAnalysisContext()` - 16 edges
10. `泊松概率分析：赫尔蒙德 vs 坎布尔` - 16 edges

## Surprising Connections (you probably didn't know these)
- `LambdaBounds` --provides_mathematical_scoreline_formulas--> `比分建模与投注手册（泊松版）`  [INFERRED]
  scripts/poisson_lib.py → docs/比分建模与投注手册.md
- `LambdaBounds` --provides_mathematical_scoreline_formulas--> `泊松概率计算手册（足彩用）`  [INFERRED]
  scripts/poisson_lib.py → docs/泊松概率计算手册.md
- `LambdaBounds` --calculates_scoreline_lambda--> `4 家一致的“操盘手法一致”识别（亚盘专用）`  [INFERRED]
  scripts/poisson_lib.py → skills/deep-analysis/SKILL.md
- `LambdaBounds` --calculates_scoreline_lambda--> `4 家一致的“操盘手法一致”识别（大小球专用）`  [INFERRED]
  scripts/poisson_lib.py → skills/deep-analysis/SKILL.md
- `LambdaBounds` --calculates_scoreline_lambda--> `变动历史分析示例（亚盘，必须像这样写）`  [INFERRED]
  scripts/poisson_lib.py → skills/deep-analysis/SKILL.md

## Import Cycles
- None detected.

## Communities (85 total, 2 thin omitted)

### Community 0 - "titan007.js"
Cohesion: 0.12
Nodes (32): applyLatestHistoryToCompanies(), cleanTeamLabel(), clearMarketCurrent(), DEFAULT_REQUEST_DELAY_RANGE_MS, extractArrayLiteral(), HANDICAP_NAMES, handicapName(), isKickoffInPast() (+24 more)

### Community 1 - "第一部分：赛前分析模板"
Cohesion: 0.06
Nodes (31): 3.1 水位数据, 3.2 水位变化历史（关键时点）, 3.3 综合判断（不机械）, 4.1 欧指数据（威廉/365 交叉认证）, 4.2 欧指 vs 亚盘一致性, 一、盘口大类, 三、浅盘三种形态（重点）, 二、错盘分类 (+23 more)

### Community 2 - "盘口与走势阅读手册（简版）"
Cohesion: 0.06
Nodes (30): 4.1 看初盘：谁是庄家心里的「正路上盘」, 4.2 看盘变：盘口往哪边走, 4.3 看水位：顺资金，还是反资金, 4.4 非EV版的小结（纯看盘时的方向感）, 5.1 「盘深就下盘，盘浅就上盘」, 5.2 单看一瞬间的水位判断冷热, 5.3 把单家公司当作「真理」, 5.4 各种江湖口诀（降盘=必冷、低平赔=必平…） (+22 more)

### Community 3 - "[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告"
Cohesion: 0.07
Nodes (29): λ值计算, 三线一致性, 亚盘推断, 交锋往绩, 价值评估, 关键点, 博德闪耀缺阵, 大小球推断 (+21 more)

### Community 4 - "titan007.test.js"
Cohesion: 0.10
Nodes (33): 五、与 Skills / TOOLS 的关系, 单场深度分析数据抓取, ref_node_assert, ref_node_test, ref_node_url, formatHistoryWindow(), localDateString(), main() (+25 more)

### Community 5 - "SOUL.md - 你是谁"
Cohesion: 0.22
Nodes (8): IDENTITY.md - Who Am I?, SOUL.md - 你是谁, 性格, 核心原则, 核心特质, 沟通风格, 行为边界, 连续性

### Community 6 - "泊松概率计算手册（足彩用）"
Cohesion: 0.07
Nodes (28): 10.1 离线拟合思路（以后可精细化）, 10.2 日常使用规则（经验参数版）, 1.1 公式, 1.2 性质, 3.1 所需数据, 3.2 步骤一：基础 λ（仅用主队主场 + 客队客场）, 3.3 步骤二：掺入近六场（加权）, 3.4 步骤三：伤停修正（可选） (+20 more)

### Community 7 - "titan007 抓取 → 缓存层 → 内部 API 化设计方案"
Cohesion: 0.07
Nodes (27): 1. 目标与范围, 2. 整体架构, 3.1 比赛基础信息 `matches`, 3.2 联赛与球队 `leagues` / `teams`, 3.3 赔率时间序列 `odds_snapshots`, 3.4 赛果 `results`, 3. 数据结构设计, 4.1 赛程相关 (+19 more)

### Community 8 - "泊松概率分析：布伦特福德 vs 狼队"
Cohesion: 0.07
Nodes (26): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 与泊松概率对比, 主队, 主队（λ₁=1.53）, 主队 / 客队进球数 (+18 more)

### Community 9 - "案例 10（慢跌诱强杀大冷）：客胜慢跌破1.80掩护主胜爆冷【多德勒支 3:2 阿尔梅勒城】"
Cohesion: 0.18
Nodes (11): 案例 10（慢跌诱强杀大冷）：客胜慢跌破1.80掩护主胜爆冷【多德勒支 3:2 阿尔梅勒城】, 案例 11（慢跌诱客杀闷平）：客让半球破1.75引流死胆杀平局【平赔稳守3.62通杀案】, 案例 12（降让胜诱大胜杀穿盘）：低赔破1.30引流穿盘暗杀让平【让平3.85通杀案】, 案例 13（低赔易主真崩盘）：主胜暴拉+0.39客胜加速破位【客胜 2.45 顺水推舟案】, 案例 14（二元盲区与让盘双弃案）：主升平降诱中路，让球双弃出客胜【客胜 3.13 爆冷通杀案】, 案例 15（三大门禁实战首捷）：主胜独跌破位+让盘双降穿盘【胜 1.65 与让胜 3.15 穿盘大捷案】, 案例 16（让胜跳水式暴跌穿盘案）：胜赔暴跌破1.55+让胜狂砍0.43【主胜与让胜穿盘通杀案】, 案例 17（超深盘初赔如骨与庄共舞案）：初赔1.19奠定骨架，终赔1.12+让胜1.56顺势大破深盘案 (+3 more)

### Community 10 - "SAFETY.md"
Cohesion: 0.08
Nodes (24): 1.1 操作分级定义, 1.2 高危操作清单 🔴, 1.3 中危操作清单 🟡, 1.4 低危操作清单 🟢, 1.5 操作预览与确认规范, 1. 回滚前创建保护性备份, 1. 操作分级与确认机制, 2026-03-10 14:32 (+16 more)

### Community 11 - "泊松概率分析：赫尔蒙德 vs 坎布尔"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.34）, 主队 / 客队进球数, 主队 赫尔蒙德 (+13 more)

### Community 12 - "泊松概率分析：克雷莫纳 vs 佛罗伦萨"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.12）, 主队 克雷莫纳, 主队 / 客队进球数 (+13 more)

### Community 13 - "泊松概率分析：阿纳西 vs 特鲁瓦"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.22）, 主队 / 客队进球数, 主队 阿纳西 (+13 more)

### Community 14 - "泊松概率分析：朴茨茅斯 vs 德比郡"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.27）, 主队 / 客队进球数, 主队 朴茨茅斯 (+13 more)

### Community 15 - "泊松概率分析：巴列卡诺 vs 莱万特"
Cohesion: 0.09
Nodes (21): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 主队, 主队（λ₁=1.49）, 主队 / 客队进球数, 主队 巴列卡诺 (+13 more)

### Community 16 - "Agent（pansuan）— OpenClaw 足彩分析师 Agent"
Cohesion: 0.09
Nodes (21): 1. 确保 OpenClaw 已安装且 pansuan agent 已创建, 2. 复制 Workspace 文件, 3. 合并配置, 4. 安装 agent-browser, 5. 刷新 Skills, 6. 测试, Agent（pansuan）— OpenClaw 足彩分析师 Agent, 使用方式 (+13 more)

### Community 17 - "OpenClaw：AGENTS.md 与 Skills 说明"
Cohesion: 0.12
Nodes (15): 1. 是什么, 2. 作用, 2. 加载位置与优先级, 3. 作用, 3. 使用方式, 4. 使用方式, OpenClaw：AGENTS.md 与 Skills 说明, 一、Workspace 里的 AGENTS.md (+7 more)

### Community 18 - "深度分析报告：马洛卡 VS 西班牙人"
Cohesion: 0.15
Nodes (12): Memory 摘要, 深度分析报告：马洛卡 VS 西班牙人, 第 1 步：基本面分析, 第 1 段：基本面 + 伤停 + 自开盘, 第 2 步：伤停分析, 第 2 段：欧指分析, 第 3 步：欧洲指数（胜平负）赔率分析, 第 3 段：亚盘分析 (+4 more)

### Community 19 - "模型扩展与组合手册（除泊松之外）"
Cohesion: 0.11
Nodes (18): 1.1 双泊松模型（Bivariate Poisson）, 1.2 Dixon–Coles 修正, 2.1 Poisson 回归 / 负二项回归, 3.1 Logistic / 多项 Logit, 3.2 树模型 / 集成模型（Random Forest / XGBoost / LightGBM）, 4.1 多家赔率反演的「综合隐含概率」, 7.1 总体原则, 7.2 程序层（服务 / 库）职责 (+10 more)

### Community 20 - "累计战绩"
Cohesion: 0.14
Nodes (12): 2026-03-11 — 高危操作未等待确认, Errors Log, Feature Requests, 串关统计, 关键教训, 各玩法命中率, 各联赛命中率, 比分预测统计 (+4 more)

### Community 21 - "buildAnalysisContext"
Cohesion: 0.22
Nodes (17): appendCompanyList(), appendCorrectScoreRows(), appendCrowFullIndex(), appendEuropeCompanyList(), appendEuropeHistories(), appendGroupedHistories(), appendHeadToHead(), appendHistory() (+9 more)

### Community 22 - "球队风格判定手册（简版）"
Cohesion: 0.18
Nodes (10): 3.1 长期大小球盘, 3.2 让球盘表现, 5.1 大小球方向, 5.2 比分权重（用在 w(i:j) 上）, 一、你到底需要什么级别的「风格」？, 三、借助盘口反推风格, 五、风格对比分和大小球的具体影响, 六、最低可执行版本（给自己一个懒人流程） (+2 more)

### Community 23 - "titan007 欧冠杯 CupMatch c103.js 数据结构分析"
Cohesion: 0.13
Nodes (14): arrCup：赛事基础信息, arrCupKind：阶段与轮次定义, arrTeam：球队字典, extraInfo：加时、点球与晋级说明, G：赛程与赛果, jh：核心业务数据, S：分组积分榜, titan007 欧冠杯 CupMatch c103.js 数据结构分析 (+6 more)

### Community 24 - "cleanText"
Cohesion: 0.16
Nodes (23): attrOfFirst(), cleanText(), detectHistoryRowFormat(), extractCells(), extractFormation(), findFirstPositiveIndex(), firstMatch(), isHistoryChangeTime() (+15 more)

### Community 25 - "fetchMatchData"
Cohesion: 0.18
Nodes (15): buildOddsHistoryUrls(), buildRequestHeaders(), createHumanLikeFetch(), launchLoop(), launchPendingRequests(), runRequest(), fetchMatchData(), fetchOddsHistories() (+7 more)

### Community 26 - "比分建模与投注手册（泊松版）"
Cohesion: 0.14
Nodes (13): 1.1 单场比分概率 P(i:j), 1.2 胜平负与比分的关系, 2.1 基本思路, 2.2 操作步骤, 4.1 从胜平负 / 亚盘反推比分范围, 4.2 用比分辅助「盘口纠结」, 一、从 λ 到比分概率, 三、用泊松 + 赔率筛选「有价值的比分」 (+5 more)

### Community 27 - "执行流程"
Cohesion: 0.14
Nodes (14): 变动历史分析示例（欧指，必须像这样写）, 执行流程, 步骤 1：运行 sporttery-sniper 获取上下文数据, 步骤 2：历史记忆召回, 步骤 3：10 步分析过程（固定顺序）, 步骤 3 续：第 4 步 — 泊松建模（比分概率）, 第 1 步：基本面分析, 第 2 步：伤情分析 (+6 more)

### Community 28 - "TOOLS.md"
Cohesion: 0.18
Nodes (11): sessions_spawn — 启动后台 subagent, Subagent 工具, TOOLS.md - 工具使用指南, absolutizeVipUrl(), applyLatestEuropeHistoryToCompanies(), extractArrayFunctionStrings(), isAfterKickoff(), parseEuropeOddsScript() (+3 more)

### Community 29 - "盘赔分析系统化框架（2026-03-17 整理 · 主人亲授）"
Cohesion: 0.14
Nodes (14): 001 场案例分析, 判断速查表, 升盘 + 升水的双重性（难点）, 后续行动, 如何区分阻 vs 诱？, 我们的局限与应对, 核心认知（庄家视角）, 案例验证表（持续更新） (+6 more)

### Community 30 - "check_consistency.py"
Cohesion: 0.22
Nodes (12): dataclasses, Path, Pattern, re, Finding, is_ignored_line(), iter_text_files(), main() (+4 more)

### Community 31 - "AGENTS.md - 足彩分析工作流操作手册"
Cohesion: 0.05
Nodes (37): 1. 庄家运作的底层逻辑（庄家第一性原理）, 2. 站在庄家视角精准预测「胜平负」的核心方法, AGENTS.md - 足彩分析工作流操作手册, Subagent 注意事项, 一、工作流程总览, 七、红线与安全, 三、技能流程指引, 不使用 Subagent 的情况 (+29 more)

### Community 32 - "下注决策手册（版本 1）"
Cohesion: 0.06
Nodes (34): 10.1 串关：用 EV 和相关性约束, 10.2 特殊盘口的期望拆分, 1.1 必须直接跳过的场次（乱局）, 2.1 用泊松算出基础概率, 2.2 欧指平均：胜平负 EV, 2.3 欧指平均：大小球 EV（可选）, 3.1 平博：尖锐参考盘（胜平负 / 亚盘 / 大小球）, 3.2 亚盘四家：澳彩 / 皇冠 / Bet365 / 易胜博 (+26 more)

### Community 33 - "联赛配置手册（泊松 + 盘口）"
Cohesion: 0.17
Nodes (11): 3.1 在 λ 与风格判定中的使用, 3.2 在比分权重与大小球中的使用, 3.3 在盘深 / 盘浅判断中的使用, 4.1 荷乙, 4.2 意乙, 一、为什么要按联赛配置？, 三、如何在现有手册中使用联赛配置, 二、每个联赛需要配置哪些东西？ (+3 more)

### Community 34 - "poisson_lib.py"
Cohesion: 0.23
Nodes (12): math, clamp_lambda(), implied_line_half(), LambdaBounds, load_params(), OUAnchor, OUSearch, _parse_score_key() (+4 more)

### Community 35 - "scripts"
Cohesion: 0.15
Nodes (12): engines, node, name, private, scripts, analyze, review, schedule (+4 more)

### Community 36 - "赔率与泊松比较：何时值得下注（案例详解）"
Cohesion: 0.21
Nodes (11): 总结：怎么比较才叫“值得下注”, 案例一：布伦特福德 vs 狼队（真实赔率）, 案例三：巴列卡诺 vs 莱万特（假设赔率：主略被低估）, 案例二：赫尔蒙德 vs 坎布尔（假设赔率：主队被低估）, 步骤 1：赔率 → 隐含概率, 步骤 1：赔率 → 隐含概率, 步骤 2：逐项比较, 步骤 2：逐项比较 (+3 more)

### Community 37 - "执行步骤"
Cohesion: 0.29
Nodes (7): 执行步骤, 步骤 1：检查脚本目录, 步骤 2：运行脚本同步赛程, 步骤 3：解析脚本输出, 步骤 4：格式化输出并写入 memory, 步骤 5：结构化输出, 步骤 6：写入每日记忆

### Community 38 - "执行步骤"
Cohesion: 0.17
Nodes (12): 执行步骤, 步骤 1：读取推荐记录, 步骤 2：获取比赛结果, 步骤 3.5：分析质量自评（泊松模型质量）, 步骤 3：逐场核对, 步骤 4.5：反事实分析, 步骤 4：分析复盘（逐场，不只看未命中）, 步骤 5：计算统计 (+4 more)

### Community 39 - "案例 31（狂砸低平2.65掩护天价冷负案）：平赔砸穿至2.65做终极蜜罐，负赔暴拉+0.62真空偷鸡【负3.55与让负1.53通杀案】"
Cohesion: 0.15
Nodes (13): 案例 31（狂砸低平2.65掩护天价冷负案）：平赔砸穿至2.65做终极蜜罐，负赔暴拉+0.62真空偷鸡【负3.55与让负1.53通杀案】, 案例 32（客让半球高水让负诱穿暗杀让平案）：客胜1.83锁定，让负4.80狂降至4.15高水诱穿，让平4.00高悬暗杀【负1.83与让平3.97通杀案】, 案例 33（让胜反超定格最低项穿盘大捷案）：初盘让胜2.50最高，终盘暴砍至2.19反超定格全盘最低【胜1.29与让胜2.19大胜案】, 案例 34（让平相对斜率真防守大捷案）：让平连续暴跌4档砸至3.15，降幅为让胜2.1倍锁定小胜【胜1.56与让平3.15案】, 案例 35（初盘让平3.85天堑与让胜砸破2.00真穿盘案）：初盘让平3.85如铁，让胜砸破2.00定格全盘最低【胜1.33与让胜1.95大捷案】, 案例 36（平半弱让让负毒诱饵与让平独降杀局案）：主胜2.05死水，让负1.59毒诱饵屠杀串关，让平独降3.75小胜通杀【胜2.05与让平3.75通杀案】, 案例 37（深V洗盘诱空与1.40毒诱饵杀局案）：主胜2.45暴砍2.20深V破位，让负1.40毒诱饵全网屠戮，让平4.50天价通杀【胜2.20与让平4.50通杀案】, 案例 38（初盘让平3.72天堑与让胜单调下砸穿盘案）：胜赔1.42连砸1.34，让平3.72死焊否定小胜，让胜2.22砸至2.06真穿盘【胜1.34与让胜2.06双红案】 (+5 more)

### Community 40 - "verify_poisson.py"
Cohesion: 0.28
Nodes (11): argparse, 泊松比分预测模型 (Dixon-Coles & Poisson Modeling), pathlib, main(), anchor_lambda_tot(), format_top(), poisson_pmf(), Light OU anchor. Returns (L1', L2', lambda_tot_raw, lambda_tot_anchored). (+3 more)

### Community 41 - "巴列卡诺 vs 莱万特：泊松 + 盘口综合实战案例"
Cohesion: 0.18
Nodes (10): 2.1 初盘 EV 计算, 2.2 即时盘 EV 计算, 3.1 泊松对 2.5 球线的看法, 3.2 多家公司大小球盘口（2.5 球）走势概览, 3.3 是否有大小球价值？, 一、基础信息与泊松结果（来自 `006-巴列卡诺-vs-莱万特-泊松分析.md`）, 三、大小球 2.5：走势 + 泊松判断, 二、胜平负：欧指平均 vs 泊松（价值判断） (+2 more)

### Community 42 - "基本面（分析页）"
Cohesion: 0.18
Nodes (10): 下一步, 交锋往绩, 伤停, 基本面（分析页）, 已获取数据, 待抓取, 深度分析进度 - 2950955 里斯本 vs 博德闪耀, 状态 (+2 more)

### Community 43 - "一、发现的 BUG / 漏洞"
Cohesion: 0.18
Nodes (10): 1. 编排写入深度分析时可能覆盖当日已有场次（中）, 2. 「去掉第3场」后精选用的列表未持久化（中）, 3. 初筛 0 场时编排写入的 ## 推荐格式未统一（低）, 4. 复盘时 memory 文件不存在未明确（低）, 5. 深度分析「此场已分析」时的行为未定义（低）, 6. 浏览器共享导致并行 worker 数据串号（高 — 待解决）, 一、发现的 BUG / 漏洞, 三、建议修改优先级 (+2 more)

### Community 44 - "generate_deep_graph.py"
Cohesion: 0.18
Nodes (8): graphify_analyze, graphify_cluster, graphify_export, graphify_report, json, networkx, os, run_deep_graphify()

### Community 45 - "赔率分析推演：庄家操盘逻辑与双盘联动推演心法"
Cohesion: 0.17
Nodes (20): 赔率分析推演：庄家操盘逻辑与双盘联动推演心法, 五、 彻底杜绝推演反复犯错的三大定量物理门禁（根治二元钟摆与阴谋论妄想症）, 公理 10：让盘双弃与平半毒诱饵分水岭（深盘双弃抹杀主胜 vs 平半毒诱饵杀让负）, 公理 1：超低平（< 3.00）防御一致性检验（全周期低平真闷平 vs 诱平蜜罐杀冷负）, 公理 2：极低赔（< 1.30）四轨分流与反弹回踩鉴别标尺（真穿盘 / 杀冷平 / 杀让平）, 公理 3：让平下挫辨识标尺（真防一球小胜 vs 假防小胜真大胜穿盘）, 公理 4：受让胜低锁 + 让负暴拉，下盘不败铁律, 公理 5：假崩盘赶客与毒诱饵定律（仅限有代差让球盘，严禁用于均势盘） (+12 more)

### Community 46 - "recommendation/SKILL.md"
Cohesion: 0.29
Nodes (5): 变动历史分析示例（亚盘，必须像这样写）, 第 7 步：进球数赔率分析, USER.md - About Your Human, 投注偏好, 输出偏好

### Community 47 - "二、建议修补的漏洞 / 不一致"
Cohesion: 0.20
Nodes (9): 1. MEMORY.md 中 CLV 用词与「各玩法」不统一, 2. 主会话「无赛程时」行为略模糊, 3. 两套比分时「比分首选」未约定, 4. 已分析过再分析：询问 vs 跳过, 一、已确认一致的部分, 三、可选优化（非漏洞）, 二、建议修补的漏洞 / 不一致, 四、小结 (+1 more)

### Community 48 - "每日检查（daily-check）"
Cohesion: 0.20
Nodes (9): 何时使用, 前提条件, 执行步骤, 步骤 1：获取今日日期与时间范围, 步骤 2：拉取日历/待办/通知, 步骤 3：汇总并格式化, 步骤 4：（可选）写入 memory, 每日检查（daily-check） (+1 more)

### Community 49 - "执行步骤"
Cohesion: 0.20
Nodes (9): 何时使用, 前提条件, 执行步骤, 数据抓取（data-fetch）, 步骤 1：确认数据源与范围, 步骤 2：执行抓取, 步骤 3：解析与校验, 步骤 4：输出与落盘（可选） (+1 more)

### Community 50 - "执行步骤"
Cohesion: 0.20
Nodes (9): 何时使用, 前提条件, 执行步骤, 报告生成（report-generate）, 步骤 1：确定报告类型与输入来源, 步骤 2：收集与筛选内容, 步骤 3：按模板组织报告, 步骤 4：输出与留痕 (+1 more)

### Community 51 - "1. 不变量一：初赔骨架定位律（Bone Invariant：初盘定能量场）"
Cohesion: 0.20
Nodes (10): 1. 不变量一：初赔骨架定位律（Bone Invariant：初盘定能量场）, 2. 不变量二：让球盘成本刚性门禁（Gate Invariant：让球查真敞口）, 3. 不变量三：散户羊群心理逆向审查（Flow Invariant：诱饵反推正解）, 4. 不变量四：做市商极小化损失与利润最大化闭环解（Minimax Liability & Optimal Payout Invariant）, 5. 双盘联动统一博弈模型（与庄共舞：胜平负 × 让球盘条件概率矩阵与交叉破译）, 一、 盘口动力学统一智慧心法：超越个案死板记忆的四大物理不变量, 二、 五大经典实战盘口复盘, 案例 1：低赔造胆杀平局【澳大利亚 1:1 巴西】（周五003） (+2 more)

### Community 52 - "案例 55（初盘<1.35与让胜单调破2.00真穿盘案）：胜1.33砸至1.31，平负双清退，让胜2.05砸入2.00真避险【胜1.31与让胜2.00穿盘双红案】"
Cohesion: 0.22
Nodes (9): 案例 55（初盘<1.35与让胜单调破2.00真穿盘案）：胜1.33砸至1.31，平负双清退，让胜2.05砸入2.00真避险【胜1.31与让胜2.00穿盘双红案】, 案例 56（客让盘砸让平诱小胜与让负升水阻上穿盘案）：客负1.81锁定，让平暴跌-0.25做蜜罐，让负3.47升水阻上大胜【客负1.81与让负3.47穿盘通杀案】, 案例 57（平赔单边狂砸至2.55成全盘第一低赔案）：平赔暴跌8档至2.55反超胜负，让负1.60锁死闷平【平局2.55与让负1.60双红案】, 案例 58（客胜回踩造死胆与终盘胜平并列杀局案）：客胜1.69回踩1.72拒降，让胜1.85独降锁不败【平局3.65与让胜1.85双红案】, 案例 59（客胜崩盘平赔狂砸2.72与受让独降杀局案）：客负2.05暴涨2.44崩盘，平赔狂砸2.72锁闷平【平局2.72与让胜1.53双红案】, 案例 60（半一盘主胜升水虚晃与客负跳水诱下杀局案）：主胜1.62升水1.70赶客，客负砸至3.90诱下盘，让负1.99升水杀让平【主胜1.70与让平3.50双红案】, 案例 61（均势客优盘做空诱主与客负暴拉真空杀局案）：均势初盘负2.45微优，主砸2.32与让胜1.35造神级毒饵，客负暴拉2.68通杀【客负2.68与让平4.45双红案】, 案例 62（平半让负毒诱饵与让平死焊小胜杀局案）：主胜2.01破二入1.97锁定，让负1.64毒诱饵，让平3.80死焊通杀【主胜1.97与让平3.80双红案】 (+1 more)

### Community 53 - "parseCrowFullIndexData"
Cohesion: 0.33
Nodes (9): alignedOddsRow(), findTableByLabel(), parseCrowCorrectScores(), parseCrowFullIndexData(), parseCrowGoalBands(), parseCrowTeamTotals(), reverseScore(), tableRows() (+1 more)

### Community 54 - "精选推荐与串关决策 (Recommendation & Parlay Strategy)"
Cohesion: 0.22
Nodes (7): 足球庄家倍率精算师 (Persona / Role), 赔率分析推演铁律 (A+B 推演准则), 赛后复盘与记忆沉淀 (Post Review & Memory System), 精选推荐与串关决策 (Recommendation & Parlay Strategy), 球探数据采集引擎 (sporttery-sniper), 十步盘赔深度分析法 (10-step Deep Analysis), 主人 (User / Master Decision Maker)

### Community 55 - "4 家一致的“操盘手法一致”识别（亚盘专用）"
Cohesion: 0.33
Nodes (5): OpenClaw 示例：AGENTS.md + Skills 结构模板, 如何使用, 目录结构, 相关文档, 4 家一致的“操盘手法一致”识别（亚盘专用）

### Community 56 - "三、逐场分析（按流程执行）"
Cohesion: 0.12
Nodes (15): 001 赫尔蒙德 vs 坎布尔, 002 克雷莫纳 vs 佛罗伦萨, 003 阿纳西 vs 特鲁瓦, 004 布伦特福德 vs 狼队, 005 朴茨茅斯 vs 德比郡, 006 巴列卡诺 vs 莱万特, 一、统一流程（学习用）, 三、逐场分析（按流程执行） (+7 more)

### Community 57 - "AGENTS.md — 工作区操作手册（提纲模板）"
Cohesion: 0.22
Nodes (8): AGENTS.md — 工作区操作手册（提纲模板）, 一、工作流程总览, 七、可配置参数（可选）, 三、红线与安全, 二、记忆与写入规则, 六、群聊与心跳（可选）, 四、内外边界, 零、会话启动

### Community 58 - "执行步骤"
Cohesion: 0.33
Nodes (6): 执行步骤, 步骤 1：逐场推送分析报告（内容格式规范）, 步骤 2：精选（全部分析完成后执行）, 步骤 3：生成汇总消息（含精选 + 串关建议）, 步骤 4：推送汇总, 步骤 5：写入记忆

### Community 59 - "盘口分类体系（主人亲授 · 2026-03-18）"
Cohesion: 0.22
Nodes (9): 一、盘口大类, 三、浅盘三种形态（重点）, 二、错盘分类, 五、分析框架（完整版）, 六、案例记录, 四、其他错盘类型, 浅盘阻上 vs 浅盘诱上 对比, 盘口分类体系（主人亲授 · 2026-03-18） (+1 more)

### Community 60 - "案例 44（半球生死盘诱主杀闷平案）：主胜1.90半球热胆，让胜3.95否定穿盘，平赔3.22通杀主胜【平3.22与让负1.70双红案】"
Cohesion: 0.18
Nodes (11): 案例 44（半球生死盘诱主杀闷平案）：主胜1.90半球热胆，让胜3.95否定穿盘，平赔3.22通杀主胜【平3.22与让负1.70双红案】, 案例 45（初盘让负最小与主崩平降通杀案）：(-1)让负1.65初盘最小定性主不胜，平降至3.10直取平局【平3.10与让负1.56双红案】, 案例 46（初让胜最小阻上杀平案）：(+1)让胜2.10初盘最小锁死客不胜，升水2.23阻上客降1.48诱多【平4.20与让胜2.23双红案】, 案例 47（初让负最小均势杀平案）：(-1)让负1.44初盘最小锁死主不胜，均势两头分流杀平局【平3.34与让负1.44双红案】, 案例 48（极低神胆回踩与诱穿杀冷平案）：胜1.20升水拒破，平5.75回踩避险，让胜1.62蜜罐杀全盘【平5.75与让负3.65通杀案】, 案例 49（让平独跌3.35与公理三小胜真防案）：主胜1.83坚挺，让平独降至3.35锁一球小胜【胜1.83与让平3.35通杀案】, 案例 50（主胜微降诱多与负赔暴拉真空案）：主胜1.66造神胆，负赔暴拉3.85赶客制造真空【客负3.85与让负1.94通杀案】, 案例 51（公理三形态二与让平相对斜率真防守案）：主胜砸破1.60，让平跳水-0.23达让胜两倍入3.15【胜1.56与让平3.15双红案】 (+3 more)

### Community 61 - "深度分析推送通知模板"
Cohesion: 0.25
Nodes (7): 1. 标题与场次信息（首段开头）, 2. 分析过程（第 1～3 段，可多段）, 3. 结论（最后一段，必须含以下全部）, 一、推送结构总览, 三、检查清单（主人/复盘用）, 二、必含块与顺序, 深度分析推送通知模板

### Community 62 - "四、模拟示例（周日 018 巴萨 vs 塞维利亚）"
Cohesion: 0.18
Nodes (11): 四、模拟示例（周日 018 巴萨 vs 塞维利亚）, 【深度分析 周日 018 第 1 段/共 5 段】, 【深度分析 周日 018 第 2 段/共 5 段】, 【深度分析 周日 018 第 3 段/共 5 段】, 【深度分析 周日 018 第 4 段/共 5 段】, 【深度分析 周日 018 第 5 段/共 5 段】, 2.1 盘口数据, 2.2 判断实盘 or 错盘 (+3 more)

### Community 63 - "深度分析（deep-analysis）"
Cohesion: 0.15
Nodes (13): 异常处理, 数据抓取方式（强制）, 数据源限流/网络异常, 方式 1：来自初筛流程（默认）, 方式 2：主人指定比赛 ID, 方式 3：主人提供分析页 URL, 方式 4：主人指定竞彩编号, 深度分析（deep-analysis） (+5 more)

### Community 64 - "执行流程"
Cohesion: 0.25
Nodes (8): 执行流程, 阶段 0：预处理与标签, 阶段 1：联赛层级筛选, 阶段 2：时间与信息可获性, 阶段 3：杯赛、战意与特殊标记, 阶段 4：基本面与伤情 → 自开盘, 阶段 5：各公司盘口对比 → 认证 → 关键点/疑点/核心矛盾, 阶段 6：综合排序与数量控制

### Community 65 - "赛后复盘（post-review）"
Cohesion: 0.25
Nodes (7): 比赛取消/推迟, 比赛未全部完场, 特殊场景, 赛后复盘（post-review）, 输入, 输出, 首次复盘（无历史数据）

### Community 66 - "003 场完整分析案例（2026-03-18 反思）"
Cohesion: 0.25
Nodes (8): 003 场完整分析案例（2026-03-18 反思）, 8 维度完整分析, 关键信号识别, 反思（核心教训）, 实际结果：1-1 平局 ✅, 比赛信息, 盘赔分析, 综合判断

### Community 67 - "2784765 场（意甲 拉齐奥 1-0 AC 米兰）复盘总结"
Cohesion: 0.25
Nodes (8): 2784765 场（意甲 拉齐奥 1-0 AC 米兰）复盘总结, 主人点评, 亚盘数据, 基本面 8 维度, 核心教训, 浅盘形态判断, 盘口类型判断, 赛果验证

### Community 68 - "案例 20（拉马努金注意到与相对斜率双降穿盘案）：初盘胜平同值3.30，让负狂砍0.28远超让平【客负1.70与让负3.52穿盘大捷案】"
Cohesion: 0.18
Nodes (11): 案例 20（拉马努金注意到与相对斜率双降穿盘案）：初盘胜平同值3.30，让负狂砍0.28远超让平【客负1.70与让负3.52穿盘大捷案】, 案例 21（破2.00诱穿盘与拉让平至4.00赶客双杀案）：客胜1.20砸破2.00诱穿暗杀让平【客负1.20与让平4.00案】, 案例 22（中盘优势拉让平诱穿盘暗杀让平案）：主胜1.53拉高让平至3.51赶客，降让胜诱穿暗杀让平【主胜1.53与让平3.51通杀案】, 案例 23（让盘双弃与客队唯一下砸大捷案）：让胜4.15+让平3.75判主胜死刑，客负3.06破位【客负3.06与让负1.61双红案】, 案例 24（中盘低水让平蜜罐杀大胜穿盘案）：让平砸破3.10做蜜罐，让胜暴拉3.40制造真空【主胜1.59与让胜3.40大胜通杀案】, 案例 25（客让转主让攻守易势案）：受让胜1.52锁死不败，主胜狂砍0.24反客为主【主胜2.50与让胜1.52双红案】, 案例 26（极端低平2.75真防守与让盘双弃案）：平赔暴跌至2.75真闷平，让球双弃锁死让负【平局2.75与让负1.40双红案】, 案例 27（超低平全周期锁死<3.00杀主胜案）：平赔全流程处于<3.00禁区，破2.00虚诱主胜暗杀平局【平局2.95与让负1.59通杀案】 (+3 more)

### Community 69 - "第 4 段：大小球 + 第 6-10 步摘要"
Cohesion: 0.29
Nodes (7): 第 10 步：泊松比分建模, 第 4 段：大小球 + 第 6-10 步摘要, 第 5 步：进球数赔率分析, 第 6 步：赔率合理性评估, 第 7 步：赔率变动解读, 第 8 步：关键点/疑点/矛盾, 第 9 步：风险提示

### Community 70 - "案例 3：慢跌诱强杀冷负【格鲁吉亚 0:1 北爱尔兰】（周五006）"
Cohesion: 0.33
Nodes (6): 案例 3：慢跌诱强杀冷负【格鲁吉亚 0:1 北爱尔兰】（周五006）, 案例 4：双盘背离破单关【马德里竞技 2:1 皇家马德里】（周日016）, 案例 5（假防平真杀客胜）：平跌破3.00做蜜罐，客胜2.40升水阻上【客胜2.40与让平4.05案】, 案例 6（假崩盘赶客杀主胜）：主胜暴涨制造恐慌，让负1.45毒诱饵杀主胜【诺茨郡 2:1 格里姆斯比】, 案例 7（声东击西穿深盘）：降让平掩护让胜大胜【胜赔破1.85穿盘案】, 案例 8（双向引流暗度陈仓）：客死水平微降分流，主胜2.70升水阻上【主胜2.70反杀案】

### Community 71 - "sporttery-sniper"
Cohesion: 0.29
Nodes (6): sporttery-sniper, 使用方式, 抓取范围, 数据注意事项, 部署, 验证

### Community 72 - "推荐输出（recommendation）"
Cohesion: 0.29
Nodes (7): 推荐输出（recommendation）, 无推荐场景, 特殊场景处理, 用户要求调整, 用户追问单场, 输入, 输出

### Community 73 - "核心工具：sporttery-sniper"
Cohesion: 0.29
Nodes (7): 数据安全规则, 数据范围, 核心工具：sporttery-sniper, 赛后复盘数据抓取, 赛程同步, 运行环境, 验证脚本

### Community 74 - "赛程抓取（match-scraper）"
Cohesion: 0.40
Nodes (5): 异常处理, 查看其他日期赛程, 赛程抓取（match-scraper）, 输出, 销售窗口检查（定时任务触发时必须执行）

### Community 75 - "三、 赔率分析推演十大公理（胜平负 + 让球联动）"
Cohesion: 0.20
Nodes (10): 三、 赔率分析推演十大公理（胜平负 + 让球联动）, 案例 65（让球双升清退唯一下砸穿盘大捷案）：客负1.27微升1.31洗盘，平赔跳水虚诱，让负2.10唯一下砸穿盘【客负1.31与让负2.10双红案】, 案例 66（让平独跌3.25与主胜微升诱下杀局案）：主胜1.39升1.45虚晃赶客，让平3.25唯一下砸锁小胜【主胜1.45与让平3.25双红案】, 案例 67（拉马努金客负断崖与让胜蜜罐杀大冷案）：胜1.26突升1.29，客负暴跌-0.45内幕抢筹，让负2.96通杀全盘【客负6.75与让负2.96惊天大冷案】, 案例 68（双盘条件集合交集与客负虚热杀主胜案）：初让胜1.62锁主不败，平赔3.98排除平局，唯一交集直取主胜【主胜2.74与让胜1.64双红案】, 案例 69（高平大球让平独降杀让负蜜罐案）：平赔4.05天堑排除闷平，胜回落2.01防守，让平独降4.22通杀让负【胜2.01与让平4.22通杀案】, 案例 70（V型诱下盘反手全线关门穿盘案）：胜赔探底1.81关门，平负两端升水弃守，让胜3.32领跌大胜穿盘【胜1.81与让胜3.32大捷案】, 案例 71（超深盘初让平3.83天堑与让胜单边唯一下砸穿盘案）：主胜1.28断层代差，让平3.83飙升3.96弃守，让胜1.90砸至1.87真穿盘【胜1.28与让胜1.87双红案】 (+2 more)

### Community 76 - "三、盘口与走势过滤危险热门"
Cohesion: 0.40
Nodes (5): 8 维度清单（每次分析必须逐项填写）, 为什么必须完整？, ⚠️ 基本面分析强制规则（2026-03-18 主人强调）, 案例：001 场完整分析, 综合评估方法

### Community 77 - "七、下注频率与资金管理（建议版）"
Cohesion: 0.50
Nodes (4): 2.1 判定总进球倾向, 2.2 进攻 / 防守强弱, 2.3 主客场 & 近况修正, 二、从硬数据判定球队风格

### Community 78 - "步骤 1.5：校验脚本赔率与数据完整性"
Cohesion: 0.40
Nodes (5): 1. 确认分析依据公司列表, 2. 赔率数据归属与整理, 3. 赔率数据整理规则, 8. 存档原始赔率数据, 步骤 1.5：校验脚本赔率与数据完整性

### Community 79 - "变动历史分析示例（大小球，必须像这样写）"
Cohesion: 0.40
Nodes (5): 变动历史分析示例（大小球，必须像这样写）, 第 10 步：关键点 / 疑点 / 矛盾分析, 第 11 步：风险提示, 第 8 步：赔率合理性评估, 第 9 步：赔率变动解读

### Community 81 - "写入记忆"
Cohesion: 0.20
Nodes (9): 六阶段赛事初筛流程 (Match Screening Workflow), 4 家一致的“操盘手法一致”识别（大小球专用）, 前提条件, 写入记忆, 初筛本意与分析逻辑, 赛事初筛（match-screening）, 输入, 输出 (+1 more)

### Community 86 - "Heartbeat 检查清单"
Cohesion: 0.50
Nodes (3): Heartbeat 检查清单, 赛前分析补漏, 赛后复盘补漏

### Community 88 - "solve_lambda_for_over_prob"
Cohesion: 0.50
Nodes (4): poisson_cdf_leq(), P(T<=k). Use recurrence to avoid factorial in a loop., Solve λ s.t. P(T > line_half) ≈ p_over, where T ~ Poisson(λ). For half line…, solve_lambda_for_over_prob()

## Knowledge Gaps
- **621 isolated node(s):** `零、会话启动`, `赛程同步（每日 11:10）`, `赛前分析流程（每日 17:00）`, `手动交互模式`, `赛后复盘流程（每日 09:30）` (+616 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 680 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` connect `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` to `第一部分：赛前分析模板`, `盘口与走势阅读手册（简版）`, `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告`, `SOUL.md - 你是谁`, `泊松概率计算手册（足彩用）`, `titan007 抓取 → 缓存层 → 内部 API 化设计方案`, `泊松概率分析：布伦特福德 vs 狼队`, `案例 10（慢跌诱强杀大冷）：客胜慢跌破1.80掩护主胜爆冷【多德勒支 3:2 阿尔梅勒城】`, `SAFETY.md`, `泊松概率分析：赫尔蒙德 vs 坎布尔`, `泊松概率分析：克雷莫纳 vs 佛罗伦萨`, `泊松概率分析：阿纳西 vs 特鲁瓦`, `泊松概率分析：朴茨茅斯 vs 德比郡`, `泊松概率分析：巴列卡诺 vs 莱万特`, `Agent（pansuan）— OpenClaw 足彩分析师 Agent`, `OpenClaw：AGENTS.md 与 Skills 说明`, `深度分析报告：马洛卡 VS 西班牙人`, `模型扩展与组合手册（除泊松之外）`, `累计战绩`, `球队风格判定手册（简版）`, `titan007 欧冠杯 CupMatch c103.js 数据结构分析`, `比分建模与投注手册（泊松版）`, `执行流程`, `下注决策手册（版本 1）`, `联赛配置手册（泊松 + 盘口）`, `赔率与泊松比较：何时值得下注（案例详解）`, `执行步骤`, `案例 31（狂砸低平2.65掩护天价冷负案）：平赔砸穿至2.65做终极蜜罐，负赔暴拉+0.62真空偷鸡【负3.55与让负1.53通杀案】`, `巴列卡诺 vs 莱万特：泊松 + 盘口综合实战案例`, `基本面（分析页）`, `一、发现的 BUG / 漏洞`, `recommendation/SKILL.md`, `二、建议修补的漏洞 / 不一致`, `每日检查（daily-check）`, `执行步骤`, `执行步骤`, `1. 不变量一：初赔骨架定位律（Bone Invariant：初盘定能量场）`, `案例 55（初盘<1.35与让胜单调破2.00真穿盘案）：胜1.33砸至1.31，平负双清退，让胜2.05砸入2.00真避险【胜1.31与让胜2.00穿盘双红案】`, `精选推荐与串关决策 (Recommendation & Parlay Strategy)`, `4 家一致的“操盘手法一致”识别（亚盘专用）`, `三、逐场分析（按流程执行）`, `AGENTS.md — 工作区操作手册（提纲模板）`, `执行步骤`, `案例 44（半球生死盘诱主杀闷平案）：主胜1.90半球热胆，让胜3.95否定穿盘，平赔3.22通杀主胜【平3.22与让负1.70双红案】`, `四、模拟示例（周日 018 巴萨 vs 塞维利亚）`, `执行流程`, `案例 20（拉马努金注意到与相对斜率双降穿盘案）：初盘胜平同值3.30，让负狂砍0.28远超让平【客负1.70与让负3.52穿盘大捷案】`, `案例 3：慢跌诱强杀冷负【格鲁吉亚 0:1 北爱尔兰】（周五006）`, `sporttery-sniper`, `核心工具：sporttery-sniper`, `赛程抓取（match-scraper）`, `三、 赔率分析推演十大公理（胜平负 + 让球联动）`, `写入记忆`, `Heartbeat 检查清单`?**
  _High betweenness centrality (0.464) - this node is a cross-community bridge._
- **Why does `执行流程` connect `执行流程` to `titan007.js`, `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告`, `titan007 抓取 → 缓存层 → 内部 API 化设计方案`, `深度分析报告：马洛卡 VS 西班牙人`, `球队风格判定手册（简版）`, `poisson_lib.py`, `基本面（分析页）`, `一、发现的 BUG / 漏洞`, `赔率分析推演：庄家操盘逻辑与双盘联动推演心法`, `recommendation/SKILL.md`, `二、建议修补的漏洞 / 不一致`, `4 家一致的“操盘手法一致”识别（亚盘专用）`, `执行步骤`, `四、模拟示例（周日 018 巴萨 vs 塞维利亚）`, `深度分析（deep-analysis）`, `执行流程`, `步骤 1.5：校验脚本赔率与数据完整性`, `变动历史分析示例（大小球，必须像这样写）`, `写入记忆`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `4 家一致的“操盘手法一致”识别（亚盘专用）` connect `4 家一致的“操盘手法一致”识别（亚盘专用）` to `盘口与走势阅读手册（简版）`, `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告`, `titan007.test.js`, `泊松概率计算手册（足彩用）`, `titan007 抓取 → 缓存层 → 内部 API 化设计方案`, `泊松概率分析：布伦特福德 vs 狼队`, `泊松概率分析：赫尔蒙德 vs 坎布尔`, `泊松概率分析：克雷莫纳 vs 佛罗伦萨`, `泊松概率分析：阿纳西 vs 特鲁瓦`, `泊松概率分析：朴茨茅斯 vs 德比郡`, `泊松概率分析：巴列卡诺 vs 莱万特`, `OpenClaw：AGENTS.md 与 Skills 说明`, `深度分析报告：马洛卡 VS 西班牙人`, `模型扩展与组合手册（除泊松之外）`, `球队风格判定手册（简版）`, `titan007 欧冠杯 CupMatch c103.js 数据结构分析`, `比分建模与投注手册（泊松版）`, `执行流程`, `TOOLS.md`, `下注决策手册（版本 1）`, `联赛配置手册（泊松 + 盘口）`, `poisson_lib.py`, `赔率与泊松比较：何时值得下注（案例详解）`, `巴列卡诺 vs 莱万特：泊松 + 盘口综合实战案例`, `基本面（分析页）`, `一、发现的 BUG / 漏洞`, `赔率分析推演：庄家操盘逻辑与双盘联动推演心法`, `recommendation/SKILL.md`, `二、建议修补的漏洞 / 不一致`, `每日检查（daily-check）`, `执行步骤`, `执行步骤`, `精选推荐与串关决策 (Recommendation & Parlay Strategy)`, `三、逐场分析（按流程执行）`, `AGENTS.md — 工作区操作手册（提纲模板）`, `四、模拟示例（周日 018 巴萨 vs 塞维利亚）`, `写入记忆`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 63 inferred relationships involving `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` (e.g. with `泊松概率分析：赫尔蒙德 vs 坎布尔` and `泊松概率分析：克雷莫纳 vs 佛罗伦萨`) actually correct?**
  _`赔率分析推演：庄家操盘逻辑与双盘联动推演心法` has 63 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `4 家一致的“操盘手法一致”识别（亚盘专用）` (e.g. with `泊松概率分析：赫尔蒙德 vs 坎布尔` and `泊松概率分析：克雷莫纳 vs 佛罗伦萨`) actually correct?**
  _`4 家一致的“操盘手法一致”识别（亚盘专用）` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `累计战绩` (e.g. with `泊松概率分析：赫尔蒙德 vs 坎布尔` and `泊松概率分析：克雷莫纳 vs 佛罗伦萨`) actually correct?**
  _`累计战绩` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `执行步骤` (e.g. with `泊松概率分析：赫尔蒙德 vs 坎布尔` and `泊松概率分析：克雷莫纳 vs 佛罗伦萨`) actually correct?**
  _`执行步骤` has 19 INFERRED edges - model-reasoned connections that need verification._