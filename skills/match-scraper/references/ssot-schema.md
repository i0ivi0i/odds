# `raw/{matchId}.json` SSOT Schema

- **唯一写者**：`skills/match-scraper/scripts/ingest_spider.py`
- **唯一读者**：EvoOntology MCP 定向提取；人类只读 `data/{销售日}/{matchId}.md` 看板。
- **原子写**：先写同目录隐藏临时文件，`os.replace` 覆盖；失败删除临时文件；不产生第二份 JSON。
- **读回校验**：写入后立刻 `validate_bundle`，失败删除刚写的文件并退出 1。

## 顶层四段

```json
{
  "match": {
    "match_id": "3073801",
    "sales_date": "2026-10-22",
    "home": "格拉茨风暴",
    "away": "马赛"
  },
  "payloads": {
    "1x2d.js": "<原始 JS 文本>",
    "analysis.html": "<原始 HTML>",
    "ah_1.html": "<#odds2 table Markdown>"
  },
  "receipt": {
    "endpoints": {
      "1x2d.js": {
        "url": "https://1x2d.titan007.com/3073801.js",
        "status": 200,
        "state": "ok",
        "errors": [],
        "raw_bytes": 427298,
        "chars": 427298,
        "sha256": "<payload 文本 sha256>",
        "raw_sha256": "<原始 bytes sha256>",
        "encoding": "utf-8",
        "attempts": 1,
        "fetched_at": "2026-10-22T22:15:31+08:00",
        "empty_state": null
      }
    },
    "endpoints_count": 28,
    "all_success": true,
    "all_required_present": true
  },
  "gates": {
    "ok": true,
    "errors": [],
    "counts": {
      "payload_keys": 28,
      "bookmaker_slots": 23,
      "euro_cids": 21,
      "change_tables": 21
    },
    "slots": {
      "澳彩": "supported",
      "188Bet": "supported",
      "Polymarket": "supported"
    }
  }
}
```

## `match`

| 字段 | 类型 | 规则 |
| :--- | :--- | :--- |
| `match_id` | string | 必须与 `1x2d.js` 的 `ScheduleID` 一致 |
| `sales_date` | string | `YYYY-MM-DD`，决定输出目录 |
| `home` | string | 优先用 `--home`；否则从 `hometeam_cn` 回填 |
| `away` | string | 优先用 `--away`；否则从 `guestteam_cn` 回填 |

## `payloads`

- 键集合必须恰为 `config/endpoints.json` 的 28 个 `key`。
- `1x2d.js`、`analysis.html`、`odds.html`、`analy.json`、`polymarket.json` 为 UTF-8 原文。
- `ah_*`、`ou_*`、`eu_*`、`asian_odds.html`、`over_under.html` 为 GB18030 解码后的 Markdown。
- 合法空态：`polymarket.json` 为 `[]`、`analy.json` 的 `had` 为 `null`、`eu_42.html` 为 `""`；其余空串失败。
- 禁止 U+FFFD；禁止 WAF 标记（`Just a moment...`、`Cloudflare`、`Access Denied` 等）。

## `receipt.endpoints[key]`

| 字段 | 规则 |
| :--- | :--- |
| `url` | 实际请求 URL |
| `status` | HTTP 状态；0 表示未发请求或请求异常 |
| `state` | `ok` / `not_offered` / `failed` |
| `errors` | 失败原因列表；成功时为空 |
| `raw_bytes` | 原始响应字节数 |
| `chars` | `payloads[key]` 的字符数，必须精确相等 |
| `sha256` | `payloads[key]` 的 UTF-8 SHA256，必须精确相等 |
| `raw_sha256` | 原始响应字节 SHA256 |
| `encoding` | 该端点契约编码 |
| `attempts` | 尝试次数；异常可为 1 |
| `fetched_at` | ISO 8601 本地时间 |
| `empty_state` | 仅 `not_offered` 时为 `not_offered`，否则 `null` |

## `receipt` 汇总

| 字段 | 规则 |
| :--- | :--- |
| `endpoints_count` | 必须为 28 |
| `all_success` | 所有端点 `state != failed` |
| `all_required_present` | 28 个键全部存在 |

## `gates`

- `ok`：唯一放行位；`false` 时不得写 JSON。
- `errors`：至少包含 `missing_payload:*`、`missing_receipt:*`、`endpoint_failed:*`、`receipt_chars_mismatch:*`、`receipt_sha256_mismatch:*`、`missing_euro_cid:*`、`duplicate_cid:*`、`slot_missing_change_evidence:*` 之一。
- `counts`：`payload_keys=28`、`bookmaker_slots=23`、`euro_cids=21`、`change_tables=21`。
- `slots`：23 个官方名，值为 `supported` 或 `not_offered`。

## 23 槽位判定

1. 21 个 `euro_cid` 必须在 `1x2d.js` 中出现；缺失即失败。
2. 7 家核心机构的 `ah_*`/`ou_*`/`eu_*` 必须请求成功；合法未开盘带证据时可为 `not_offered`。
3. 188Bet 不看 `1x2d.js`；`ah_42`/`ou_42` 必须非空，`eu_42` 可为空；整体槽位仍 `supported`。
4. Polymarket 只看 `polymarket.json`；`[]` 为 `not_offered`；绝不伪造挂单价。
5. 非名册 cid `71`、`370`、`18`、`517`、`976` 不得计入 23；`976` 绝不能填给 188Bet。
