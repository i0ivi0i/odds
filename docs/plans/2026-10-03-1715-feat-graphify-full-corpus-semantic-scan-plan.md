---
title: 全系统文献与推演资产多模型并行语义扫描建网计划
date: 2026-10-03
type: feat
status: in-progress
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-plan
execution: code
---

## Goal Capsule

- **Objective:** 彻底打破此前“图谱只有大纲标题、正文宛如盲区、summary 字段 100% 为空”的严重空壳问题。对全库 19 篇顶尖博弈学术论文（已 100% 逐页核准）、13 本实战推演手册、5 大技能规范及 4 份核心基石规范（共计 41 份文档），实施**“微观概念深度提炼 + 官方 RFC 标准高浓度 summary 注入 + 跨文档多跳因果网络拓扑 + 物理真值 Quote 反向验证”**，为全图谱注入数百个带有 150~300 字精辟人话判词的微观认知节点，让主人在实战中任意说出一句口语或关键点，AI 均能瞬间穿透多跳图谱、举一反三、触类旁通。
- **Means:** 实施“单篇独立抽取 + 物理 Quote 真值反向校验 + 150~300 字高浓度 Summary 门禁 + 全图 0 孤岛强连通”四重防作弊审计流水线。
- **Product Authority:** 遵循主人最高立宪铁律：严禁编写推演与倍率仲裁业务代码；全流程仅做知识抽取与认知拓扑增强；每一个概念节点必须能物理溯源到原文真实语句。
- **Open Blockers:** 无阻碍，41 份源文档已全部就绪且高保真规整。

## Product Contract

### Problem Statement & 前期 Plan 漏洞深度反思

#### 1. 为什么此前计划被主人敏锐察觉“又留了作弊漏洞”？
主人一语中的：“这个 plan 不会被你又偷懒作弊了吧？”
经严肃自查，上一版 Draft Plan 存在四大严重硬伤：
1. **半拉子烂尾工程**：写到第 136 行列出 41 份文件后戛然而止，**既无 Implementation Units（工件拆解），也无 Verification Contract（自动化测试脚本），更无 Definition of Done（完成标准）**，完全是空头支票！
2. **缺乏防幻觉硬核检测机制**：大模型抽取概念时最容易“望文生义、凭空捏造”。如果抽取的 `quote` 根本不在原文中，或者摘要只是“本文讨论了某某概念”的流水账套话，整个图谱就会充斥劣质垃圾信息。
3. **缺乏物理快照与强连通性自动化回归管道**：没有规定单批提取物的结构校验脚本，无法防止合图时破坏图谱现有的连通性结构。

#### 2. 本计划的彻底重构与防作弊四重硬核门禁
- **Gate 1 (Physical Quote Exact Match)**：每一个概念节点必须携带原文 20~100 字的物理摘录（`quote`），且该文本必须在 `source_file` 中 100% 字符级精确匹配（`find(quote) != -1`），彻底杜绝 AI 凭空捏造。
- **Gate 2 (High-Density RFC Summary Gate)**：每个概念节点必须包含 150~300 字的精辟人话总结（`summary`），核心必须讲透**“博弈本质、庄家利益诱导、散户认知偏差与风控防守底线”**，字数不合规或废话套话直接判红灯。
- **Gate 3 (Multi-Hop Semantic Topology Gate)**：每个概念节点必须建立至少 2 条与其他概念或大纲节点的跨文档有向/无向连边（如 `reveals_bookmaker_intent`、`defends_asian_line`、`counteracts_bias`），置信度介于 0.70~0.95。
- **Gate 4 (Graphify 0 孤岛 100% 强连通回归)**：所有提取成果合并入 `graphify-out/graph.json` 后，必须运行 `check_consistency.py`，保证全图连通分量恒为 1，孤立节点恒为 0。

### Scope Boundaries

#### In Scope (明确涵盖)
- 全量 41 份目标文献与规范文件的无遗漏地毯式扫描：
  - 19 篇顶尖博弈学术论文（`docs/论文/*.calibrated.md`）
  - 13 本实战看盘与数据手册（`docs/*.md`）
  - 5 大推演与复盘 Skill（`skills/*/SKILL.md`）
  - 4 份核心基石文件（`AGENTS.md`、`MEMORY.md`、`STRATEGY.md`、`SOUL.md`）
- 微观概念节点定义与提取：每个概念具备唯一英汉 ID、精炼 Label、来源文件及行号/页码。
- 官方 RFC 标准高浓度 `summary` 注入：每个概念节点配备 150~300 字的人话精辟总结（讲透博弈本质、庄家利益与风控底线）。
- 语义相似度与因果关系网络构建：提取 `semantically_similar_to`、`causes_head_fake`、`defends_line`、`hedges_risk` 等真实语义边。
- 防偷懒防作弊证据链：生成中间快照文件 `graphify-out/semantic-extractions/<doc_id>.json`，每条记录携带原文摘录（`quote`），支持物理溯源。
- 图谱拓扑合并、Leiden 社区更新与全连通性检验。

#### Out of Scope (严格排除)
- 严禁编写任何推演、倍率仲裁或下注决策相关的业务代码（严格遵守代码禁令）。
- 不改动 19 篇论文正文的内容，保持原文真实性。
- 不引入重型外部向量数据库（如 Chroma、Milvus 等），遵循 Graphify 官方原生“图即相似度”轻量纯净架构。

### Requirements

- R1. 文档覆盖完备性：全量 41 份目标文件必须 100% 逐一扫描并生成对应提取结果，严禁遗漏任何一份。
- R2. 概念节点标准规范：提取出的概念节点必须符合以下数据契约：
  - `id`：符合命名空间的唯一标识（如 `concept_winkelmann_head_fake`）
  - `label`：直观中文标签（如 `状态空间假摔识别`）
  - `source_file`：准确的仓库相对路径
  - `source_location`：具体的页码或章节（如 `Page 14` 或 `L120`）
  - `node_kind`：固定为 `concept`
- R3. 官方 RFC 标准 Summary 契约：每个概念节点必须拥有 `summary` 属性，长度介于 150 至 300 字符，清晰讲明该概念在实战中的因果逻辑与防守底线，杜绝无意义套话。
- R4. 跨概念语义多跳连边：每个概念节点必须与至少 2 个同义、因果或对立的概念节点相连（关系涵盖 `semantically_similar_to`、`reveals_bookmaker_intent`、`defends_asian_line` 等），并打上置信度（0.70~0.95）。
- R5. 防作弊物理审计链：扫描产物必须先落地在 `graphify-out/semantic-extractions/` 目录下，并保留字段 `quote`（原文 20~80 字摘录），以便随时抽查验证真实性。
- R6. 全图谱 0 孤岛连通性：合图后全图谱节点数需大幅增长（预期概念节点新增 800+ 个），且全图必须保持 100% 强连通，0 孤岛。

### Key Decisions (Session-Settled)

- KTD1. 对齐 Graphify 官方 v8 与 `node-summaries-rfc` 规范：直接采用节点内嵌 `summary` 属性方案，配合 Leiden 图聚类算法，不额外增加向量存储负担。
- KTD2. 两阶段推进机制：
  - 阶段一：批处理提取并输出全量证据快照（由大模型逐批深度阅读文档正文，生成结构化 JSON 证据库）；
  - 阶段二：由编排脚本（如 `scripts/generate_deep_graph.py`）将快照安全合并入主图，执行重新聚类与拓扑验证。
- KTD3. 坚持无代码业务决策：提取脚本仅作为离线数据管道，负责格式转换与图数据组装，不包含任何预测裁判逻辑。

### Key Flows

- F1. 任务分发与文档切片
  - 调度器读取 41 份清单，按批次（学术论文批、实战手册批、技能基石批）分发大模型提取任务。
- F2. 大模型深度语义提炼与证据落地
  - 大模型阅读各篇正文，抽取核心论点与博弈模型，输出符合 R2-R5 规范的 JSON 数据存入 `graphify-out/semantic-extractions/`。
- F3. 拓扑融合与质量验收
  - 校验提取总数与原文对应关系，确认无空壳、无作弊；随后将节点与边注入 `graphify-out/graph.json`，运行 `check_consistency.py` 确保 100% 满分连通。

### Acceptance Examples

- AE1. 民间黑话联想测试：
  - 场景：检索词为“早盘平赔假摔”；
  - 结果：图谱精准命中 `concept_winkelmann_head_fake`（带 200 字精辟 summary），且 1 跳内连通至 `concept_asian_handicap_defense_line`（让球盘真实防守底线），实现多维度联想。
- AE2. 审计快照完整性检验：
  - 场景：检查 `graphify-out/semantic-extractions/` 目录；
  - 结果：必须存在 41 个对应的 JSON 审计文件，概念节点总数 $\ge 800$ 个，且每个节点均带有非空 `quote` 与 `summary`。

### Anti-Patterns and Guardrails

- 严禁伪造或跳步：禁止通过脚本机械截取大纲标题来冒充大模型深入阅读提炼。
- 严禁空壳摘要：摘要内容必须包含实战推演逻辑，严禁出现“本文介绍了某某概念”等流水账废话。
- 严禁代码化决策：全流程严格限于知识抽取与图谱更新，禁止增加硬编码的推演规则。

### Target Document Inventory (41 Files)

#### 1. 学术论文体系（19 篇）
1. `docs/论文/1802.08848_结合历史数据与庄家赔率预测足球比分.calibrated.md`
2. `docs/论文/2004_Levitt_NBER_w9422.calibrated.md`
3. `docs/论文/2006_Giacomini_条件预测能力检验.calibrated.md`
4. `docs/论文/2011_Andrikogiannopoulou_博彩市场效率与行为偏差_工作论文.calibrated.md`
5. `docs/论文/2017_Feng_英超赔率与动态进球分布_arXiv_v5.calibrated.md`
6. `docs/论文/2017_Kaunitz_用庄家赔率寻找足球错价_arXiv_v2.calibrated.md`
7. `docs/论文/2019_Wheatcroft_足球概率预测评分.calibrated.md`
8. `docs/论文/2021_Dimitriadis_稳定可靠性图_CORP.calibrated.md`
9. `docs/论文/2022_Constantinou_亚洲让球与胜平负市场效率_arXiv_v2.calibrated.md`
10. `docs/论文/2023_Aiyer_结果偏见与决策评价.calibrated.md`
11. `docs/论文/2023_Choe_序贯预测者比较_arXiv_v6.calibrated.md`
12. `docs/论文/2023_Hegarty_Whelan_足球赔率预测_双市场_MPRA工作论文.calibrated.md`
13. `docs/论文/2023_Hewamalage_预测评估陷阱与最佳实践.calibrated.md`
14. `docs/论文/2025_Macri_足球贝叶斯加权动态模型_arXiv.calibrated.md`
15. `docs/论文/2025_德甲赔率能否预感进球_arXiv_v1.calibrated.md`
16. `docs/论文/2026_Wilkens_德甲预测与滚动验证.calibrated.md`
17. `docs/论文/2403.16282_足球博彩演进_机器学习预测与庄家赔率估算.calibrated.md`
18. `docs/论文/2604.17194_Forecast_Sports_Outcomes_under_EMH_Odds_Only_Models.calibrated.md`
19. `docs/论文/2605.30209_识别异常赔率波动与市场动态.calibrated.md`

#### 2. 实战看盘与推演手册（13 本）
20. `docs/盘口与走势阅读手册.md`
21. `docs/下注决策手册.md`
22. `docs/比分建模与投注手册.md`
23. `docs/泊松概率计算手册.md`
24. `docs/球队风格判定手册.md`
25. `docs/赔率与泊松比较案例.md`
26. `docs/数据源与API矩阵手册.md`
27. `docs/联赛配置手册.md`
28. `docs/模型扩展与组合手册.md`
29. `docs/Polymarket链接查找教程.md`
30. `docs/深度分析推送通知模板.md`
31. `docs/FLOW-AUDIT-2026-03.md`
32. `docs/check-漏洞与一致性问题.md`

#### 3. 核心推演技能规范（5 个）
33. `skills/deep-analysis/SKILL.md`
34. `skills/match-screening/SKILL.md`
35. `skills/recommendation/SKILL.md`
36. `skills/post-review/SKILL.md`
37. `skills/match-scraper/SKILL.md`

#### 4. 系统基石规范（4 份）
38. `AGENTS.md`
39. `MEMORY.md`
40. `STRATEGY.md`
41. `SOUL.md`

## Implementation Units (分批独立攻坚单元：拒绝大包、逐批过关)

### U1. 审计与抽取契约校验基础设施（Validator Gate）
- **Goal:** 编写离线校验脚本 `scripts/validate_semantic_extractions.py`，实现对抽取 JSON 的字段、字数、Quote 物理存在性与语义边有效性的严苛自动化检测。
- **Files:** `scripts/validate_semantic_extractions.py`
- **Verification:** 运行校验脚本，能准确捕获缺失字段、Quote 伪造与字数不足的测试用例。

### U2. 第一批学术文献：经典博弈收割与基准检验（5 篇）
- **Goal:** 深入扫描提取 Levitt(2004)、Giacomini(2006)、Wheatcroft(2019)、1802.08848、Wilkens(2026)，提炼庄家非对称收割、条件预测能力、攻防泊松凸组合等核心博弈概念。
- **Files:** `graphify-out/semantic-extractions/` 下对应的 5 个 JSON 证据文件。
- **Verification:** 运行 `validate_semantic_extractions.py` 对应文件全部通过。

### U3. 第二批学术文献：双盘联动与市场效率（5 篇）
- **Goal:** 深入扫描提取 Constantinou(2022)、Hegarty-Whelan(2023)、Andrikogiannopoulou(2011)、Feng(2017)、Kaunitz(2017)，提炼让球盘防守底线、双市场无偏效率差异、滚球走地 Skellam 过程、错价挖掘策略等概念。
- **Files:** 对应的 5 个 JSON 证据文件。
- **Verification:** 运行 `validate_semantic_extractions.py` 对应文件全部通过。

### U4. 第三批学术文献：时序评估、动态先验与前沿序列检验（5 篇）
- **Goal:** 深入扫描提取 Hewamalage(2023)、Macri(2025)、Wilkens 德甲预感(2025)、Choe(2023)、Dimitriadis(2021)，提炼评估陷阱、共度先验动态更新、进球预感异动、时齐经验伯恩斯坦置信序列、CORP 可靠性图等概念。
- **Files:** 对应的 5 个 JSON 证据文件。
- **Verification:** 运行 `validate_semantic_extractions.py` 对应文件全部通过。

### U5. 第四批学术文献：结果偏见与微观异常识别（4 篇）
- **Goal:** 深入扫描提取 Aiyer(2023)、2403.16282、2604.17194、2605.30209，提炼结果偏见心理学盲区、机器学习赔率权重、纯赔率 OO-EPC 无偏去水、状态空间假摔识别等概念。
- **Files:** 对应的 4 个 JSON 证据文件。
- **Verification:** 运行 `validate_semantic_extractions.py` 对应文件全部通过。

### U6. 实战手册与推演规范全量扫描（18 份实操资产）
- **Goal:** 扫描 13 本看盘实战手册（《盘口与走势阅读手册》《下注决策手册》等）及 5 大推演技能（`deep-analysis` 等），提炼早盘假摔做市、诱平阻胜、欧亚背离破译、资金逆向等核心实操概念。
- **Files:** 对应的 18 个 JSON 证据文件。
- **Verification:** 运行 `validate_semantic_extractions.py` 对应文件全部通过。

### U7. 系统立宪基石提取与图谱全量拓扑合流（4 份规范 + 合图归档）
- **Goal:** 扫描 `AGENTS.md`、`MEMORY.md`、`STRATEGY.md`、`SOUL.md`，将全量 41 份证据库的概念节点与跨文档语义边安全合入 `graphify-out/graph.json`，运行 Leiden 社区聚类，更新 `GRAPH_REPORT.md`，验证全图连通性与检索举一反三能力。
- **Files:** `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`
- **Verification:** 运行 `py -3.13 scripts/check_consistency.py --print-ok` 确认图谱 0 孤岛 100% 连通；运行 `graphify query` 实测民间黑话穿透效果。

## Verification Contract

### 自动化硬核门禁测试脚本集合
1. **Quote 物理反向索引与 Summary 字数质量门禁**：
   ```bash
   py -3.13 scripts/validate_semantic_extractions.py --dir graphify-out/semantic-extractions/
   ```
   *要求：41 个 JSON 证据文件全在，每个 Quote 在源文件中精确命中，每个 Summary 在 150-300 字之间，无流水账废话。*
2. **全图谱拓扑连通性与零孤岛门禁**：
   ```bash
   py -3.13 scripts/check_consistency.py --print-ok
   ```
   *要求：图谱连通分量恒为 1，孤立节点恒为 0。*
3. **举一反三实测检索门禁**：
   ```bash
   graphify query "早盘平赔突然连降0.15是诱盘还是真降？"
   ```
   *要求：直接穿透返回状态空间假摔识别、让球盘防守底线及 1802.08848 凸组合概念。*

## Definition of Done

- 全量 41 份文档在 `graphify-out/semantic-extractions/` 中拥有 41 个独立的 JSON 证据文件；
- 提取的概念节点总数 $\ge 300$ 个，且每个节点拥有经过物理反查的 `quote` 与 150~300 字精辟 `summary`；
- `scripts/validate_semantic_extractions.py` 100% 退出码 0；
- `graphify-out/graph.json` 节点规模扩大，所有新概念节点 100% 融入图谱拓扑；
- `check_consistency.py` 100% 满分通过，图谱 0 孤岛；
- 现场运行 `graphify query` 展现端到端举一反三效果。
