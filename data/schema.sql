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
CREATE VIEW v_euro_snapshot AS
SELECT * FROM euro_snapshot;
/* v_euro_snapshot(match_id,cid,bookmaker,record_id,hist_count,initial_home,initial_draw,initial_away,initial_prob_home,initial_prob_draw,initial_prob_away,initial_return,latest_home,latest_draw,latest_away,latest_prob_home,latest_prob_draw,latest_prob_away,latest_return,source_time,alias) */
CREATE VIEW v_euro_history AS
SELECT
  match_id, cid, record_id, source_index, ts_local, ts_iso, year,
  home, draw, away, kelly_home, kelly_draw, kelly_away
FROM euro_history
ORDER BY ts_iso ASC, source_index ASC;
/* v_euro_history(match_id,cid,record_id,source_index,ts_local,ts_iso,year,home,draw,away,kelly_home,kelly_draw,kelly_away) */
CREATE VIEW v_asian_odds AS
SELECT * FROM asian_odds;
/* v_asian_odds(match_id,company_id,bookmaker,odds_id,first_home,first_line,first_away,home,line,away,modify_ts,modify_iso) */
CREATE VIEW v_over_under AS
SELECT * FROM over_under;
/* v_over_under(match_id,company_id,bookmaker,odds_id,first_over,first_line,first_under,"over",line,under,modify_ts,modify_iso) */
CREATE VIEW v_ah_history AS
SELECT
  match_id, endpoint_key, company_id, source_index,
  status, home, line_text, away, ts_local, ts_iso
FROM ah_history
ORDER BY ts_iso ASC, source_index ASC;
/* v_ah_history(match_id,endpoint_key,company_id,source_index,status,home,line_text,away,ts_local,ts_iso) */
CREATE VIEW v_ou_history AS
SELECT
  match_id, endpoint_key, company_id, source_index,
  status, "over", line_text, "under", ts_local, ts_iso
FROM ou_history
ORDER BY ts_iso ASC, source_index ASC;
/* v_ou_history(match_id,endpoint_key,company_id,source_index,status,"over",line_text,under,ts_local,ts_iso) */
CREATE VIEW v_eu_detail_history AS
SELECT
  match_id, endpoint_key, company_id, source_index,
  home, draw, away, return_rate,
  kelly_home, kelly_draw, kelly_away, ts_local, ts_iso
FROM eu_detail_history
ORDER BY ts_iso ASC, source_index ASC;
/* v_eu_detail_history(match_id,endpoint_key,company_id,source_index,home,draw,away,return_rate,kelly_home,kelly_draw,kelly_away,ts_local,ts_iso) */
CREATE VIEW v_injury AS
SELECT * FROM injury;
/* v_injury(match_id,side,source_index,number,name,player_id,position,injury_reason,captain_type,player_kind,source_endpoint) */
CREATE VIEW v_lineup AS
SELECT * FROM lineup;
/* v_lineup(match_id,side,role,source_index,number,name,player_id,position,formation,source_endpoint) */
CREATE VIEW v_team_stats AS
SELECT * FROM team_stats;
/* v_team_stats(match_id,section,side,item,metric,value,text_value,source_index,source_endpoint) */
CREATE VIEW v_bookmaker_slots AS
SELECT
  match_id, bookmaker, euro_cid, ah_cid, ou_cid,
  ah_status, ou_status, eu_status, source_label, evidence,
  'database' AS slot_kind
FROM bookmaker_slots
UNION ALL
SELECT
  match_id, 'Polymarket', NULL, NULL, NULL,
  'delivery_only', 'delivery_only', 'delivery_only',
  'Polymarket', 'delivery-only link, no payload', 'delivery_only'
FROM (SELECT DISTINCT match_id FROM bookmaker_slots);
/* v_bookmaker_slots(match_id,bookmaker,euro_cid,ah_cid,ou_cid,ah_status,ou_status,eu_status,source_label,evidence,slot_kind) */
CREATE VIEW v_payload_coverage AS
SELECT
  match_id,
  COUNT(*) AS payload_rows,
  COUNT(DISTINCT endpoint_key) AS endpoint_keys,
  SUM(CASE WHEN content_type = 'empty' THEN 1 ELSE 0 END) AS empty_payloads,
  SUM(CASE WHEN content_type = 'json' THEN 1 ELSE 0 END) AS json_payloads,
  SUM(CASE WHEN content_type = 'html' THEN 1 ELSE 0 END) AS html_payloads,
  SUM(CASE WHEN content_type = 'markdown' THEN 1 ELSE 0 END) AS markdown_payloads,
  SUM(CASE WHEN content_type = 'javascript' THEN 1 ELSE 0 END) AS javascript_payloads
FROM endpoint_payload
GROUP BY match_id;
/* v_payload_coverage(match_id,payload_rows,endpoint_keys,empty_payloads,json_payloads,html_payloads,javascript_payloads) */
CREATE VIEW v_analysis_status AS
SELECT *
FROM endpoint_parse_status
WHERE endpoint_key IN ('analysis.html', 'odds.html', 'analy.json');
/* v_analysis_status(match_id,endpoint_key,row_count,status,note) */
CREATE VIEW "球队基本情况" AS
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
    COALESCE(NULLIF(TRIM(i.injury_reason), ''), '未说明'),
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
/* 球队基本情况(比赛ID,数据类型,联赛,主队,客队,开球时间,竞彩编号,销售日,队伍,身份,姓名,伤停原因) */
CREATE VIEW "欧指" AS
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
  e.initial_return AS "初盘返还率",
  e.latest_home AS "最新主胜",
  e.latest_draw AS "最新平局",
  e.latest_away AS "最新客胜",
  e.latest_return AS "最新返还率",
  e.source_time AS "数据时间",
  (SELECT COUNT(*) FROM euro_history h
    WHERE h.match_id = e.match_id AND h.cid = e.cid) AS "变盘行数",
  (SELECT MIN(h.ts_iso) FROM euro_history h
    WHERE h.match_id = e.match_id AND h.cid = e.cid) AS "首笔时间",
  (SELECT MAX(h.ts_iso) FROM euro_history h
    WHERE h.match_id = e.match_id AND h.cid = e.cid) AS "末笔时间"
FROM euro_snapshot e;
/* 欧指(比赛ID,机构编号,机构,初盘主胜,初盘平局,初盘客胜,初盘返还率,最新主胜,最新平局,最新客胜,最新返还率,数据时间,变盘行数,首笔时间,末笔时间) */
CREATE VIEW "亚盘" AS
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
  a.modify_iso AS "更新时间",
  (SELECT COUNT(*) FROM ah_history h
    WHERE h.match_id = a.match_id AND h.company_id = a.company_id) AS "变盘行数",
  (SELECT MIN(h.ts_iso) FROM ah_history h
    WHERE h.match_id = a.match_id AND h.company_id = a.company_id) AS "首笔时间",
  (SELECT MAX(h.ts_iso) FROM ah_history h
    WHERE h.match_id = a.match_id AND h.company_id = a.company_id) AS "末笔时间"
FROM asian_odds a;
/* 亚盘(比赛ID,机构编号,机构,初盘主水,初盘盘口,初盘客水,最新主水,最新盘口,最新客水,更新时间,变盘行数,首笔时间,末笔时间) */
CREATE VIEW "大小球" AS
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
  o.modify_iso AS "更新时间",
  (SELECT COUNT(*) FROM ou_history h
    WHERE h.match_id = o.match_id AND h.company_id = o.company_id) AS "变盘行数",
  (SELECT MIN(h.ts_iso) FROM ou_history h
    WHERE h.match_id = o.match_id AND h.company_id = o.company_id) AS "首笔时间",
  (SELECT MAX(h.ts_iso) FROM ou_history h
    WHERE h.match_id = o.match_id AND h.company_id = o.company_id) AS "末笔时间"
FROM over_under o;
/* 大小球(比赛ID,机构编号,机构,初盘大球,初盘盘口,初盘小球,最新大球,最新盘口,最新小球,更新时间,变盘行数,首笔时间,末笔时间) */
