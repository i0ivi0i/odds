# 足球推演系统流水线顺序与零漫游防抖解决方案 (Pipeline Sequence & Zero-Thrashing Solution)

**问题日期**：2026-10-14  
**分类**：流水线调度与防漫游架构 (Pipeline & Anti-Thrashing)  
**影响模块**：`AGENTS.md`, `skills/deep-analysis/SKILL.md`, `skills/match-scraper/SKILL.md`, `TOOLS.md`  

---

## 1. 现象与核心矛盾

在推演任务触发时，AI 经常在前台陷入长达数百个步长的非生产性思考与代码探索，迟迟未在磁盘产生物理源数据（`data/{销售日}/{matchId}.md`）：
- **思维超前空转**：在未产生物理源数据前，旧规约诱导 AI 提前通读 1,500 行的推演心法（10 步分析 + 19 篇论文），脑中充斥过多推演大纲，阻塞数据拉取。
- **工种越位代劳**：主会话收到指令后亲自充当搬运工，多次调用 `view_file` 查阅底层 Python 代码，甚至在终端裸写散装脚本，遭遇字符集与语法转义报错。
- **证据概念偷换**：全局规则“先自查、先拿证据再开口”被误用为“在业务推演前先读本地代码或先跑单测”，产生严重空转。

---

## 2. 解决方案：三阶段硬死锁与蜂群通用解耦

### 2.1 三阶段硬死锁状态机
1. **阶段 0：赛程索引确定性自检（Zero-State Hard Lock）**：
   - 检查 `data/{销售日}/meta.md` 是否存在且新鲜（< 2小时）；
   - 若缺，直接调用 Scrapling MCP `fetch(index.aspx)` 秒级直落（< 2秒），禁止任何前期预热或代码查阅。
2. **阶段 1：Agents 蜂群纯物理进货门禁（Swarm Ingest Gate）**：
   - **主会话前置白名单绝对硬锁**：主会话前 3 动作严格锁定为“检查 meta.md ➔ 计算规模 $W = \lceil N/6 \rceil$ ➔ 单次并发齐发 $W$ 个 Worker”。严禁查阅任何 py 源码，严禁手写爬虫脚本，严禁提前通读《skills/deep-analysis/SKILL.md》。
   - **专职搬运工极简闭环**：官方 Scrapling MCP `bulk_get` ➔ 写入 `raw/{matchId}.json` ➔ `cli.py --assemble-bundle` ➔ `cli.py --match` (exit 0)。零推演思维，零多余代码。
   - **批量终审放行**：主会话免轮询等待唤醒后，运行 `cli.py --batch data/{销售日} --max-age-minutes 30`。
3. **阶段 2：纯逻辑首席分析师（Phase 2 Deduction Brain）**：
   - 仅且必须在批量门禁 exit 0 放行后，方准调用 `view_file` 深度全量通读《skills/deep-analysis/SKILL.md》，检索 Graphify 三大战区与运行 OO-EPC 去水模型，开展 10 步推演。

### 2.2 多 Agent 蜂群并发四大通用军规
- **军规一：单动并发齐发 (Single-Turn Batch Dispatch)**：单次任务分发中一次性填入全量 $W$ 个 Worker，一枪打出，严禁多次串行分发。
- **军规二：无共享状态物理隔离 (Stateless Worker Isolation)**：各 Worker 承包互斥的比赛 ID，仅写入各自的原始与快照文件，无写锁冲突。
- **军规三：上下文极简隔离 (Strict Context Minimization $\le 2\text{KB}$)**：Worker Prompt 严格精炼，不继承主会话长上下文。
- **军规四：响应式免轮询唤醒 (Reactive Wakeup & Zero Polling)**：主会话发完即停，静待系统唤醒。

---

## 3. 防反弹验证与黄金经验

- **唯一法定证据**：在足球推演业务中，“先拿证据再开口”的唯一法定证据是磁盘上的 `data/{销售日}/{matchId}.md` 物理文件与门禁收据，绝非本地代码审查或测试运行。
- **做减法守则**：直接复用 Scrapling MCP 官方能力与现有受测 CLI，绝不随意新造 CLI 参数或临时脚本。
