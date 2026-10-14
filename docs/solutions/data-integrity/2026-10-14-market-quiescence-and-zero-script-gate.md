# 市场静默期鉴伪与推演态零散脚本根治方案

## 背景与问题根因
在分析次日凌晨 03:00 的晚盘赛事（如 3073150）时，早盘至晚盘前期（18:00~21:00）机构盘口往往处于合法做市商静默期（Market Quiescence）。当平博（Pinnacle）因散户小额试水在 20:57 产生单笔微调水位，而 Bet365 与易胜博仍停留在官方真实最后变动（17:59 与 17:57）时，因时差 > 90 分钟触发门禁 `SUSPECTED_PATCH_CHEAT` 误判。
旧有 Agent 遇到门禁失败，习惯性在 `scratch/` 目录下编写大量临时 `.py` 脚本试图打补丁或测试，违反 Scrapling 官方零代码原则并引发严重时延与安全隐患。

## 解决方案
1. **静默期加密存证鉴伪（`verifier.py`）**：
   引入 `is_genuine_quiescence` 逻辑：当 Markdown 文件的 SHA-256 哈希值与原始报文原子包（`raw/{matchId}.json`）的加密封条完全吻合且未被篡改时，判定该时序落后为真实做市商静默期（Market Quiescence），不再误判为作弊。
2. **CLI 内置单命令自诊断（`cli.py --diagnose-gate <file>`）**：
   无需编写任何外部 Python 脚本，一键输出核心机构时序、全盘最新水位、SHA-256 存证封条与差异状态。
3. **推演态零散脚本硬禁令（Zero-Script Iron Rule）**：
   在 `AGENTS.md` 与 `skills/match-scraper/SKILL.md` 中全面封禁推演态散装脚本编写，数据搬运全部归属 Scrapling MCP 原生工具与 `cli.py`。
