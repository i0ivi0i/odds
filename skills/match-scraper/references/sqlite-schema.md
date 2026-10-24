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

- `euro_snapshot`：21 家欧指初即盘。
- `euro_history`：欧指变盘时序。
- `asian_odds` / `over_under`：亚盘与大小球初即全景。
- `ah_history` / `ou_history` / `eu_detail_history`：7 家机构变盘流水。
- `injury` / `lineup` / `team_stats`：伤停、首发与攻防技统。
- `bookmaker_slots`：22 家博彩做市商槽位；`v_bookmaker_slots` 另映射 Polymarket 参考槽位，共 23 家。
- `endpoint_parse_status` / `build_manifest`：端点解析状态与构建清单。

## 5. 只读视图

`v_euro_snapshot`、`v_euro_history`、`v_asian_odds`、`v_over_under`、`v_ah_history`、`v_ou_history`、`v_eu_detail_history`、`v_injury`、`v_lineup`、`v_team_stats`、`v_bookmaker_slots`、`v_payload_coverage`、`v_analysis_status`。

EvoOntology 的 `sqlite_view` 映射指向这些视图；分析必须经官方 MCP 视网膜先取 Mapping，再做受限查询。

## 6. 最终门禁

```sql
SELECT COUNT(*) AS payloads,
       COUNT(DISTINCT endpoint_key) AS keys
FROM endpoint_payload;
-- 期望 27 | 27

SELECT COUNT(*) FROM endpoint_payload
WHERE endpoint_key = 'polymarket.json';
-- 期望 0
```

再检查 `endpoint_parse_status` 无 `failed`、`v_bookmaker_slots` 23 家均有合法状态、`PRAGMA integrity_check` 返回 `ok`。
