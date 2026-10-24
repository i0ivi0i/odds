-- Physical SQLite schema for one match database.
-- This file owns STRICT tables, primary keys, NOT NULL, CHECK constraints, and foreign-key declarations.
-- Business cleaning, the four Chinese business tables, and all v_* read-only views live in data/pipeline.md.
-- ETLX creates the business tables and views after the raw tables are loaded.
CREATE TABLE endpoint_payload (
  match_id TEXT NOT NULL,
  endpoint_key TEXT NOT NULL,
  content_type TEXT NOT NULL CHECK (content_type IN ('javascript', 'html', 'json', 'markdown', 'empty')),
  content TEXT NOT NULL,
  chars INTEGER NOT NULL CHECK (chars >= 0),
  raw_sha256 TEXT NOT NULL CHECK (length(raw_sha256) = 64),
  sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
  source_url TEXT NOT NULL,
  fetched_at TEXT NOT NULL,
  status INTEGER NOT NULL,
  state TEXT NOT NULL,
  empty_state TEXT,
  PRIMARY KEY (match_id, endpoint_key)
) STRICT;
CREATE TABLE euro_snapshot (
  match_id TEXT NOT NULL,
  cid INTEGER NOT NULL,
  bookmaker TEXT NOT NULL,
  record_id TEXT NOT NULL,
  hist_count INTEGER NOT NULL CHECK (hist_count >= 0),
  initial_home REAL NOT NULL CHECK (initial_home > 1.0),
  initial_draw REAL NOT NULL CHECK (initial_draw > 1.0),
  initial_away REAL NOT NULL CHECK (initial_away > 1.0),
  initial_prob_home REAL NOT NULL,
  initial_prob_draw REAL NOT NULL,
  initial_prob_away REAL NOT NULL,
  initial_return REAL NOT NULL CHECK (initial_return > 0.0 AND initial_return < 200.0),
  latest_home REAL NOT NULL CHECK (latest_home > 1.0),
  latest_draw REAL NOT NULL CHECK (latest_draw > 1.0),
  latest_away REAL NOT NULL CHECK (latest_away > 1.0),
  latest_prob_home REAL NOT NULL,
  latest_prob_draw REAL NOT NULL,
  latest_prob_away REAL NOT NULL,
  latest_return REAL NOT NULL CHECK (latest_return > 0.0 AND latest_return < 200.0),
  source_time TEXT NOT NULL,
  alias TEXT NOT NULL,
  PRIMARY KEY (match_id, cid),
  UNIQUE (match_id, record_id)
) STRICT;
CREATE TABLE euro_history (
  match_id TEXT NOT NULL,
  cid INTEGER NOT NULL,
  record_id TEXT NOT NULL,
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  ts_local TEXT NOT NULL,
  ts_iso TEXT NOT NULL CHECK (ts_iso GLOB '????-??-?? ??:??'),
  year INTEGER NOT NULL,
  home REAL NOT NULL CHECK (home > 1.0),
  draw REAL NOT NULL CHECK (draw > 1.0),
  away REAL NOT NULL CHECK (away > 1.0),
  kelly_home REAL NOT NULL,
  kelly_draw REAL NOT NULL,
  kelly_away REAL NOT NULL,
  PRIMARY KEY (match_id, cid, ts_iso, home, draw, away),
  FOREIGN KEY (match_id, cid) REFERENCES euro_snapshot(match_id, cid)
) STRICT;
CREATE TABLE asian_odds (
  match_id TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  bookmaker TEXT NOT NULL,
  odds_id INTEGER NOT NULL,
  first_home REAL NOT NULL CHECK (first_home > 0.0),
  first_line REAL CHECK (first_line IS NULL OR first_line BETWEEN -10.0 AND 10.0),
  first_away REAL NOT NULL CHECK (first_away > 0.0),
  home REAL NOT NULL CHECK (home > 0.0),
  line REAL CHECK (line IS NULL OR line BETWEEN -10.0 AND 10.0),
  away REAL NOT NULL CHECK (away > 0.0),
  modify_ts INTEGER NOT NULL CHECK (modify_ts > 0),
  modify_iso TEXT NOT NULL CHECK (modify_iso GLOB '????-??-?? ??:??'),
  PRIMARY KEY (match_id, company_id, odds_id)
) STRICT;
CREATE TABLE over_under (
  match_id TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  bookmaker TEXT NOT NULL,
  odds_id INTEGER NOT NULL,
  first_over REAL NOT NULL CHECK (first_over > 0.0),
  first_line REAL CHECK (first_line IS NULL OR first_line BETWEEN 0.0 AND 20.0),
  first_under REAL NOT NULL CHECK (first_under > 0.0),
  over REAL NOT NULL CHECK (over > 0.0),
  line REAL CHECK (line IS NULL OR line BETWEEN 0.0 AND 20.0),
  under REAL NOT NULL CHECK (under > 0.0),
  modify_ts INTEGER NOT NULL CHECK (modify_ts > 0),
  modify_iso TEXT NOT NULL CHECK (modify_iso GLOB '????-??-?? ??:??'),
  PRIMARY KEY (match_id, company_id, odds_id)
) STRICT;
CREATE TABLE ah_history (
  match_id TEXT NOT NULL,
  endpoint_key TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  status TEXT NOT NULL,
  home REAL NOT NULL CHECK (home > 0.0),
  line_text TEXT,
  away REAL NOT NULL CHECK (away > 0.0),
  ts_local TEXT NOT NULL,
  ts_iso TEXT NOT NULL CHECK (ts_iso GLOB '????-??-?? ??:??'),
  PRIMARY KEY (match_id, endpoint_key, source_index)
) STRICT;
CREATE TABLE ou_history (
  match_id TEXT NOT NULL,
  endpoint_key TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  status TEXT NOT NULL,
  over REAL NOT NULL CHECK (over > 0.0),
  line_text TEXT,
  under REAL NOT NULL CHECK (under > 0.0),
  ts_local TEXT NOT NULL,
  ts_iso TEXT NOT NULL CHECK (ts_iso GLOB '????-??-?? ??:??'),
  PRIMARY KEY (match_id, endpoint_key, source_index)
) STRICT;
CREATE TABLE eu_detail_history (
  match_id TEXT NOT NULL,
  endpoint_key TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  home REAL NOT NULL CHECK (home > 1.0),
  draw REAL NOT NULL CHECK (draw > 1.0),
  away REAL NOT NULL CHECK (away > 1.0),
  return_rate REAL NOT NULL CHECK (return_rate > 0.0 AND return_rate < 200.0),
  kelly_home REAL NOT NULL,
  kelly_draw REAL NOT NULL,
  kelly_away REAL NOT NULL,
  ts_local TEXT NOT NULL,
  ts_iso TEXT NOT NULL CHECK (ts_iso GLOB '????-??-?? ??:??'),
  PRIMARY KEY (match_id, endpoint_key, source_index)
) STRICT;
CREATE TABLE bookmaker_slots (
  match_id TEXT NOT NULL,
  bookmaker TEXT NOT NULL,
  euro_cid INTEGER,
  ah_cid INTEGER,
  ou_cid INTEGER,
  ah_status TEXT NOT NULL CHECK (ah_status IN ('supported', 'not_offered')),
  ou_status TEXT NOT NULL CHECK (ou_status IN ('supported', 'not_offered')),
  eu_status TEXT NOT NULL CHECK (eu_status IN ('supported', 'not_offered')),
  source_label TEXT NOT NULL,
  evidence TEXT NOT NULL,
  PRIMARY KEY (match_id, bookmaker)
) STRICT;
CREATE TABLE injury (
  match_id TEXT NOT NULL,
  side TEXT NOT NULL CHECK (side IN ('home', 'away')),
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  number TEXT NOT NULL,
  name TEXT NOT NULL,
  player_id TEXT NOT NULL,
  position TEXT NOT NULL,
  injury_reason TEXT NOT NULL,
  captain_type INTEGER NOT NULL,
  player_kind INTEGER NOT NULL,
  source_endpoint TEXT NOT NULL,
  PRIMARY KEY (match_id, side, player_id)
) STRICT;
CREATE TABLE lineup (
  match_id TEXT NOT NULL,
  side TEXT NOT NULL CHECK (side IN ('home', 'away')),
  role TEXT NOT NULL CHECK (role IN ('starter', 'bench')),
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  number TEXT NOT NULL,
  name TEXT NOT NULL,
  player_id TEXT NOT NULL,
  position TEXT NOT NULL,
  formation TEXT NOT NULL,
  source_endpoint TEXT NOT NULL,
  PRIMARY KEY (match_id, side, role, player_id)
) STRICT;
CREATE TABLE team_stats (
  match_id TEXT NOT NULL,
  section TEXT NOT NULL,
  side TEXT NOT NULL CHECK (side IN ('home', 'away', 'match')),
  item TEXT NOT NULL,
  metric TEXT NOT NULL,
  value REAL,
  text_value TEXT,
  source_index INTEGER NOT NULL CHECK (source_index >= 0),
  source_endpoint TEXT NOT NULL,
  PRIMARY KEY (match_id, section, side, item, metric, source_index)
) STRICT;
CREATE TABLE endpoint_parse_status (
  match_id TEXT NOT NULL,
  endpoint_key TEXT NOT NULL,
  row_count INTEGER NOT NULL CHECK (row_count >= 0),
  status TEXT NOT NULL CHECK (status IN ('ok', 'empty', 'not_offered', 'unparsed')),
  note TEXT,
  PRIMARY KEY (match_id, endpoint_key)
) STRICT;
CREATE TABLE build_manifest (
  build_id TEXT PRIMARY KEY,
  match_id TEXT NOT NULL,
  fetched_at TEXT NOT NULL,
  payload_rows INTEGER NOT NULL CHECK (payload_rows >= 0),
  euro_snapshot_rows INTEGER NOT NULL CHECK (euro_snapshot_rows >= 0),
  euro_history_rows INTEGER NOT NULL CHECK (euro_history_rows >= 0),
  asian_rows INTEGER NOT NULL CHECK (asian_rows >= 0),
  over_under_rows INTEGER NOT NULL CHECK (over_under_rows >= 0),
  slot_rows INTEGER NOT NULL CHECK (slot_rows >= 0),
  ah_history_rows INTEGER NOT NULL CHECK (ah_history_rows >= 0),
  ou_history_rows INTEGER NOT NULL CHECK (ou_history_rows >= 0),
  eu_detail_rows INTEGER NOT NULL CHECK (eu_detail_rows >= 0),
  injury_rows INTEGER NOT NULL CHECK (injury_rows >= 0),
  lineup_rows INTEGER NOT NULL CHECK (lineup_rows >= 0),
  team_stats_rows INTEGER NOT NULL CHECK (team_stats_rows >= 0),
  integrity_check TEXT NOT NULL,
  notes TEXT
) STRICT;
CREATE TABLE match_meta (
  match_id TEXT PRIMARY KEY,
  sales_date TEXT NOT NULL CHECK (sales_date GLOB '????-??-??'),
  match_no TEXT NOT NULL,
  league TEXT NOT NULL,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  kickoff_at TEXT NOT NULL CHECK (kickoff_at GLOB '????-??-?? ??:??'),
  source TEXT NOT NULL
) STRICT;

-- Read-only views are generated by data/pipeline.md (VIEWS step).
