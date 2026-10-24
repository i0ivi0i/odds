# `data/{销售日}/{matchId}.db` SQLite SSOT Schema

> 2026-10-24 起，比赛数据的唯一持久化真相是 SQLite。Scrapling 导出仓库外临时 JSONL，ETLX `-file` 只载入 `ENDPOINT_PAYLOAD`，其余步骤只读 `DB.endpoint_payload`；raw JSON 不再是 active 分析路径。

## 1. 装配顺序

```bash
sqlite3 data/{销售日}/{matchId}.build.db < data/schema.sql
etlx -config data/pipeline.md -date {销售日} -file <临时.jsonl> -only ENDPOINT_PAYLOAD
etlx -config data/pipeline.md -date {销售日} -skip ENDPOINT_PAYLOAD
```

门禁 `violations=0` 后，用 SQLite `.backup` 将 build 库提升为 `data/{销售日}/{matchId}.db`。

## 2. `endpoint_payload`（唯一原始存证表）

每行对应一个分析端点：

| 字段 | 说明 |
| :--- | :--- |
| `match_id` | 球探 `matchId` |
| `endpoint_key` | 27 个分析端点 key 之一 |
| `content_type` | `javascript` / `html` / `json` / `markdown` / `empty` |
| `content` | 真实响应文本 |
| `chars` | `content` 字符数 |
| `raw_sha256` | JSONL 原始字节 SHA256 |
| `sha256` | `content` 的 SHA256 |
| `source_url` | 采集 URL |
| `fetched_at` | 采集时间 |
| `status` | HTTP 状态 |
| `state` | `supported` / `not_offered` / `failed` |
| `empty_state` | 空状态说明；无则为 `NULL` |

约束：27 个分析端点、27 个 distinct key；`polymarket.json` 不在该表。`chars = length(content)`，`sha256 = sha256(content)`。

## 3. JSONL 行形状

```json
{"match_id":"3003920","endpoint_key":"1x2d.js","content_type":"javascript","content":"...","chars":312540,"raw_sha256":"...","sha256":"...","source_url":"https://txt.titan007.com/1x2/3003920.js","fetched_at":"2026-10-24 12:10:00","status":200,"state":"supported","empty_state":null,"extraction_type":"text"}
```

`extraction_type` 只用于采集分类，ETLX 载入时可不写入目标表。

## 4. 派生表

- `match_meta`：队名、联赛、竞彩编号、开球时间；来自 `meta.md`，不是新的网络端点。
- `euro_snapshot`：21 家欧指初即盘。
- `euro_history`：欧指变盘时序。
- `asian_odds` / `over_under`：亚盘与大小球初即全景。
- `ah_history` / `ou_history` / `eu_detail_history`：7 家机构变盘流水。
- `injury` / `lineup` / `team_stats`：伤停、首发与攻防技统。
- `bookmaker_slots`：22 家博彩做市商槽位；`v_bookmaker_slots` 另映射 Polymarket 参考槽位，共 23 家。
- `endpoint_parse_status` / `build_manifest`：端点解析状态与构建清单。

## 5. 只读视图

### 5.1 四个业务入口（人、机器、AI 共用）

第一屏只看四张视图。它们只放事实，不放预测、推荐、信心、评分或胜负判断。

| 入口视图 | 一行代表 | 主要列 |
| :--- | :--- | :--- |
| `球队基本情况` | 比赛信息一行、首发/替补、伤停 | `数据类型`、`联赛`、`主队`、`客队`、`开球时间`、`竞彩编号`、`销售日`、`队伍`、`身份`、`姓名`、`伤停原因` |
| `欧指` | 一家机构的欧指当前盘 | 初盘主平客、最新主平客、返还率、历史行数、首末时间 |
| `亚盘` | 一家机构的亚盘当前盘 | 初盘主水/盘口/客水、最新主水/盘口/客水、历史行数 |
| `大小球` | 一家机构的大小球当前盘 | 初盘大球/盘口/小球、最新大球/盘口/小球、历史行数 |

`球队基本情况` 不是一行摘要；它用 1 条比赛信息、40 条阵容、9 条伤停按“数据类型”展开，共 50 行。每行只代表一个实体：比赛、球员或伤员。位置、阵型、胜率、胜平负、联赛积分、预期进球等统计不进入这个抽屉。

### 5.2 下钻与原始层

需要逐笔流水时，从四入口下钻：

- 欧指：`v_euro_history`、`v_eu_detail_history`
- 亚盘：`v_ah_history`
- 大小球：`v_ou_history`
- 阵容/伤停/技统：`v_lineup`、`v_injury`、`v_team_stats`

历史视图按 `ts_iso` 升序：初盘最早，变盘在中间，最新盘是最后一笔。不要用 `source_index` 代替时间。

原始证据层（`endpoint_payload`、`endpoint_parse_status`、`build_manifest`）只给审计和排错；四入口视图和 EvoOntology 都不读原始层。

### 5.3 EvoOntology 的边界

EvoOntology 的 `sqlite_view` 映射应从四入口或其明确列出的下钻视图开始。它只做只读看数：概念定位、字段定位、取事实数据。它不负责思考、分析、推演、评分、推荐或结论；这些由外部 AI 大脑完成。现有 active `v5` 的映射若仍落在明细视图，按“四入口下钻”阅读，不伪造新映射，也不改 active 版本。

机器查询示例（不碰原始层）：

```sql
SELECT "数据类型", "联赛", "主队", "客队", "队伍", "身份", "姓名", "伤停原因" FROM "球队基本情况"
ORDER BY "数据类型", "队伍";
SELECT "机构编号", "机构", "最新主胜", "最新平局", "最新客胜" FROM "欧指" ORDER BY "机构编号";
SELECT "机构编号", "机构", "最新盘口", "最新主水", "最新客水" FROM "亚盘" ORDER BY "机构编号";
SELECT "机构编号", "机构", "最新盘口", "最新大球", "最新小球" FROM "大小球" ORDER BY "机构编号";
SELECT ts_iso, home, draw, away FROM v_euro_history WHERE cid = 80 ORDER BY ts_iso;
```

## 6. 最终门禁

```sql
SELECT COUNT(*) AS payloads,
       COUNT(DISTINCT endpoint_key) AS keys
FROM endpoint_payload;
-- 期望 27 | 27

SELECT COUNT(*) FROM endpoint_payload
WHERE endpoint_key = 'polymarket.json';
-- 期望 0

SELECT COUNT(*) FROM match_meta;
-- 期望 1

SELECT '球队基本情况' AS 视图, COUNT(*) FROM "球队基本情况"
UNION ALL SELECT '欧指', COUNT(*) FROM "欧指"
UNION ALL SELECT '亚盘', COUNT(*) FROM "亚盘"
UNION ALL SELECT '大小球', COUNT(*) FROM "大小球";
-- 本场期望 50 | 21 | 22 | 24（球队明细为 1 条比赛信息 + 40 条阵容 + 9 条伤停）
```

再检查 `endpoint_parse_status` 无 `failed`、`v_bookmaker_slots` 23 家均有合法状态、`PRAGMA integrity_check` 返回 `ok`。
