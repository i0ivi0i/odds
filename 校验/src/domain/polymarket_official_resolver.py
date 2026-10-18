"""
校验/src/domain/polymarket_official_resolver.py
领域服务: Polymarket 官方 Discover Markets 规范发现与解析引擎

依据 Polymarket 官方文档 (https://docs.polymarket.com/llms.txt):
1. Discover Markets: 通过 Gamma API public-search 发现事件
2. 双向核对: 提取主客队官方英文名，进行双向对阵匹配，严格过滤 active: true, closed: false
3. 官方 Slug 提取: 获取官方 events.slug，按官方规范拼接标准链接 https://polymarket.com/event/{slug}
4. 市场与挂单深度: 获取 1X2 胜平负 markets 与各端点 outcomePrices
"""

import json
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def extract_team_keywords(name: str) -> List[str]:
    """提取球队核心辨识关键字，剥离 FC, CF, SC, City, United 等通用后缀"""
    clean = re.sub(
        r"\b(FC|CF|SC|City|United|Town|Athletic|Club|de|la|del|FK|BV|SE|AC|AS|Real|Borussia|Sporting)\b",
        "",
        name,
        flags=re.I,
    ).strip()
    words = [w for w in re.split(r"[\s\.\-]+", clean) if len(w) >= 3]
    return words if words else [name.strip()]


import subprocess

def _curl_get_json(url: str, timeout: int = 15) -> Optional[Any]:
    """使用 Windows 原生 curl.exe 获取 JSON 数据，带 --ssl-no-revoke 与 --http1.1 防止截断"""
    try:
        cmd = [
            "curl.exe", "-s", "--ssl-no-revoke", "--http1.1",
            "--max-time", str(timeout),
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            url
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and res.stdout:
            raw_text = res.stdout.decode("utf-8", errors="replace")
            return json.loads(raw_text)
    except Exception:
        pass
    return None

# Polymarket 官方 /sports 联赛标识与 primaryTagId 映射表 (源自 GET https://gamma-api.polymarket.com/sports)
OFFICIAL_SOCCER_LEAGUES: Dict[str, Tuple[str, int]] = {
    # 核心五大联赛及次级
    "西甲": ("lal", 780),
    "laliga": ("lal", 780),
    "la liga": ("lal", 780),
    "英超": ("epl", 306),
    "premier league": ("epl", 306),
    "意甲": ("sea", 101962),
    "serie a": ("sea", 101962),
    "德甲": ("bun", 1494),
    "bundesliga": ("bun", 1494),
    "法甲": ("fl1", 102070),
    "ligue 1": ("fl1", 102070),
    "英冠": ("elc", 102643),
    "championship": ("elc", 102643),
    "西乙": ("es2", 102866),
    "laliga2": ("es2", 102866),
    "德乙": ("bl2", 102864),
    "2. bundesliga": ("bl2", 102864),
    "意乙": ("itsb", 102870),
    "serie b": ("itsb", 102870),
    "法乙": ("fr2", 102871),
    "ligue 2": ("fr2", 102871),
    "荷乙": ("ned2", 105727),
    "eerste divisie": ("ned2", 105727),
    # 欧洲各主流联赛
    "荷甲": ("ere", 101735),
    "eredivisie": ("ere", 101735),
    "葡超": ("por", 101772),
    "primeira liga": ("por", 101772),
    "芬超": ("fin1", 105243),
    "芬超冠": ("fin1", 105243),
    "veikkausliiga": ("fin1", 105243),
    "瑞典超": ("swe", 104930),
    "allsvenskan": ("swe", 104930),
    "挪超": ("nor", 102651),
    "eliteserien": ("nor", 102651),
    "比甲": ("bel1", 105725),
    "belgium pro league": ("bel1", 105725),
    "丹超": ("den", 102652),
    "danish superliga": ("den", 102652),
    "瑞士超": ("sui", 105704),
    "swiss super league": ("sui", 105704),
    "土超": ("tur", 102564),
    "süper lig": ("tur", 102564),
    "苏超": ("scop", 102872),
    "scottish premiership": ("scop", 102872),
    "俄超": ("rus", 102593),
    "russian premier league": ("rus", 102593),
    "波兰超": ("pol", 105705),
    "ekstraklasa": ("pol", 105705),
    # 美洲与亚洲
    "美职联": ("mls", 100100),
    "mls": ("mls", 100100),
    "巴西甲": ("bra", 102648),
    "brasileirão": ("bra", 102648),
    "brasileirao": ("bra", 102648),
    "日职": ("jap", 102649),
    "j1": ("jap", 102649),
    "j1 league": ("jap", 102649),
    "韩k": ("kor", 102771),
    "k1": ("kor", 102771),
    "k league 1": ("kor", 102771),
    "阿甲": ("arg", 102561),
    "墨联": ("mex", 102448),
    "澳超": ("aus", 102765),
    # 洲际与杯赛
    "欧冠": ("ucl", 1234),
    "champions league": ("ucl", 1234),
    "欧联": ("uel", 101787),
    "欧罗巴": ("uel", 101787),
    "europa league": ("uel", 101787),
    "欧协联": ("col", 102763),
    "conference league": ("col", 102763),
    "欧国联": ("unl", 100816),
    "nations league": ("unl", 100816),
    "解放者杯": ("lib", 102562),
    "copa libertadores": ("lib", 102562),
    "亚冠": ("acle", 104937),
    "亚冠精英": ("acle", 104937),
}

COMMON_PREFIXES = [
    "fin1", "nor", "swe", "lal", "epl", "bun", "sea", "fl1", "por", "bra",
    "ere", "mls", "elc", "es2", "bl2", "itsb", "fr2", "ned2", "bel1", "den",
    "sui", "tur", "scop", "jap", "kor", "arg", "mex", "aus", "ucl", "uel", "col", "unl"
]

ALIAS_MAP = {
    "copenhagen": "kob",
    "kobenhavn": "kob",
    "saint gilloise": "usg",
    "salzburg": "rbs",
    "sturm graz": "stu",
    "torreense": "ut",
    "lech poznan": "lep",
    "universitatea craiova": "ucr",
    "celta vigo": "cel1",
    "estudiantes": "est",
    "flamengo": "fla",
    "sociedad": "rso",
    "milan": "mil1",
    "juventus": "juv",
    "besiktas": "bes",
    "olympiakos": "oly",
    "olympiacos": "oly",
    "bournemouth": "bou",
    "celtic": "cel",
    "braga": "scb",
    "kups": "kups",
    "vps": "vps",
    "racing": "rrc",
    "santander": "rrc",
    "rosenborg": "rbk",
    "sarpsborg": "sar",
    "elfsborg": "elf",
    "sirius": "sir",
}

import unicodedata

def _clean_str(s: str) -> str:
    """去除西欧语言变音符（如 ç -> c, ø -> o, é -> e）并转小写"""
    nkfd_form = unicodedata.normalize('NFKD', str(s or ""))
    return "".join([c for c in nkfd_form if not unicodedata.combining(c)]).lower()


def match_event_for_teams(
    event: Dict[str, Any],
    home_keywords: List[str],
    away_keywords: List[str],
    match_date: Optional[str] = None,
) -> bool:
    """严格比对 Gamma API 返回的 event 是否为当前对阵双方的活跃比赛"""
    if not isinstance(event, dict):
        return False

    # 官方规约: 排除已关闭或非活跃事件
    if event.get("active") is False or event.get("closed") is True:
        return False

    title_clean = _clean_str(event.get("title") or "")
    slug_clean = _clean_str(event.get("slug") or "")

    # 必须同时命中主队核心词与客队核心词 (支持变音符归一化与缩写匹配)
    def _matches_any(word: str) -> bool:
        w_clean = _clean_str(word)
        if w_clean in title_clean or w_clean in slug_clean:
            return True
        # 3~4 字母缩写匹配 slug (如 fen 匹配 fenerbahce, ast/avl 匹配 aston)
        if len(w_clean) >= 4 and w_clean[:3] in slug_clean:
            return True
        return False

    has_home = any(_matches_any(w) for w in home_keywords)
    has_away = any(_matches_any(w) for w in away_keywords)

    if not (has_home and has_away):
        return False

    # 如果有开球日期 (YYYY-MM-DD)，且 slug 包含日期，核对日期
    if match_date and re.search(r"\d{4}-\d{2}-\d{2}", slug_clean):
        if match_date in slug_clean:
            return True
        # 否则若为完全不同年份/月份/日期，排除
        m_slug_date = re.search(r"(\d{4}-\d{2}-\d{2})", slug_clean)
        if m_slug_date and m_slug_date.group(1) != match_date:
            return False

    return True


def parse_teams_from_1x2d(js_text: str) -> Tuple[str, str, str]:
    """从球探网 1x2d.js 中提取主客队英文名及比赛日期"""
    hm = re.search(r'var\s+hometeam\s*=\s*"([^"]+)"', js_text)
    gm = re.search(r'var\s+guestteam\s*=\s*"([^"]+)"', js_text)
    tm = re.search(r'var\s+MatchTime\s*=\s*"([^"]+)"', js_text)

    h_name = hm.group(1).strip() if hm else ""
    g_name = gm.group(1).strip() if gm else ""
    m_date = ""

    if tm:
        parts = tm.group(1).split(",")
        if len(parts) >= 3:
            year = parts[0].strip()
            month_part = parts[1].strip()
            month = month_part.split("-")[0] if "-" in month_part else month_part
            day = parts[2].strip()
            m_date = f"{year}-{int(month):02d}-{int(day):02d}"

    return h_name, g_name, m_date


def parse_match_info_from_1x2d(js_text: str) -> Tuple[str, str, str, str, str]:
    """从球探网 1x2d.js 中提取主客队英文名、比赛日期以及联赛中英文名称"""
    h_name, g_name, m_date = parse_teams_from_1x2d(js_text)
    lm_cn = re.search(r'var\s+matchname_cn\s*=\s*"([^"]+)"', js_text)
    lm_en = re.search(r'var\s+matchname\s*=\s*"([^"]+)"', js_text)
    l_cn = lm_cn.group(1).strip() if lm_cn else ""
    l_en = lm_en.group(1).strip() if lm_en else ""
    return h_name, g_name, m_date, l_cn, l_en


class PolymarketOfficialResolver:
    """Polymarket 官方发现与解析引擎"""

    def __init__(self, session=None):
        self._session = session
        self._teams_cache: Dict[str, List[Dict[str, Any]]] = {}

    def fetch_league_teams(self, league_code: str) -> List[Dict[str, Any]]:
        """依据 Polymarket 官方 Discover Markets 规范: 调用 GET /teams?league={league}&limit=100 直取官方球队名册与标准缩写"""
        if league_code in self._teams_cache:
            return self._teams_cache[league_code]
        url = f"https://gamma-api.polymarket.com/teams?league={league_code}&limit=100"
        data = _curl_get_json(url, timeout=12)
        if isinstance(data, list):
            self._teams_cache[league_code] = data
            return data
        return []

    def _get_session(self):
        if self._session is None:
            try:
                from curl_cffi import requests
                self._session = requests.Session(impersonate="chrome")
            except ImportError:
                import urllib.request
                self._session = "urllib"
        return self._session

    def query_public_search(self, query: str) -> List[Dict[str, Any]]:
        """按官方 Discover Markets 规范调用 /public-search?q={query}"""
        sess = self._get_session()
        url = f"https://gamma-api.polymarket.com/public-search?q={query}"

        for attempt in range(3):
            try:
                if sess != "urllib":
                    resp = sess.get(url, timeout=12)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data.get("events") or []
                else:
                    import urllib.request
                    req = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                            "Accept": "application/json",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=12) as response:
                        data = json.loads(response.read().decode("utf-8"))
                        return data.get("events") or []
            except Exception:
                time.sleep(1.0 * (attempt + 1))
        return []

    def fetch_event_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """按官方 /events?slug={slug} 获取完整事件结构（含 markets 与挂单 outcomePrices）"""
        sess = self._get_session()
        url = f"https://gamma-api.polymarket.com/events?slug={slug}"

        for attempt in range(3):
            try:
                if sess != "urllib":
                    resp = sess.get(url, timeout=12)
                    if resp.status_code == 200:
                        data = resp.json()
                        if isinstance(data, list) and data:
                            return data[0]
                else:
                    import urllib.request
                    req = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                            "Accept": "application/json",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=12) as response:
                        data = json.loads(response.read().decode("utf-8"))
                        if isinstance(data, list) and data:
                            return data[0]
            except Exception:
                time.sleep(1.0 * (attempt + 1))
        return None

    def fetch_events_by_tag_id(self, tag_id: int) -> List[Dict[str, Any]]:
        """依据 Polymarket 官方 Discover Markets 规范: 按 tag_id 直取联赛全量活跃事件"""
        url = f"https://gamma-api.polymarket.com/events?tag_id={tag_id}&closed=false&limit=100"
        data = _curl_get_json(url, timeout=12)
        if isinstance(data, list):
            return data
        return []

    def resolve_match(
        self,
        home_en: str,
        away_en: str,
        match_date: Optional[str] = None,
        league_hint: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """官方主客双向发现流：从两队关键字自动匹配官方 Event"""
        if not home_en or not away_en:
            return None

        h_words = extract_team_keywords(home_en)
        a_words = extract_team_keywords(away_en)

        # 1. 官方正道第一优先级：若有联赛标识，结合 /teams 官方缩写与 tag_id 直通
        if league_hint:
            clean_l = _clean_str(league_hint)
            tag_info = None
            for lk, val in OFFICIAL_SOCCER_LEAGUES.items():
                if _clean_str(lk) in clean_l or clean_l in _clean_str(lk):
                    tag_info = val
                    break
            if tag_info:
                sport_code, tag_id = tag_info
                # 1a. 从 GET /teams?league={sport} 提取官方主客缩写直拼标准 Slug
                league_teams = self.fetch_league_teams(sport_code)
                h_abbrs: List[str] = []
                a_abbrs: List[str] = []
                for t in league_teams:
                    t_name = _clean_str(t.get("name") or "")
                    t_alias = _clean_str(t.get("alias") or "")
                    t_abbr = _clean_str(t.get("abbreviation") or "")
                    if any(w.lower() in t_name or w.lower() in t_alias or w.lower() == t_abbr for w in h_words):
                        # 精确匹配排前
                        if _clean_str(home_en) == t_name or _clean_str(home_en) == t_alias:
                            h_abbrs.insert(0, t_abbr)
                        elif t_abbr not in h_abbrs:
                            h_abbrs.append(t_abbr)
                    if any(w.lower() in t_name or w.lower() in t_alias or w.lower() == t_abbr for w in a_words):
                        if _clean_str(away_en) == t_name or _clean_str(away_en) == t_alias:
                            a_abbrs.insert(0, t_abbr)
                        elif t_abbr not in a_abbrs:
                            a_abbrs.append(t_abbr)
                
                if h_abbrs and a_abbrs and match_date:
                    for h_cur in h_abbrs:
                        for a_cur in a_abbrs:
                            official_slug = f"{sport_code}-{h_cur}-{a_cur}-{match_date}"
                            ev = self.fetch_event_by_slug(official_slug)
                            if ev and match_event_for_teams(ev, h_words, a_words, match_date):
                                return ev

                # 1b. 若官方缩写未命中，通过 tag_id 获取该联赛全部活跃事件
                tag_events = self.fetch_events_by_tag_id(tag_id)
                for ev in tag_events:
                    if match_event_for_teams(ev, h_words, a_words, match_date):
                        slug = ev.get("slug")
                        if slug:
                            full_event = self.fetch_event_by_slug(slug)
                            return full_event or ev

        # 2. 官方正道第二优先级：候选 Slug 靶向直通 (Discover Markets)
        if match_date:
            h_slug_tokens = [w.lower() for w in h_words if len(w) >= 2]
            a_slug_tokens = [w.lower() for w in a_words if len(w) >= 2]
            for w in h_words:
                alias = ALIAS_MAP.get(w.lower())
                if alias and alias not in h_slug_tokens:
                    h_slug_tokens.append(alias)
            for w in a_words:
                alias = ALIAS_MAP.get(w.lower())
                if alias and alias not in a_slug_tokens:
                    a_slug_tokens.append(alias)

            candidate_slugs = []
            for hp in h_slug_tokens:
                for ap in a_slug_tokens:
                    for pfx in COMMON_PREFIXES:
                        candidate_slugs.append(f"{pfx}-{hp}-{ap}-{match_date}")

            for c_slug in candidate_slugs:
                ev = self.fetch_event_by_slug(c_slug)
                if ev and match_event_for_teams(ev, h_words, a_words, match_date):
                    return ev

        # 3. 官方公共检索兜底：依次以主客完整英文名、各关键词检索官方接口
        candidate_queries: List[str] = []
        for q_cand in [home_en, away_en] + h_words + a_words:
            if q_cand and q_cand not in candidate_queries:
                candidate_queries.append(q_cand)

        for q in candidate_queries:
            events = self.query_public_search(q)
            for ev in events:
                if match_event_for_teams(ev, h_words, a_words, match_date):
                    slug = ev.get("slug")
                    if slug:
                        full_event = self.fetch_event_by_slug(slug)
                        return full_event or ev
            time.sleep(0.3)

        return None

    def resolve_raw_bundle(self, raw_bundle: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """为单文件原子包自动补齐真实 polymarket.json 报文"""
        payloads = raw_bundle.get("payloads") or raw_bundle.get("rawFiles") or {}
        js_text = payloads.get("1x2d.js", "")
        if not js_text:
            return False, "缺少 1x2d.js，无法获取官方英文队名"

        home_en, away_en, match_date, l_cn, l_en = parse_match_info_from_1x2d(js_text)
        if not home_en or not away_en:
            return False, "无法从 1x2d.js 提取英文队名"

        league_hint = l_cn or l_en
        event = self.resolve_match(home_en, away_en, match_date, league_hint=league_hint)
        if event:
            event_json_str = json.dumps([event], ensure_ascii=False, indent=2)
            payloads["polymarket.json"] = event_json_str
            slug = event.get("slug", "")
            return True, f"https://polymarket.com/event/{slug}"

        # 严格遵守立宪：绝不合成任何「官方未开盘（经Gamma双向核验...）」等假套话
        unopened_event = {
            "url": "未开盘",
            "status": "unopened",
            "proof": f"未检索到活跃市场标的 (home={home_en}, away={away_en}, date={match_date})",
            "home": home_en,
            "away": away_en,
            "matchDate": match_date,
        }
        payloads["polymarket.json"] = json.dumps([unopened_event], ensure_ascii=False, indent=2)
        return False, "未开盘"
