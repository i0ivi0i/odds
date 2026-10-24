<!-- One-file ETLX pipeline for one match at a time. data/schema.sql creates the typed physical tables only; this file lands the 27 analysis endpoints through the official ETLX -file handoff into the fixed data/.staging/build.db, derives every analysis table from DB.endpoint_payload, builds the four Chinese business tables, and creates all 13 read-only v_* views. A from-zero rebuild requires the schema bootstrap because ETLX's DuckDB SQLite attach cannot execute SQLite STRICT or foreign-key DDL. -->

# PIPELINE

```yaml
name: PIPELINE
description: Load one match into the fixed data/.staging/build.db from the official Scrapling JSONL; schema and views must already exist.
runs_as: ELT
active: true
```

## ENDPOINT_PAYLOAD

```yaml
name: ENDPOINT_PAYLOAD
table: endpoint_payload
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_endpoint_payload
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.endpoint_payload
active: true
```

```sql
-- land_endpoint_payload
INSERT INTO DB.endpoint_payload (
  match_id, endpoint_key, content_type, content, chars, raw_sha256, sha256,
  source_url, fetched_at, status, state, empty_state
)
SELECT
  match_id,
  endpoint_key,
  content_type,
  coalesce(content, ''),
  coalesce(chars, length(coalesce(content, ''))),
  coalesce(raw_sha256, sha256),
  sha256,
  coalesce(source_url, ''),
  fetched_at,
  coalesce(status, 0),
  state,
  empty_state
FROM read_json_auto('{file}')
WHERE endpoint_key <> 'polymarket.json';
```

## MATCH_META

```yaml
name: MATCH_META
table: match_meta
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_match_meta
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.match_meta
active: true
```

```sql
-- land_match_meta
INSERT INTO DB.match_meta (
  match_id, sales_date, match_no, league, home_team, away_team, kickoff_at, source
)
SELECT
  trim(f[2]) AS match_id,
  '{YYYY-MM-DD}' AS sales_date,
  trim(f[1]) AS match_no,
  trim(f[3]) AS league,
  trim(f[4]) AS home_team,
  trim(f[5]) AS away_team,
  trim(f[6]) AS kickoff_at,
  'data/{YYYY-MM-DD}/meta.md' AS source
FROM (
  SELECT string_split(trim(line, '|'), '|') AS f
  FROM (
    SELECT unnest(string_split(content, chr(10))) AS line
    FROM read_text('data/{YYYY-MM-DD}/meta.md')
  ) lines
  WHERE trim(line) LIKE '|%'
) cells
WHERE trim(f[2]) = (SELECT match_id FROM DB.endpoint_payload LIMIT 1);
```

## EURO_SNAPSHOT

```yaml
name: EURO_SNAPSHOT
table: euro_snapshot
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_euro_snapshot
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.euro_snapshot
active: true
```

```sql
-- land_euro_snapshot
WITH raw AS (
  SELECT
    match_id,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = '1x2d.js'
),
js AS (
  SELECT
    match_id,
    regexp_extract(content, 'var game=Array\((.*?)\);', 1) AS game_array
  FROM raw
),
game_rows AS (
  SELECT
    match_id,
    unnest(regexp_extract_all(game_array, '"([^"]*)"', 1)) AS row
  FROM js
),
fields AS (
  SELECT
    match_id,
    string_split(row, '|') AS f
  FROM game_rows
),
snapshots AS (
  SELECT
    match_id,
    (f[1])::INTEGER AS cid,
    f[2] AS record_id,
    f[3] AS bookmaker,
    (f[4])::DOUBLE AS initial_home,
    (f[5])::DOUBLE AS initial_draw,
    (f[6])::DOUBLE AS initial_away,
    (f[7])::DOUBLE AS initial_prob_home,
    (f[8])::DOUBLE AS initial_prob_draw,
    (f[9])::DOUBLE AS initial_prob_away,
    (f[10])::DOUBLE AS initial_return,
    (f[11])::DOUBLE AS latest_home,
    (f[12])::DOUBLE AS latest_draw,
    (f[13])::DOUBLE AS latest_away,
    (f[14])::DOUBLE AS latest_prob_home,
    (f[15])::DOUBLE AS latest_prob_draw,
    (f[16])::DOUBLE AS latest_prob_away,
    (f[17])::DOUBLE AS latest_return,
    trim(f[21]) AS source_time,
    f[22] AS alias
  FROM fields
  WHERE (f[1])::INTEGER IN (80, 545, 281, 90, 177, 432, 115, 82, 81, 104, 255, 110, 2, 474, 649, 800, 482, 386, 826, 16, 1129)
)
INSERT INTO DB.euro_snapshot (
  match_id, cid, bookmaker, record_id,
  initial_home, initial_draw, initial_away,
  initial_prob_home, initial_prob_draw, initial_prob_away, initial_return,
  latest_home, latest_draw, latest_away,
  latest_prob_home, latest_prob_draw, latest_prob_away, latest_return,
  source_time, alias
)
SELECT
  match_id, cid, bookmaker, record_id,
  initial_home, initial_draw, initial_away,
  initial_prob_home, initial_prob_draw, initial_prob_away, initial_return,
  latest_home, latest_draw, latest_away,
  latest_prob_home, latest_prob_draw, latest_prob_away, latest_return,
  source_time, alias
FROM snapshots;
```

## EURO_HISTORY

```yaml
name: EURO_HISTORY
table: euro_history
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_euro_history
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.euro_history
active: true
```

```sql
-- land_euro_history
WITH raw AS (
  SELECT
    match_id,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = '1x2d.js'
),
js AS (
  SELECT
    match_id,
    regexp_extract(content, 'var gameDetail=Array\((.*?)\);', 1) AS detail_array
  FROM raw
),
detail_rows AS (
  SELECT
    match_id,
    unnest(regexp_extract_all(detail_array, '"([^"]*)"', 1)) AS row
  FROM js
),
detail_parts AS (
  SELECT
    match_id,
    string_split(row, '^') AS p
  FROM detail_rows
),
segments AS (
  SELECT
    match_id,
    p[1] AS record_id,
    string_split(p[2], ';') AS segs,
    len(string_split(p[2], ';')) AS n
  FROM detail_parts
  WHERE length(trim(p[2])) > 0
),
segment_rows AS (
  SELECT
    match_id,
    record_id,
    i,
    list_extract(segs, i) AS seg
  FROM segments,
  generate_series(1, n) AS t(i)
  WHERE length(trim(list_extract(segs, i))) > 0
),
fields AS (
  SELECT
    match_id,
    record_id,
    i - 1 AS source_index,
    string_split(seg, '|') AS f
  FROM segment_rows
),
history AS (
  SELECT
    f.match_id,
    s.cid,
    f.record_id,
    f.source_index,
    trim(f.f[4]) AS ts_local,
    (f.f[8] || '-' || trim(f.f[4])) AS ts_iso,
    (f.f[8])::INTEGER AS year,
    (f.f[1])::DOUBLE AS home,
    (f.f[2])::DOUBLE AS draw,
    (f.f[3])::DOUBLE AS away,
    (f.f[5])::DOUBLE AS kelly_home,
    (f.f[6])::DOUBLE AS kelly_draw,
    (f.f[7])::DOUBLE AS kelly_away
  FROM fields f
  JOIN DB.euro_snapshot s
    ON s.match_id = f.match_id
   AND s.record_id = f.record_id
)
INSERT INTO DB.euro_history (
  match_id, cid, record_id, source_index, ts_local, ts_iso, year,
  home, draw, away, kelly_home, kelly_draw, kelly_away
)
SELECT
  match_id, cid, record_id, source_index, ts_local, ts_iso, year,
  home, draw, away, kelly_home, kelly_draw, kelly_away
FROM history;
```

## ASIAN_ODDS

```yaml
name: ASIAN_ODDS
table: asian_odds
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_asian_odds
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.asian_odds
active: true
```

```sql
-- land_asian_odds
WITH raw AS (
  SELECT
    match_id,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = 'asian_odds.html'
),
companies AS (
  SELECT
    match_id,
    unnest(json_extract(json_extract(content, '$.companies'), '$[*]')) AS company
  FROM raw
),
details AS (
  SELECT
    match_id,
    company,
    unnest(json_extract(company, '$.details[*]')) AS detail
  FROM companies
),
parsed AS (
  SELECT
    match_id,
    (company->>'companyId')::INTEGER AS company_id,
    CASE (company->>'companyId')::INTEGER
      WHEN 1 THEN '澳彩'
      WHEN 3 THEN '皇冠'
      WHEN 8 THEN 'Bet365'
      WHEN 12 THEN '易胜博'
      WHEN 42 THEN '188Bet'
      WHEN 47 THEN '平博'
      WHEN 48 THEN '香港马会'
    END AS bookmaker,
    (detail->>'oddsId')::INTEGER AS odds_id,
    (detail->>'firstHomeOdds')::DOUBLE AS first_home,
    (detail->>'firstDrawOdds')::DOUBLE AS first_line,
    (detail->>'firstAwayOdds')::DOUBLE AS first_away,
    (detail->>'homeOdds')::DOUBLE AS home,
    (detail->>'drawOdds')::DOUBLE AS line,
    (detail->>'awayOdds')::DOUBLE AS away,
    (detail->>'modifyTime')::BIGINT AS modify_ts,
    strftime(to_timestamp((detail->>'modifyTime')::BIGINT) AT TIME ZONE 'Asia/Shanghai', '%Y-%m-%d %H:%M') AS modify_iso
  FROM details
  WHERE (company->>'companyId')::INTEGER IN (1, 3, 8, 12, 42, 47, 48)
)
INSERT INTO DB.asian_odds (
  match_id, company_id, bookmaker, odds_id,
  first_home, first_line, first_away, home, line, away,
  modify_ts, modify_iso
)
SELECT
  match_id, company_id, bookmaker, odds_id,
  first_home, first_line, first_away, home, line, away,
  modify_ts, modify_iso
FROM parsed;
```

## OVER_UNDER

```yaml
name: OVER_UNDER
table: over_under
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_over_under
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.over_under
active: true
```

```sql
-- land_over_under
WITH raw AS (
  SELECT
    match_id,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = 'over_under.html'
),
companies AS (
  SELECT
    match_id,
    unnest(json_extract(json_extract(content, '$.companies'), '$[*]')) AS company
  FROM raw
),
details AS (
  SELECT
    match_id,
    company,
    unnest(json_extract(company, '$.details[*]')) AS detail
  FROM companies
),
parsed AS (
  SELECT
    match_id,
    (company->>'companyId')::INTEGER AS company_id,
    CASE (company->>'companyId')::INTEGER
      WHEN 1 THEN '澳彩'
      WHEN 3 THEN '皇冠'
      WHEN 8 THEN 'Bet365'
      WHEN 12 THEN '易胜博'
      WHEN 42 THEN '188Bet'
      WHEN 47 THEN '平博'
      WHEN 48 THEN '香港马会'
    END AS bookmaker,
    (detail->>'oddsId')::INTEGER AS odds_id,
    (detail->>'firstHomeOdds')::DOUBLE AS first_over,
    (detail->>'firstDrawOdds')::DOUBLE AS first_line,
    (detail->>'firstAwayOdds')::DOUBLE AS first_under,
    (detail->>'homeOdds')::DOUBLE AS over,
    (detail->>'drawOdds')::DOUBLE AS line,
    (detail->>'awayOdds')::DOUBLE AS under,
    (detail->>'modifyTime')::BIGINT AS modify_ts,
    strftime(to_timestamp((detail->>'modifyTime')::BIGINT) AT TIME ZONE 'Asia/Shanghai', '%Y-%m-%d %H:%M') AS modify_iso
  FROM details
  WHERE (company->>'companyId')::INTEGER IN (1, 3, 8, 12, 42, 47, 48)
)
INSERT INTO DB.over_under (
  match_id, company_id, bookmaker, odds_id,
  first_over, first_line, first_under, over, line, under,
  modify_ts, modify_iso
)
SELECT
  match_id, company_id, bookmaker, odds_id,
  first_over, first_line, first_under, over, line, under,
  modify_ts, modify_iso
FROM parsed;
```

## BOOKMAKER_SLOTS

```yaml
name: BOOKMAKER_SLOTS
table: bookmaker_slots
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_bookmaker_slots
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.bookmaker_slots
active: true
```

```sql
-- land_bookmaker_slots
INSERT INTO DB.bookmaker_slots (
  match_id, bookmaker, euro_cid, ah_cid, ou_cid,
  ah_status, ou_status, eu_status, source_label, evidence
)
WITH payload AS (
  SELECT match_id, endpoint_key, state
  FROM DB.endpoint_payload
),
matches AS (
  SELECT DISTINCT match_id FROM payload
),
roster(bookmaker, euro_cid, ah_cid, ou_cid) AS (
  VALUES
    ('澳彩', 80, 1, 1),
    ('皇冠', 545, 3, 3),
    ('Bet365', 281, 8, 8),
    ('易胜博', 90, 12, 12),
    ('平博', 177, 47, 47),
    ('香港马会', 432, 48, 48),
    ('188Bet', NULL, 42, 42),
    ('威廉希尔', 115, NULL, NULL),
    ('立博', 82, NULL, NULL),
    ('伟德', 81, NULL, NULL),
    ('Interwetten', 104, NULL, NULL),
    ('Bwin', 255, NULL, NULL),
    ('SNAI', 110, NULL, NULL),
    ('必发', 2, NULL, NULL),
    ('利记', 474, NULL, NULL),
    ('沙巴', 649, NULL, NULL),
    ('Marathon', 800, NULL, NULL),
    ('Betway', 482, NULL, NULL),
    ('Unibet', 386, NULL, NULL),
    ('Paddy Power', 826, NULL, NULL),
    ('10Bet', 16, NULL, NULL),
    ('中国体彩', 1129, NULL, NULL)
),
slots AS (
  SELECT
    m.match_id,
    r.bookmaker,
    r.euro_cid,
    r.ah_cid,
    r.ou_cid,
    CASE
      WHEN r.ah_cid IS NULL THEN 'not_offered'
      WHEN EXISTS (
        SELECT 1 FROM payload p
        WHERE p.match_id = m.match_id
          AND p.endpoint_key = 'ah_' || r.ah_cid || '.html'
          AND p.state = 'ok'
      ) THEN 'supported'
      ELSE 'not_offered'
    END AS ah_status,
    CASE
      WHEN r.ou_cid IS NULL THEN 'not_offered'
      WHEN EXISTS (
        SELECT 1 FROM payload p
        WHERE p.match_id = m.match_id
          AND p.endpoint_key = 'ou_' || r.ou_cid || '.html'
          AND p.state = 'ok'
      ) THEN 'supported'
      ELSE 'not_offered'
    END AS ou_status,
    CASE
      WHEN r.euro_cid IS NULL THEN 'not_offered'
      WHEN EXISTS (
        SELECT 1 FROM DB.euro_snapshot e
        WHERE e.match_id = m.match_id
          AND e.cid = r.euro_cid
      ) THEN 'supported'
      ELSE 'not_offered'
    END AS eu_status,
    r.bookmaker AS source_label,
    'euro_cid=' || coalesce(CAST(r.euro_cid AS VARCHAR), 'none')
      || '; ah=' || coalesce(CAST(r.ah_cid AS VARCHAR), 'none')
      || '; ou=' || coalesce(CAST(r.ou_cid AS VARCHAR), 'none')
      AS evidence
  FROM matches m
  CROSS JOIN roster r
)
SELECT
  match_id, bookmaker, euro_cid, ah_cid, ou_cid,
  ah_status, ou_status, eu_status, source_label, evidence
FROM slots;
```

## AH_HISTORY

```yaml
name: AH_HISTORY
table: ah_history
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_ah_history
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.ah_history
active: true
```

```sql
-- land_ah_history
WITH endpoints AS (
  SELECT
    match_id,
    endpoint_key,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key LIKE 'ah_%'
),
matches AS (
  SELECT
    match_id,
    endpoint_key,
    unnest(regexp_extract_all(content, '\|\s*(?:即|早)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|', 0)) AS record
  FROM endpoints
),
fields AS (
  SELECT
    match_id,
    endpoint_key,
    row_number() OVER (PARTITION BY endpoint_key) - 1 AS source_index,
    string_split(record, '|') AS f
  FROM matches
),
parsed AS (
  SELECT
    match_id,
    endpoint_key,
    CASE endpoint_key
      WHEN 'ah_1.html' THEN 1
      WHEN 'ah_3.html' THEN 3
      WHEN 'ah_8.html' THEN 8
      WHEN 'ah_12.html' THEN 12
      WHEN 'ah_42.html' THEN 42
      WHEN 'ah_47.html' THEN 47
      WHEN 'ah_48.html' THEN 48
    END AS company_id,
    source_index,
    trim(f[2]) AS status,
    (trim(f[3]))::DOUBLE AS home,
    trim(f[4]) AS line_text,
    (trim(f[5]))::DOUBLE AS away,
    trim(f[6]) AS ts_local,
    '2026-' || trim(f[6]) AS ts_iso
  FROM fields
)
INSERT INTO DB.ah_history (
  match_id, endpoint_key, company_id, source_index, status,
  home, line_text, away, ts_local, ts_iso
)
SELECT
  match_id, endpoint_key, company_id, source_index, status,
  home, line_text, away, ts_local, ts_iso
FROM parsed;
```

## OU_HISTORY

```yaml
name: OU_HISTORY
table: ou_history
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_ou_history
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.ou_history
active: true
```

```sql
-- land_ou_history
WITH endpoints AS (
  SELECT
    match_id,
    endpoint_key,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key LIKE 'ou_%'
),
matches AS (
  SELECT
    match_id,
    endpoint_key,
    unnest(regexp_extract_all(content, '\|\s*(?:即|早)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|', 0)) AS record
  FROM endpoints
),
fields AS (
  SELECT
    match_id,
    endpoint_key,
    row_number() OVER (PARTITION BY endpoint_key) - 1 AS source_index,
    string_split(record, '|') AS f
  FROM matches
),
parsed AS (
  SELECT
    match_id,
    endpoint_key,
    CASE endpoint_key
      WHEN 'ou_1.html' THEN 1
      WHEN 'ou_3.html' THEN 3
      WHEN 'ou_8.html' THEN 8
      WHEN 'ou_12.html' THEN 12
      WHEN 'ou_42.html' THEN 42
      WHEN 'ou_47.html' THEN 47
      WHEN 'ou_48.html' THEN 48
    END AS company_id,
    source_index,
    trim(f[2]) AS status,
    (trim(f[3]))::DOUBLE AS over,
    trim(f[4]) AS line_text,
    (trim(f[5]))::DOUBLE AS under,
    trim(f[6]) AS ts_local,
    '2026-' || trim(f[6]) AS ts_iso
  FROM fields
)
INSERT INTO DB.ou_history (
  match_id, endpoint_key, company_id, source_index, status,
  over, line_text, under, ts_local, ts_iso
)
SELECT
  match_id, endpoint_key, company_id, source_index, status,
  over, line_text, under, ts_local, ts_iso
FROM parsed;
```

## EU_DETAIL_HISTORY

```yaml
name: EU_DETAIL_HISTORY
table: eu_detail_history
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_eu_detail_history
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.eu_detail_history
active: true
```

```sql
-- land_eu_detail_history
WITH endpoints AS (
  SELECT
    match_id,
    endpoint_key,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key LIKE 'eu_%'
),
matches AS (
  SELECT
    match_id,
    endpoint_key,
    unnest(regexp_extract_all(content, '\|\s*[0-9.]+\s*\|\s*[0-9.]+\s*\|\s*[0-9.]+\s*\|\s*[0-9.]+\s*\|\s*[^|]+\|\s*[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}\s*\|', 0)) AS record
  FROM endpoints
),
fields AS (
  SELECT
    match_id,
    endpoint_key,
    row_number() OVER (PARTITION BY endpoint_key) - 1 AS source_index,
    string_split(record, '|') AS f
  FROM matches
),
parsed AS (
  SELECT
    match_id,
    endpoint_key,
    CASE endpoint_key
      WHEN 'eu_1.html' THEN 80
      WHEN 'eu_3.html' THEN 545
      WHEN 'eu_8.html' THEN 281
      WHEN 'eu_12.html' THEN 90
      WHEN 'eu_47.html' THEN 177
      WHEN 'eu_48.html' THEN 432
    END AS company_id,
    source_index,
    trim(f[2])::DOUBLE AS home,
    trim(f[3])::DOUBLE AS draw,
    trim(f[4])::DOUBLE AS away,
    trim(f[5])::DOUBLE AS return_rate,
    (regexp_extract_all(trim(f[6]), '[0-9.]+', 0))[1]::DOUBLE AS kelly_home,
    (regexp_extract_all(trim(f[6]), '[0-9.]+', 0))[2]::DOUBLE AS kelly_draw,
    (regexp_extract_all(trim(f[6]), '[0-9.]+', 0))[3]::DOUBLE AS kelly_away,
    trim(f[7]) AS ts_local,
    '2026-' || regexp_replace(trim(f[7]), '\s+', ' ', 'g') AS ts_iso
  FROM fields
  WHERE length(f) >= 8
    AND trim(f[2]) <> ''
)
INSERT INTO DB.eu_detail_history (
  match_id, endpoint_key, company_id, source_index,
  home, draw, away, return_rate, kelly_home, kelly_draw, kelly_away,
  ts_local, ts_iso
)
SELECT
  match_id, endpoint_key, company_id, source_index,
  home, draw, away, return_rate, kelly_home, kelly_draw, kelly_away,
  ts_local, ts_iso
FROM parsed;
```

## INJURY

```yaml
name: INJURY
table: injury
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_injury
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.injury
active: true
```

```sql
-- land_injury
WITH raw AS (
  SELECT
    match_id,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = 'odds.html'
),
lineup_json AS (
  SELECT
    match_id,
    regexp_extract(content, '(?s)var lineupObj\s*=\s*(\{.*?\});', 1) AS lineup
  FROM raw
),
injuries AS (
  SELECT
    match_id,
    'home' AS side,
    unnest(json_extract(lineup, '$.lineup.homeInjury[*]')) AS player
  FROM lineup_json
  UNION ALL
  SELECT
    match_id,
    'away' AS side,
    unnest(json_extract(lineup, '$.lineup.guestInjury[*]')) AS player
  FROM lineup_json
),
parsed AS (
  SELECT
    match_id,
    side,
    row_number() OVER (PARTITION BY side) - 1 AS source_index,
    coalesce(trim(player->>'number', '"'), '') AS number,
    coalesce(trim(player->>'name', '"'), '') AS name,
    coalesce(trim(player->>'Id', '"'), '') AS player_id,
    coalesce(trim(player->>'pos', '"'), '') AS position,
    coalesce(trim(player->>'injuryReson', '"'), '') AS injury_reason,
    coalesce((player->>'captainType')::INTEGER, 0) AS captain_type,
    coalesce((player->>'playerKind')::INTEGER, 0) AS player_kind
  FROM injuries
)
INSERT INTO DB.injury (
  match_id, side, source_index, number, name, player_id,
  position, injury_reason, captain_type, player_kind, source_endpoint
)
SELECT
  match_id, side, source_index, number, name, player_id,
  position, injury_reason, captain_type, player_kind, 'odds.html'
FROM parsed;
```

## LINEUP

```yaml
name: LINEUP
table: lineup
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_lineup
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.lineup
active: true
```

```sql
-- land_lineup
WITH raw AS (
  SELECT
    match_id,
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = 'odds.html'
),
lineup_json AS (
  SELECT
    match_id,
    try_cast(regexp_extract(content, '(?s)var lineupObj\s*=\s*(\{.*?\});', 1) AS JSON) AS lineup
  FROM raw
),
rosters AS (
  SELECT
    match_id,
    'home' AS side,
    'starter' AS role,
    unnest(json_extract(lineup, '$.lineup.homePlayerList[*]')) AS player,
    coalesce(json_extract_string(lineup, '$.lineup.homeFormation'), '') AS formation
  FROM lineup_json
  UNION ALL
  SELECT
    match_id,
    'home' AS side,
    'bench' AS role,
    unnest(json_extract(lineup, '$.lineup.homeBakPlayerList[*]')) AS player,
    coalesce(json_extract_string(lineup, '$.lineup.homeFormation'), '') AS formation
  FROM lineup_json
  UNION ALL
  SELECT
    match_id,
    'away' AS side,
    'starter' AS role,
    unnest(json_extract(lineup, '$.lineup.guestPlayerList[*]')) AS player,
    coalesce(json_extract_string(lineup, '$.lineup.guestFormation'), '') AS formation
  FROM lineup_json
  UNION ALL
  SELECT
    match_id,
    'away' AS side,
    'bench' AS role,
    unnest(json_extract(lineup, '$.lineup.guestBakPlayerList[*]')) AS player,
    coalesce(json_extract_string(lineup, '$.lineup.guestFormation'), '') AS formation
  FROM lineup_json
),
parsed AS (
  SELECT
    match_id,
    side,
    role,
    row_number() OVER (PARTITION BY side, role) - 1 AS source_index,
    coalesce(trim(player->>'number', '"'), '') AS number,
    coalesce(trim(player->>'name', '"'), '') AS name,
    coalesce(trim(player->>'Id', '"'), '') AS player_id,
    coalesce(trim(player->>'pos', '"'), '') AS position,
    formation
  FROM rosters
)
INSERT INTO DB.lineup (
  match_id, side, role, source_index, number, name, player_id,
  position, formation, source_endpoint
)
SELECT
  match_id, side, role, source_index, number, name, player_id,
  position, formation, 'odds.html'
FROM parsed;
```

## TEAM_STATS

```yaml
name: TEAM_STATS
table: team_stats
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_team_stats
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.team_stats
active: true
```

```sql
-- land_team_stats
WITH raw AS (
  SELECT
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = 'analysis.html'
),
j AS (
  SELECT
    regexp_extract(content, '(?s)var jsonData\s*=\s*(\{.*?\});', 1) AS s
  FROM raw
),
raw_analy AS (
  SELECT
    content
  FROM DB.endpoint_payload
  WHERE endpoint_key = 'analy.json'
),
j_analy AS (
  SELECT
    regexp_extract(content, '(?s)var jsonData\s*=\s*(\{.*?\});', 1) AS s
  FROM raw_analy
),
points AS (
  SELECT
    'currentPoints' AS section,
    'home' AS side,
    unnest(json_extract(s, '$.currentPoints.homePoints.points[*]')) AS point
  FROM j
  UNION ALL
  SELECT 'currentPoints', 'away',
    unnest(json_extract(s, '$.currentPoints.awayPoints.points[*]'))
  FROM j
  UNION ALL
  SELECT 'halfPoints', 'home',
    unnest(json_extract(s, '$.currentPoints.halfHomePoints.points[*]'))
  FROM j
  UNION ALL
  SELECT 'halfPoints', 'away',
    unnest(json_extract(s, '$.currentPoints.halfAwayPoints.points[*]'))
  FROM j
),
point_rows AS (
  SELECT
    section,
    side,
    row_number() OVER (PARTITION BY section, side, point->>'name') - 1 AS source_index,
    point->>'name' AS item,
    e.key AS metric,
    try_cast(json_extract_string(point, '$.' || e.key) AS DOUBLE) AS value,
    CASE
      WHEN try_cast(json_extract_string(point, '$.' || e.key) AS DOUBLE) IS NULL
      THEN json_extract_string(point, '$.' || e.key)
    END AS text_value
  FROM points,
  json_each(point) e
),
statistics AS (
  SELECT
    unnest(json_extract(s, '$.leagueStatistics.statisticses[*]')) AS stat
  FROM j
),
stat_rows AS (
  SELECT
    'leagueStatistics' AS section,
    'match' AS side,
    row_number() OVER (PARTITION BY stat->>'round') - 1 AS source_index,
    'round_' || coalesce(stat->>'round', 'unknown') AS item,
    e.key AS metric,
    try_cast(json_extract_string(stat, '$.' || e.key) AS DOUBLE) AS value,
    CASE
      WHEN try_cast(json_extract_string(stat, '$.' || e.key) AS DOUBLE) IS NULL
      THEN json_extract_string(stat, '$.' || e.key)
    END AS text_value
  FROM statistics,
  json_each(stat) e
),
features AS (
  SELECT
    unnest(json_extract(s, '$.matchFeature.features[*]')) AS feature
  FROM j
),
feature_rows AS (
  SELECT
    'matchFeature' AS section,
    'match' AS side,
    row_number() OVER (PARTITION BY feature->>'title') - 1 AS source_index,
    feature->>'title' AS item,
    e.key AS metric,
    NULL::DOUBLE AS value,
    json_extract_string(feature, '$.' || e.key) AS text_value
  FROM features,
  json_each(feature) e
),
xg_items AS (
  SELECT
    unnest(json_extract(s, '$.lastXgTechStat.itemList[*]')) AS item
  FROM j_analy
),
xg_sides AS (
  SELECT
    item,
    'home' AS side,
    json_extract(item, '$.home') AS side_obj
  FROM xg_items
  WHERE json_extract(item, '$.home') IS NOT NULL
  UNION ALL
  SELECT
    item,
    'away' AS side,
    json_extract(item, '$.away') AS side_obj
  FROM xg_items
  WHERE json_extract(item, '$.away') IS NOT NULL
),
xg_rows AS (
  SELECT
    'xg' AS section,
    side,
    row_number() OVER (PARTITION BY side) - 1 AS source_index,
    coalesce(item->>'kind', 'xg') AS item,
    'xg' AS metric,
    try_cast(side_obj->>'text' AS DOUBLE) AS value,
    nullif(trim(side_obj->>'text'), '') AS text_value
  FROM xg_sides
),
all_rows AS (
  SELECT * FROM point_rows
  UNION ALL
  SELECT * FROM stat_rows
  UNION ALL
  SELECT * FROM feature_rows
  UNION ALL
  SELECT * FROM xg_rows
)
INSERT INTO DB.team_stats (
  match_id, section, side, item, metric, value, text_value,
  source_index, source_endpoint
)
SELECT
  (SELECT match_id FROM DB.endpoint_payload WHERE endpoint_key = 'analysis.html'),
  section, side, item, metric, value, text_value,
  source_index,
  CASE WHEN section = 'xg' THEN 'analy.json' ELSE 'analysis.html' END
FROM all_rows;
```

## BUSINESS_TABLES

```yaml
name: BUSINESS_TABLES
table: "球队基本情况"
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
  - USE DB
load_sql: land_business_tables
load_after_sql:
  - USE memory
  - DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB."球队基本情况"
active: true
```

```sql
-- land_business_tables
CREATE OR REPLACE TABLE "球队基本情况" AS
SELECT
  x."比赛ID",
  x."数据类型",
  x."联赛",
  x."主队",
  x."客队",
  x."开球时间",
  x."竞彩编号",
  x."销售日",
  x."队伍",
  x."身份",
  x."姓名",
  x."伤停原因"
FROM (
  SELECT
    m.match_id AS "比赛ID", '比赛信息' AS "数据类型",
    m.league AS "联赛", m.home_team AS "主队", m.away_team AS "客队",
    m.kickoff_at AS "开球时间", m.match_no AS "竞彩编号", m.sales_date AS "销售日",
    '比赛' AS "队伍", NULL AS "身份", NULL AS "姓名",
    NULL AS "伤停原因", 0 AS "排序"
  FROM match_meta m
  UNION ALL
  SELECT
    l.match_id,
    '阵容',
    NULL, NULL, NULL, NULL, NULL, NULL,
    CASE l.side WHEN 'home' THEN '主队' WHEN 'away' THEN '客队' ELSE '未知队伍' END,
    CASE l.role WHEN 'starter' THEN '首发' WHEN 'bench' THEN '替补' ELSE '其他身份' END,
    l.name,
    NULL,
    CASE l.role WHEN 'starter' THEN 0 ELSE 10000 END + l.source_index
  FROM lineup l
  UNION ALL
  SELECT
    i.match_id,
    '伤停',
    NULL, NULL, NULL, NULL, NULL, NULL,
    CASE i.side WHEN 'home' THEN '主队' WHEN 'away' THEN '客队' ELSE '未知队伍' END,
    NULL,
    i.name,
    i.injury_reason,
    i.source_index
  FROM injury i
) x
ORDER BY
  CASE x."数据类型"
    WHEN '比赛信息' THEN 1
    WHEN '阵容' THEN 2
    WHEN '伤停' THEN 3
    ELSE 4
  END,
  CASE x."队伍"
    WHEN '比赛' THEN 0
    WHEN '主队' THEN 1
    WHEN '客队' THEN 2
    ELSE 3
  END,
  x."排序";

-- One row per bookmaker cid. Only direct source snapshot fields are exposed.
-- No MIN/MAX/COUNT, no derived probability, no filled missing values.
CREATE OR REPLACE TABLE "欧指" AS
SELECT
  e.match_id AS "比赛ID",
  e.cid AS "机构编号",
  CASE e.bookmaker
    WHEN 'Macauslot' THEN '澳彩'
    WHEN 'Crown' THEN '皇冠'
    WHEN 'Bet 365' THEN 'Bet365'
    WHEN 'Easybets' THEN '易胜博'
    WHEN 'Pinnacle' THEN '平博'
    WHEN 'HK Jockey Club' THEN '香港马会'
    WHEN 'Sbobet' THEN '利记'
    WHEN 'IBCBET' THEN '沙巴'
    WHEN 'Lottery Official' THEN '中国体彩'
    WHEN 'William Hill' THEN '威廉希尔'
    WHEN 'Ladbrokes' THEN '立博'
    WHEN 'Vcbet' THEN '伟德'
    WHEN 'Betfair' THEN '必发'
    WHEN '10BET' THEN '10Bet'
    WHEN 'Unibet' THEN '优胜客'
    WHEN 'Marathon' THEN '马拉松'
    WHEN 'Betway' THEN '必威'
    ELSE e.bookmaker
  END AS "机构",
  e.initial_home AS "初盘主胜",
  e.initial_draw AS "初盘平局",
  e.initial_away AS "初盘客胜",
  e.initial_return AS "初盘返还率(%)",
  e.latest_home AS "最新主胜",
  e.latest_draw AS "最新平局",
  e.latest_away AS "最新客胜",
  e.latest_return AS "最新返还率(%)"
FROM euro_snapshot e
ORDER BY CASE e.cid
  WHEN 80 THEN 1
  WHEN 545 THEN 2
  WHEN 281 THEN 3
  WHEN 90 THEN 4
  WHEN 177 THEN 5
  WHEN 432 THEN 6
  WHEN 115 THEN 7
  WHEN 82 THEN 8
  WHEN 81 THEN 9
  WHEN 104 THEN 10
  WHEN 255 THEN 11
  WHEN 110 THEN 12
  WHEN 2 THEN 13
  WHEN 474 THEN 14
  WHEN 649 THEN 15
  WHEN 800 THEN 16
  WHEN 482 THEN 17
  WHEN 386 THEN 18
  WHEN 826 THEN 19
  WHEN 16 THEN 20
  WHEN 1129 THEN 21
  ELSE 99
END, e.cid;

-- Full euro time series: one row per source change. Never dedupe timestamps.
-- Sort globally by time first so the whole table has one arrow of time;
-- source_index keeps the original order and is latest-first.
CREATE OR REPLACE TABLE "欧指变盘" AS
SELECT
  h.match_id AS "比赛ID",
  h.cid AS "机构编号",
  CASE h.cid
    WHEN 80 THEN '澳彩'
    WHEN 545 THEN '皇冠'
    WHEN 281 THEN 'Bet365'
    WHEN 90 THEN '易胜博'
    WHEN 177 THEN '平博'
    WHEN 432 THEN '香港马会'
    WHEN 115 THEN '威廉希尔'
    WHEN 82 THEN '立博'
    WHEN 81 THEN '伟德'
    WHEN 104 THEN 'Interwetten'
    WHEN 255 THEN 'Bwin'
    WHEN 110 THEN 'SNAI'
    WHEN 2 THEN '必发'
    WHEN 474 THEN '利记'
    WHEN 649 THEN '沙巴'
    WHEN 800 THEN '马拉松'
    WHEN 482 THEN '必威'
    WHEN 386 THEN '优胜客'
    WHEN 826 THEN 'Paddy Power'
    WHEN 16 THEN '10Bet'
    WHEN 1129 THEN '中国体彩'
    ELSE CAST(h.cid AS VARCHAR)
  END AS "机构",
  h.source_index AS "源序号",
  h.ts_iso AS "变盘时间",
  h.home AS "主胜赔率",
  h.draw AS "平局赔率",
  h.away AS "客胜赔率",
  h.kelly_home AS "凯利主胜",
  h.kelly_draw AS "凯利平局",
  h.kelly_away AS "凯利客胜"
FROM euro_history h
ORDER BY h.ts_iso ASC, h.cid, h.source_index DESC;

CREATE OR REPLACE TABLE "亚盘" AS
SELECT
  a.match_id AS "比赛ID",
  a.company_id AS "机构编号",
  a.bookmaker AS "机构",
  a.first_home AS "初盘主水",
  a.first_line AS "初盘盘口",
  a.first_away AS "初盘客水",
  a.home AS "最新主水",
  a.line AS "最新盘口",
  a.away AS "最新客水",
  a.modify_iso AS "更新时间"
FROM asian_odds a
ORDER BY a.company_id, a.odds_id;

CREATE OR REPLACE TABLE "大小球" AS
SELECT
  o.match_id AS "比赛ID",
  o.company_id AS "机构编号",
  o.bookmaker AS "机构",
  o.first_over AS "初盘大球",
  o.first_line AS "初盘盘口",
  o.first_under AS "初盘小球",
  o."over" AS "最新大球",
  o.line AS "最新盘口",
  o."under" AS "最新小球",
  o.modify_iso AS "更新时间"
FROM over_under o
ORDER BY o.company_id, o.odds_id;
```

## VIEWS

```yaml
name: VIEWS
table: "v_euro_snapshot"
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
  - USE DB
load_sql: land_views
load_after_sql:
  - USE memory
  - DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.main.sqlite_master WHERE type = 'view' AND name LIKE 'v_%'
active: true
```

```sql
-- land_views
CREATE OR REPLACE VIEW "v_euro_snapshot" AS
SELECT * FROM euro_snapshot;

CREATE OR REPLACE VIEW "v_euro_history" AS
SELECT
  match_id, cid, record_id, source_index, ts_local, ts_iso, year,
  home, draw, away, kelly_home, kelly_draw, kelly_away
FROM euro_history
ORDER BY ts_iso ASC, source_index DESC;

CREATE OR REPLACE VIEW "v_asian_odds" AS
SELECT * FROM asian_odds;

CREATE OR REPLACE VIEW "v_over_under" AS
SELECT * FROM over_under;

CREATE OR REPLACE VIEW "v_ah_history" AS
SELECT
  match_id, endpoint_key, company_id, source_index,
  status, home, line_text, away, ts_local, ts_iso
FROM ah_history
ORDER BY ts_iso ASC, source_index DESC;

CREATE OR REPLACE VIEW "v_ou_history" AS
SELECT
  match_id, endpoint_key, company_id, source_index,
  status, "over", line_text, "under", ts_local, ts_iso
FROM ou_history
ORDER BY ts_iso ASC, source_index DESC;

CREATE OR REPLACE VIEW "v_eu_detail_history" AS
SELECT
  match_id, endpoint_key, company_id, source_index,
  home, draw, away, return_rate,
  kelly_home, kelly_draw, kelly_away, ts_local, ts_iso
FROM eu_detail_history
ORDER BY ts_iso ASC, source_index DESC;

CREATE OR REPLACE VIEW "v_injury" AS
SELECT * FROM injury;

CREATE OR REPLACE VIEW "v_lineup" AS
SELECT * FROM lineup;

CREATE OR REPLACE VIEW "v_team_stats" AS
SELECT * FROM team_stats;

-- ETLX's SQLite writer rejects parenthesized compound SELECTs in views;
-- build the 22 raw slots plus the Polymarket delivery slot from a VALUES spine.
CREATE OR REPLACE VIEW "v_bookmaker_slots" AS
WITH nums(rn) AS (
  VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
         (11), (12), (13), (14), (15), (16), (17), (18), (19), (20),
         (21), (22), (23)
),
ranked AS (
  SELECT
    match_id, bookmaker, euro_cid, ah_cid, ou_cid,
    ah_status, ou_status, eu_status, source_label, evidence,
    row_number() OVER (ORDER BY bookmaker) AS rn
  FROM bookmaker_slots
)
SELECT
  COALESCE(r.match_id, (SELECT MIN(match_id) FROM bookmaker_slots)) AS match_id,
  COALESCE(r.bookmaker, 'Polymarket') AS bookmaker,
  r.euro_cid, r.ah_cid, r.ou_cid,
  COALESCE(r.ah_status, 'delivery_only') AS ah_status,
  COALESCE(r.ou_status, 'delivery_only') AS ou_status,
  COALESCE(r.eu_status, 'delivery_only') AS eu_status,
  COALESCE(r.source_label, 'Polymarket') AS source_label,
  COALESCE(r.evidence, 'delivery-only link, no payload') AS evidence,
  CASE WHEN r.rn IS NULL THEN 'delivery_only' ELSE 'database' END AS slot_kind
FROM nums n
LEFT JOIN ranked r ON r.rn = n.rn
WHERE (SELECT COUNT(match_id) FROM bookmaker_slots) = 22
   OR r.rn IS NOT NULL
ORDER BY n.rn;

-- COUNT(match_id) avoids DuckDB's count_star() leaking into the SQLite view.
CREATE OR REPLACE VIEW "v_payload_coverage" AS
SELECT
  match_id,
  COUNT(match_id) AS payload_rows,
  COUNT(DISTINCT endpoint_key) AS endpoint_keys,
  SUM(CASE WHEN content_type = 'empty' THEN 1 ELSE 0 END) AS empty_payloads,
  SUM(CASE WHEN content_type = 'json' THEN 1 ELSE 0 END) AS json_payloads,
  SUM(CASE WHEN content_type = 'html' THEN 1 ELSE 0 END) AS html_payloads,
  SUM(CASE WHEN content_type = 'markdown' THEN 1 ELSE 0 END) AS markdown_payloads,
  SUM(CASE WHEN content_type = 'javascript' THEN 1 ELSE 0 END) AS javascript_payloads
FROM endpoint_payload
GROUP BY match_id;

CREATE OR REPLACE VIEW "v_analysis_status" AS
SELECT *
FROM endpoint_parse_status
WHERE endpoint_key IN ('analysis.html', 'odds.html', 'analy.json');
```

## ENDPOINT_STATUS

```yaml
name: ENDPOINT_STATUS
table: endpoint_parse_status
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_endpoint_status
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.endpoint_parse_status
active: true
```

```sql
-- land_endpoint_status
INSERT INTO DB.endpoint_parse_status (match_id, endpoint_key, row_count, status, note)
SELECT
  p.match_id,
  p.endpoint_key,
  CASE
    WHEN p.endpoint_key = '1x2d.js'
      THEN (SELECT COUNT(*) FROM DB.euro_history h WHERE h.match_id = p.match_id)
    WHEN p.endpoint_key = 'analysis.html'
      THEN (SELECT COUNT(*) FROM DB.team_stats t WHERE t.match_id = p.match_id AND t.source_endpoint = 'analysis.html')
    WHEN p.endpoint_key = 'odds.html'
      THEN (SELECT COUNT(*) FROM DB.injury i WHERE i.match_id = p.match_id)
        + (SELECT COUNT(*) FROM DB.lineup l WHERE l.match_id = p.match_id)
    WHEN p.endpoint_key = 'analy.json'
      THEN (SELECT COUNT(*) FROM DB.team_stats t WHERE t.match_id = p.match_id AND t.source_endpoint = 'analy.json')
    WHEN p.endpoint_key LIKE 'ah_%'
      THEN (SELECT COUNT(*) FROM DB.ah_history h WHERE h.match_id = p.match_id AND h.endpoint_key = p.endpoint_key)
    WHEN p.endpoint_key LIKE 'ou_%'
      THEN (SELECT COUNT(*) FROM DB.ou_history h WHERE h.match_id = p.match_id AND h.endpoint_key = p.endpoint_key)
    WHEN p.endpoint_key LIKE 'eu_%'
      THEN (SELECT COUNT(*) FROM DB.eu_detail_history h WHERE h.match_id = p.match_id AND h.endpoint_key = p.endpoint_key)
    WHEN p.endpoint_key = 'asian_odds.html'
      THEN (SELECT COUNT(*) FROM DB.asian_odds a WHERE a.match_id = p.match_id)
    WHEN p.endpoint_key = 'over_under.html'
      THEN (SELECT COUNT(*) FROM DB.over_under o WHERE o.match_id = p.match_id)
    ELSE 0
  END AS row_count,
  CASE
    WHEN p.state = 'failed' THEN 'unparsed'
    WHEN p.state = 'not_offered' THEN 'not_offered'
    WHEN p.endpoint_key = 'analy.json'
      AND (SELECT COUNT(*) FROM DB.team_stats t WHERE t.match_id = p.match_id AND t.source_endpoint = 'analy.json') > 0
      THEN 'ok'
    WHEN p.endpoint_key = 'analy.json' THEN 'empty'
    WHEN p.content_type = 'empty' THEN 'empty'
    ELSE 'ok'
  END AS status,
  CASE
    WHEN p.state = 'not_offered' THEN 'declared empty state'
    WHEN p.state = 'failed' THEN 'classification failed; build gate blocks'
    WHEN p.endpoint_key = 'odds.html'
      AND (SELECT COUNT(*) FROM DB.lineup l WHERE l.match_id = p.match_id) > 0
      THEN 'lineup_published'
    WHEN p.endpoint_key = 'odds.html' THEN 'lineup_not_published'
    WHEN p.endpoint_key = 'analy.json'
      AND (SELECT COUNT(*) FROM DB.team_stats t WHERE t.match_id = p.match_id AND t.source_endpoint = 'analy.json') > 0
      THEN 'xg rows parsed'
    WHEN p.endpoint_key = 'analy.json'
      AND (SELECT
             (COALESCE(json_array_length(json_extract(j, '$.lastXgTechStat.itemList')), 0) > 0)
             OR (json_extract(j, '$.lastXgTechStat') IS NOT NULL
                 AND json_extract(j, '$.lastXgTechStat.itemList') IS NULL)
             FROM (SELECT TRY_CAST(regexp_extract(
                     content, '(?s)var jsonData\s*=\s*(\{.*?\});', 1
                   ) AS JSON) AS j
                   FROM DB.endpoint_payload
                   WHERE endpoint_key = 'analy.json') src)
      THEN 'xg_parse_failed'
    WHEN p.endpoint_key = 'analy.json' THEN 'xg_not_present'
    ELSE 'derived from typed tables'
  END AS note
FROM DB.endpoint_payload p;
```

## BUILD_MANIFEST

```yaml
name: BUILD_MANIFEST
table: build_manifest
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
load_sql: land_build_manifest
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.build_manifest
active: true
```

```sql
-- land_build_manifest
INSERT INTO DB.build_manifest (
  build_id, match_id, fetched_at, payload_rows,
  euro_snapshot_rows, euro_history_rows, asian_rows, over_under_rows,
  slot_rows, ah_history_rows, ou_history_rows, eu_detail_rows,
  injury_rows, lineup_rows, team_stats_rows, integrity_check, notes
)
SELECT
  (SELECT match_id FROM DB.endpoint_payload LIMIT 1)
    || '-' || (SELECT max(fetched_at) FROM DB.endpoint_payload),
  (SELECT match_id FROM DB.endpoint_payload LIMIT 1),
  (SELECT max(fetched_at) FROM DB.endpoint_payload),
  (SELECT COUNT(*) FROM DB.endpoint_payload),
  (SELECT COUNT(*) FROM DB.euro_snapshot),
  (SELECT COUNT(*) FROM DB.euro_history),
  (SELECT COUNT(*) FROM DB.asian_odds),
  (SELECT COUNT(*) FROM DB.over_under),
  (SELECT COUNT(*) FROM DB.bookmaker_slots),
  (SELECT COUNT(*) FROM DB.ah_history),
  (SELECT COUNT(*) FROM DB.ou_history),
  (SELECT COUNT(*) FROM DB.eu_detail_history),
  (SELECT COUNT(*) FROM DB.injury),
  (SELECT COUNT(*) FROM DB.lineup),
  (SELECT COUNT(*) FROM DB.team_stats),
  'not_checked_in_pipeline',
  'official Scrapling JSONL -> ETLX; external SQLite gate required';
```


# QUALITY

```yaml
name: QUALITY
runs_as: DATA_QUALITY
description: "Assert the final row counts and delivery-only exclusions."
active: true
```

## GATE_LIVE

```yaml
name: GATE_LIVE
description: "Check live row counts, payload coverage, hashes, and delivery-only exclusions."
connection: "duckdb:"
before_sql: "ATTACH 'data/.staging/build.db' AS DB (TYPE SQLITE)"
query: gate_live
column: violations
after_sql: "DETACH DB"
active: true
```

```sql
-- gate_live
WITH checks(gate, observed, expected) AS (
  SELECT 'endpoint_payload_rows', (SELECT COUNT(*) FROM DB.endpoint_payload), 27
  UNION ALL SELECT 'endpoint_keys', (SELECT COUNT(DISTINCT endpoint_key) FROM DB.endpoint_payload), 27
  UNION ALL SELECT 'single_match_id', (SELECT COUNT(DISTINCT match_id) FROM DB.endpoint_payload), 1
  UNION ALL SELECT 'match_identity',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.build_manifest WHERE match_id = (SELECT MIN(match_id) FROM DB.endpoint_payload)) = 1
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'match_meta_rows', (SELECT COUNT(*) FROM DB.match_meta), 1
  UNION ALL SELECT 'match_meta_identity',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.match_meta
             WHERE match_id = (SELECT MIN(match_id) FROM DB.endpoint_payload)
               AND length(trim(match_no)) > 0
               AND length(trim(league)) > 0
               AND length(trim(home_team)) > 0
               AND length(trim(away_team)) > 0
               AND length(trim(kickoff_at)) >= 16) = 1
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'failed_payload_rows', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE state = 'failed'), 0
  UNION ALL SELECT 'content_hash_mismatches', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE lower(sha256) <> lower(sha256(content))), 0
  UNION ALL SELECT 'payload_chars_mismatches', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE coalesce(chars, -1) <> length(content)), 0
  UNION ALL SELECT 'raw_hash_lengths', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE length(coalesce(raw_sha256, '')) <> 64), 0
  UNION ALL SELECT 'bookmaker_coverage',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.euro_snapshot) = 21
       AND (SELECT COUNT(DISTINCT cid) FROM DB.euro_history) = 21
       AND (SELECT COUNT(*) FROM DB.bookmaker_slots) = 22
       AND (SELECT COUNT(DISTINCT match_id) FROM DB.bookmaker_slots) = 1
       AND (SELECT COUNT(*) FROM DB.endpoint_parse_status) = 27
       AND (SELECT COUNT(*) FROM DB.bookmaker_slots
             WHERE bookmaker IN ('澳彩', '皇冠', 'Bet365', '易胜博', '平博', '香港马会', '188Bet')
               AND ah_status = 'supported' AND ou_status = 'supported') = 7
       AND (SELECT COUNT(DISTINCT company_id) FROM DB.asian_odds) >= 7
       AND (SELECT COUNT(DISTINCT company_id) FROM DB.over_under) >= 7
       AND (SELECT COUNT(DISTINCT company_id) FROM DB.ah_history) >= 7
       AND (SELECT COUNT(DISTINCT company_id) FROM DB.ou_history) >= 7
       AND (SELECT COUNT(DISTINCT company_id) FROM DB.eu_detail_history) >= 6
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'core_tables_present',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.match_meta) > 0
       AND (SELECT COUNT(*) FROM DB.euro_snapshot) > 0
       AND (SELECT COUNT(*) FROM DB.euro_history) > 0
       AND (SELECT COUNT(*) FROM DB.asian_odds) > 0
       AND (SELECT COUNT(*) FROM DB.over_under) > 0
       AND (SELECT COUNT(*) FROM DB.ah_history) > 0
       AND (SELECT COUNT(*) FROM DB.ou_history) > 0
       AND (SELECT COUNT(*) FROM DB.eu_detail_history) > 0
       AND (SELECT COUNT(*) FROM DB.team_stats) > 0
       AND (SELECT COUNT(*) FROM DB.team_stats WHERE source_endpoint = 'analysis.html') > 0
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'business_tables_present',
    CASE
      WHEN (SELECT COUNT(*) FROM main.sqlite_master
             WHERE type = 'table'
               AND name IN ('球队基本情况', '欧指', '欧指变盘', '亚盘', '大小球')) = 5
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'euro_detail_rows',
    CASE
      WHEN (SELECT COUNT(*) FROM DB."欧指变盘") =
           (SELECT COUNT(*) FROM DB.euro_history)
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'read_views_present',
    CASE
      WHEN (SELECT COUNT(*) FROM main.sqlite_master
             WHERE type = 'view'
               AND name IN (
                 'v_euro_snapshot', 'v_euro_history', 'v_asian_odds',
                 'v_over_under', 'v_ah_history', 'v_ou_history',
                 'v_eu_detail_history', 'v_injury', 'v_lineup',
                 'v_team_stats', 'v_bookmaker_slots',
                 'v_payload_coverage', 'v_analysis_status'
               )) = 13
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'manifest_payload_binding',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.build_manifest
             WHERE fetched_at = (SELECT MAX(fetched_at) FROM DB.endpoint_payload)
               AND match_id = (SELECT MIN(match_id) FROM DB.endpoint_payload)) = 1
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'content_types',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.endpoint_payload
            WHERE (endpoint_key = 'analy.json' AND content_type = 'html')
               OR (endpoint_key IN ('asian_odds.html', 'over_under.html') AND content_type = 'json')) = 3
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'capture_timestamp',
    (SELECT COUNT(*) FROM DB.build_manifest WHERE fetched_at IS NOT NULL AND length(fetched_at) >= 19),
    1
  UNION ALL SELECT 'xg_state',
    (SELECT COUNT(*) FROM DB.endpoint_parse_status
      WHERE endpoint_key = 'analy.json' AND note IN ('xg rows parsed', 'xg_not_present')),
    1
  UNION ALL SELECT 'lineup_state', (SELECT COUNT(*) FROM DB.endpoint_parse_status WHERE endpoint_key = 'odds.html' AND note IN ('lineup_published', 'lineup_not_published')), 1
  UNION ALL SELECT 'lineup_parse_consistency',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.lineup WHERE role = 'starter') = 0
        AND (
          (SELECT content FROM DB.endpoint_payload WHERE endpoint_key = 'odds.html')
            NOT LIKE '%"homePlayerList":[]%'
          OR (SELECT content FROM DB.endpoint_payload WHERE endpoint_key = 'odds.html')
            NOT LIKE '%"guestPlayerList":[]%'
        )
      THEN 1 ELSE 0
    END,
    0
  UNION ALL SELECT 'lineup_count_matches',
    CASE
      WHEN (SELECT COUNT(*) FROM DB.lineup) =
           (SELECT COALESCE(json_array_length(json_extract(j, '$.lineup.homePlayerList')), 0)
                 + COALESCE(json_array_length(json_extract(j, '$.lineup.guestPlayerList')), 0)
                 + COALESCE(json_array_length(json_extract(j, '$.lineup.homeBakPlayerList')), 0)
                 + COALESCE(json_array_length(json_extract(j, '$.lineup.guestBakPlayerList')), 0)
            FROM (SELECT TRY_CAST(regexp_extract(
                    content, '(?s)var lineupObj\s*=\s*(\{.*?\});', 1
                  ) AS JSON) AS j
                  FROM DB.endpoint_payload
                  WHERE endpoint_key = 'odds.html') src)
      THEN 1 ELSE 0
    END,
    1
  UNION ALL SELECT 'presence_rows', (SELECT COUNT(*) FROM DB.team_stats WHERE metric = 'presence'), 0
)
SELECT COALESCE(SUM(CASE WHEN observed = expected THEN 0 ELSE 1 END), 0) AS violations FROM checks;
```
