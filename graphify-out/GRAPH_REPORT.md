# Graph Report - 倍率分析推演  (2026-09-29)

## Corpus Check
- 45 files · ~158,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1177 nodes · 1802 edges · 91 communities (90 shown, 1 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 304 edges (avg confidence: 0.92)
- Token cost: 12,500 input · 3,500 output

## Community Hubs (Navigation)
- titan007.js
- 第一部分：赛前分析模板
- 盘口与走势阅读手册（简版）
- [欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告
- titan007.test.js
- AGENTS.md - 足彩分析工作流操作手册
- 泊松概率计算手册（足彩用）
- titan007 抓取 → 缓存层 → 内部 API 化设计方案
- 泊松概率分析：布伦特福德 vs 狼队
- 赔率分析推演：庄家操盘逻辑与双盘联动推演心法
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
- 各场景的 Subagent 用法
- 下注决策手册（版本 1）
- 联赛配置手册（泊松 + 盘口）
- poisson_lib.py
- scripts
- 赔率与泊松比较：何时值得下注（案例详解）
- 赛程抓取（match-scraper）
- 执行步骤
- 案例 27（超低平全周期锁死<3.00杀主胜案）：平赔全流程处于<3.00禁区，破2.00虚诱主胜暗杀平局【平局2.95与让负1.59通杀案】
- verify_poisson.py
- 巴列卡诺 vs 莱万特：泊松 + 盘口综合实战案例
- 基本面（分析页）
- 一、发现的 BUG / 漏洞
- generate_deep_graph.py
- 五、 彻底杜绝推演反复犯错的三大定量物理门禁（根治二元钟摆与阴谋论妄想症）
- 4 家一致的“操盘手法一致”识别（亚盘专用）
- 二、建议修补的漏洞 / 不一致
- 每日检查（daily-check）
- 执行步骤
- 执行步骤
- 三、 赔率分析推演十大公理（胜平负 + 让球联动）
- 案例 56（客让盘砸让平诱小胜与让负升水阻上穿盘案）：客负1.81锁定，让平暴跌-0.25做蜜罐，让负3.47升水阻上大胜【客负1.81与让负3.47穿盘通杀案】
- parseCrowFullIndexData
- 精选推荐与串关决策 (Recommendation & Parlay Strategy)
- deep-analysis/SKILL.md
- 一、统一流程（学习用）
- AGENTS.md — 工作区操作手册（提纲模板）
- 执行步骤
- 盘口分类体系（主人亲授 · 2026-03-18）
- 案例 47（初让负最小均势杀平案）：(-1)让负1.44初盘最小锁死主不胜，均势两头分流杀平局【平3.34与让负1.44双红案】
- 深度分析推送通知模板
- 四、模拟示例（周日 018 巴萨 vs 塞维利亚）
- 深度分析（deep-analysis）
- 执行流程
- 赛后复盘（post-review）
- 003 场完整分析案例（2026-03-18 反思）
- 2784765 场（意甲 拉齐奥 1-0 AC 米兰）复盘总结
- 案例 19（极低赔拉让平阻客实杀让平案）：主胜1.10诱穿盘暗杀让平【主胜1.10与天价让平3.80案】
- 案例 39（均势微让僵局与平赔领跌杀两头案）：主胜微降未易主（2.51 vs 2.30），平赔降幅超胜赔真防平【平3.38与让胜1.48通杀案】
- 一、工作流程总览
- sporttery-sniper
- 推荐输出（recommendation）
- 核心工具：sporttery-sniper
- parseOddsChangeHistory
- 案例 67（拉马努金客负断崖与让胜蜜罐杀大冷案）：胜1.26突升1.29，客负暴跌-0.45内幕抢筹，让负2.96通杀全盘【客负6.75与让负2.96惊天大冷案】
- 三、盘口与走势过滤危险热门
- 七、下注频率与资金管理（建议版）
- 步骤 1.5：校验脚本赔率与数据完整性
- 变动历史分析示例（大小球，必须像这样写）
- 输入
- 赛事初筛（match-screening）
- 四、Memory 写入规则
- 二、价值扫描（泊松 + 欧指平均）
- 四、让球盘：买上盘还是下盘
- 八、战绩记录与复盘（下一步必须补齐的环节）
- Heartbeat 检查清单
- 第二步：亚盘盘口类型判断（主人亲授体系）
- solve_lambda_for_over_prob
- 八、心跳机制
- Errors Log

## God Nodes (most connected - your core abstractions)
1. `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` - 165 edges
2. `AGENTS.md - 足彩分析工作流操作手册` - 62 edges
3. `4 家一致的“操盘手法一致”识别（亚盘专用）` - 41 edges
4. `累计战绩` - 34 edges
5. `执行步骤` - 32 edges
6. `执行流程` - 27 edges
7. `fetchMatchData()` - 17 edges
8. `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告` - 17 edges
9. `泊松概率分析：布伦特福德 vs 狼队` - 17 edges
10. `buildAnalysisContext()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `LambdaBounds` --calculates_scoreline_lambda--> `4 家一致的“操盘手法一致”识别（亚盘专用）`  [INFERRED]
  scripts/poisson_lib.py → skills/deep-analysis/SKILL.md
- `LambdaBounds` --calculates_scoreline_lambda--> `4 家一致的“操盘手法一致”识别（大小球专用）`  [INFERRED]
  scripts/poisson_lib.py → skills/deep-analysis/SKILL.md
- `LambdaBounds` --calculates_scoreline_lambda--> `变动历史分析示例（亚盘，必须像这样写）`  [INFERRED]
  scripts/poisson_lib.py → skills/deep-analysis/SKILL.md
- `LambdaBounds` --provides_mathematical_scoreline_formulas--> `比分建模与投注手册（泊松版）`  [INFERRED]
  scripts/poisson_lib.py → docs/比分建模与投注手册.md
- `LambdaBounds` --provides_mathematical_scoreline_formulas--> `泊松概率计算手册（足彩用）`  [INFERRED]
  scripts/poisson_lib.py → docs/泊松概率计算手册.md

## Import Cycles
- None detected.

## Communities (91 total, 1 thin omitted)

### Community 0 - "titan007.js"
Cohesion: 0.12
Nodes (32): cleanTeamLabel(), DEFAULT_REQUEST_DELAY_RANGE_MS, extractArrayLiteral(), HANDICAP_NAMES, handicapName(), isPreMatchPhase(), JC_STATE_NAMES, leagueKey() (+24 more)

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
Cohesion: 0.13
Nodes (27): ref_node_assert, ref_node_test, ref_node_url, formatHistoryWindow(), localDateString(), main(), parseCliArgs(), parseFormat() (+19 more)

### Community 5 - "AGENTS.md - 足彩分析工作流操作手册"
Cohesion: 0.09
Nodes (20): 足球庄家倍率精算师 (Persona / Role), 赔率分析推演铁律 (A+B 推演准则), 主人 (User / Master Decision Maker), AGENTS.md - 足彩分析工作流操作手册, 七、红线与安全, 三、技能流程指引, 九、群聊规则, 二、数据来源 (+12 more)

### Community 6 - "泊松概率计算手册（足彩用）"
Cohesion: 0.07
Nodes (28): 10.1 离线拟合思路（以后可精细化）, 10.2 日常使用规则（经验参数版）, 1.1 公式, 1.2 性质, 3.1 所需数据, 3.2 步骤一：基础 λ（仅用主队主场 + 客队客场）, 3.3 步骤二：掺入近六场（加权）, 3.4 步骤三：伤停修正（可选） (+20 more)

### Community 7 - "titan007 抓取 → 缓存层 → 内部 API 化设计方案"
Cohesion: 0.07
Nodes (27): 1. 目标与范围, 2. 整体架构, 3.1 比赛基础信息 `matches`, 3.2 联赛与球队 `leagues` / `teams`, 3.3 赔率时间序列 `odds_snapshots`, 3.4 赛果 `results`, 3. 数据结构设计, 4.1 赛程相关 (+19 more)

### Community 8 - "泊松概率分析：布伦特福德 vs 狼队"
Cohesion: 0.07
Nodes (26): λ 与预期总进球, 一、原始数据整理, 七、总进球数概率, 三、掺入近六场（0.7 主客场 + 0.3 近六场）, 与泊松概率对比, 主队, 主队（λ₁=1.53）, 主队 / 客队进球数 (+18 more)

### Community 9 - "赔率分析推演：庄家操盘逻辑与双盘联动推演心法"
Cohesion: 0.15
Nodes (27): 赔率分析推演：庄家操盘逻辑与双盘联动推演心法, 1. 不变量一：初赔骨架定位律（Bone Invariant：初盘定能量场）, 2. 不变量二：让球盘成本刚性门禁（Gate Invariant：让球查真敞口）, 3. 不变量三：散户羊群心理逆向审查（Flow Invariant：诱饵反推正解）, 4. 不变量四：做市商极小化损失与利润最大化闭环解（Minimax Liability & Optimal Payout Invariant）, 5. 双盘联动统一博弈模型（与庄共舞：胜平负 × 让球盘条件概率矩阵与交叉破译）, 一、 盘口动力学统一智慧心法：超越个案死板记忆的四大物理不变量, 二、 五大经典实战盘口复盘 (+19 more)

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
Cohesion: 0.10
Nodes (19): 1. 是什么, 2. 作用, 2. 加载位置与优先级, 3. 作用, 3. 使用方式, 4. 使用方式, OpenClaw：AGENTS.md 与 Skills 说明, 一、Workspace 里的 AGENTS.md (+11 more)

### Community 18 - "深度分析报告：马洛卡 VS 西班牙人"
Cohesion: 0.10
Nodes (19): Memory 摘要, 深度分析报告：马洛卡 VS 西班牙人, 第 10 步：泊松比分建模, 第 1 步：基本面分析, 第 1 段：基本面 + 伤停 + 自开盘, 第 2 步：伤停分析, 第 2 段：欧指分析, 第 3 步：欧洲指数（胜平负）赔率分析 (+11 more)

### Community 19 - "模型扩展与组合手册（除泊松之外）"
Cohesion: 0.11
Nodes (18): 1.1 双泊松模型（Bivariate Poisson）, 1.2 Dixon–Coles 修正, 2.1 Poisson 回归 / 负二项回归, 3.1 Logistic / 多项 Logit, 3.2 树模型 / 集成模型（Random Forest / XGBoost / LightGBM）, 4.1 多家赔率反演的「综合隐含概率」, 7.1 总体原则, 7.2 程序层（服务 / 库）职责 (+10 more)

### Community 20 - "累计战绩"
Cohesion: 0.12
Nodes (16): 8 维度清单（每次分析必须逐项填写）, MEMORY.md - 长期记忆, 串关统计, 为什么必须完整？, 关键教训, 各玩法命中率, 各联赛命中率, ⚠️ 基本面分析强制规则（2026-03-18 主人强调） (+8 more)

### Community 21 - "buildAnalysisContext"
Cohesion: 0.22
Nodes (17): appendCompanyList(), appendCorrectScoreRows(), appendCrowFullIndex(), appendEuropeCompanyList(), appendEuropeHistories(), appendGroupedHistories(), appendHeadToHead(), appendHistory() (+9 more)

### Community 22 - "球队风格判定手册（简版）"
Cohesion: 0.13
Nodes (14): 2.1 判定总进球倾向, 2.2 进攻 / 防守强弱, 2.3 主客场 & 近况修正, 3.1 长期大小球盘, 3.2 让球盘表现, 5.1 大小球方向, 5.2 比分权重（用在 w(i:j) 上）, 一、你到底需要什么级别的「风格」？ (+6 more)

### Community 23 - "titan007 欧冠杯 CupMatch c103.js 数据结构分析"
Cohesion: 0.13
Nodes (14): arrCup：赛事基础信息, arrCupKind：阶段与轮次定义, arrTeam：球队字典, extraInfo：加时、点球与晋级说明, G：赛程与赛果, jh：核心业务数据, S：分组积分榜, titan007 欧冠杯 CupMatch c103.js 数据结构分析 (+6 more)

### Community 24 - "cleanText"
Cohesion: 0.27
Nodes (15): attrOfFirst(), cleanText(), extractFormation(), findFirstPositiveIndex(), firstMatch(), normalizeCompany(), parseDetailHtml(), parseInjuryPlayers() (+7 more)

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
Cohesion: 0.15
Nodes (13): sessions_spawn — 启动后台 subagent, Subagent 工具, TOOLS.md - 工具使用指南, applyLatestEuropeHistoryToCompanies(), applyLatestHistoryToCompanies(), clearMarketCurrent(), extractArrayFunctionStrings(), isAfterKickoff() (+5 more)

### Community 29 - "盘赔分析系统化框架（2026-03-17 整理 · 主人亲授）"
Cohesion: 0.14
Nodes (14): 001 场案例分析, 判断速查表, 升盘 + 升水的双重性（难点）, 后续行动, 如何区分阻 vs 诱？, 我们的局限与应对, 核心认知（庄家视角）, 案例验证表（持续更新） (+6 more)

### Community 30 - "check_consistency.py"
Cohesion: 0.22
Nodes (12): argparse, dataclasses, Path, Pattern, re, Finding, is_ignored_line(), iter_text_files() (+4 more)

### Community 31 - "各场景的 Subagent 用法"
Cohesion: 0.15
Nodes (13): Subagent 注意事项, 不使用 Subagent 的情况, 主人中途干预, 五、Subagent 编排规则, 各场景的 Subagent 用法, 场景 1：赛前全流程（「给推荐」/ cron 17:00）, 场景 2：手动分析（「分析 2950979」/「帮我看看 A 和 B」/「分析 001」）, 场景 3：赛程同步（cron 11:10 / 手动） (+5 more)

### Community 32 - "下注决策手册（版本 1）"
Cohesion: 0.15
Nodes (12): 10.1 串关：用 EV 和相关性约束, 10.2 特殊盘口的期望拆分, 1.1 必须直接跳过的场次（乱局）, 9.1 明知有 EV 也要放弃的场景, 9.2 在整轮赛程中挑出「必须下」的少数场次, 一、先判定：这场「要不要碰」, 下注决策手册（版本 1）, 九、择机与放弃：有 EV 也可以「不下注」 (+4 more)

### Community 33 - "联赛配置手册（泊松 + 盘口）"
Cohesion: 0.15
Nodes (12): 3.1 在 λ 与风格判定中的使用, 3.2 在比分权重与大小球中的使用, 3.3 在盘深 / 盘浅判断中的使用, 4.1 荷乙, 4.2 意乙, 一、为什么要按联赛配置？, 三、如何在现有手册中使用联赛配置, 二、每个联赛需要配置哪些东西？ (+4 more)

### Community 34 - "poisson_lib.py"
Cohesion: 0.23
Nodes (12): math, clamp_lambda(), implied_line_half(), LambdaBounds, load_params(), OUAnchor, OUSearch, _parse_score_key() (+4 more)

### Community 35 - "scripts"
Cohesion: 0.15
Nodes (12): engines, node, name, private, scripts, analyze, review, schedule (+4 more)

### Community 36 - "赔率与泊松比较：何时值得下注（案例详解）"
Cohesion: 0.21
Nodes (11): 总结：怎么比较才叫“值得下注”, 案例一：布伦特福德 vs 狼队（真实赔率）, 案例三：巴列卡诺 vs 莱万特（假设赔率：主略被低估）, 案例二：赫尔蒙德 vs 坎布尔（假设赔率：主队被低估）, 步骤 1：赔率 → 隐含概率, 步骤 1：赔率 → 隐含概率, 步骤 2：逐项比较, 步骤 2：逐项比较 (+3 more)

### Community 37 - "赛程抓取（match-scraper）"
Cohesion: 0.17
Nodes (12): 异常处理, 执行步骤, 查看其他日期赛程, 步骤 1：检查脚本目录, 步骤 2：运行脚本同步赛程, 步骤 3：解析脚本输出, 步骤 4：格式化输出并写入 memory, 步骤 5：结构化输出 (+4 more)

### Community 38 - "执行步骤"
Cohesion: 0.17
Nodes (12): 执行步骤, 步骤 1：读取推荐记录, 步骤 2：获取比赛结果, 步骤 3.5：分析质量自评（泊松模型质量）, 步骤 3：逐场核对, 步骤 4.5：反事实分析, 步骤 4：分析复盘（逐场，不只看未命中）, 步骤 5：计算统计 (+4 more)

### Community 39 - "案例 27（超低平全周期锁死<3.00杀主胜案）：平赔全流程处于<3.00禁区，破2.00虚诱主胜暗杀平局【平局2.95与让负1.59通杀案】"
Cohesion: 0.17
Nodes (12): 案例 27（超低平全周期锁死<3.00杀主胜案）：平赔全流程处于<3.00禁区，破2.00虚诱主胜暗杀平局【平局2.95与让负1.59通杀案】, 案例 28（均势弱让诱平蜜罐掩护高水穿盘案）：平赔暴跌至3.18做蜜罐，终盘让胜狂砍0.21大破深盘【主胜2.19与让胜4.55通杀案】, 案例 29（平半倒挂诱客杀平局案）：客负易主引流追热，平赔砸入2.80超低水真防平【平局2.83与让负1.43通杀案】, 案例 30（极低赔反弹回踩诱多杀冷平案）：胜赔1.16反复升水回踩，终盘让胜反弹1.64杀冷平【平局5.70与让负3.80通杀案】, 案例 31（狂砸低平2.65掩护天价冷负案）：平赔砸穿至2.65做终极蜜罐，负赔暴拉+0.62真空偷鸡【负3.55与让负1.53通杀案】, 案例 32（客让半球高水让负诱穿暗杀让平案）：客胜1.83锁定，让负4.80狂降至4.15高水诱穿，让平4.00高悬暗杀【负1.83与让平3.97通杀案】, 案例 33（让胜反超定格最低项穿盘大捷案）：初盘让胜2.50最高，终盘暴砍至2.19反超定格全盘最低【胜1.29与让胜2.19大胜案】, 案例 34（让平相对斜率真防守大捷案）：让平连续暴跌4档砸至3.15，降幅为让胜2.1倍锁定小胜【胜1.56与让平3.15案】 (+4 more)

### Community 40 - "verify_poisson.py"
Cohesion: 0.30
Nodes (10): pathlib, main(), anchor_lambda_tot(), format_top(), poisson_pmf(), Light OU anchor. Returns (L1', L2', lambda_tot_raw, lambda_tot_anchored)., score_probs(), main() (+2 more)

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

### Community 45 - "五、 彻底杜绝推演反复犯错的三大定量物理门禁（根治二元钟摆与阴谋论妄想症）"
Cohesion: 0.18
Nodes (11): 五、 彻底杜绝推演反复犯错的三大定量物理门禁（根治二元钟摆与阴谋论妄想症）, 公理 10：让盘双弃与平半毒诱饵分水岭（深盘双弃抹杀主胜 vs 平半毒诱饵杀让负）, 公理 9：低赔易主与真崩盘定律（真崩盘客胜 vs 假易主诱客杀平局）, 六、 双盘联动与庄共舞大一统速查表（全网研报精髓与四维意图矩阵）, 四、 第一性原理动态推演刚性四步顺序流水线（Sequential Pipeline Protocol：彻底终结顺序倒置）, 门禁一：三维强制全景扫描门禁（彻底消灭“非胜即平”二元死穴）, 门禁三：诱平蜜罐 vs 真防平定量标尺门禁（彻底根治“只认破3.00”教条主义）, 门禁二：让球盘双轨成本门禁（用物理数学击碎主观脑补） (+3 more)

### Community 46 - "4 家一致的“操盘手法一致”识别（亚盘专用）"
Cohesion: 0.24
Nodes (8): 六阶段赛事初筛流程 (Match Screening Workflow), 五、与 Skills / TOOLS 的关系, 4 家一致的“操盘手法一致”识别（亚盘专用）, 变动历史分析示例（亚盘，必须像这样写）, 第 7 步：进球数赔率分析, 前提条件, 单场深度分析数据抓取, buildAnalysisUrl()

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

### Community 51 - "三、 赔率分析推演十大公理（胜平负 + 让球联动）"
Cohesion: 0.20
Nodes (10): 三、 赔率分析推演十大公理（胜平负 + 让球联动）, 公理 1：超低平（< 3.00）防御一致性检验（全周期低平真闷平 vs 诱平蜜罐杀冷负）, 公理 2：极低赔（< 1.30）四轨分流与反弹回踩鉴别标尺（真穿盘 / 杀冷平 / 杀让平）, 公理 3：让平下挫辨识标尺（真防一球小胜 vs 假防小胜真大胜穿盘）, 公理 4：受让胜低锁 + 让负暴拉，下盘不败铁律, 公理 5：假崩盘赶客与毒诱饵定律（仅限有代差让球盘，严禁用于均势盘）, 公理 6：相对斜率穿盘定律（让胜降幅远超让平，声东击西大破深盘）, 公理 7：双向引流与升水阻上定律（暗度陈仓杀主胜） (+2 more)

### Community 52 - "案例 56（客让盘砸让平诱小胜与让负升水阻上穿盘案）：客负1.81锁定，让平暴跌-0.25做蜜罐，让负3.47升水阻上大胜【客负1.81与让负3.47穿盘通杀案】"
Cohesion: 0.20
Nodes (10): 案例 56（客让盘砸让平诱小胜与让负升水阻上穿盘案）：客负1.81锁定，让平暴跌-0.25做蜜罐，让负3.47升水阻上大胜【客负1.81与让负3.47穿盘通杀案】, 案例 57（平赔单边狂砸至2.55成全盘第一低赔案）：平赔暴跌8档至2.55反超胜负，让负1.60锁死闷平【平局2.55与让负1.60双红案】, 案例 58（客胜回踩造死胆与终盘胜平并列杀局案）：客胜1.69回踩1.72拒降，让胜1.85独降锁不败【平局3.65与让胜1.85双红案】, 案例 59（客胜崩盘平赔狂砸2.72与受让独降杀局案）：客负2.05暴涨2.44崩盘，平赔狂砸2.72锁闷平【平局2.72与让胜1.53双红案】, 案例 60（半一盘主胜升水虚晃与客负跳水诱下杀局案）：主胜1.62升水1.70赶客，客负砸至3.90诱下盘，让负1.99升水杀让平【主胜1.70与让平3.50双红案】, 案例 61（均势客优盘做空诱主与客负暴拉真空杀局案）：均势初盘负2.45微优，主砸2.32与让胜1.35造神级毒饵，客负暴拉2.68通杀【客负2.68与让平4.45双红案】, 案例 62（平半让负毒诱饵与让平死焊小胜杀局案）：主胜2.01破二入1.97锁定，让负1.64毒诱饵，让平3.80死焊通杀【主胜1.97与让平3.80双红案】, 案例 64（初客优诱主与客负暴拉真空再现案）：均势初盘负2.33微优，主砸2.12与让胜1.40造神级毒饵，客负暴拉2.69通杀【客负2.69与让平4.45双红案】 (+2 more)

### Community 53 - "parseCrowFullIndexData"
Cohesion: 0.29
Nodes (10): alignedOddsRow(), extractCells(), findTableByLabel(), parseCrowCorrectScores(), parseCrowFullIndexData(), parseCrowGoalBands(), parseCrowTeamTotals(), reverseScore() (+2 more)

### Community 54 - "精选推荐与串关决策 (Recommendation & Parlay Strategy)"
Cohesion: 0.28
Nodes (7): 泊松比分预测模型 (Dixon-Coles & Poisson Modeling), 赛后复盘与记忆沉淀 (Post Review & Memory System), 精选推荐与串关决策 (Recommendation & Parlay Strategy), 球探数据采集引擎 (sporttery-sniper), 十步盘赔深度分析法 (10-step Deep Analysis), 4 家一致的“操盘手法一致”识别（大小球专用）, absolutizeVipUrl()

### Community 55 - "deep-analysis/SKILL.md"
Cohesion: 0.22
Nodes (7): 001 赫尔蒙德 vs 坎布尔, 002 克雷莫纳 vs 佛罗伦萨, 003 阿纳西 vs 特鲁瓦, 004 布伦特福德 vs 狼队, 005 朴茨茅斯 vs 德比郡, 006 巴列卡诺 vs 莱万特, 三、逐场分析（按流程执行）

### Community 56 - "一、统一流程（学习用）"
Cohesion: 0.22
Nodes (8): 一、统一流程（学习用）, 二、六场初盘与泊松数据, 初盘赔率与泊松价值分析（001～006）, 四、汇总：哪场哪个值得买, 步骤 1：写出泊松概率, 步骤 2：赔率 → 庄家隐含概率, 步骤 3：逐项比较 + 算期望值, 步骤 4：下结论——哪个值得买

### Community 57 - "AGENTS.md — 工作区操作手册（提纲模板）"
Cohesion: 0.22
Nodes (8): AGENTS.md — 工作区操作手册（提纲模板）, 一、工作流程总览, 七、可配置参数（可选）, 三、红线与安全, 二、记忆与写入规则, 六、群聊与心跳（可选）, 四、内外边界, 零、会话启动

### Community 58 - "执行步骤"
Cohesion: 0.22
Nodes (9): 执行步骤, 步骤 1：逐场推送分析报告（内容格式规范）, 步骤 2：精选（全部分析完成后执行）, 步骤 3：生成汇总消息（含精选 + 串关建议）, 步骤 4：推送汇总, 步骤 5：写入记忆, USER.md - About Your Human, 投注偏好 (+1 more)

### Community 59 - "盘口分类体系（主人亲授 · 2026-03-18）"
Cohesion: 0.22
Nodes (9): 一、盘口大类, 三、浅盘三种形态（重点）, 二、错盘分类, 五、分析框架（完整版）, 六、案例记录, 四、其他错盘类型, 浅盘阻上 vs 浅盘诱上 对比, 盘口分类体系（主人亲授 · 2026-03-18） (+1 more)

### Community 60 - "案例 47（初让负最小均势杀平案）：(-1)让负1.44初盘最小锁死主不胜，均势两头分流杀平局【平3.34与让负1.44双红案】"
Cohesion: 0.22
Nodes (9): 案例 47（初让负最小均势杀平案）：(-1)让负1.44初盘最小锁死主不胜，均势两头分流杀平局【平3.34与让负1.44双红案】, 案例 48（极低神胆回踩与诱穿杀冷平案）：胜1.20升水拒破，平5.75回踩避险，让胜1.62蜜罐杀全盘【平5.75与让负3.65通杀案】, 案例 49（让平独跌3.35与公理三小胜真防案）：主胜1.83坚挺，让平独降至3.35锁一球小胜【胜1.83与让平3.35通杀案】, 案例 50（主胜微降诱多与负赔暴拉真空案）：主胜1.66造神胆，负赔暴拉3.85赶客制造真空【客负3.85与让负1.94通杀案】, 案例 51（公理三形态二与让平相对斜率真防守案）：主胜砸破1.60，让平跳水-0.23达让胜两倍入3.15【胜1.56与让平3.15双红案】, 案例 52（半一盘主胜深V诱多与客负暴拉真空杀局案）：主胜1.88砸至1.74造神胆，客负3.21暴拉3.77真空偷鸡【客负3.77与让负1.78通杀案】, 案例 53（极低神胆诱穿与(-2)让胜做蜜罐杀局案）：主胜1.11超神胆，(-2)让胜2.20诱穿蜜罐，让负2.38天价收割【主胜1.11与让负2.38通杀案】, 案例 54（超深盘极低死胆诱多与客负暴拉8.50惊天通杀案）：主胜1.26造百亿串关死胆，客负暴拉8.50真空偷鸡【客负8.50与让负3.05通杀案】 (+1 more)

### Community 61 - "深度分析推送通知模板"
Cohesion: 0.25
Nodes (7): 1. 标题与场次信息（首段开头）, 2. 分析过程（第 1～3 段，可多段）, 3. 结论（最后一段，必须含以下全部）, 一、推送结构总览, 三、检查清单（主人/复盘用）, 二、必含块与顺序, 深度分析推送通知模板

### Community 62 - "四、模拟示例（周日 018 巴萨 vs 塞维利亚）"
Cohesion: 0.29
Nodes (7): 四、模拟示例（周日 018 巴萨 vs 塞维利亚）, 【深度分析 周日 018 第 1 段/共 5 段】, 【深度分析 周日 018 第 2 段/共 5 段】, 【深度分析 周日 018 第 3 段/共 5 段】, 【深度分析 周日 018 第 4 段/共 5 段】, 【深度分析 周日 018 第 5 段/共 5 段】, 2.1 盘口数据

### Community 63 - "深度分析（deep-analysis）"
Cohesion: 0.25
Nodes (8): 异常处理, 数据抓取方式（强制）, 数据源限流/网络异常, 深度分析（deep-analysis）, 脚本抓取异常, 输出, 部分完成场景, 频率控制

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

### Community 68 - "案例 19（极低赔拉让平阻客实杀让平案）：主胜1.10诱穿盘暗杀让平【主胜1.10与天价让平3.80案】"
Cohesion: 0.25
Nodes (8): 案例 19（极低赔拉让平阻客实杀让平案）：主胜1.10诱穿盘暗杀让平【主胜1.10与天价让平3.80案】, 案例 20（拉马努金注意到与相对斜率双降穿盘案）：初盘胜平同值3.30，让负狂砍0.28远超让平【客负1.70与让负3.52穿盘大捷案】, 案例 21（破2.00诱穿盘与拉让平至4.00赶客双杀案）：客胜1.20砸破2.00诱穿暗杀让平【客负1.20与让平4.00案】, 案例 22（中盘优势拉让平诱穿盘暗杀让平案）：主胜1.53拉高让平至3.51赶客，降让胜诱穿暗杀让平【主胜1.53与让平3.51通杀案】, 案例 23（让盘双弃与客队唯一下砸大捷案）：让胜4.15+让平3.75判主胜死刑，客负3.06破位【客负3.06与让负1.61双红案】, 案例 24（中盘低水让平蜜罐杀大胜穿盘案）：让平砸破3.10做蜜罐，让胜暴拉3.40制造真空【主胜1.59与让胜3.40大胜通杀案】, 案例 25（客让转主让攻守易势案）：受让胜1.52锁死不败，主胜狂砍0.24反客为主【主胜2.50与让胜1.52双红案】, 案例 26（极端低平2.75真防守与让盘双弃案）：平赔暴跌至2.75真闷平，让球双弃锁死让负【平局2.75与让负1.40双红案】

### Community 69 - "案例 39（均势微让僵局与平赔领跌杀两头案）：主胜微降未易主（2.51 vs 2.30），平赔降幅超胜赔真防平【平3.38与让胜1.48通杀案】"
Cohesion: 0.25
Nodes (8): 案例 39（均势微让僵局与平赔领跌杀两头案）：主胜微降未易主（2.51 vs 2.30），平赔降幅超胜赔真防平【平3.38与让胜1.48通杀案】, 案例 40（平手均势诱客造热与临场拉高平赔杀两头案）：初盘2.42对开，客负连降2.26虚热，临场平赔拉高3.38通杀胜负【平3.38与让负1.37通杀案】, 案例 41（极低赔拒破2.00造胆杀天价冷平案）：客负1.32狂降造死胆，让负2.15拒破2.00虚诱大胜，天价冷平4.40通杀全网【平4.40与让胜2.73通杀案】, 案例 42（客负砸破2.00虚假破位诱客杀平局案）：客负2.35连砸破2.00入1.98极致诱客，让胜1.54低位死锁主不败【平3.26与让胜1.54通杀案】, 案例 43（客让未易主胶着与让胜破二真防平案）：客负2.18升水未失主导，让胜砸破2.00入1.85锁主不败，两头分流杀平局【平3.26与让胜1.85通杀案】, 案例 44（半球生死盘诱主杀闷平案）：主胜1.90半球热胆，让胜3.95否定穿盘，平赔3.22通杀主胜【平3.22与让负1.70双红案】, 案例 45（初盘让负最小与主崩平降通杀案）：(-1)让负1.65初盘最小定性主不胜，平降至3.10直取平局【平3.10与让负1.56双红案】, 案例 46（初让胜最小阻上杀平案）：(+1)让胜2.10初盘最小锁死客不胜，升水2.23阻上客降1.48诱多【平4.20与让胜2.23双红案】

### Community 70 - "一、工作流程总览"
Cohesion: 0.29
Nodes (7): 一、工作流程总览, 手动交互模式, 状态推送规则, 赛前分析流程（每日 17:00）, 赛后复盘流程（每日 09:30）, 赛程同步（每日 11:10）, 跳过当日分析

### Community 71 - "sporttery-sniper"
Cohesion: 0.29
Nodes (6): sporttery-sniper, 使用方式, 抓取范围, 数据注意事项, 部署, 验证

### Community 72 - "推荐输出（recommendation）"
Cohesion: 0.29
Nodes (7): 推荐输出（recommendation）, 无推荐场景, 特殊场景处理, 用户要求调整, 用户追问单场, 输入, 输出

### Community 73 - "核心工具：sporttery-sniper"
Cohesion: 0.29
Nodes (7): 数据安全规则, 数据范围, 核心工具：sporttery-sniper, 赛后复盘数据抓取, 赛程同步, 运行环境, 验证脚本

### Community 74 - "parseOddsChangeHistory"
Cohesion: 0.33
Nodes (7): detectHistoryRowFormat(), isHistoryChangeTime(), isHistoryHeaderRow(), isHistoryStatus(), isRollingStatus(), normalizeHistoryRow(), parseOddsChangeHistory()

### Community 75 - "案例 67（拉马努金客负断崖与让胜蜜罐杀大冷案）：胜1.26突升1.29，客负暴跌-0.45内幕抢筹，让负2.96通杀全盘【客负6.75与让负2.96惊天大冷案】"
Cohesion: 0.33
Nodes (6): 案例 67（拉马努金客负断崖与让胜蜜罐杀大冷案）：胜1.26突升1.29，客负暴跌-0.45内幕抢筹，让负2.96通杀全盘【客负6.75与让负2.96惊天大冷案】, 案例 68（双盘条件集合交集与客负虚热杀主胜案）：初让胜1.62锁主不败，平赔3.98排除平局，唯一交集直取主胜【主胜2.74与让胜1.64双红案】, 案例 69（高平大球让平独降杀让负蜜罐案）：平赔4.05天堑排除闷平，胜回落2.01防守，让平独降4.22通杀让负【胜2.01与让平4.22通杀案】, 案例 70（V型诱下盘反手全线关门穿盘案）：胜赔探底1.81关门，平负两端升水弃守，让胜3.32领跌大胜穿盘【胜1.81与让胜3.32大捷案】, 案例 71（超深盘初让平3.83天堑与让胜单边唯一下砸穿盘案）：主胜1.28断层代差，让平3.83飙升3.96弃守，让胜1.90砸至1.87真穿盘【胜1.28与让胜1.87双红案】, 案例 72（极限初低平2.75天堑与主胜假突破反弹杀局案）：平初盘2.75锁闷平，胜砸2.00被拒反弹2.07，让负1.54通杀追胜盘【平2.85与让负1.54双红案】

### Community 76 - "三、盘口与走势过滤危险热门"
Cohesion: 0.40
Nodes (5): 3.1 平博：尖锐参考盘（胜平负 / 亚盘 / 大小球）, 3.2 亚盘四家：澳彩 / 皇冠 / Bet365 / 易胜博, 3.3 欧指客群盘：威廉 / Interwetten / 马会 / 中国竞彩网, 3.4 过滤规则, 三、盘口与走势过滤危险热门

### Community 77 - "七、下注频率与资金管理（建议版）"
Cohesion: 0.40
Nodes (5): 7.1 下注频率：宁少不多, 7.2 单场下注比例：三档 + 上限, 7.3 相关性控制：避免同逻辑赌太多场, 7.4 确定下注前的最后自检, 七、下注频率与资金管理（建议版）

### Community 78 - "步骤 1.5：校验脚本赔率与数据完整性"
Cohesion: 0.40
Nodes (5): 1. 确认分析依据公司列表, 2. 赔率数据归属与整理, 3. 赔率数据整理规则, 8. 存档原始赔率数据, 步骤 1.5：校验脚本赔率与数据完整性

### Community 79 - "变动历史分析示例（大小球，必须像这样写）"
Cohesion: 0.40
Nodes (5): 变动历史分析示例（大小球，必须像这样写）, 第 10 步：关键点 / 疑点 / 矛盾分析, 第 11 步：风险提示, 第 8 步：赔率合理性评估, 第 9 步：赔率变动解读

### Community 80 - "输入"
Cohesion: 0.40
Nodes (5): 方式 1：来自初筛流程（默认）, 方式 2：主人指定比赛 ID, 方式 3：主人提供分析页 URL, 方式 4：主人指定竞彩编号, 输入

### Community 81 - "赛事初筛（match-screening）"
Cohesion: 0.40
Nodes (5): 初筛本意与分析逻辑, 赛事初筛（match-screening）, 输入, 输出, 输出格式

### Community 82 - "四、Memory 写入规则"
Cohesion: 0.50
Nodes (4): 写下来 — 不要"心里记着", 四、Memory 写入规则, 每日记忆（memory/YYYY-MM-DD.md）, 长期记忆（MEMORY.md）

### Community 83 - "二、价值扫描（泊松 + 欧指平均）"
Cohesion: 0.50
Nodes (4): 2.1 用泊松算出基础概率, 2.2 欧指平均：胜平负 EV, 2.3 欧指平均：大小球 EV（可选）, 二、价值扫描（泊松 + 欧指平均）

### Community 84 - "四、让球盘：买上盘还是下盘"
Cohesion: 0.50
Nodes (4): 4.1 真实赢盘概率（用比分表聚合）, 4.2 水位 ≈ 赔率，算 EV, 4.3 盘感只做辅助，不做自动信号, 四、让球盘：买上盘还是下盘

### Community 85 - "八、战绩记录与复盘（下一步必须补齐的环节）"
Cohesion: 0.50
Nodes (4): 8.1 每一注需要记录什么, 8.2 如何按月 / 按联赛看战绩, 8.3 区分运气波动和模型问题, 八、战绩记录与复盘（下一步必须补齐的环节）

### Community 86 - "Heartbeat 检查清单"
Cohesion: 0.50
Nodes (3): Heartbeat 检查清单, 赛前分析补漏, 赛后复盘补漏

### Community 87 - "第二步：亚盘盘口类型判断（主人亲授体系）"
Cohesion: 0.50
Nodes (4): 2.2 判断实盘 or 错盘, 2.3 错盘分类（如为错盘）, 2.4 浅盘形态细分（如为浅盘）, 第二步：亚盘盘口类型判断（主人亲授体系）

### Community 88 - "solve_lambda_for_over_prob"
Cohesion: 0.50
Nodes (4): poisson_cdf_leq(), P(T<=k). Use recurrence to avoid factorial in a loop., Solve λ s.t. P(T > line_half) ≈ p_over, where T ~ Poisson(λ). For half line…, solve_lambda_for_over_prob()

### Community 89 - "八、心跳机制"
Cohesion: 0.67
Nodes (3): 八、心跳机制, 心跳 vs Cron：何时使用哪一个, 心跳期间的行为

## Knowledge Gaps
- **619 isolated node(s):** `2.2 判断实盘 or 错盘`, `2.3 错盘分类（如为错盘）`, `2.4 浅盘形态细分（如为浅盘）`, `3.1 水位数据`, `3.2 水位变化历史（关键时点）` (+614 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 676 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` connect `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` to `第一部分：赛前分析模板`, `盘口与走势阅读手册（简版）`, `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告`, `AGENTS.md - 足彩分析工作流操作手册`, `泊松概率计算手册（足彩用）`, `titan007 抓取 → 缓存层 → 内部 API 化设计方案`, `泊松概率分析：布伦特福德 vs 狼队`, `SAFETY.md`, `泊松概率分析：赫尔蒙德 vs 坎布尔`, `泊松概率分析：克雷莫纳 vs 佛罗伦萨`, `泊松概率分析：阿纳西 vs 特鲁瓦`, `泊松概率分析：朴茨茅斯 vs 德比郡`, `泊松概率分析：巴列卡诺 vs 莱万特`, `Agent（pansuan）— OpenClaw 足彩分析师 Agent`, `OpenClaw：AGENTS.md 与 Skills 说明`, `深度分析报告：马洛卡 VS 西班牙人`, `模型扩展与组合手册（除泊松之外）`, `累计战绩`, `球队风格判定手册（简版）`, `titan007 欧冠杯 CupMatch c103.js 数据结构分析`, `比分建模与投注手册（泊松版）`, `执行流程`, `下注决策手册（版本 1）`, `联赛配置手册（泊松 + 盘口）`, `赔率与泊松比较：何时值得下注（案例详解）`, `赛程抓取（match-scraper）`, `执行步骤`, `案例 27（超低平全周期锁死<3.00杀主胜案）：平赔全流程处于<3.00禁区，破2.00虚诱主胜暗杀平局【平局2.95与让负1.59通杀案】`, `巴列卡诺 vs 莱万特：泊松 + 盘口综合实战案例`, `基本面（分析页）`, `一、发现的 BUG / 漏洞`, `五、 彻底杜绝推演反复犯错的三大定量物理门禁（根治二元钟摆与阴谋论妄想症）`, `4 家一致的“操盘手法一致”识别（亚盘专用）`, `二、建议修补的漏洞 / 不一致`, `每日检查（daily-check）`, `执行步骤`, `执行步骤`, `三、 赔率分析推演十大公理（胜平负 + 让球联动）`, `案例 56（客让盘砸让平诱小胜与让负升水阻上穿盘案）：客负1.81锁定，让平暴跌-0.25做蜜罐，让负3.47升水阻上大胜【客负1.81与让负3.47穿盘通杀案】`, `精选推荐与串关决策 (Recommendation & Parlay Strategy)`, `deep-analysis/SKILL.md`, `AGENTS.md — 工作区操作手册（提纲模板）`, `执行步骤`, `案例 47（初让负最小均势杀平案）：(-1)让负1.44初盘最小锁死主不胜，均势两头分流杀平局【平3.34与让负1.44双红案】`, `四、模拟示例（周日 018 巴萨 vs 塞维利亚）`, `执行流程`, `案例 19（极低赔拉让平阻客实杀让平案）：主胜1.10诱穿盘暗杀让平【主胜1.10与天价让平3.80案】`, `案例 39（均势微让僵局与平赔领跌杀两头案）：主胜微降未易主（2.51 vs 2.30），平赔降幅超胜赔真防平【平3.38与让胜1.48通杀案】`, `sporttery-sniper`, `核心工具：sporttery-sniper`, `案例 67（拉马努金客负断崖与让胜蜜罐杀大冷案）：胜1.26突升1.29，客负暴跌-0.45内幕抢筹，让负2.96通杀全盘【客负6.75与让负2.96惊天大冷案】`, `Heartbeat 检查清单`, `Errors Log`?**
  _High betweenness centrality (0.471) - this node is a cross-community bridge._
- **Why does `AGENTS.md - 足彩分析工作流操作手册` connect `AGENTS.md - 足彩分析工作流操作手册` to `第一部分：赛前分析模板`, `赔率分析推演：庄家操盘逻辑与双盘联动推演心法`, `SAFETY.md`, `Agent（pansuan）— OpenClaw 足彩分析师 Agent`, `OpenClaw：AGENTS.md 与 Skills 说明`, `累计战绩`, `执行流程`, `TOOLS.md`, `各场景的 Subagent 用法`, `联赛配置手册（泊松 + 盘口）`, `赛程抓取（match-scraper）`, `执行步骤`, `4 家一致的“操盘手法一致”识别（亚盘专用）`, `每日检查（daily-check）`, `执行步骤`, `执行步骤`, `精选推荐与串关决策 (Recommendation & Parlay Strategy)`, `deep-analysis/SKILL.md`, `AGENTS.md — 工作区操作手册（提纲模板）`, `执行步骤`, `四、模拟示例（周日 018 巴萨 vs 塞维利亚）`, `执行流程`, `赛后复盘（post-review）`, `一、工作流程总览`, `sporttery-sniper`, `核心工具：sporttery-sniper`, `四、Memory 写入规则`, `Heartbeat 检查清单`, `八、心跳机制`, `Errors Log`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `执行流程` connect `执行流程` to `titan007.js`, `[欧冠杯] 葡萄牙体育 vs 博德闪耀 深度分析报告`, `AGENTS.md - 足彩分析工作流操作手册`, `titan007 抓取 → 缓存层 → 内部 API 化设计方案`, `赔率分析推演：庄家操盘逻辑与双盘联动推演心法`, `深度分析报告：马洛卡 VS 西班牙人`, `球队风格判定手册（简版）`, `poisson_lib.py`, `基本面（分析页）`, `一、发现的 BUG / 漏洞`, `4 家一致的“操盘手法一致”识别（亚盘专用）`, `二、建议修补的漏洞 / 不一致`, `精选推荐与串关决策 (Recommendation & Parlay Strategy)`, `执行步骤`, `四、模拟示例（周日 018 巴萨 vs 塞维利亚）`, `深度分析（deep-analysis）`, `执行流程`, `步骤 1.5：校验脚本赔率与数据完整性`, `变动历史分析示例（大小球，必须像这样写）`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 64 inferred relationships involving `赔率分析推演：庄家操盘逻辑与双盘联动推演心法` (e.g. with `下注决策手册（版本 1）` and `盘口与走势阅读手册（简版）`) actually correct?**
  _`赔率分析推演：庄家操盘逻辑与双盘联动推演心法` has 64 INFERRED edges - model-reasoned connections that need verification._
- **Are the 50 inferred relationships involving `AGENTS.md - 足彩分析工作流操作手册` (e.g. with `AGENTS.md — 工作区操作手册（提纲模板）` and `每日检查（daily-check）`) actually correct?**
  _`AGENTS.md - 足彩分析工作流操作手册` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 40 inferred relationships involving `4 家一致的“操盘手法一致”识别（亚盘专用）` (e.g. with `LambdaBounds` and `applyLatestEuropeHistoryToCompanies()`) actually correct?**
  _`4 家一致的“操盘手法一致”识别（亚盘专用）` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `累计战绩` (e.g. with `FEATURE_REQUESTS.md` and `Errors Log`) actually correct?**
  _`累计战绩` has 20 INFERRED edges - model-reasoned connections that need verification._