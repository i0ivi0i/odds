---
module: pipeline
date: 2026-10-11
problem_type: workflow_issue
component: pipeline_orchestration
severity: high
symptoms:
  - "大模型触发推演任务后在后台长时间思考、检索图谱或翻旧账，迟迟未在 data/ 落盘快照文件"
  - "快照落盘与批量门禁过验变为推演中途碰壁后的修补产物"
  - "skills/deep-analysis/SKILL.md 存在步骤 2 倒置于步骤 1 的反序说明"
root_cause: missing_workflow_step
resolution_type: workflow_improvement
tags:
  - first-action-lock
  - pipeline-ordering
  - scrapling-bulk-get
  - two-phase-isolation
---

# 根除推演前时序倒挂：第一动作死锁与搬运工/分析师硬隔离

## 1. 问题现象与根因

在足球倍率分析推演系统中，当触发赛前分析或“重新推演”时，大模型经常在后台长时间查图谱、召回记忆与构思比赛，最后才跑去抓取数据落盘 `data/{销售日}/`。

### 核心根因
1. **缺第一动作死锁（First-Action Hard Lock）**：系统启动指令未锁定醒来后第 0 秒工具调用，大模型默认抢跑思考。
2. **编排大脑角色越权**：编排者混入了 10 步推演心法，在阶段一未降维为“纯物理进货搬运工”，越权构思推演。
3. **缺未见文件严禁开脑禁令（No Snapshot, No Thinking）**：未物理禁止在快照过验前在 Thinking 链中推演比赛；`deep-analysis` 残留“步骤 2 先于步骤 1”倒序文本。
4. **抓取调度缺乏一键并发矩阵**：未强制使用 `mcp__scrapling__bulk_get` 一次性拉齐全量 URL 矩阵。

## 2. 解决方案与架构重构

### 两阶段物理硬隔离
- **阶段一：纯物理进货搬运工**：
  - 任务触发第 0 秒第一工具动作：核对赛程 ➔ 组装 URL 矩阵调用 `mcp__scrapling__bulk_get` ➔ SnapshotAssembler 批量落盘 `data/{销售日}/{matchId}.md` ➔ 运行 `python 校验/src/adapter/cli.py --batch data/{销售日}`。
  - **禁令**：未见全部快照过验（exit 0）前，绝对禁止调用 Graphify 三大战区、绝对禁止翻阅历史记忆、绝对禁止在脑中推演比赛胜负。缺一门或 exit 1 立即物理熔断中止。
- **阶段二：纯逻辑首席分析师**：
  - 仅当阶段一全量 exit 0 后，方可分发 Worker 纯只读加载当场快照。
  - 此时按顺序执行：Graphify 三大战区检索 ➔ OO-EPC CLI 计算 ➔ 10 步深度推演。

### 落地文件与修改点
- `AGENTS.md`：在 `## 零、会话启动` 与 `## 五、Subagent 编排规则` 植入第一动作死锁与角色隔离规范。
- `skills/deep-analysis/SKILL.md`：删除原第 297 行“步骤 2 必须在步骤 1 之前执行”倒序说明，统一通道为 Scrapling（BrowserOS 辅助），行数严格缩减至 1674 行（恪守封顶做减法）。
- `TOOLS.md`：第 1 节新增“批量赛事一键并发矩阵与第 0 秒落盘规约”。
- `skills/match-scraper/SKILL.md` 与 `skills/match-screening/SKILL.md`：收拢采集入口至 Scrapling 协议流，消除初筛阶段手工浏览器阻塞。
- `pansuan-workflow`：植入两阶段硬隔离条款。

## 3. 预防防线
- **代码零改动守门**：`校验/` 与 `算法/` 保持 0 代码改动，纯依靠提示词与工作流契约卡紧。
- **倒序敏感词检索**：日常巡检严查“步骤 1 之前”等反序指令，确保流水线永远单向向前。
