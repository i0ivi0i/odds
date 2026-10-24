<!-- One-file ETLX pipeline for the live 3003920 build. The typed schema and read-only views come from data/schema.sql; this file lands the 27 analysis endpoints through the official ETLX -file handoff, then derives every analysis table from DB.endpoint_payload. A from-zero rebuild requires the schema bootstrap because ETLX's DuckDB SQLite attach cannot execute SQLite STRICT or foreign-key DDL. -->

# PIPELINE

```yaml
name: PIPELINE
description: Load the 3003920 build database from the official Scrapling JSONL; schema and views must already exist.
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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

## EURO_SNAPSHOT

```yaml
name: EURO_SNAPSHOT
table: euro_snapshot
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  match_id, cid, bookmaker, record_id, hist_count,
  initial_home, initial_draw, initial_away,
  initial_prob_home, initial_prob_draw, initial_prob_away, initial_return,
  latest_home, latest_draw, latest_away,
  latest_prob_home, latest_prob_draw, latest_prob_away, latest_return,
  source_time, alias
)
SELECT
  match_id, cid, bookmaker, record_id, 0,
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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

## EURO_REFRESH

```yaml
name: EURO_REFRESH
table: euro_snapshot
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
load_sql: refresh_euro_counts
load_after_sql: DETACH DB
rows_sql: SELECT COUNT(*) AS nrows FROM DB.euro_snapshot WHERE hist_count > 0
active: true
```

```sql
-- refresh_euro_counts
UPDATE DB.euro_snapshot AS e
SET hist_count = (
  SELECT COUNT(*)
  FROM DB.euro_history AS h
  WHERE h.match_id = e.match_id
    AND h.cid = e.cid
);
```

## ASIAN_ODDS

```yaml
name: ASIAN_ODDS
table: asian_odds
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
    coalesce(player->>'number', '') AS number,
    coalesce(player->>'name', '') AS name,
    coalesce(player->>'Id', '') AS player_id,
    coalesce(player->>'pos', '') AS position,
    coalesce(player->>'injuryReson', '') AS injury_reason,
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

## TEAM_STATS

```yaml
name: TEAM_STATS
table: team_stats
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
all_rows AS (
  SELECT * FROM point_rows
  UNION ALL
  SELECT * FROM stat_rows
  UNION ALL
  SELECT * FROM feature_rows
  UNION ALL
  SELECT 'xg', 'match', 0, 'xg_presence', 'presence', NULL::DOUBLE, 'not_present'
  UNION ALL
  SELECT 'events', 'match', 0, 'analy_json_presence', 'presence', NULL::DOUBLE, 'no_structured_event_rows'
)
INSERT INTO DB.team_stats (
  match_id, section, side, item, metric, value, text_value,
  source_index, source_endpoint
)
SELECT
  (SELECT match_id FROM DB.endpoint_payload WHERE endpoint_key = 'analysis.html'),
  section, side, item, metric, value, text_value,
  source_index,
  CASE WHEN section = 'events' THEN 'analy.json' ELSE 'analysis.html' END
FROM all_rows;
```

## ENDPOINT_STATUS

```yaml
name: ENDPOINT_STATUS
table: endpoint_parse_status
load_conn: "duckdb:"
load_before_sql:
  - INSTALL sqlite
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
    WHEN p.endpoint_key = 'analy.json' THEN 'empty'
    WHEN p.content_type = 'empty' THEN 'empty'
    ELSE 'ok'
  END AS status,
  CASE
    WHEN p.state = 'not_offered' THEN 'declared empty state'
    WHEN p.state = 'failed' THEN 'classification failed; build gate blocks'
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
  - "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  'ok',
  'official Scrapling JSONL -> ETLX; final promotion gate required';
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
before_sql: "ATTACH 'data/2026-10-24/3003920.build.db' AS DB (TYPE SQLITE)"
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
  UNION ALL SELECT 'polymarket_payload_rows', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE endpoint_key = 'polymarket.json'), 0
  UNION ALL SELECT 'eu42_not_offered', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE endpoint_key = 'eu_42.html' AND content_type = 'empty' AND state = 'not_offered'), 1
  UNION ALL SELECT 'failed_payload_rows', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE state = 'failed'), 0
  UNION ALL SELECT 'content_hash_mismatches', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE lower(sha256) <> lower(sha256(content))), 0
  UNION ALL SELECT 'bad_raw_hash_lengths', (SELECT COUNT(*) FROM DB.endpoint_payload WHERE length(raw_sha256) <> 64), 0
  UNION ALL SELECT 'euro_snapshot_rows', (SELECT COUNT(*) FROM DB.euro_snapshot), 21
  UNION ALL SELECT 'euro_history_cids', (SELECT COUNT(DISTINCT cid) FROM DB.euro_history), 21
  UNION ALL SELECT 'bookmaker_slots_rows', (SELECT COUNT(*) FROM DB.bookmaker_slots), 22
  UNION ALL SELECT 'bookmaker_view_rows', (SELECT COUNT(*) FROM DB.v_bookmaker_slots), 23
  UNION ALL SELECT 'endpoint_parse_status_rows', (SELECT COUNT(*) FROM DB.endpoint_parse_status), 27
  UNION ALL SELECT 'build_manifest_rows', (SELECT COUNT(*) FROM DB.build_manifest), 1
  UNION ALL SELECT 'euro_snapshot_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.euro_snapshot), 1
  UNION ALL SELECT 'euro_history_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.euro_history), 1
  UNION ALL SELECT 'asian_odds_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.asian_odds), 1
  UNION ALL SELECT 'over_under_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.over_under), 1
  UNION ALL SELECT 'ah_history_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.ah_history), 1
  UNION ALL SELECT 'ou_history_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.ou_history), 1
  UNION ALL SELECT 'eu_detail_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.eu_detail_history), 1
  UNION ALL SELECT 'team_stats_floor', (SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM DB.team_stats), 1
)
SELECT COALESCE(SUM(CASE WHEN observed = expected THEN 0 ELSE 1 END), 0) AS violations FROM checks;
```
